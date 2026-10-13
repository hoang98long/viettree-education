"""Membership checks use real PostgreSQL, isolated from the application database."""

from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.core.security import now
from app.db import db
from app.schemas.memberships import MembershipGrantInput, MembershipRevokeInput
from app.services.attempts import assign_self, start_attempt
from app.services.memberships import change_membership
from tests.test_concurrency import create_student

pytestmark = pytest.mark.integration


def identities(client, conn):
    student_id = UUID(client.get("/api/v1/auth/me").json()["id"])
    users = db.table("users")
    admin_id = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    return student_id, admin_id


def membership(conn, student_id, admin_id, operation="grant", key=None):
    payload = (
        MembershipRevokeInput(reason="Kiểm tra thu hồi quyền")
        if operation == "revoke"
        else MembershipGrantInput(duration_days=30, reason="Kiểm tra cấp gói VIP")
    )
    return change_membership(conn, admin_id, student_id, operation, payload, key or uuid4())


def premium(conn, name="assessments"):
    table, policies = db.table(name), db.table("content_access_policies")
    kind = "lesson" if name == "lessons" else "assessment"
    return (
        conn.execute(
            select(table.c.id)
            .join(policies, policies.c[f"{kind}_id"] == table.c.id)
            .where(policies.c.minimum_plan_code == "vip", table.c.code.like("VT4-%"))
            .order_by(table.c.code)
        )
        .scalars()
        .first()
    )


def start_premium(client, conn):
    assessment_id = premium(conn)
    response = client.post(f"/api/v1/students/me/assessments/{assessment_id}/assign-self")
    assert response.status_code == 200, response.text
    assignment = response.json()
    response = client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]})
    assert response.status_code == 200, response.text
    return response.json()["id"], assignment


def admin_login(client):
    client.cookies.clear()
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": settings().seed_admin_password},
    )
    assert response.status_code == 200
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]


