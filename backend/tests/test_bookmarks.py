from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.core.security import now
from app.curriculum.supplements.explorers.pack import PACK
from app.db import db
from tests.test_academy import insert_user

pytestmark = pytest.mark.integration


def lesson_id(conn, grade=4, vip=False):
    lessons, topics, policies = (
        db.table(name) for name in ("lessons", "topics", "content_access_policies")
    )
    return conn.execute(
        select(lessons.c.id)
        .select_from(lessons.join(topics).join(policies, policies.c.lesson_id == lessons.c.id))
        .where(
            topics.c.grade == grade,
            lessons.c.status == "published",
            policies.c.minimum_plan_code == ("vip" if vip else "free"),
        )
        .order_by(lessons.c.id)
        .limit(1)
    ).scalar_one()


def test_bookmarks_are_idempotent_private_and_visible_after_new_session(logged_student, conn):
    client = logged_student
    identifier = lesson_id(conn)
    endpoint = f"/api/v1/students/me/lessons/{identifier}/bookmark"
    for _ in range(2):
        response = client.put(endpoint, json={"saved": True})
        assert response.status_code == 200 and response.json() == {"saved": True}
    bookmarks = db.table("student_lesson_bookmarks")
    student_id = UUID(client.get("/api/v1/auth/me").json()["id"])
    assert (
        conn.execute(
            select(func.count()).select_from(bookmarks).where(bookmarks.c.student_id == student_id)
        ).scalar_one()
        == 1
    )
    assert client.get(f"/api/v1/lessons/{identifier}").json()["is_bookmarked"]
    library = client.get("/api/v1/students/me/lesson-library?bookmarked_only=true").json()
    assert library["summary"]["total"] == library["summary"]["bookmarked"] == 1
    assert library["items"][0]["id"] == str(identifier)
    # Changing the principal cannot read or remove the first student's bookmark.
    from app.core.config import settings
    from tests.test_academy import login

    other_id, name = insert_user(conn, "student", 4)
    login(client, name, settings().seed_student_password)
    assert (
        client.get("/api/v1/students/me/lesson-library?bookmarked_only=true").json()["items"] == []
    )
    assert client.put(endpoint, json={"saved": False}).status_code == 200
    assert (
        conn.execute(
            select(func.count()).select_from(bookmarks).where(bookmarks.c.student_id == student_id)
        ).scalar_one()
        == 1
    )
    assert (
        client.put(endpoint, json={"saved": True, "student_id": str(student_id)}).status_code == 422
    )
    for _ in range(2):
        assert client.put(endpoint, json={"saved": False}).json() == {"saved": False}
    assert (
        conn.execute(
            select(func.count()).select_from(bookmarks).where(bookmarks.c.student_id == other_id)
        ).scalar_one()
        == 0
    )


def test_save_enforces_grade_publication_membership_and_csrf_but_can_remove_old_bookmarks(
    logged_student, conn
):
    client = logged_student
    student_id = UUID(client.get("/api/v1/auth/me").json()["id"])
    foreign = lesson_id(conn, 1)
    assert (
        client.put(
            f"/api/v1/students/me/lessons/{foreign}/bookmark", json={"saved": True}
        ).status_code
        == 404
    )
    vip = lesson_id(conn, vip=True)
    path = f"/api/v1/students/me/lessons/{vip}/bookmark"
    assert client.put(path, json={"saved": True}).status_code == 403
    from app.schemas.memberships import MembershipRevokeInput
    from app.services.memberships import change_membership
    from tests.test_classrooms import grant

    grant(conn, student_id)
    assert client.put(path, json={"saved": True}).status_code == 200
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        admin,
        student_id,
        "revoke",
        MembershipRevokeInput(reason="Kiểm tra lưu bài sau thu hồi"),
        uuid4(),
    )
    saved = client.get("/api/v1/students/me/lesson-library?bookmarked_only=true").json()["items"][0]
    assert saved["id"] == str(vip) and saved["locked"] and saved["is_bookmarked"]
    assert client.get(f"/api/v1/lessons/{vip}").status_code == 403
    assert client.put(path, json={"saved": False}).status_code == 200
    free = lesson_id(conn)
    free_path = f"/api/v1/students/me/lessons/{free}/bookmark"
    assert client.put(free_path, json={"saved": True}).status_code == 200
    lessons = db.table("lessons")
    conn.execute(lessons.update().where(lessons.c.id == free).values(status="archived"))
    assert (
        client.get("/api/v1/students/me/lesson-library?bookmarked_only=true").json()["items"] == []
    )
    assert client.put(free_path, json={"saved": True}).status_code == 404
    assert client.put(free_path, json={"saved": False}).status_code == 200
    token = client.headers.pop("X-CSRF-Token")
    assert client.put(free_path, json={"saved": False}).status_code == 403
    client.headers["X-CSRF-Token"] = token
    client.cookies.clear()
    assert client.put(free_path, json={"saved": False}).status_code == 401


def test_grade_change_hides_old_saved_lessons_and_can_remove_them(logged_student, conn):
    student_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    lesson = lesson_id(conn)
    path = f"/api/v1/students/me/lessons/{lesson}/bookmark"
    assert logged_student.put(path, json={"saved": True}).status_code == 200
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student_id).values(current_grade=3)
    )
    assert (
        logged_student.get("/api/v1/students/me/lesson-library?bookmarked_only=true").json()[
            "items"
        ]
        == []
    )
    assert logged_student.put(path, json={"saved": False}).status_code == 200


def test_dashboard_counts_all_finalized_attempts_beyond_history_limit(logged_student, conn):
    student_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    assessments = db.table("assessments")
    assessment = conn.execute(
        select(assessments.c.id).where(assessments.c.grade == 4).limit(1)
    ).scalar_one()
    at = now() - timedelta(days=2)
    assignment_ids = [uuid4() for _ in range(205)]
    conn.execute(
        db.table("student_assignments").insert(),
        [
            {
                "id": identifier,
                "student_id": student_id,
                "assessment_id": assessment,
                "assignment_source": "system",
                "status": "completed",
                "available_at": at - timedelta(hours=1),
            }
            for identifier in assignment_ids
        ],
    )
    conn.execute(
        db.table("attempts").insert(),
        [
            {
                "assignment_id": identifier,
                "student_id": student_id,
                "assessment_id": assessment,
                "status": "graded",
                "started_at": at,
                "submitted_at": at + timedelta(minutes=1),
                "graded_at": at + timedelta(minutes=1),
                "max_score": 4,
            }
            for identifier in assignment_ids
        ],
    )
    data = logged_student.get("/api/v1/students/me/dashboard")
    assert data.status_code == 200, data.text
    assert len(data.json()["history"]) == 200
    assert data.json()["graded_attempt_count"] == 205


def test_new_release_is_bookmarkable_without_exposing_hidden_hints(logged_student, conn):
    PACK.seed(conn, [4])
    lessons = db.table("lessons")
    identifier = conn.execute(
        select(lessons.c.id).where(
            lessons.c.code == "VT4-VIETNAMESE-explorers-2026-01-words-around-us-lesson"
        )
    ).scalar_one()
    assert (
        logged_student.put(
            f"/api/v1/students/me/lessons/{identifier}/bookmark", json={"saved": True}
        ).status_code
        == 200
    )
    response = logged_student.get(f"/api/v1/lessons/{identifier}")
    assert response.json()["is_bookmarked"]
    assert len(response.json()["content"]["hints"]) == 1
