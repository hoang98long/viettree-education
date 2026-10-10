from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.core.security import now
from app.db import db
from app.seed import seed_advanced_content
from app.services import attempts as service
from app.services.grading import grade_answer, validate_answer
from app.vip_curriculum import VIP_EXTENSION
from tests.test_grading import correct_answer
from tests.test_memberships import identities, membership

QUESTIONS = [q for lessons in VIP_EXTENSION.values() for item in lessons for q in item["questions"]]


@pytest.mark.parametrize("question", QUESTIONS)
def test_new_vip_questions_are_valid_and_gradable(question):
    assert question["explanation"]["text"]
    answer = correct_answer(question)
    assert validate_answer(question["question_type"], question["content"], answer) == answer
    assert grade_answer(question["question_type"], question["grading"], answer) is True
    assert grade_answer(question["question_type"], question["grading"], None) is False


def enable(client, conn):
    student, admin = identities(client, conn)
    membership(conn, student, admin)
    return student, admin


def attempt(client):
    items = client.get("/api/v1/assessments?grade=4&subject_code=MATH").json()
    assessment = next(item for item in items if item["code"] == "VT4-MATH-numbers-practice")
    assigned = client.post(f"/api/v1/students/me/assessments/{assessment['id']}/assign-self").json()
    created = client.post("/api/v1/attempts", json={"assignment_id": assigned["id"]})
    assert created.status_code == 200, created.text
    return client.get(f"/api/v1/attempts/{created.json()['id']}").json()


@pytest.mark.integration
@pytest.mark.parametrize("path", ["library", "mistakes", "report?days=7", "report?days=30"])
def test_free_is_denied_for_every_new_tool(logged_student, path):
    response = logged_student.get(f"/api/v1/students/me/vip/{path}")
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "MEMBERSHIP_REQUIRED"


@pytest.mark.integration
def test_library_new_content_and_content_seed_are_idempotent(logged_student, conn):
    client = logged_student
    enable(client, conn)
    library = client.get("/api/v1/students/me/vip/library")
    assert library.status_code == 200, library.text
    assert len(library.json()["lessons"]) >= 18
    assert all("content" not in item for item in library.json()["lessons"])
    lessons = db.table("lessons")
    before = conn.execute(select(func.count()).select_from(lessons)).scalar_one()
    seed_advanced_content(conn, VIP_EXTENSION)
    assert conn.execute(select(func.count()).select_from(lessons)).scalar_one() == before
    for subject, sources in VIP_EXTENSION.items():
        for source in sources:
            identifier = conn.execute(
                select(lessons.c.id).where(
                    lessons.c.code == f"VT4-{subject}-{source['code']}-lesson"
                )
            ).scalar_one()
            opened = client.get(f"/api/v1/lessons/{identifier}")
            assert opened.status_code == 200
            assert opened.json()["minimum_plan_code"] == "vip"
            assert len(opened.json()["practice"]) >= 1


@pytest.mark.integration
def test_mistakes_latest_grade_only_and_self_review_never_changes_scores(logged_student, conn):
    client = logged_student
    enable(client, conn)
    created = attempt(client)
    # Draft must not be visible in the notebook.
    assert client.get("/api/v1/students/me/vip/mistakes").json()["total"] == 0
    submitted = client.post(f"/api/v1/attempts/{created['id']}/submit")
    assert submitted.status_code == 200
    notes = client.get("/api/v1/students/me/vip/mistakes").json()
    assert notes["total"] == 8
    source = notes["items"][0]
    assert "grading" not in source and "explanation" not in source
    versions = db.table("question_versions")
    version = (
        conn.execute(select(versions).where(versions.c.id == source["question_version_id"]))
        .mappings()
        .one()
    )
    before = dict(
        conn.execute(select(db.table("attempts")).where(db.table("attempts").c.id == created["id"]))
        .mappings()
        .one()
    )
    reviewed = client.post(
        f"/api/v1/students/me/vip/mistakes/{source['id']}/check",
        json={"answer": correct_answer(version)},
    )
    assert reviewed.status_code == 200, reviewed.text
    assert reviewed.json()["is_correct"] is True and reviewed.json()["affects_score"] is False
    assert (
        dict(
            conn.execute(
                select(db.table("attempts")).where(db.table("attempts").c.id == created["id"])
            )
            .mappings()
            .one()
        )
        == before
    )
    assert client.get("/api/v1/students/me/vip/mistakes").json()["total"] == 8
    second = attempt(client)
    item = next(
        row
        for row in second["items"]
        if row["question_version_id"] == source["question_version_id"]
    )
    assert (
        client.put(
            f"/api/v1/attempts/{second['id']}/answers/{item['id']}",
            json={"answer": correct_answer(version)},
        ).status_code
        == 200
    )
    assert client.post(f"/api/v1/attempts/{second['id']}/submit").status_code == 200
    assert client.get("/api/v1/students/me/vip/mistakes").json()["total"] == 7
    assert (
        client.post(
            f"/api/v1/students/me/vip/mistakes/{source['id']}/check",
            json={"answer": correct_answer(version)},
        ).status_code
        == 404
    )