def test_free_catalog_and_preview_do_not_return_premium_content(logged_student, conn):
    client = logged_student
    tables = db.table("content_access_policies")
    for field, free_count, vip_count in (("lesson_id", 24, 6), ("assessment_id", 12, 6)):
        for plan, count in (("free", free_count), ("vip", vip_count)):
            assert (
                conn.execute(
                    select(func.count())
                    .select_from(tables)
                    .where(tables.c[field].is_not(None), tables.c.minimum_plan_code == plan)
                ).scalar_one()
                >= count
            )
    lesson_id, assessment_id = premium(conn, "lessons"), premium(conn)
    blocked = client.get(f"/api/v1/lessons/{lesson_id}")
    assert blocked.status_code == 403
    assert blocked.json()["detail"]["code"] == "MEMBERSHIP_REQUIRED"
    assert "blocks" not in blocked.text
    preview = client.get(f"/api/v1/lessons/{lesson_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["locked"] and preview.json()["preview"]["summary"]
    assert all(key not in preview.json() for key in ("blocks", "content", "grading", "practice"))
    assessment = client.get(f"/api/v1/assessments/{assessment_id}")
    assert assessment.json()["locked"]
    assert "items" not in assessment.json()
    assert (
        client.post(f"/api/v1/students/me/assessments/{assessment_id}/assign-self").status_code
        == 403
    )
    for action in ("visit", "complete"):
        assert client.post(f"/api/v1/lessons/{lesson_id}/{action}").status_code == 403
    assert client.get("/api/v1/students/me/membership").json()["plan_code"] == "free"


def test_student_cannot_self_upgrade_or_access_admin(logged_student, conn):
    client = logged_student
    student_id, _ = identities(client, conn)
    assert (
        client.post(
            f"/api/v1/admin/students/{student_id}/membership/grant",
            json={"duration_days": 30, "reason": "Self upgrade"},
            headers={"Idempotency-Key": str(uuid4())},
        ).status_code
        == 403
    )
    assert (
        client.put(
            "/api/v1/students/me/accessibility",
            json={"text_size": "large", "is_vip": True, "plan_code": "vip"},
        ).status_code
        == 422
    )
    assert client.get("/api/v1/admin/content-access").status_code == 403
    assert (
        client.post(
            "/api/v1/students/me/learning-plans", json={"subject_code": "MATH", "mode": "adaptive"}
        ).status_code
        == 403
    )


def test_admin_grant_extend_revoke_csrf_idempotency_audit(logged_student, conn):
    client = logged_student
    student_id, _ = identities(client, conn)
    admin_login(client)
    path = f"/api/v1/admin/students/{student_id}/membership"
    payload = {"duration_days": 30, "reason": "Cấp VIP theo yêu cầu phụ huynh"}
    key = str(uuid4())
    csrf = client.headers.pop("X-CSRF-Token")
    assert (
        client.post(path + "/grant", json=payload, headers={"Idempotency-Key": key}).status_code
        == 403
    )
    client.headers["X-CSRF-Token"] = csrf
    assert client.post(path + "/grant", json=payload).status_code == 422
    first = client.post(path + "/grant", json=payload, headers={"Idempotency-Key": key})
    assert first.status_code == 200, first.text
    assert (
        client.post(path + "/grant", json=payload, headers={"Idempotency-Key": key}).json()
        == first.json()
    )
    assert (
        client.post(
            path + "/grant", json={**payload, "duration_days": 90}, headers={"Idempotency-Key": key}
        ).status_code
        == 409
    )
    assert (
        client.post(
            path + "/grant", json=payload, headers={"Idempotency-Key": str(uuid4())}
        ).status_code
        == 409
    )
    extension_key = str(uuid4())
    extended = client.post(
        path + "/extend", json=payload, headers={"Idempotency-Key": extension_key}
    )
    assert extended.status_code == 200
    assert datetime.fromisoformat(extended.json()["ends_at"]) - datetime.fromisoformat(
        first.json()["ends_at"]
    ) == timedelta(days=30)
    assert (
        client.post(
            path + "/extend", json=payload, headers={"Idempotency-Key": extension_key}
        ).json()
        == extended.json()
    )
    assert (
        client.post(
            path + "/extend",
            json={**payload, "duration_days": 7},
            headers={"Idempotency-Key": str(uuid4())},
        ).status_code
        == 422
    )
    assert (
        client.post(
            path + "/revoke", json={"reason": ""}, headers={"Idempotency-Key": str(uuid4())}
        ).status_code
        == 422
    )
    revoked = client.post(
        path + "/revoke",
        json={"reason": "Phụ huynh yêu cầu dừng"},
        headers={"Idempotency-Key": str(uuid4())},
    )
    assert revoked.json()["status"] == "revoked"
    assert revoked.json()["plan_code"] == "free"
    history = client.get(path + "/history").json()
    assert len(history) == 3
    logs = db.table("audit_logs")
    assert (
        conn.execute(
            select(func.count())
            .select_from(logs)
            .where(logs.c.entity_id == student_id, logs.c.action.like("membership.%"))
        ).scalar_one()
        == 3
    )
    assert client.get(f"/api/v1/admin/students/{uuid4()}/membership").status_code == 404


def test_vip_unlocks_in_same_session_but_not_other_students(logged_student, conn):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    assert client.get("/api/v1/students/me/membership").json()["plan_code"] == "vip"
    assert client.get(f"/api/v1/lessons/{premium(conn, 'lessons')}").status_code == 200
    assert client.get("/api/v1/admin/questions").status_code == 403
    attempt_id, _ = start_premium(client, conn)
    data = client.get(f"/api/v1/attempts/{attempt_id}")
    assert data.status_code == 200
    assert all(
        secret not in data.text
        for secret in ("grading", "correct_option", "answer_key", "explanation")
    )
    other = create_student(conn)
    membership(conn, other["id"], admin_id)
    assignment = assign_self(conn, other["id"], premium(conn))
    other_attempt = start_attempt(conn, other["id"], assignment["id"])["id"]
    assert client.get(f"/api/v1/attempts/{other_attempt}").status_code == 404
    assert client.post(f"/api/v1/attempts/{other_attempt}/submit").status_code == 404
    assert (
        client.post("/api/v1/attempts", json={"assignment_id": str(assignment["id"])}).status_code
        == 404
    )


@pytest.mark.parametrize("offset,allowed", [(0, True), (3599, True), (3600, False)])
def test_expiry_grace_only_for_original_attempt(logged_student, conn, monkeypatch, offset, allowed):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    members = db.table("student_memberships")
    ends = now() + timedelta(minutes=5)
    conn.execute(members.update().where(members.c.student_id == student_id).values(ends_at=ends))
    attempt_id, assignment = start_premium(client, conn)
    item_id = client.get(f"/api/v1/attempts/{attempt_id}").json()["items"][0]["id"]
    at = ends + timedelta(seconds=offset)
    monkeypatch.setattr("app.services.access.now", lambda: at)
    monkeypatch.setattr("app.services.attempts.now", lambda: at)
    assert client.get("/api/v1/students/me/membership").json()["status"] == "expired"
    assert client.get(f"/api/v1/lessons/{premium(conn, 'lessons')}").status_code == 403
    assert (
        client.post(f"/api/v1/students/me/assessments/{premium(conn)}/assign-self").status_code
        == 403
    )
    assert client.get(f"/api/v1/attempts/{attempt_id}").status_code == (200 if allowed else 403)
    assert client.put(
        f"/api/v1/attempts/{attempt_id}/answers/{item_id}", json={"answer": {"option_id": "a"}}
    ).status_code == (200 if allowed else 403)
    assert client.post(
        "/api/v1/attempts", json={"assignment_id": assignment["id"]}
    ).status_code == (200 if allowed else 403)
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").status_code == (
        200 if allowed else 403
    )
    if allowed:
        assert client.get(f"/api/v1/attempts/{attempt_id}/result").status_code == 200
        assert (
            client.post("/api/v1/attempts", json={"assignment_id": assignment["id"]}).status_code
            == 403
        )


