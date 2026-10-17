from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import event, select

from app.academy.media import uid
from app.core.security import now
from app.db import db
from app.schemas.memberships import MembershipRevokeInput
from app.services.attempts import assign_self, start_attempt
from app.services.memberships import change_membership
from app.services.resume_learning import recent_work
from tests.test_classrooms import grant
from tests.test_concurrency import create_student

pytestmark = pytest.mark.integration


def lesson(conn, grade=4, plan="free", offset=0):
    lessons, topics, policies = (
        db.table(n) for n in ("lessons", "topics", "content_access_policies")
    )
    return conn.execute(
        select(lessons.c.id)
        .select_from(lessons.join(topics).join(policies, policies.c.lesson_id == lessons.c.id))
        .where(
            topics.c.grade == grade,
            lessons.c.status == "published",
            policies.c.minimum_plan_code == plan,
        )
        .order_by(lessons.c.id)
        .offset(offset)
        .limit(1)
    ).scalar_one()


def reading(conn, user, identifier, at, status="in_progress"):
    conn.execute(
        db.table("student_lesson_progress")
        .insert()
        .values(student_id=user, lesson_id=identifier, status=status, last_accessed_at=at)
    )


def practice(conn, user, plan="free"):
    exams, policies = db.table("assessments"), db.table("content_access_policies")
    exam = conn.execute(
        select(exams.c.id)
        .join(policies, policies.c.assessment_id == exams.c.id)
        .where(
            exams.c.grade == 4,
            exams.c.status == "published",
            exams.c.time_limit_seconds.is_(None),
            policies.c.minimum_plan_code == plan,
        )
        .order_by(exams.c.code)
        .limit(1)
    ).scalar_one()
    assignment = assign_self(conn, user, exam)
    started = start_attempt(conn, user, assignment["id"])
    return started["id"], assignment["id"]


def ai_progress(conn, user, code, at):
    versions = db.table("ai_lesson_versions")
    version = conn.execute(
        select(versions.c.id).where(
            versions.c.lesson_id == uid(code), versions.c.status == "published"
        )
    ).scalar_one()
    conn.execute(
        db.table("ai_progress")
        .insert()
        .values(
            student_id=user, lesson_id=uid(code), version_id=version, next_step=2, updated_at=at
        )
    )