@pytest.mark.integration
def test_notebook_owner_validation_and_revocation(logged_student, conn):
    client = logged_student
    student, admin = enable(client, conn)
    created = attempt(client)
    assert client.post(f"/api/v1/attempts/{created['id']}/submit").status_code == 200
    notes = client.get("/api/v1/students/me/vip/mistakes").json()
    assert client.get("/api/v1/students/me/vip/mistakes?subject_code=ENGLISH").json()["total"] == 0
    assert client.get("/api/v1/students/me/vip/mistakes?page=2").json()["items"] == []
    assert client.get("/api/v1/students/me/vip/mistakes?subject_code=unknown").status_code == 404
    assert (
        client.post(
            f"/api/v1/students/me/vip/mistakes/{uuid4()}/check",
            json={"answer": {"text": "anything"}},
        ).status_code
        == 404
    )
    answer_id = notes["items"][0]["id"]
    assert (
        client.post(
            f"/api/v1/students/me/vip/mistakes/{answer_id}/check",
            json={"answer": {"invalid": True}},
        ).status_code
        == 422
    )
    # Another student's actual answer ID must remain invisible.
    from tests.test_concurrency import create_student

    actor = create_student(conn)
    assignment = service.assign_self(conn, actor["id"], UUID(created["assessment_id"]))
    other = service.start_attempt(conn, actor["id"], assignment["id"])
    service.submit(conn, actor, other["id"])
    answers = db.table("attempt_answers")
    foreign_id = (
        conn.execute(select(answers.c.id).where(answers.c.attempt_id == other["id"]))
        .scalars()
        .first()
    )
    assert (
        client.post(
            f"/api/v1/students/me/vip/mistakes/{foreign_id}/check",
            json={"answer": {"text": "anything"}},
        ).status_code
        == 404
    )
    assert client.get("/api/v1/students/me/vip/mistakes").json()["total"] == 8
    assert client.get("/api/v1/students/me/vip/report").json()["attempt_count"] == 1
    membership(conn, student, admin, "revoke")
    assert client.get("/api/v1/students/me/vip/report").status_code == 403
    assert client.get("/api/v1/students/me/vip/library").status_code == 403
    assert (
        client.post(
            f"/api/v1/students/me/vip/mistakes/{answer_id}/check",
            json={"answer": {"text": "anything"}},
        ).status_code
        == 403
    )
    assert client.get(f"/api/v1/attempts/{created['id']}/result").status_code == 200


@pytest.mark.integration
def test_report_empty_periods_and_local_date_boundaries(logged_student, conn):
    client = logged_student
    student, _ = enable(client, conn)
    report = client.get("/api/v1/students/me/vip/report?days=7")
    assert report.status_code == 200, report.text
    assert report.json()["score_percent"] is None
    assert len(report.json()["daily"]) == 7
    assert client.get("/api/v1/students/me/vip/report?days=8").status_code == 422
    created = attempt(client)
    assert client.post(f"/api/v1/attempts/{created['id']}/submit").status_code == 200
    current = client.get("/api/v1/students/me/vip/report?days=7").json()
    assert current["attempt_count"] == 1 and current["score_percent"] == 0
    assert sum(item["attempt_count"] for item in current["daily"]) == 1
    assert current["active_days"] == 1
    assert current["subjects"][0]["subject_code"] == "MATH"
    start = datetime.fromisoformat(current["starts_at"])
    attempts = db.table("attempts")
    conn.execute(
        attempts.update()
        .where(attempts.c.id == created["id"])
        .values(graded_at=start - timedelta(microseconds=1))
    )
    moved = client.get("/api/v1/students/me/vip/report?days=7").json()
    assert moved["attempt_count"] == 0 and moved["previous"]["attempt_count"] == 1
    thirty = client.get("/api/v1/students/me/vip/report?days=30").json()
    assert len(thirty["daily"]) == 30 and thirty["attempt_count"] == 1
    # Expiry is enforced without waiting for a frontend timer.
    members = db.table("student_memberships")
    conn.execute(
        members.update()
        .where(members.c.student_id == student)
        .values(starts_at=now() - timedelta(days=3), ends_at=now() - timedelta(days=1))
    )
    assert client.get("/api/v1/students/me/vip/report").status_code == 403
