from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.core.security import hasher, now
from app.db import db
from app.fixtures.development import seed
from app.personalization.engine import rebuild_statistics, rebuild_student
from tests.test_grading import correct_answer

pytestmark = pytest.mark.integration


def start(client):
    assessment = next(
        item
        for item in client.get("/api/v1/assessments?grade=4&subject_code=MATH").json()
        if item["code"] == "VT4-MATH-numbers-practice"
    )
    assignment = client.post(
        f"/api/v1/students/me/assessments/{assessment['id']}/assign-self"
    ).json()
    response = client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]})
    assert response.status_code == 200, response.text
    return response.json()["id"], assessment, assignment


def test_login_logout_csrf_and_rbac(client):
    assert (
        client.post(
            "/api/v1/auth/login", json={"username": "longnh", "password": "wrong"}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"username": "longnh", "password": settings().seed_student_password},
            headers={"Origin": "https://evil.invalid"},
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"username": "longnh", "password": settings().seed_student_password},
        ).status_code
        == 200
    )
    assert client.get("/api/v1/auth/me").json()["roles"] == ["student"]
    assert client.get("/api/v1/admin/questions").status_code == 403
    assert client.post("/api/v1/auth/logout").status_code == 403
    cookie = client.cookies["viettree_session"]
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    assert client.post("/api/v1/auth/logout").status_code == 200
    client.cookies.set("viettree_session", cookie)
    assert client.get("/api/v1/auth/me").status_code == 401


def test_attempt_clock_repeat_save_and_server_deadline(logged_student, conn):
    client = logged_student
    attempt_id, assessment, _ = start(client)
    assessments = db.table("assessments")
    conn.execute(
        assessments.update()
        .where(assessments.c.id == assessment["id"])
        .values(time_limit_seconds=60)
    )
    before = now()
    data = client.get(f"/api/v1/attempts/{attempt_id}").json()
    assert before <= datetime.fromisoformat(data["server_time"]) <= now()
    assert datetime.fromisoformat(data["deadline"]) > datetime.fromisoformat(data["server_time"])
    item = data["items"][0]
    answer = {"option_id": item["content"]["options"][0]["id"]}
    path = f"/api/v1/attempts/{attempt_id}/answers/{item['id']}"
    for _ in range(2):
        assert client.put(path, json={"answer": answer}).status_code == 200
    answers = db.table("attempt_answers")
    saved = conn.execute(select(answers).where(answers.c.attempt_id == attempt_id)).mappings().all()
    assert len(saved) == 1 and saved[0]["student_answer"] == answer
    assert client.get(f"/api/v1/attempts/{attempt_id}").json()["items"][0]["answer"] == answer
    attempts = db.table("attempts")
    conn.execute(
        attempts.update()
        .where(attempts.c.id == attempt_id)
        .values(started_at=now() - timedelta(seconds=61))
    )
    assert client.put(path, json={"answer": answer}).status_code == 409
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").status_code == 409


def test_delayed_answer_cannot_overwrite_a_later_received_answer(logged_student, conn):
    from fastapi import HTTPException

    from app.schemas.attempts import AnswerInput
    from app.services.attempts import save_answer

    attempt_id, _, _ = start(logged_student)
    item = logged_student.get(f"/api/v1/attempts/{attempt_id}").json()["items"][0]
    user = logged_student.get("/api/v1/auth/me").json()
    user["id"] = UUID(user["id"])
    received = now()
    latest = {"option_id": item["content"]["options"][1]["id"]}
    save_answer(
        conn, user, UUID(attempt_id), UUID(item["id"]), AnswerInput(answer=latest), received
    )
    with pytest.raises(HTTPException) as rejected:
        save_answer(
            conn,
            user,
            UUID(attempt_id),
            UUID(item["id"]),
            AnswerInput(answer={"option_id": item["content"]["options"][0]["id"]}),
            received - timedelta(seconds=1),
        )
    assert rejected.value.status_code == 409
    saved = logged_student.get(f"/api/v1/attempts/{attempt_id}").json()
    assert saved["items"][0]["answer"] == latest


def test_cleared_saved_answers_not_counted_and_archived_result_stays_readable(logged_student, conn):
    client = logged_student
    attempt_id, assessment, _ = start(client)
    items = client.get(f"/api/v1/attempts/{attempt_id}").json()["items"]
    cleared = []
    for item in items:
        if item["question_type"] == "fill_blank":
            answer = {"text": " \n "}
        elif item["question_type"] == "multiple_choice":
            answer = {"option_ids": []}
        else:
            continue
        path = f"/api/v1/attempts/{attempt_id}/answers/{item['id']}"
        assert client.put(path, json={"answer": answer}).status_code == 200
        cleared.append(item["id"])
    assert len(cleared) >= 2
    result = client.post(f"/api/v1/attempts/{attempt_id}/submit")
    assert result.status_code == 200, result.text
    assert result.json()["answered_count"] == 0
    assert result.json()["grade"] == 4
    assert result.json()["correct_count"] == 0
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").json() == result.json()
    assessments = db.table("assessments")
    conn.execute(
        assessments.update().where(assessments.c.id == assessment["id"]).values(status="archived")
    )
    history = client.get(f"/api/v1/attempts/{attempt_id}/result")
    assert history.status_code == 200, history.text
    assert history.json() == result.json()