def test_revocation_blocks_attempt_permanently_but_preserves_results(logged_student, conn):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    completed_id, _ = start_premium(client, conn)
    assert client.post(f"/api/v1/attempts/{completed_id}/submit").status_code == 200
    result = client.get(f"/api/v1/attempts/{completed_id}/result").json()
    active_id, _ = start_premium(client, conn)
    item_id = client.get(f"/api/v1/attempts/{active_id}").json()["items"][0]["id"]
    membership(conn, student_id, admin_id, "revoke")
    assert (
        client.get(f"/api/v1/attempts/{active_id}").json()["detail"]["code"] == "MEMBERSHIP_REVOKED"
    )
    assert (
        client.put(
            f"/api/v1/attempts/{active_id}/answers/{item_id}", json={"answer": {"option_id": "a"}}
        ).status_code
        == 403
    )
    assert client.post(f"/api/v1/attempts/{active_id}/submit").status_code == 403
    assert client.get(f"/api/v1/attempts/{completed_id}/result").json() == result
    membership(conn, student_id, admin_id)
    assert client.get(f"/api/v1/attempts/{active_id}").status_code == 403
    assert client.get(f"/api/v1/attempts/{completed_id}/result").json() == result


def test_policy_missing_and_linked_vip_cannot_leak(logged_student, conn):
    client = logged_student
    policies, lessons = db.table("content_access_policies"), db.table("lessons")
    free_lesson = (
        conn.execute(
            select(lessons.c.id)
            .join(policies, policies.c.lesson_id == lessons.c.id)
            .where(policies.c.minimum_plan_code == "free")
        )
        .scalars()
        .first()
    )
    conn.execute(policies.delete().where(policies.c.lesson_id == free_lesson))
    blocked = client.get(f"/api/v1/lessons/{free_lesson}")
    assert blocked.status_code == 403 and blocked.json()["detail"]["code"] == "POLICY_NOT_READY"
    assessment_id = premium(conn)
    conn.execute(
        policies.update()
        .where(policies.c.assessment_id == assessment_id)
        .values(minimum_plan_code="free")
    )
    assert client.get(f"/api/v1/assessments/{assessment_id}").json()["minimum_plan_code"] == "vip"
    assert (
        client.post(f"/api/v1/students/me/assessments/{assessment_id}/assign-self").status_code
        == 403
    )