def test_dashboard_uses_latest_activity_across_three_types_without_keys(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    at = now()
    core = lesson(conn)
    reading(conn, student, core, at - timedelta(hours=2))
    attempt, _ = practice(conn, student)
    ai_progress(conn, student, "AI4-01", at + timedelta(minutes=1))
    response = logged_student.get("/api/v1/students/me/dashboard")
    assert response.status_code == 200, response.text
    data = response.json()
    assert [r["kind"] for r in data["resume_items"]] == ["ai", "practice", "lesson"]
    assert data["resume_items"][0]["next_step"] == 2 and data["resume_items"][0]["step_count"] == 7
    assert data["resume_items"][1]["id"] == str(attempt)
    assert data["continue_lesson"]["id"] == str(core)
    assert all(
        not {"content", "payload", "answers", "grading", "student_id"} & r.keys()
        for r in data["resume_items"]
    )


def test_reading_skips_wrong_grade_completed_inactive_locked_and_other_owner(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    at = now()
    expected, completed, hidden, premium, wrong = (
        lesson(conn),
        lesson(conn, offset=1),
        lesson(conn, offset=2),
        lesson(conn, plan="vip"),
        lesson(conn, grade=3),
    )
    for identifier, status in [
        (expected, "in_progress"),
        (completed, "completed"),
        (hidden, "in_progress"),
        (premium, "in_progress"),
        (wrong, "in_progress"),
    ]:
        reading(
            conn,
            student,
            identifier,
            at if identifier != expected else at - timedelta(days=1),
            status,
        )
    conn.execute(
        db.table("lessons")
        .update()
        .where(db.table("lessons").c.id == hidden)
        .values(status="archived")
    )
    outsider = create_student(conn)
    reading(conn, outsider["id"], lesson(conn, offset=3), at + timedelta(hours=1))
    result = recent_work(conn, {"id": student, "roles": ["student"]}, 4)
    assert [(r["kind"], r["id"]) for r in result] == [("lesson", expected)]


def test_ai_resumes_lower_grade_pinned_version_and_disappears_on_revoke(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    at = now()
    ai_progress(conn, student, "AI1-01", at)
    ai_progress(conn, student, "AI5-01", at + timedelta(hours=2))
    ai_progress(conn, student, "AI4-38", at + timedelta(hours=1))
    actor = {"id": student, "roles": ["student"]}
    assert recent_work(conn, actor, 4)[0]["id"] == uid("AI1-01")
    grant(conn, student)
    assert recent_work(conn, actor, 4)[0]["id"] == uid("AI4-38")
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        admin,
        student,
        "revoke",
        MembershipRevokeInput(reason="Test live resume access"),
        uuid4(),
    )
    assert recent_work(conn, actor, 4)[0]["id"] == uid("AI1-01")


def test_practice_skips_closed_assignment_and_expired_time_limit(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    attempt, assignment = practice(conn, student)
    actor = {"id": student, "roles": ["student"]}
    assert recent_work(conn, actor, 4)[0]["id"] == attempt
    assignments = db.table("student_assignments")
    conn.execute(
        assignments.update()
        .where(assignments.c.id == assignment)
        .values(available_at=now() - timedelta(hours=1), due_at=now() - timedelta(seconds=1))
    )
    assert recent_work(conn, actor, 4) == []
    conn.execute(assignments.update().where(assignments.c.id == assignment).values(due_at=None))
    attempts, exams = db.table("attempts"), db.table("assessments")
    exam = conn.execute(
        select(attempts.c.assessment_id).where(attempts.c.id == attempt)
    ).scalar_one()
    conn.execute(exams.update().where(exams.c.id == exam).values(time_limit_seconds=1))
    conn.execute(
        attempts.update()
        .where(attempts.c.id == attempt)
        .values(started_at=now() - timedelta(minutes=1))
    )
    assert recent_work(conn, actor, 4) == []


def test_resume_is_read_only_and_query_count_is_bounded(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    reading(conn, student, lesson(conn), now())
    practice(conn, student)
    ai_progress(conn, student, "AI4-01", now())
    statements = []

    def capture(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement)

    event.listen(conn, "before_cursor_execute", capture)
    try:
        assert len(recent_work(conn, {"id": student, "roles": ["student"]}, 4)) == 3
    finally:
        event.remove(conn, "before_cursor_execute", capture)
    assert len(statements) <= 25
    assert all(s.lstrip().upper().startswith("SELECT") for s in statements)


def test_premium_practice_grace_is_honored_but_expired_grant_is_hidden(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    grant(conn, student)
    attempt, assignment = practice(conn, student, "vip")
    membership, grants = db.table("student_memberships"), db.table("attempt_access_grants")
    at = now()
    conn.execute(
        membership.update()
        .where(membership.c.student_id == student)
        .values(starts_at=at - timedelta(days=2), ends_at=at - timedelta(minutes=30))
    )
    conn.execute(
        grants.update()
        .where(grants.c.attempt_id == attempt)
        .values(granted_at=at - timedelta(hours=1), allowed_until=at + timedelta(minutes=30))
    )
    conn.execute(
        db.table("attempts")
        .update()
        .where(db.table("attempts").c.id == attempt)
        .values(started_at=at - timedelta(hours=1))
    )
    conn.execute(
        db.table("student_assignments")
        .update()
        .where(db.table("student_assignments").c.id == assignment)
        .values(available_at=at - timedelta(hours=2))
    )
    actor = {"id": student, "roles": ["student"]}
    assert recent_work(conn, actor, 4)[0]["id"] == attempt
    conn.execute(
        grants.update()
        .where(grants.c.attempt_id == attempt)
        .values(allowed_until=at - timedelta(seconds=1))
    )
    assert recent_work(conn, actor, 4) == []


def test_regranting_vip_does_not_resurface_a_revoked_attempt(logged_student, conn):
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    grant(conn, student)
    practice(conn, student, "vip")
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        admin,
        student,
        "revoke",
        MembershipRevokeInput(reason="Permanent attempt revocation"),
        uuid4(),
    )
    grant(conn, student)
    assert recent_work(conn, {"id": student, "roles": ["student"]}, 4) == []
