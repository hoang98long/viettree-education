"""Các test này ghi thêm dữ liệu trong DB test riêng để dùng nhiều connection thực."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from app.db import db
from app.seed import seed
from app.services.attempts import assign_self, start_attempt, submit

pytestmark = pytest.mark.integration


def create_student(conn):
    user_id = uuid4()
    conn.execute(
        db.table("users")
        .insert()
        .values(id=user_id, username="concurrency-" + str(user_id), display_name="Concurrency Test")
    )
    conn.execute(db.table("user_roles").insert().values(user_id=user_id, role="student"))
    conn.execute(db.table("student_profiles").insert().values(student_id=user_id, current_grade=4))
    return {"id": user_id, "roles": ["student"]}


def test_concurrent_start_submit_and_statistics(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        table = db.table("assessments")
        assessment_id = conn.execute(
            select(table.c.id).where(table.c.code == "VT4-MATH-numbers-practice")
        ).scalar_one()
        user = create_student(conn)
        assignment = assign_self(conn, user["id"], assessment_id)
    barrier = Barrier(2)

    def concurrent_start():
        barrier.wait(timeout=10)
        with test_engine.begin() as conn:
            return start_attempt(conn, user["id"], assignment["id"])

    with ThreadPoolExecutor(max_workers=2) as pool:
        starts = list(pool.map(lambda _: concurrent_start(), range(2)))
    assert starts[0]["id"] == starts[1]["id"]
    assert sum(int(start["resumed"]) for start in starts) == 1
    attempt_id = starts[0]["id"]
    barrier = Barrier(2)

    def concurrent_submit():
        barrier.wait(timeout=10)
        with test_engine.begin() as conn:
            return submit(conn, user, attempt_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: concurrent_submit(), range(2)))
    assert results[0] == results[1]
    with test_engine.connect() as conn:
        mastery, events = db.table("student_skill_mastery"), db.table("learning_events")
        assert (
            conn.execute(
                select(mastery.c.questions_attempted).where(mastery.c.student_id == user["id"])
            ).scalar_one()
            == 8
        )
        assert (
            conn.execute(
                select(func.count())
                .select_from(events)
                .where(events.c.attempt_id == attempt_id, events.c.event_type == "attempt_graded")
            ).scalar_one()
            == 1
        )


def test_two_students_submit_together_keep_global_stats(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        table = db.table("assessments")
        assessment_id = conn.execute(
            select(table.c.id).where(table.c.code == "VT4-ENGLISH-school-practice")
        ).scalar_one()
        users = [create_student(conn), create_student(conn)]
        ids = [
            start_attempt(conn, user["id"], assign_self(conn, user["id"], assessment_id)["id"])[
                "id"
            ]
            for user in users
        ]
    barrier = Barrier(2)

    def run(index):
        barrier.wait(timeout=10)
        with test_engine.begin() as conn:
            submit(conn, users[index], ids[index])

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, range(2)))
    with test_engine.connect() as conn:
        answers, attempts, stats = (
            db.table(name) for name in ("attempt_answers", "attempts", "question_statistics")
        )
        expected = dict(
            conn.execute(
                select(answers.c.question_version_id, func.count())
                .select_from(answers.join(attempts))
                .where(attempts.c.status == "graded")
                .group_by(answers.c.question_version_id)
            ).all()
        )
        actual = dict(
            conn.execute(select(stats.c.question_version_id, stats.c.attempts_count)).all()
        )
        assert all(actual[version] == count for version, count in expected.items())
