from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.db import db
from tests.test_memberships import admin_login, identities

pytestmark = pytest.mark.integration
BASE = "/api/v1/admin/authoring"


def question_payload(client, plan="free", kind="single_choice"):
    options = client.get(BASE + "/options").json()
    subject = next(item for item in options["subjects"] if item["code"] == "MATH")
    topic = next(item for item in options["topics"] if item["subject_id"] == subject["id"])
    skill = next(item for item in options["skills"] if item["topic_id"] == topic["id"])
    keys = {
        "single_choice": {"correct_option_id": "a"},
        "multiple_choice": {"correct_option_ids": ["a", "c"]},
        "ordering": {"ordered_ids": ["b", "a", "c"]},
        "fill_blank": {"accepted_answers": ["4"]},
    }
    return {
        "code": "author-test-" + str(uuid4()),
        "grade": 4,
        "subject_id": subject["id"],
        "topic_id": topic["id"],
        "skill_ids": [skill["id"]],
        "question_type": kind,
        "difficulty": 2,
        "minimum_plan_code": plan,
        "content": {
            "prompt": "Hai cộng hai bằng bao nhiêu?",
            "options": []
            if kind == "fill_blank"
            else [{"id": "a", "text": "4"}, {"id": "b", "text": "3"}, {"id": "c", "text": "6"}],
        },
        "grading": keys[kind],
        "explanation": "Hai cộng hai bằng bốn.",
    }


def action(client, kind, data, operation):
    response = client.post(
        f"{BASE}/{kind}/{data['id']}/{operation}",
        json={"expected_revision": data["edit_revision"], "reason": "Kiểm tra nội dung và đáp án"},
    )
    assert response.status_code == 200, response.text
    return response.json()


def publish_question(client, plan="free", kind="single_choice"):
    payload = question_payload(client, plan, kind)
    response = client.post(BASE + "/questions", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    data = action(client, "questions", data, "review")
    return payload, action(client, "questions", data, "publish")


def assessment_payload(question_payload, question):
    return {
        "code": "assessment-test-" + str(uuid4()),
        "grade": 4,
        "subject_id": question_payload["subject_id"],
        "topic_id": question_payload["topic_id"],
        "title": "Bài tập kiểm tra soạn nội dung",
        "minimum_plan_code": question_payload["minimum_plan_code"],
        "items": [{"question_version_id": question["id"], "points": 2}],
    }


def restore_student(client, cookies):
    client.cookies.clear()
    client.cookies.update(cookies)
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]