def test_shared_question_versions_cannot_hide_behind_free_policy(logged_student, conn):
    client = logged_student
    policies, items = db.table("content_access_policies"), db.table("assessment_items")
    vip_id = premium(conn)
    assessments = db.table("assessments")
    source = dict(
        conn.execute(select(assessments).where(assessments.c.id == vip_id)).mappings().one()
    )
    free_id = uuid4()
    source.update(id=free_id, code="test-shared-" + str(free_id), lesson_id=None)
    conn.execute(assessments.insert().values(**source))
    conn.execute(policies.insert().values(assessment_id=free_id, minimum_plan_code="free"))
    version_id = (
        conn.execute(select(items.c.question_version_id).where(items.c.assessment_id == vip_id))
        .scalars()
        .first()
    )
    conn.execute(
        items.insert().values(
            assessment_id=free_id, question_version_id=version_id, position=1, points=1
        )
    )
    assert client.get(f"/api/v1/assessments/{free_id}").json()["locked"]
    assert client.post(f"/api/v1/students/me/assessments/{free_id}/assign-self").status_code == 403


def test_adaptive_plan_pauses_without_losing_progress_and_basic_stays_free(logged_student, conn):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    plan = client.post(
        "/api/v1/students/me/learning-plans", json={"subject_code": "MATH", "mode": "adaptive"}
    )
    assert plan.status_code == 200, plan.text
    assert plan.json()["mode"] == "adaptive" and plan.json()["explanation"]
    first = next(item for item in plan.json()["items"] if item["lesson_id"])
    assert client.post(f"/api/v1/lessons/{first['lesson_id']}/complete").status_code == 200
    membership(conn, student_id, admin_id, "revoke")
    plans = client.get("/api/v1/students/me/learning-plans").json()
    saved = next(row for row in plans if row["id"] == plan.json()["id"])
    assert saved["status"] == "paused" and saved["completed_count"] == 1
    assert (
        client.post(
            "/api/v1/students/me/learning-plans", json={"subject_code": "MATH", "mode": "adaptive"}
        ).status_code
        == 403
    )
    basic = client.post(
        "/api/v1/students/me/learning-plans", json={"subject_code": "MATH", "mode": "basic"}
    )
    assert basic.status_code == 200
    assert all(not item["locked"] for item in basic.json()["items"])


def test_guardian_requires_verified_link(logged_student, conn):
    client = logged_student
    student_id, _ = identities(client, conn)
    assert client.get("/api/v1/guardian/students").status_code == 403
    guardian_id, username = uuid4(), "guardian-" + str(uuid4())
    users = db.table("users")
    password_hash = conn.execute(
        select(users.c.password_hash).where(users.c.id == student_id)
    ).scalar_one()
    conn.execute(
        users.insert().values(
            id=guardian_id,
            username=username,
            display_name="Test Guardian",
            password_hash=password_hash,
        )
    )
    conn.execute(db.table("user_roles").insert().values(user_id=guardian_id, role="guardian"))
    links = db.table("guardian_students")
    conn.execute(
        links.insert().values(
            guardian_user_id=guardian_id, student_id=student_id, relationship="guardian"
        )
    )
    client.cookies.clear()
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": settings().seed_student_password},
        ).status_code
        == 200
    )
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]
    assert client.get("/api/v1/guardian/students").json() == []
    assert client.get(f"/api/v1/guardian/students/{student_id}/membership").status_code == 404
    conn.execute(
        links.update().where(links.c.guardian_user_id == guardian_id).values(verified_at=now())
    )
    assert client.get("/api/v1/guardian/students").json()[0]["id"] == str(student_id)
    assert client.get(f"/api/v1/guardian/students/{student_id}/membership").status_code == 200
    assert client.get(f"/api/v1/guardian/students/{uuid4()}/membership").status_code == 404


def test_admin_policy_update_is_audited_and_seed_preserves_it(logged_student, conn):
    from app.fixtures.development import seed

    client = logged_student
    lesson_id = premium(conn, "lessons")
    admin_login(client)
    path = f"/api/v1/admin/content/lesson/{lesson_id}/policy"
    payload = {
        "minimum_plan_code": "free",
        "learning_level": "advanced",
        "preview": {"summary": "Giới thiệu riêng", "goals": ["Mục tiêu ngắn"]},
        "reason": "Mở miễn phí theo kế hoạch",
    }
    assert client.put(path, json=payload).status_code == 200
    seed(conn)
    policies = db.table("content_access_policies")
    saved = conn.execute(select(policies).where(policies.c.lesson_id == lesson_id)).mappings().one()
    assert saved["minimum_plan_code"] == "free" and saved["preview"] == payload["preview"]
    logs = db.table("audit_logs")
    assert (
        conn.execute(
            select(logs.c.new_values).where(
                logs.c.entity_id == lesson_id, logs.c.action == "content.policy_update"
            )
        ).scalar_one()["reason"]
        == payload["reason"]
    )
    assert client.put(path, json={**payload, "preview": {"summary": "x" * 351}}).status_code == 422
    conn.execute(policies.delete().where(policies.c.lesson_id == lesson_id))
    assert (
        client.put(path, json=payload).status_code == 200
    )  # Creation also audits an empty previous state.


