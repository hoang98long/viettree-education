from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select, update

from app.academy.media import uid
from app.classroom.recognition import aggregate
from app.core.config import settings
from app.db import db
from app.schemas import MembershipGrantInput, MembershipRevokeInput
from app.services.memberships import change_membership
from tests.test_academy import insert_user, login


def grant(conn, identifier):
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    return change_membership(
        conn,
        admin,
        identifier,
        "grant",
        MembershipGrantInput(duration_days=30, reason="Kiểm thử quyền VIP đào tạo"),
        uuid4(),
    )


def make_class(client, teacher=None):
    response = client.post(
        "/api/v1/classroom/classes",
        json={
            "name": "Lớp kiểm thử " + uuid4().hex[:6],
            "grade": 4,
            "teacher_id": str(teacher) if teacher else None,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["id"]


@pytest.mark.integration
def test_classes_enroll_free_scope_and_edit_revision(client, conn):
    teacher, tname = insert_user(conn, "teacher")
    outsider, oname = insert_user(conn, "teacher")
    student, sname = insert_user(conn, "student", 4)
    wrong, _ = insert_user(conn, "student", 3)
    login(client)
    classroom = make_class(client, teacher)
    roster = f"/api/v1/classroom/classes/{classroom}/enrollments"
    assert client.post(roster, json={"student_id": str(wrong)}).status_code == 422
    assert client.post(roster, json={"student_id": str(student)}).status_code == 200
    free = client.get("/api/v1/classroom/students?grade=4&free_only=true&search=" + sname).json()
    assert free["total"] == 0
    body = {"name": "Lớp đã chỉnh", "grade": 4, "teacher_id": str(teacher), "revision": 1}
    assert client.put(f"/api/v1/classroom/classes/{classroom}", json=body).status_code == 200
    assert client.put(f"/api/v1/classroom/classes/{classroom}", json=body).status_code == 409
    login(client, oname, settings().seed_student_password)
    assert (
        client.post(roster, json={"student_id": str(student), "enrolled": False}).status_code == 403
    )
    assert client.get(f"/api/v1/classroom/classes/{classroom}/leaderboard").status_code == 403
    login(client, tname, settings().seed_student_password)
    assert (
        client.get(f"/api/v1/classroom/students?class_id={classroom}&grade=4").json()["total"] == 1
    )
    assert client.get("/api/v1/classroom/students?grade=4&free_only=true").status_code == 403
    assert (
        client.post(roster, json={"student_id": str(student), "enrolled": False}).status_code == 200
    )
    login(client, sname, settings().seed_student_password)
    assert client.get("/api/v1/classroom/classes").json() == []
    assert client.get(f"/api/v1/classroom/classes/{classroom}/recognition").status_code == 403
    assert conn.execute(
        select(db.table("users").c.id).where(db.table("users").c.id.in_([student, outsider]))
    ).all()


@pytest.mark.integration
def test_individual_and_class_assignments_idempotent_and_membership_checked(client, conn):
    student, sname = insert_user(conn, "student", 4)
    login(client)
    classroom = make_class(client)
    assert (
        client.post(
            f"/api/v1/classroom/classes/{classroom}/enrollments", json={"student_id": str(student)}
        ).status_code
        == 200
    )
    key = str(uuid4())
    body = {
        "kind": "ai_lesson",
        "resource_id": str(uid("AI4-01")),
        "student_ids": [str(student)],
        "idempotency_key": key,
    }
    first = client.post("/api/v1/classroom/assignments", json=body)
    assert first.status_code == 200, first.text
    assert (
        client.post("/api/v1/classroom/assignments", json=body).json()["id"] == first.json()["id"]
    )
    assert (
        client.post(
            "/api/v1/classroom/assignments", json={**body, "resource_id": str(uid("AI4-04"))}
        ).status_code
        == 409
    )
    premium = {
        "kind": "ai_lesson",
        "resource_id": str(uid("AI4-02")),
        "class_id": classroom,
        "idempotency_key": str(uuid4()),
    }
    assert client.post("/api/v1/classroom/assignments", json=premium).status_code == 403
    grant(conn, student)
    assert client.post("/api/v1/classroom/assignments", json=premium).status_code == 200
    resources = client.get("/api/v1/classroom/resources?kind=assessment&grade=4").json()
    assessment = next(r for r in resources if r["minimum_plan_code"] == "free")
    assigned = client.post(
        "/api/v1/classroom/assignments",
        json={
            "kind": "assessment",
            "resource_id": assessment["id"],
            "class_id": classroom,
            "idempotency_key": str(uuid4()),
        },
    )
    assert assigned.status_code == 200, assigned.text
    login(client, sname, settings().seed_student_password)
    tasks = client.get("/api/v1/classroom/my-assignments").json()
    assert len(tasks) == 3 and any(t["assignment_id"] for t in tasks)
    academy_tasks = client.get("/api/v1/ai-academy/home").json()["assignments"]
    assert len(academy_tasks) == 2
    assert sum(t["class_name"] == "Bài giao riêng" for t in academy_tasks) == 1
    assert {t["lesson_id"] for t in academy_tasks} == {str(uid("AI4-01")), str(uid("AI4-02"))}
    assert client.post("/api/v1/classroom/assignments", json=body).status_code == 403


def test_ranking_best_per_resource_and_deterministic_ties():
    first, second, task = uuid4(), uuid4(), uuid4()
    at = datetime(2026, 10, 12, tzinfo=timezone.utc)
    rows = [
        {"student_id": first, "resource_id": task, "score": 80, "at": at},
        {"student_id": first, "resource_id": task, "score": 95, "at": at},
        {"student_id": first, "resource_id": task, "score": 95, "at": at + timedelta(seconds=10)},
        {"student_id": second, "resource_id": task, "score": 95, "at": at + timedelta(seconds=1)},
    ]
    ranked = aggregate(rows)
    assert len(ranked) == 2 and ranked[0]["student_id"] == first
    assert ranked[0]["completed"] == 1 and ranked[0]["score"] == 95


@pytest.mark.integration
def test_ai_ranking_private_top_three_snapshots_and_no_repeat_bonus(client, conn):
    teacher, tname = insert_user(conn, "teacher")
    people = [insert_user(conn, "student", 4) for _ in range(4)]
    login(client)
    classroom = make_class(client, teacher)
    versions = db.table("ai_lesson_versions")
    version = conn.execute(
        select(versions.c.id).where(
            versions.c.lesson_id == uid("AI4-01"), versions.c.status == "published"
        )
    ).scalar_one()
    for i, (student, name) in enumerate(people):
        assert (
            client.post(
                f"/api/v1/classroom/classes/{classroom}/enrollments",
                json={"student_id": str(student)},
            ).status_code
            == 200
        )
        for _ in range(3):
            conn.execute(
                db.table("ai_attempts")
                .insert()
                .values(
                    student_id=student,
                    version_id=version,
                    step_id="checkpoint",
                    idempotency_key=uuid4(),
                    level=2,
                    answers={},
                    score=(95 - i * 10) / 100,
                    feedback={},
                )
            )
    board = f"/api/v1/classroom/classes/{classroom}/leaderboard?category=AI"
    login(client, tname, settings().seed_student_password)
    response = client.get(board)
    assert response.status_code == 200, response.text
    ranked = response.json()
    assert len(ranked["rows"]) == 4 and len(ranked["top_three"]) == 3
    assert ranked["rows"][0]["score"] == 95 and ranked["rows"][0]["completed"] == 1
    recognition = f"/api/v1/classroom/classes/{classroom}/recognition"
    published = client.post(recognition, json={"category": "AI", "period": "month"})
    assert published.status_code == 200, published.text
    assert client.post(recognition, json={"category": "AI", "period": "month"}).json()["replayed"]
    awards = client.get(recognition).json()
    assert len(awards) == 1 and len(awards[0]["winners"]) == 3
    login(client, people[0][1], settings().seed_student_password)
    result = client.get(board).json()
    assert all("student_id" not in r and "username" not in r for r in result["rows"])
    assert all(r["display_name"].startswith("Bạn ") for r in result["rows"])
    assert result["rows"][0]["is_me"]
    assert client.post(recognition, json={"category": "AI"}).status_code == 403
    own = client.get("/api/v1/classroom/my-achievements")
    assert own.status_code == 200, own.text
    assert next(r for r in own.json()["categories"] if r["category"] == "AI")["score"] == 95
    for category in ["MATH", "VIETNAMESE", "ENGLISH", "AI_PROJECT"]:
        empty = client.get(board.replace("category=AI", "category=" + category))
        assert empty.status_code == 200, empty.text
    login(client)
    users = db.table("users")
    conn.execute(update(users).where(users.c.id == people[3][0]).values(is_active=False))
    assert len(client.get(board).json()["rows"]) == 3
    profiles = db.table("student_profiles")
    conn.execute(
        update(profiles).where(profiles.c.student_id == people[2][0]).values(current_grade=5)
    )
    assert len(client.get(board).json()["rows"]) == 2
    assert (
        client.post(
            f"/api/v1/classroom/classes/{classroom}/enrollments",
            json={"student_id": str(people[0][0]), "enrolled": False},
        ).status_code
        == 200
    )
    login(client, people[0][1], settings().seed_student_password)
    assert client.get(board).status_code == 403


@pytest.mark.integration
def test_reference_pricing_sale_dates_and_confirmation(client, conn, monkeypatch):
    monkeypatch.setattr(
        "app.classroom.pricing.now", lambda: datetime(2026, 10, 12, 12, tzinfo=timezone.utc)
    )
    public = client.get("/api/v1/membership/prices")
    assert public.status_code == 200, public.text
    data = public.json()
    assert [r["effective_price_vnd"] for r in data["offers"]] == [79000, 219000, 699000]
    assert len(data["market_references"]) == 4 and data["reference_only"]
    assert all("updated_by" not in r for r in data["offers"])
    monkeypatch.setattr(
        "app.classroom.pricing.now", lambda: datetime(2026, 12, 1, tzinfo=timezone.utc)
    )
    assert all(
        r["promotion"] is None for r in client.get("/api/v1/membership/prices").json()["offers"]
    )
    login(client)
    price = client.get("/api/v1/admin/membership/prices").json()["price_options"][0]
    payload = {
        "label": price["label"],
        "reference_price_vnd": 109000,
        "is_active": True,
        "revision": price["revision"],
        "reason": "Điều chỉnh giá tham khảo",
        "actor_password": "incorrect-password",
    }
    path = "/api/v1/admin/membership/prices/" + price["code"]
    assert client.put(path, json=payload).status_code == 403
    payload["actor_password"] = settings().seed_admin_password
    assert client.put(path, json=payload).status_code == 200
    assert client.put(path, json=payload).status_code == 409
    promotion = {
        "code": "test-" + uuid4().hex,
        "price_code": price["code"],
        "label": "Ưu đãi kiểm thử có thời hạn",
        "sale_price_vnd": 110000,
        "starts_at": "2026-10-12T00:00:00+07:00",
        "ends_at": "2026-12-31T00:00:00+07:00",
        "reason": "Kiểm tra điều kiện giá sale",
        "actor_password": settings().seed_admin_password,
    }
    route = "/api/v1/admin/membership/promotions"
    assert client.post(route, json=promotion).status_code == 422
    promotion["sale_price_vnd"] = 89000
    assert client.post(route, json=promotion).status_code == 200
    lower = {**promotion, "code": "test-" + uuid4().hex, "sale_price_vnd": 79000}
    assert client.post(route, json=lower).status_code == 200
    assert (
        client.get("/api/v1/membership/prices").json()["offers"][0]["effective_price_vnd"] == 79000
    )
    assert client.post(route, json={**lower, "is_active": False, "revision": 1}).status_code == 200
    assert client.post(route, json={**lower, "is_active": False, "revision": 1}).status_code == 409
    assert (
        client.get("/api/v1/membership/prices").json()["offers"][0]["effective_price_vnd"] == 89000
    )


@pytest.mark.integration
def test_vip_replay_after_revoke_and_extend_revoked_requires_new_grant(client, conn):
    student, _ = insert_user(conn, "student", 4)
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    key = uuid4()
    payload = MembershipGrantInput(duration_days=30, reason="Kiểm thử cấp VIP")
    change_membership(conn, admin, student, "grant", payload, key)
    change_membership(
        conn, admin, student, "revoke", MembershipRevokeInput(reason="Kiểm thử thu hồi"), uuid4()
    )
    replay = change_membership(conn, admin, student, "grant", payload, key)
    assert replay["status"] == "revoked" and replay["plan_code"] == "free"
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as error:
        change_membership(conn, admin, student, "extend", payload, uuid4())
    assert error.value.status_code == 409
    assert change_membership(conn, admin, student, "grant", payload, uuid4())["plan_code"] == "vip"


@pytest.mark.integration
def test_ai_free_vip_gate_revocation_media_and_training_never_calls_provider(
    logged_student, conn, monkeypatch
):
    client = logged_student
    student = UUID(client.get("/api/v1/auth/me").json()["id"])
    catalog = client.get("/api/v1/ai-academy/catalog?grade=4").json()
    assert len([r for r in catalog if not r["locked"]]) == 3
    lesson = str(uid("AI4-02"))
    start = f"/api/v1/ai-academy/lessons/{lesson}/start"
    assert client.post(start).status_code == 403
    assert client.get("/api/v1/ai-academy/media/AI4-02-support-1").status_code == 403
    assert client.get("/api/v1/ai-academy/lab").status_code == 403
    assert client.get("/api/v1/ai-academy/projects").status_code == 403
    grant(conn, student)
    assert client.post(start).status_code == 200
    assert (
        client.get("/api/v1/ai-academy/media/AI4-02-support-1").headers["cache-control"]
        == "no-store"
    )
    flags, providers = db.table("ai_feature_flags"), db.table("ai_provider_configs")
    conn.execute(update(flags).where(flags.c.code == "tutor_enabled").values(enabled=True))
    conn.execute(
        update(providers)
        .where(providers.c.code == "ollama")
        .values(enabled=True, policy_approved=True)
    )
    conn.execute(
        db.table("privacy_consents")
        .insert()
        .values(
            student_id=student,
            purpose_code="ai_academy_provider",
            policy_version="ai-academy-v1",
            consent_given=True,
        )
    )
    monkeypatch.setattr(settings(), "ai_provider", "ollama")
    calls = []
    monkeypatch.setattr("app.academy.tutor.httpx.post", lambda *a, **k: calls.append(k))
    assert (
        client.post(
            "/api/v1/ai-academy/tutor", json={"lesson_id": lesson, "mode": "ExplainConcept"}
        ).json()["mode"]
        == "simulation"
    )
    assert calls == []
    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        admin,
        student,
        "revoke",
        MembershipRevokeInput(reason="Thu hồi trong khi bài đã mở"),
        uuid4(),
    )
    assert client.post(start).status_code == 403
    assert (
        client.post(
            f"/api/v1/ai-academy/lessons/{lesson}/steps", json={"step_id": "story"}
        ).status_code
        == 403
    )
    assert client.get("/api/v1/ai-academy/portfolio").status_code == 200
    assert client.get("/api/v1/classroom/my-achievements").status_code == 200
    progress = db.table("ai_progress")
    assert (
        conn.execute(
            select(func.count())
            .select_from(progress)
            .where(progress.c.student_id == student, progress.c.lesson_id == lesson)
        ).scalar_one()
        == 1
    )


@pytest.mark.integration
def test_ai_access_policy_confirmation_revision_and_live_effect(client, conn):
    student, name = insert_user(conn, "student", 4)
    _, tname = insert_user(conn, "teacher")
    lesson = uid("AI4-02")
    lessons = db.table("ai_lessons")
    revision = conn.execute(select(lessons.c.revision).where(lessons.c.id == lesson)).scalar_one()
    path = f"/api/v1/ai-academy/admin/lessons/{lesson}/access"
    payload = {
        "minimum_plan_code": "free",
        "revision": revision,
        "reason": "Mở bài trải nghiệm cho học sinh",
        "actor_password": "wrong-password",
    }
    login(client)
    assert client.put(path, json=payload).status_code == 403
    payload["actor_password"] = settings().seed_admin_password
    assert client.put(path, json=payload).status_code == 200
    assert client.put(path, json=payload).status_code == 409
    login(client, name, settings().seed_student_password)
    assert client.post(f"/api/v1/ai-academy/lessons/{lesson}/start").status_code == 200
    login(client, tname, settings().seed_student_password)
    assert client.put(path, json={**payload, "revision": revision + 1}).status_code == 403
    login(client)
    assert (
        client.put(
            path, json={**payload, "revision": revision + 1, "minimum_plan_code": "vip"}
        ).status_code
        == 200
    )
    login(client, name, settings().seed_student_password)
    assert (
        client.post(
            f"/api/v1/ai-academy/lessons/{lesson}/steps", json={"step_id": "story"}
        ).status_code
        == 403
    )
    assert conn.execute(
        select(db.table("ai_progress").c.student_id).where(
            db.table("ai_progress").c.student_id == student
        )
    ).first()


@pytest.mark.integration
def test_existing_academy_assignment_checks_vip_recipients(client, conn):
    student, _ = insert_user(conn, "student", 4)
    login(client)
    classroom = make_class(client)
    assert (
        client.post(
            f"/api/v1/classroom/classes/{classroom}/enrollments", json={"student_id": str(student)}
        ).status_code
        == 200
    )
    payload = {"class_id": classroom, "lesson_id": str(uid("AI4-02"))}
    assert client.post("/api/v1/ai-academy/teacher/assignments", json=payload).status_code == 403
    assignments = db.table("ai_assignments")
    assert not conn.execute(
        select(assignments.c.id).where(assignments.c.class_id == classroom)
    ).first()
    grant(conn, student)
    assert (
        client.post("/api/v1/ai-academy/teacher/assignments", json=payload).json()["targets"] == 1
    )


@pytest.mark.integration
def test_core_ranking_normalizes_scores_and_project_results_stay_in_class(client, conn):
    from app.core.security import now

    student, _ = insert_user(conn, "student", 4)
    login(client)
    classroom = make_class(client)
    other = make_class(client)
    assert (
        client.post(
            f"/api/v1/classroom/classes/{classroom}/enrollments", json={"student_id": str(student)}
        ).status_code
        == 200
    )
    assessments, subjects, policies = (
        db.table(n) for n in ("assessments", "subjects", "content_access_policies")
    )
    resource = conn.execute(
        select(assessments.c.id)
        .join(subjects)
        .join(policies, policies.c.assessment_id == assessments.c.id)
        .where(
            assessments.c.grade == 4,
            subjects.c.code == "MATH",
            policies.c.minimum_plan_code == "free",
            assessments.c.status == "published",
        )
    ).scalar()
    assert resource
    batch = client.post(
        "/api/v1/classroom/assignments",
        json={
            "kind": "assessment",
            "resource_id": str(resource),
            "student_ids": [str(student)],
            "idempotency_key": str(uuid4()),
        },
    ).json()["id"]
    targets = db.table("learning_assignment_targets")
    assignment = conn.execute(
        select(targets.c.assignment_id).where(targets.c.batch_id == batch)
    ).scalar_one()
    attempts = db.table("attempts")
    at = now()
    for number, (score, maximum, status) in enumerate(
        [(2.1, 3, "graded"), (2.7, 3, "graded"), (3, 3, "in_progress"), (0, 0, "graded")], 1
    ):
        conn.execute(
            attempts.insert().values(
                assignment_id=assignment,
                student_id=student,
                assessment_id=resource,
                attempt_no=number,
                status=status,
                started_at=at,
                submitted_at=at if status == "graded" else None,
                graded_at=at if status == "graded" else None,
                total_score=score,
                max_score=maximum,
            )
        )
    board = f"/api/v1/classroom/classes/{classroom}/leaderboard"
    ranked = client.get(board + "?category=MATH").json()["rows"]
    assert len(ranked) == 1 and ranked[0]["score"] == 90 and ranked[0]["completed"] == 1
    assert client.get(board + f"?category=MATH&resource_id={uuid4()}").json()["rows"] == []
    project = conn.execute(
        select(db.table("ai_projects").c.id).where(db.table("ai_projects").c.grade == 4)
    ).scalar_one()
    admin = conn.execute(
        select(db.table("users").c.id).where(db.table("users").c.username == "admin")
    ).scalar_one()
    submission = uuid4()
    submissions = db.table("ai_project_submissions")
    conn.execute(
        submissions.insert().values(
            id=submission,
            project_id=project,
            student_id=student,
            class_id=other,
            artifact={},
            status="reviewed",
            reviewed_by=admin,
        )
    )
    conn.execute(
        db.table("ai_rubric_scores")
        .insert()
        .values(submission_id=submission, scores={}, total=80, reviewer_id=admin)
    )
    assert client.get(board + "?category=AI_PROJECT").json()["rows"] == []
    conn.execute(
        update(submissions).where(submissions.c.id == submission).values(class_id=classroom)
    )
    assert client.get(board + "?category=AI_PROJECT").json()["rows"][0]["score"] == 80