@pytest.mark.parametrize("kind", ["single_choice", "multiple_choice", "fill_blank", "ordering"])
def test_question_draft_review_publish_and_invalid_keys(logged_student, conn, kind):
    client = logged_student
    admin_login(client)
    payload = question_payload(client, kind=kind)
    wrong = {**payload, "grading": {"correct_option_id": "missing"}}
    assert client.post(BASE + "/questions", json=wrong).status_code == 422
    response = client.post(BASE + "/questions", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "draft" and data["reviewed_by"] is None
    assert client.post(BASE + "/questions", json=payload).status_code == 409
    assert (
        client.post(
            f"{BASE}/questions/{data['id']}/publish",
            json={"expected_revision": data["edit_revision"], "reason": "Chưa qua duyệt nội dung"},
        ).status_code
        == 409
    )
    reviewed = action(client, "questions", data, "review")
    assert (
        client.put(
            f"{BASE}/questions/{data['id']}",
            json={**payload, "expected_revision": data["edit_revision"]},
        ).status_code
        == 409
    )
    updated = client.put(
        f"{BASE}/questions/{data['id']}",
        json={**payload, "expected_revision": reviewed["edit_revision"]},
    )
    assert updated.status_code == 200 and updated.json()["reviewed_by"] is None
    published = action(
        client, "questions", action(client, "questions", updated.json(), "review"), "publish"
    )
    assert published["status"] == "published"
    assert (
        client.put(
            f"{BASE}/questions/{data['id']}",
            json={**payload, "expected_revision": published["edit_revision"]},
        ).status_code
        == 409
    )
    csrf = client.headers.pop("X-CSRF-Token")
    assert (
        client.post(BASE + "/questions", json={**payload, "code": "different-code"}).status_code
        == 403
    )
    client.headers["X-CSRF-Token"] = csrf


def test_scope_and_duplicate_options_rejected(logged_student, conn):
    client = logged_student
    admin_login(client)
    payload = question_payload(client)
    assert client.post(BASE + "/questions", json={**payload, "grade": 3}).status_code == 422
    assert (
        client.post(BASE + "/questions", json={**payload, "skill_ids": [str(uuid4())]}).status_code
        == 422
    )
    assert (
        client.post(BASE + "/questions", json={**payload, "explanation": "     "}).status_code
        == 422
    )
    invalid = {
        **payload,
        "content": {
            **payload["content"],
            "options": [{"id": "a", "text": "4"}, {"id": "a", "text": "5"}],
        },
    }
    assert client.post(BASE + "/questions", json=invalid).status_code == 422


def test_revision_preserves_old_assessment_and_grading(logged_student, conn):
    client = logged_student
    student_id, _ = identities(client, conn)
    student_cookies = dict(client.cookies)
    admin_login(client)
    payload, question = publish_question(client)
    created = client.post(BASE + "/assessments", json=assessment_payload(payload, question))
    assert created.status_code == 200, created.text
    assessment = action(
        client, "assessments", action(client, "assessments", created.json(), "review"), "publish"
    )
    restore_student(client, student_cookies)
    assignment = client.post(
        f"/api/v1/students/me/assessments/{assessment['id']}/assign-self"
    ).json()
    attempt_id = client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).json()[
        "id"
    ]
    item_id = client.get(f"/api/v1/attempts/{attempt_id}").json()["items"][0]["id"]
    assert (
        client.put(
            f"/api/v1/attempts/{attempt_id}/answers/{item_id}", json={"answer": {"option_id": "a"}}
        ).status_code
        == 200
    )
    student_cookies = dict(client.cookies)
    admin_login(client)
    revised = client.post(f"{BASE}/questions/{question['id']}/revise")
    assert revised.status_code == 200, revised.text
    draft = revised.json()
    assert draft["version"] == 2 and draft["reviewed_by"] is None
    assert client.post(f"{BASE}/questions/{question['id']}/revise").status_code == 409
    changed = client.put(
        f"{BASE}/questions/{draft['id']}",
        json={
            **payload,
            "grading": {"correct_option_id": "b"},
            "expected_revision": draft["edit_revision"],
        },
    )
    assert changed.status_code == 200, changed.text
    action(client, "questions", action(client, "questions", changed.json(), "review"), "publish")
    assert client.get(f"{BASE}/questions/{question['id']}").json()["status"] == "archived"
    assert (
        client.put(
            f"{BASE}/assessments/{assessment['id']}",
            json={
                **assessment_payload(payload, question),
                "code": assessment["code"],
                "expected_revision": assessment["edit_revision"],
            },
        ).status_code
        == 409
    )
    restore_student(client, student_cookies)
    submitted = client.post(f"/api/v1/attempts/{attempt_id}/submit")
    assert submitted.status_code == 200 and submitted.json()["total_score"] == 2
    # Previously published assessments still start against their old immutable question versions.
    assert (
        client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).status_code == 200
    )
    assert (
        client.get(f"/api/v1/attempts/{attempt_id}/result").json()["items"][0]["grading"][
            "correct_option_id"
        ]
        == "a"
    )
    assert UUID(client.get("/api/v1/auth/me").json()["id"]) == student_id