def test_login_rate_limit_persists_failures(client):
    for _ in range(10):
        assert (
            client.post(
                "/api/v1/auth/login", json={"username": "missing", "password": "wrong"}
            ).status_code
            == 401
        )
    assert (
        client.post(
            "/api/v1/auth/login", json={"username": "missing", "password": "wrong"}
        ).status_code
        == 429
    )


def test_seed_idempotency_and_password_preserved(conn):
    tables = [
        "users",
        "user_roles",
        "student_profiles",
        "topics",
        "lessons",
        "skills",
        "questions",
        "question_versions",
        "assessments",
        "assessment_items",
    ]
    before = {
        name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
        for name in tables
    }
    users = db.table("users")
    conn.execute(
        users.update()
        .where(users.c.username == "longnh")
        .values(password_hash=hasher.hash("ChangedForTestOnly"))
    )
    original_hash = conn.execute(
        select(users.c.password_hash).where(users.c.username == "longnh")
    ).scalar_one()
    seed(conn)
    after = {
        name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
        for name in tables
    }
    assert before == after
    assert (
        conn.execute(select(users.c.password_hash).where(users.c.username == "longnh")).scalar_one()
        == original_hash
    )


@pytest.mark.parametrize("grade", [1, 2, 3, 4, 5])
def test_grade_filters(logged_student, grade):
    response = logged_student.get(f"/api/v1/subjects?grade={grade}")
    assert response.status_code == 200
    assert all(row["grade"] == grade for row in response.json())
    topics = logged_student.get(f"/api/v1/topics?grade={grade}&subject_code=MATH").json()
    assert len(topics) >= 4
    assert logged_student.get("/api/v1/subjects?grade=6").status_code == 422


def test_full_flow_answer_security_idempotent_mastery(logged_student, conn):
    client = logged_student
    attempt_id, assessment, assignment = start(client)
    same = client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).json()
    assert same["id"] == attempt_id and same["resumed"]
    response = client.get(f"/api/v1/attempts/{attempt_id}")
    assert response.status_code == 200
    assert all(
        secret not in response.text
        for secret in ["grading", "explanation", "correct_option", "answer_key"]
    )
    assert client.get(f"/api/v1/attempts/{attempt_id}/result").status_code == 409
    item = response.json()["items"][0]
    assert (
        client.put(
            f"/api/v1/attempts/{attempt_id}/answers/{item['id']}",
            json={"answer": {"option_id": "a"}, "is_correct": True},
        ).status_code
        == 422
    )
    for item in response.json()["items"]:
        qv = (
            conn.execute(
                select(db.table("question_versions")).where(
                    db.table("question_versions").c.id == item["question_version_id"]
                )
            )
            .mappings()
            .one()
        )
        answer = correct_answer(qv)
        assert (
            client.put(
                f"/api/v1/attempts/{attempt_id}/answers/{item['id']}", json={"answer": answer}
            ).status_code
            == 200
        )
    assert all(
        item["answer"] for item in client.get(f"/api/v1/attempts/{attempt_id}").json()["items"]
    )
    result = client.post(f"/api/v1/attempts/{attempt_id}/submit")
    assert result.status_code == 200, result.text
    assert result.json()["total_score"] == result.json()["max_score"] == 8
    snapshot = client.get("/api/v1/students/me/skills").json()
    repeated = client.post(f"/api/v1/attempts/{attempt_id}/submit")
    assert repeated.json() == result.json()
    assert client.get("/api/v1/students/me/skills").json() == snapshot
    events = db.table("learning_events")
    assert (
        conn.execute(
            select(func.count())
            .select_from(events)
            .where(events.c.attempt_id == attempt_id, events.c.event_type == "attempt_graded")
        ).scalar_one()
        == 1
    )
    assert client.get("/api/v1/students/me/history").json()[0]["status"] == "graded"
    assert (
        client.put(
            f"/api/v1/attempts/{attempt_id}/answers/{item['id']}", json={"answer": answer}
        ).status_code
        == 409
    )
    student_id = client.get("/api/v1/auth/me").json()["id"]
    rebuild_student(conn, student_id)
    rebuild_statistics(conn)
    assert client.get("/api/v1/students/me/skills").json() == snapshot
    seed(conn)
    assert client.get(f"/api/v1/attempts/{attempt_id}/result").json() == result.json()


