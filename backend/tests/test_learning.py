from uuid import UUID

import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.db import db

pytestmark = pytest.mark.integration
BASE = "/api/v1"


def create_plan(client, subject="MATH"):
    response = client.post(f"{BASE}/students/me/learning-plans", json={"subject_code": subject})
    assert response.status_code == 200, response.text
    return response.json()


def test_accessibility_persists_preserves_other_options_and_validates(logged_student, conn):
    client = logged_student
    student_id = UUID(client.get(f"{BASE}/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == student_id)
        .values(accessibility_options={"reduced_motion": True})
    )
    assert client.get(f"{BASE}/auth/me").json()["text_size"] == "comfortable"
    assert (
        client.put(f"{BASE}/students/me/accessibility", json={"text_size": "large"}).status_code
        == 200
    )
    assert client.get(f"{BASE}/auth/me").json()["text_size"] == "large"
    assert client.get(f"{BASE}/students/me/profile").json()["accessibility_options"] == {
        "reduced_motion": True,
        "text_size": "large",
    }
    for payload in [{"text_size": "tiny"}, {"text_size": "large", "student_id": str(student_id)}]:
        assert client.put(f"{BASE}/students/me/accessibility", json=payload).status_code == 422
    token = client.headers.pop("X-CSRF-Token")
    assert (
        client.put(
            f"{BASE}/students/me/accessibility", json={"text_size": "comfortable"}
        ).status_code
        == 403
    )
    client.headers["X-CSRF-Token"] = token
    assert client.get(f"{BASE}/auth/me").json()["text_size"] == "large"


def test_plan_create_resume_and_real_progress_are_idempotent(logged_student, conn):
    client = logged_student
    assert client.get(f"{BASE}/students/me/learning-plans").json() == []
    plan = create_plan(client)
    assert plan["status"] == "active" and plan["completed_count"] == 0
    assert len([item for item in plan["items"] if item["lesson_id"]]) == 3
    assert [item["position"] for item in plan["items"]] == list(range(1, len(plan["items"]) + 1))
    assert [item["due_at"] for item in plan["items"]] == sorted(
        item["due_at"] for item in plan["items"]
    )
    history = db.table("learning_plan_history")
    history_query = (
        select(func.count())
        .select_from(history)
        .where(history.c.learning_plan_id == UUID(plan["id"]))
    )
    assert conn.execute(history_query).scalar_one() == 1
    assert create_plan(client)["id"] == plan["id"]
    assert conn.execute(history_query).scalar_one() == 1
    lesson_id = plan["items"][0]["lesson_id"]
    assert client.post(f"{BASE}/lessons/{lesson_id}/visit").status_code == 200
    assert (
        client.get(f"{BASE}/students/me/learning-plans").json()[0]["items"][0]["status"]
        == "in_progress"
    )
    assert client.get(f"{BASE}/students/me/dashboard").json()["completed_lessons"] == 0
    for _ in range(2):
        assert client.post(f"{BASE}/lessons/{lesson_id}/complete").status_code == 200
        assert client.post(f"{BASE}/lessons/{lesson_id}/visit").status_code == 200
    assert client.get(f"{BASE}/lessons/{lesson_id}").json()["progress_status"] == "completed"
    assert client.get(f"{BASE}/students/me/dashboard").json()["completed_lessons"] == 1
    assert client.get(f"{BASE}/students/me/learning-plans").json()[0]["completed_count"] == 1
    before = conn.execute(history_query).scalar_one()
    assert client.post(f"{BASE}/lessons/{lesson_id}/complete").status_code == 200
    assert conn.execute(history_query).scalar_one() == before
    assert client.get(f"{BASE}/students/me/skills").json() == []  # Reading is not mastery.


def test_submitting_practice_finishes_plan_without_duplicate_completion(logged_student, conn):
    client = logged_student
    plan = create_plan(client, "VIETNAMESE")
    for step in plan["items"]:
        if step["lesson_id"]:
            assert client.post(f"{BASE}/lessons/{step['lesson_id']}/complete").status_code == 200
        else:
            assignment = client.post(
                f"{BASE}/students/me/assessments/{step['assessment_id']}/assign-self"
            ).json()
            attempt = client.post(
                f"{BASE}/attempts", json={"assignment_id": assignment["id"]}
            ).json()
            assert client.post(f"{BASE}/attempts/{attempt['id']}/submit").status_code == 200
            assert client.post(f"{BASE}/attempts/{attempt['id']}/submit").status_code == 200
    finished = client.get(f"{BASE}/students/me/learning-plans").json()[0]
    assert finished["status"] == "completed"
    assert finished["completed_count"] == len(finished["items"])
    history = db.table("learning_plan_history")
    assert (
        conn.execute(
            select(func.count())
            .select_from(history)
            .where(
                history.c.learning_plan_id == UUID(plan["id"]), history.c.change_type == "completed"
            )
        ).scalar_one()
        == 1
    )
    following = create_plan(client, "VIETNAMESE")
    assert following["id"] != plan["id"]
    previous_lessons = {item["lesson_id"] for item in plan["items"] if item["lesson_id"]}
    assert not previous_lessons.intersection(item["lesson_id"] for item in following["items"])


def test_new_plan_excludes_completed_lessons_and_exhausted_assessments(logged_student, conn):
    client = logged_student
    assessment = client.get(f"{BASE}/assessments?grade=4&subject_code=MATH").json()[0]
    assessments = db.table("assessments")
    conn.execute(
        assessments.update()
        .where(assessments.c.id == UUID(assessment["id"]))
        .values(max_attempts=1)
    )
    assignment = client.post(
        f"{BASE}/students/me/assessments/{assessment['id']}/assign-self"
    ).json()
    attempt = client.post(f"{BASE}/attempts", json={"assignment_id": assignment["id"]}).json()
    assert client.post(f"{BASE}/attempts/{attempt['id']}/submit").status_code == 200
    plan = create_plan(client)
    assert assessment["id"] not in [item["assessment_id"] for item in plan["items"]]
    if assessment["lesson_id"]:
        assert assessment["lesson_id"] not in [item["lesson_id"] for item in plan["items"]]


def test_grade_unavailable_subject_and_owner_checks(logged_student, conn):
    client = logged_student
    student_id = UUID(client.get(f"{BASE}/auth/me").json()["id"])
    plan = create_plan(client)
    first_lesson = plan["items"][0]["lesson_id"]
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student_id).values(current_grade=5)
    )
    assert client.get(f"{BASE}/students/me/learning-plans").json() == []
    assert client.post(f"{BASE}/lessons/{first_lesson}/complete").status_code == 403
    topics = db.table("topics")
    conn.execute(topics.update().where(topics.c.grade == 5).values(is_active=False))
    assert (
        client.post(f"{BASE}/students/me/learning-plans", json={"subject_code": "MATH"}).status_code
        == 409
    )
    assert (
        client.post(
            f"{BASE}/students/me/learning-plans", json={"subject_code": "MISSING"}
        ).status_code
        == 404
    )
    assert (
        client.post(
            f"{BASE}/students/me/learning-plans",
            json={"subject_code": "MATH", "student_id": str(student_id)},
        ).status_code
        == 422
    )
    assert client.post(f"{BASE}/auth/logout").status_code == 200
    assert client.get(f"{BASE}/students/me/learning-plans").status_code == 401
    assert (
        client.post(
            f"{BASE}/auth/login",
            json={"username": "longnh", "password": settings().seed_student_password},
        ).status_code
        == 200
    )
    assert plan["id"] not in [
        item["id"] for item in client.get(f"{BASE}/students/me/learning-plans").json()
    ]
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    assert client.post(f"{BASE}/auth/logout").status_code == 200
    assert (
        client.post(
            f"{BASE}/auth/login",
            json={"username": "admin", "password": settings().seed_admin_password},
        ).status_code
        == 200
    )
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    assert client.get(f"{BASE}/students/me/learning-plans").status_code == 403
    assert client.post(f"{BASE}/lessons/{first_lesson}/complete").status_code == 403
    assert (
        client.put(f"{BASE}/students/me/accessibility", json={"text_size": "large"}).status_code
        == 403
    )