def test_expired_extension_starts_from_server_time(logged_student, conn, monkeypatch):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    members = db.table("student_memberships")
    at = now()
    conn.execute(
        members.update()
        .where(members.c.student_id == student_id)
        .values(starts_at=at - timedelta(days=60), ends_at=at - timedelta(days=30))
    )
    monkeypatch.setattr("app.services.memberships.now", lambda: at)
    result = membership(conn, student_id, admin_id, "extend")
    assert datetime.fromisoformat(result["starts_at"]) == at
    assert datetime.fromisoformat(result["ends_at"]) == at + timedelta(days=30)


def test_adaptive_plan_prioritizes_real_weak_skill(logged_student, conn):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    topics, lessons, links = db.table("topics"), db.table("lessons"), db.table("lesson_skills")
    target_topic = conn.execute(
        select(topics.c.id).where(topics.c.code == "VT4-MATH-operations")
    ).scalar_one()
    skill_id = (
        conn.execute(
            select(links.c.skill_id)
            .join(lessons, lessons.c.id == links.c.lesson_id)
            .where(lessons.c.topic_id == target_topic)
        )
        .scalars()
        .first()
    )
    mastery = db.table("student_skill_mastery")
    conn.execute(
        mastery.insert().values(
            student_id=student_id,
            skill_id=skill_id,
            mastery_score=0.2,
            confidence=0.5,
            questions_attempted=10,
            correct_count=2,
            next_review_at=now() - timedelta(days=1),
        )
    )
    plan = client.post(
        "/api/v1/students/me/learning-plans", json={"subject_code": "MATH", "mode": "adaptive"}
    ).json()
    first = next(item for item in plan["items"] if item["lesson_id"])
    first_topic = conn.execute(
        select(lessons.c.topic_id).where(lessons.c.id == UUID(first["lesson_id"]))
    ).scalar_one()
    assert first_topic == target_topic
    policies = db.table("content_access_policies")
    assert (
        conn.execute(
            select(policies.c.learning_level).where(
                policies.c.lesson_id == UUID(first["lesson_id"])
            )
        ).scalar_one()
        == "basic"
    )
    assert (
        conn.execute(
            select(mastery.c.questions_attempted).where(mastery.c.student_id == student_id)
        ).scalar_one()
        == 10
    )


@pytest.mark.parametrize("limit", ["assignment", "assessment"])
def test_grace_never_extends_assignment_or_timed_deadline(logged_student, conn, monkeypatch, limit):
    client = logged_student
    student_id, admin_id = identities(client, conn)
    membership(conn, student_id, admin_id)
    at = now()
    members = db.table("student_memberships")
    conn.execute(
        members.update()
        .where(members.c.student_id == student_id)
        .values(ends_at=at + timedelta(seconds=5))
    )
    if limit == "assessment":
        table = db.table("assessments")
        conn.execute(
            table.update().where(table.c.id == premium(conn)).values(time_limit_seconds=10)
        )
    attempt_id, assignment = start_premium(client, conn)
    if limit == "assignment":
        # Tighten the due date after starting; server must still recheck it on submission.
        table = db.table("student_assignments")
        conn.execute(
            table.update()
            .where(table.c.id == UUID(assignment["id"]))
            .values(due_at=at + timedelta(seconds=10))
        )
    future = at + timedelta(seconds=20)
    monkeypatch.setattr("app.services.access.now", lambda: future)
    monkeypatch.setattr("app.services.attempts.now", lambda: future)
    assert client.post(f"/api/v1/attempts/{attempt_id}/submit").status_code in (403, 409)