def test_cross_student_access_and_foreign_items(logged_student, conn):
    client = logged_student
    attempt_id, _, assignment = start(client)
    users, roles, profiles = (
        db.table(name) for name in ("users", "user_roles", "student_profiles")
    )
    other_id = uuid4()
    conn.execute(
        users.insert().values(
            id=other_id,
            username="student-other",
            display_name="Other",
            password_hash=hasher.hash("OtherTestPassword"),
        )
    )
    conn.execute(roles.insert().values(user_id=other_id, role="student"))
    conn.execute(profiles.insert().values(student_id=other_id, current_grade=4))
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"username": "student-other", "password": "OtherTestPassword"},
        ).status_code
        == 200
    )
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    for suffix in ("", "/result"):
        assert client.get(f"/api/v1/attempts/{attempt_id}{suffix}").status_code == 404
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").status_code == 404
    assert (
        client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).status_code == 404
    )


def test_attempt_limits_and_time_windows(logged_student, conn):
    client = logged_student
    attempt_id, assessment, assignment = start(client)
    table = db.table("assessments")
    conn.execute(table.update().where(table.c.id == assessment["id"]).values(max_attempts=1))
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").status_code == 200
    assert (
        client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).status_code == 409
    )
    conn.execute(table.update().where(table.c.id == assessment["id"]).values(max_attempts=5))
    assignment_table = db.table("student_assignments")
    conn.execute(
        assignment_table.update()
        .where(assignment_table.c.id == assignment["id"])
        .values(available_at=now() + timedelta(hours=1))
    )
    assert (
        client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).status_code == 409
    )
    conn.execute(
        assignment_table.update()
        .where(assignment_table.c.id == assignment["id"])
        .values(available_at=now() - timedelta(days=2), due_at=now() - timedelta(days=1))
    )
    assert (
        client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).status_code == 409
    )


def test_recommendations_no_duplicates(logged_student, conn):
    client = logged_student
    assert len(client.get("/api/v1/students/me/recommendations").json()) <= 5
    table = db.table("student_recommendations")
    before = conn.execute(select(func.count()).select_from(table)).scalar_one()
    client.get("/api/v1/students/me/recommendations")
    assert conn.execute(select(func.count()).select_from(table)).scalar_one() == before
    assert client.get("/api/v1/students/me/skills").json() == []


def test_admin_read_only_and_statistics(client):
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": settings().seed_admin_password},
        ).status_code
        == 200
    )
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    for path in ("statistics", "students", "questions", "assessments", "curriculum", "users"):
        response = client.get("/api/v1/admin/" + path)
        assert response.status_code == 200, response.text
    question = client.get("/api/v1/admin/questions").json()["items"][0]
    assert "grading" in client.get("/api/v1/admin/questions/" + question["id"]).json()
    assert client.post("/api/v1/admin/questions", json={}).status_code == 405


def test_validation_does_not_reflect_password(client):
    password = "secret-value-" * 30
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": password})
    assert response.status_code == 422
    assert password not in response.text and "input" not in response.text


def test_foreign_question_version_and_deadline(logged_student, conn):
    client = logged_student
    attempt_id, assessment, assignment = start(client)
    items = db.table("assessment_items")
    foreign_item = conn.execute(
        select(items.c.id).where(items.c.assessment_id != assessment["id"])
    ).scalar()
    assert (
        client.put(
            f"/api/v1/attempts/{attempt_id}/answers/{foreign_item}",
            json={"answer": {"option_id": "a"}},
        ).status_code
        == 404
    )
    assessments, attempts = db.table("assessments"), db.table("attempts")
    conn.execute(
        assessments.update()
        .where(assessments.c.id == assessment["id"])
        .values(time_limit_seconds=1)
    )
    conn.execute(
        attempts.update()
        .where(attempts.c.id == attempt_id)
        .values(started_at=now() - timedelta(seconds=10))
    )
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").status_code == 409


def test_wrong_answers_create_low_mastery_and_targeted_review(logged_student, conn):
    client = logged_student
    attempt_id, assessment, _ = start(client)
    response = client.post(f"/api/v1/attempts/{attempt_id}/submit")
    assert response.status_code == 200
    skills = client.get("/api/v1/students/me/skills").json()
    assert skills[0]["mastery_score"] == 0 and skills[0]["questions_attempted"] == 8
    assert skills[0]["confidence"] == 0.4
    rec = client.get("/api/v1/students/me/recommendations").json()
    if "fractions" in assessment["code"]:
        assert rec[0]["reason_code"] == "prerequisite"
        assert "Phép tính" in rec[0]["explanation"]
    else:
        assert rec[0]["reason_code"] == "practice_skill"
        items, links = db.table("assessment_items"), db.table("question_skills")
        assert conn.execute(
            select(links.c.skill_id)
            .join(items, items.c.question_version_id == links.c.question_version_id)
            .where(
                items.c.assessment_id == rec[0]["assessment_id"],
                links.c.skill_id == skills[0]["skill_id"],
            )
        ).first()
        assert skills[0]["name"] in rec[0]["explanation"]