def test_standalone_vip_question_cannot_be_published_in_free_assessment(logged_student, conn):
    client = logged_student
    cookies = dict(client.cookies)
    admin_login(client)
    payload, question = publish_question(client, "vip")
    data = assessment_payload(payload, question)
    data["minimum_plan_code"] = "free"
    created = client.post(BASE + "/assessments", json=data).json()
    assert created["effective_access"]["minimum_plan_code"] == "vip"
    assert (
        client.post(
            f"{BASE}/assessments/{created['id']}/review",
            json={"expected_revision": created["edit_revision"], "reason": "Kiểm tra yêu cầu VIP"},
        ).status_code
        == 422
    )
    changed = client.put(
        f"{BASE}/assessments/{created['id']}",
        json={**data, "minimum_plan_code": "vip", "expected_revision": created["edit_revision"]},
    )
    assert changed.status_code == 200, changed.text
    published = action(
        client, "assessments", action(client, "assessments", changed.json(), "review"), "publish"
    )
    restore_student(client, cookies)
    assert (
        client.post(f"/api/v1/students/me/assessments/{published['id']}/assign-self").status_code
        == 403
    )
    assert client.get(f"{BASE}/questions/{question['id']}").status_code == 403
    assert client.post(BASE + "/questions", json=payload).status_code == 403


def test_bulk_assign_is_atomic_and_repeated_requests_reuse_task(logged_student, conn):
    from tests.test_concurrency import create_student

    client = logged_student
    student_id, _ = identities(client, conn)
    cookies = dict(client.cookies)
    admin_login(client)
    payload, question = publish_question(client)
    draft = client.post(BASE + "/assessments", json=assessment_payload(payload, question)).json()
    published = action(
        client, "assessments", action(client, "assessments", draft, "review"), "publish"
    )
    path = f"{BASE}/assessments/{published['id']}/assign"
    users = db.table("users")
    username = conn.execute(select(users.c.username).where(users.c.id == student_id)).scalar_one()
    found = client.get("/api/v1/admin/students", params={"search": username}).json()
    assert found["total"] == 1 and found["items"][0]["id"] == str(student_id)
    first = client.post(path, json={"student_ids": [str(student_id)]})
    assert first.status_code == 200, first.text
    repeated = client.post(path, json={"student_ids": [str(student_id)]})
    assert repeated.json()["assignments"][0]["id"] == first.json()["assignments"][0]["id"]
    other = create_student(conn)
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == other["id"]).values(current_grade=3)
    )
    assert (
        client.post(path, json={"student_ids": [str(student_id), str(other["id"])]}).status_code
        == 403
    )
    cloned = client.post(
        f"{BASE}/assessments/{published['id']}/clone", json={"code": "clone-" + str(uuid4())}
    )
    assert cloned.status_code == 200 and cloned.json()["status"] == "draft"
    restore_student(client, cookies)
    task = next(
        item
        for item in client.get("/api/v1/students/me/assignments").json()
        if item["assessment_id"] == published["id"]
    )
    attempt = client.post("/api/v1/attempts", json={"assignment_id": task["id"]}).json()
    admin_login(client)
    archive = client.post(
        f"{BASE}/assessments/{published['id']}/archive",
        json={"expected_revision": published["edit_revision"], "reason": "Đang có học sinh làm"},
    )
    assert archive.status_code == 409
    restore_student(client, cookies)
    assert client.post(f"/api/v1/attempts/{attempt['id']}/submit").status_code == 200


def test_expanded_content_grading_and_demo_seed_idempotency(conn):
    from app.curriculum.grades.grade_04.standard import EXPANDED
    from app.fixtures.learners import seed_demo_learners
    from app.services.grading import grade_answer, validate_answer
    from tests.test_grading import correct_answer

    for units in EXPANDED.values():
        assert len(units) == 4
        for unit in units:
            assert len(unit["questions"]) == 6
            for question in unit["questions"]:
                answer = correct_answer(question)
                validate_answer(question["question_type"], question["content"], answer)
                assert grade_answer(question["question_type"], question["grading"], answer)
    first = seed_demo_learners(conn)
    assert all(row["created"] for row in first)
    assert all(not row["created"] for row in seed_demo_learners(conn))
    users = db.table("users")
    for username in ("free4_01", "free4_02", "vip4_01", "vip4_02"):
        identifier = conn.execute(
            select(users.c.id).where(users.c.username == username)
        ).scalar_one()
        from app.services.access import resolve_membership

        assert resolve_membership(conn, identifier)["plan_code"] == (
            "vip" if username.startswith("vip") else "free"
        )
