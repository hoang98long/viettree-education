"""Progress writes must keep access checks without building a lesson view."""

from contextlib import contextmanager
from uuid import UUID

import pytest
from fastapi import HTTPException
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    event,
    func,
    select,
)

from app.db import db
from app.services.catalog import published_lesson


@contextmanager
def queries(conn):
    captured = []

    def capture(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.lstrip().upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
            captured.append(statement)

    event.listen(conn, "before_cursor_execute", capture)
    try:
        yield captured
    finally:
        event.remove(conn, "before_cursor_execute", capture)


@pytest.fixture
def lookup_tables(monkeypatch):
    metadata = MetaData()
    subjects = Table(
        "subjects",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("code", String),
        Column("name_vi", String),
    )
    topics = Table(
        "topics",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("subject_id", ForeignKey("subjects.id")),
        Column("grade", Integer),
        Column("title", String),
        Column("is_active", Boolean),
    )
    lessons = Table(
        "lessons",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("topic_id", ForeignKey("topics.id")),
        Column("title", String),
        Column("status", String),
        Column("content", JSON),
    )
    progress = Table(
        "student_lesson_progress",
        metadata,
        Column("student_id", Integer, primary_key=True),
        Column("lesson_id", ForeignKey("lessons.id"), primary_key=True),
        Column("status", String),
    )
    tables = {table.name: table for table in (subjects, topics, lessons, progress)}
    monkeypatch.setattr(db, "table", lambda name: tables[name])
    storage = create_engine("sqlite+pysqlite:///:memory:")
    metadata.create_all(storage)
    with storage.begin() as conn:
        conn.execute(subjects.insert().values(id=1, code="MATH", name_vi="Toán"))
        conn.execute(
            topics.insert().values(id=1, subject_id=1, grade=4, title="Số", is_active=True)
        )
        conn.execute(
            lessons.insert().values(
                id=1,
                topic_id=1,
                title="Ví dụ",
                status="published",
                content={"large_lesson": "not needed for writes"},
            )
        )
        yield conn, tables
    storage.dispose()


def test_progress_lookup_has_one_query_without_lesson_json_or_other_students_status(lookup_tables):
    conn, tables = lookup_tables
    conn.execute(
        tables["student_lesson_progress"]
        .insert()
        .values(student_id=2, lesson_id=1, status="completed")
    )
    with queries(conn) as captured:
        state = published_lesson(conn, 1, 1)
    assert dict(state) == {"id": 1, "grade": 4, "progress_status": "not_started"}
    assert len(captured) == 1
    assert "lessons.content" not in captured[0]
    conn.execute(
        tables["student_lesson_progress"]
        .insert()
        .values(student_id=1, lesson_id=1, status="in_progress")
    )
    assert published_lesson(conn, 1, 1)["progress_status"] == "in_progress"


def test_detail_lookup_retains_content_metadata_and_same_owner_progress(lookup_tables):
    conn, tables = lookup_tables
    conn.execute(
        tables["student_lesson_progress"]
        .insert()
        .values(student_id=1, lesson_id=1, status="completed")
    )
    row = published_lesson(conn, 1, 1, detail=True)
    assert row["progress_status"] == "completed" and row["content"]["large_lesson"]
    assert row["subject_code"] == "MATH" and row["subject_name"] == "Toán"
    assert row["topic_title"] == "Số"


@pytest.mark.parametrize("detail", [False, True])
@pytest.mark.parametrize("unavailable", ["missing", "draft", "archived", "inactive_topic"])
def test_both_lookups_apply_the_same_lesson_visibility(lookup_tables, detail, unavailable):
    conn, tables = lookup_tables
    if unavailable == "inactive_topic":
        conn.execute(tables["topics"].update().values(is_active=False))
    elif unavailable != "missing":
        conn.execute(tables["lessons"].update().values(status=unavailable))
    with pytest.raises(HTTPException) as error:
        published_lesson(conn, 999 if unavailable == "missing" else 1, 1, detail=detail)
    assert error.value.status_code == 404


def lesson_with_plan(conn, plan):
    lessons, topics, policies = (
        db.table(name) for name in ("lessons", "topics", "content_access_policies")
    )
    return conn.execute(
        select(lessons.c.id)
        .select_from(lessons.join(topics).join(policies, policies.c.lesson_id == lessons.c.id))
        .where(
            topics.c.grade == 4,
            topics.c.is_active.is_(True),
            lessons.c.status == "published",
            policies.c.minimum_plan_code == plan,
        )
        .order_by(lessons.c.code)
        .limit(1)
    ).scalar_one()


@pytest.mark.integration
def test_visit_and_completion_have_bounded_queries_and_preserve_progress(logged_student, conn):
    lesson_id = lesson_with_plan(conn, "free")
    student_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    progress = db.table("student_lesson_progress")
    completion_time = None
    for action, budget in (("visit", 12), ("complete", 13), ("complete", 12), ("visit", 12)):
        with queries(conn) as captured:
            result = logged_student.post(f"/api/v1/lessons/{lesson_id}/{action}")
        assert result.status_code == 200, result.text
        assert len(captured) <= budget
        assert not any(
            "assessments" in sql
            or "question_versions" in sql
            or "lessons.content" in sql
            or "student_lesson_bookmarks" in sql
            for sql in captured
        )
        if action == "complete":
            stored_time = conn.execute(
                select(progress.c.completed_at).where(
                    progress.c.student_id == student_id, progress.c.lesson_id == lesson_id
                )
            ).scalar_one()
            if completion_time is not None:
                assert stored_time == completion_time
            completion_time = stored_time
    progress, events = db.table("student_lesson_progress"), db.table("learning_events")
    row = (
        conn.execute(
            select(progress).where(
                progress.c.student_id == student_id, progress.c.lesson_id == lesson_id
            )
        )
        .mappings()
        .one()
    )
    assert row["status"] == "completed" and row["completion_ratio"] == 1
    assert row["first_started_at"] and row["completed_at"]
    assert (
        conn.execute(
            select(func.count())
            .select_from(events)
            .where(events.c.student_id == student_id, events.c.event_type == "lesson_completed")
        ).scalar_one()
        == 1
    )
    assert (
        logged_student.get(f"/api/v1/lessons/{lesson_id}").json()["progress_status"] == "completed"
    )


@pytest.mark.integration
def test_progress_write_cannot_use_or_change_another_students_completion(logged_student, conn):
    from app.core.security import now
    from tests.test_concurrency import create_student

    other = create_student(conn)
    lesson_id = lesson_with_plan(conn, "free")
    progress = db.table("student_lesson_progress")
    conn.execute(
        progress.insert().values(
            student_id=other["id"],
            lesson_id=lesson_id,
            status="completed",
            completion_ratio=1,
            first_started_at=now(),
            completed_at=now(),
        )
    )
    statement = select(progress).where(
        progress.c.student_id == other["id"], progress.c.lesson_id == lesson_id
    )
    before = dict(conn.execute(statement).mappings().one())
    assert (
        logged_student.post(
            f"/api/v1/lessons/{lesson_id}/complete", json={"student_id": str(other["id"])}
        ).status_code
        == 200
    )
    assert dict(conn.execute(statement).mappings().one()) == before
    student_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    assert (
        conn.execute(
            select(func.count())
            .select_from(db.table("learning_events"))
            .where(
                db.table("learning_events").c.student_id == student_id,
                db.table("learning_events").c.event_type == "lesson_completed",
            )
        ).scalar_one()
        == 1
    )


@pytest.mark.integration
@pytest.mark.parametrize("action", ["visit", "complete"])
def test_progress_writes_recheck_vip_after_grant_and_revocation(logged_student, conn, action):
    from app.core.security import now
    from tests.test_classrooms import grant

    lesson_id = lesson_with_plan(conn, "vip")
    student_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    path = f"/api/v1/lessons/{lesson_id}/{action}"
    assert logged_student.post(path).status_code == 403
    grant(conn, student_id)
    assert logged_student.post(path).status_code == 200
    progress, memberships = db.table("student_lesson_progress"), db.table("student_memberships")
    current = dict(
        conn.execute(
            select(progress).where(
                progress.c.student_id == student_id, progress.c.lesson_id == lesson_id
            )
        )
        .mappings()
        .one()
    )
    conn.execute(
        memberships.update()
        .where(memberships.c.student_id == student_id)
        .values(status="revoked", revoked_at=now(), revoke_reason="Isolated audit fixture")
    )
    assert logged_student.post(path).status_code == 403
    assert (
        dict(
            conn.execute(
                select(progress).where(
                    progress.c.student_id == student_id, progress.c.lesson_id == lesson_id
                )
            )
            .mappings()
            .one()
        )
        == current
    )


@pytest.mark.integration
@pytest.mark.parametrize("action", ["visit", "complete"])
@pytest.mark.parametrize(
    "unavailable,expected", [("draft", 404), ("inactive_topic", 404), ("wrong_grade", 403)]
)
def test_unavailable_progress_writes_do_not_create_rows(
    logged_student, conn, action, unavailable, expected
):
    lesson_id = lesson_with_plan(conn, "free")
    student_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    lessons, topics, profiles, progress = (
        db.table(name)
        for name in ("lessons", "topics", "student_profiles", "student_lesson_progress")
    )
    if unavailable == "draft":
        conn.execute(lessons.update().where(lessons.c.id == lesson_id).values(status="draft"))
    elif unavailable == "inactive_topic":
        topic_id = conn.execute(
            select(lessons.c.topic_id).where(lessons.c.id == lesson_id)
        ).scalar_one()
        conn.execute(topics.update().where(topics.c.id == topic_id).values(is_active=False))
    else:
        conn.execute(
            profiles.update().where(profiles.c.student_id == student_id).values(current_grade=5)
        )
    assert logged_student.post(f"/api/v1/lessons/{lesson_id}/{action}").status_code == expected
    assert not conn.execute(
        select(progress.c.lesson_id).where(
            progress.c.student_id == student_id, progress.c.lesson_id == lesson_id
        )
    ).first()
