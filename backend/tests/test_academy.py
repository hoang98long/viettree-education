import base64
from io import BytesIO
from uuid import uuid4

import pytest
from PIL import Image
from sqlalchemy import func, select, update

from app.academy.curriculum import content, records
from app.academy.games import predict
from app.academy.media import uid, validate_manifest
from app.academy.schemas import LessonContent
from app.academy.seed import seed, verify
from app.core.config import settings
from app.core.security import hasher, now
from app.db import db


@pytest.mark.parametrize("source", records(), ids=lambda r: r["code"])
def test_all_48_curriculum_lessons_have_valid_educational_content(source):
    payload = LessonContent.model_validate(content(source))
    assert len(payload.steps) == 7
    assert len(payload.objectives) >= 3
    assert len(payload.steps[4].questions) == 3
    assert payload.teacher_guide and payload.support and payload.advanced
    assert sum(len(s.media) for s in payload.steps) >= 4
    if source["number"] == 12:
        assert payload.steps[1].media == [source["code"] + "-hero"]


def test_media_manifest_and_required_counts():
    result = validate_manifest()
    for kind, minimum in {
        "mascot": 8,
        "cover": 9,
        "hero": 36,
        "illustration": 90,
        "card": 60,
        "badge": 12,
        "ui": 12,
    }.items():
        assert result["categories"][kind] >= minimum
    assert result["lessons"] == 48


def test_nearest_neighbor_simulation_and_missing_examples():
    balanced = predict(["sample-0", "sample-8", "sample-16"], ["sample-1", "sample-9", "sample-17"])
    assert all(r["correct"] for r in balanced)
    missing = predict(["sample-0"], ["sample-9", "sample-17"])
    assert not any(r["correct"] for r in missing)
    with pytest.raises(ValueError):
        predict(["sample-0"], ["sample-0"])


def login(client, username="admin", password=None):
    result = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password or settings().seed_admin_password},
    )
    assert result.status_code == 200, result.text
    client.headers["X-CSRF-Token"] = client.cookies["viettree_csrf"]


def insert_user(conn, role, grade=None):
    identifier = uuid4()
    username = "ai-test-" + identifier.hex
    conn.execute(
        db.table("users")
        .insert()
        .values(
            id=identifier,
            username=username,
            display_name="Tài khoản kiểm thử Academy",
            password_hash=hasher.hash(settings().seed_student_password),
        )
    )
    conn.execute(db.table("user_roles").insert().values(user_id=identifier, role=role))
    if grade:
        conn.execute(
            db.table("student_profiles").insert().values(student_id=identifier, current_grade=grade)
        )
    return identifier, username


@pytest.mark.integration
def test_seed_is_idempotent_and_preserves_teacher_edits(conn):
    before = verify(conn)
    lessons = db.table("ai_lessons")
    conn.execute(
        update(lessons).where(lessons.c.id == uid("AI4-01")).values(title="Tên do giáo viên đã sửa")
    )
    seed(conn)
    assert verify(conn) == before
    assert (
        conn.execute(select(lessons.c.title).where(lessons.c.id == uid("AI4-01"))).scalar_one()
        == "Tên do giáo viên đã sửa"
    )


@pytest.mark.integration
def test_academy_player_authorization_grading_progress_and_rewards(logged_student, conn):
    client = logged_student
    lesson_id = str(uid("AI4-01"))
    response = client.post(f"/api/v1/ai-academy/lessons/{lesson_id}/start")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "answer" not in data["content"]["steps"][4]["questions"][0]
    assert "hints" not in data["content"]["steps"][3]["activity"]
    assert "teacher_guide" not in data["content"]
    assert (
        client.post(
            f"/api/v1/ai-academy/lessons/{lesson_id}/steps", json={"step_id": "finish"}
        ).status_code
        == 409
    )
    raw = conn.execute(
        select(db.table("ai_lesson_versions").c.payload).where(
            db.table("ai_lesson_versions").c.lesson_id == uid("AI4-01"),
            db.table("ai_lesson_versions").c.status == "published",
        )
    ).scalar_one()
    for step in raw["steps"]:
        if step["kind"] in {"activity", "quiz"}:
            if step["kind"] == "quiz":
                answers = {q["id"]: str(q["answer"]) for q in step["questions"]}
            else:
                answers = {item["id"]: item["answer"] for item in step["activity"]["items"]}
            key = str(uuid4())
            body = {"step_id": step["id"], "idempotency_key": key, "level": 3, "answers": answers}
            result = client.post(f"/api/v1/ai-academy/lessons/{lesson_id}/attempts", json=body)
            assert result.status_code == 200, result.text
            assert float(result.json()["score"]) == 1
            assert (
                client.post(f"/api/v1/ai-academy/lessons/{lesson_id}/attempts", json=body).json()[
                    "id"
                ]
                == result.json()["id"]
            )
        advance = client.post(
            f"/api/v1/ai-academy/lessons/{lesson_id}/steps", json={"step_id": step["id"]}
        )
        assert advance.status_code == 200, advance.text
    home = client.get("/api/v1/ai-academy/home").json()
    assert home["points"] == 10 and home["completed"] == 1
    assert (
        client.post(
            f"/api/v1/ai-academy/lessons/{lesson_id}/steps", json={"step_id": "finish"}
        ).status_code
        == 200
    )
    assert client.get("/api/v1/ai-academy/home").json()["points"] == 10
    assert client.get("/api/v1/ai-academy/portfolio").json()["badges"]
    assert client.get("/api/v1/ai-academy/admin/overview").status_code == 403
    assert (
        client.post("/api/v1/ai-academy/lessons/" + str(uid("AI5-01")) + "/start").status_code
        == 403
    )


@pytest.mark.integration
def test_cms_versions_review_publish_and_stale_revision(client, conn):
    login(client)
    identifier = str(uid("AI4-01"))
    original = client.get("/api/v1/ai-academy/admin/lessons/" + identifier).json()
    row = original["lesson"]
    source = original["versions"][0]["payload"]
    body = {
        "unit_id": row["unit_id"],
        "code": row["code"],
        "title": "Bài được chỉnh sửa thực sự",
        "position": row["position"],
        "revision": row["revision"],
        "content": source,
    }
    saved = client.put("/api/v1/ai-academy/admin/lessons/" + identifier, json=body)
    assert saved.status_code == 200, saved.text
    assert (
        client.put("/api/v1/ai-academy/admin/lessons/" + identifier, json=body).status_code == 409
    )
    revision = saved.json()["revision"]
    assert (
        client.post(
            "/api/v1/ai-academy/admin/lessons/" + identifier + "/publish",
            json={"revision": revision},
        ).status_code
        == 409
    )
    for action in ["submit", "review", "publish"]:
        result = client.post(
            "/api/v1/ai-academy/admin/lessons/" + identifier + "/" + action,
            json={"revision": revision},
        )
        assert result.status_code == 200, result.text
        revision = result.json()["revision"]
    current = client.get("/api/v1/ai-academy/admin/lessons/" + identifier).json()
    assert current["lesson"]["title"] == body["title"]
    assert current["versions"][0]["status"] == "published"
    assert current["versions"][-1]["payload"] == source


@pytest.mark.integration
def test_tutor_default_no_provider_calls_and_pii_blocked(logged_student, monkeypatch, conn):
    client = logged_student
    calls = []
    monkeypatch.setattr("app.academy.tutor.httpx.post", lambda *a, **k: calls.append(k))
    body = {
        "lesson_id": str(uid("AI4-11")),
        "mode": "GiveHint",
        "tried": "Em vẽ 6 hộp.",
        "level": 3,
    }
    result = client.post("/api/v1/ai-academy/tutor", json=body)
    assert result.status_code == 200, result.text
    assert result.json()["mode"] == "simulation"
    assert not calls
    body["tried"] = "email-test@example.com"
    result = client.post("/api/v1/ai-academy/tutor", json=body)
    assert result.json()["mode"] == "blocked"
    reviews = db.table("ai_moderation_reviews")
    assert conn.execute(select(func.count()).select_from(reviews)).scalar_one() >= 1
    assert "email-test" not in str(conn.execute(select(reviews)).mappings().all())


@pytest.mark.integration
def test_real_provider_requires_flags_consent_and_does_not_receive_child_text(
    logged_student, conn, monkeypatch
):
    client = logged_student
    student = client.get("/api/v1/auth/me").json()["id"]
    conn.execute(
        update(db.table("ai_feature_flags"))
        .where(db.table("ai_feature_flags").c.code == "tutor_enabled")
        .values(enabled=True)
    )
    conn.execute(
        update(db.table("ai_provider_configs"))
        .where(db.table("ai_provider_configs").c.code == "ollama")
        .values(enabled=True, policy_approved=True)
    )
    monkeypatch.setattr(settings(), "ai_provider", "ollama")
    monkeypatch.setattr(settings(), "ai_ollama_model", "test-model")
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
    calls = []

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {"content": "Em thử đếm số hộp trong tranh rồi chọn phép chia phù hợp."}
            }

    def provider(*args, **kwargs):
        calls.append(kwargs["json"])
        return Response()

    monkeypatch.setattr("app.academy.tutor.httpx.post", provider)
    body = {
        "lesson_id": str(uid("AI4-11")),
        "mode": "GiveHint",
        "tried": "unique-local-working-text",
    }
    result = client.post("/api/v1/ai-academy/tutor", json=body)
    assert result.status_code == 200, result.text
    assert result.json()["mode"] == "ollama"
    assert calls and "unique-local-working-text" not in str(calls) and student not in str(calls)
    conn.execute(
        db.table("privacy_consents")
        .insert()
        .values(
            student_id=student,
            purpose_code="ai_academy_provider",
            policy_version="ai-academy-v1",
            consent_given=False,
            recorded_at=now(),
        )
    )
    assert client.post("/api/v1/ai-academy/tutor", json=body).json()["mode"] == "simulation"
    assert len(calls) == 1


@pytest.mark.integration
def test_media_upload_security_variants_and_approval(client, conn, monkeypatch, tmp_path):
    assert client.get("/api/v1/ai-academy/media/mascot-0").status_code == 401
    login(client)
    monkeypatch.setattr(settings(), "ai_media_root", tmp_path)
    image = BytesIO()
    Image.new("RGB", (1200, 900), "green").save(image, format="PNG")
    body = {
        "data": base64.b64encode(image.getvalue()).decode(),
        "alt": "Biểu đồ học tập kiểm thử",
        "license": "Ảnh tự tạo được phép dùng",
        "source": "Kiểm thử nội bộ",
    }
    result = client.post("/api/v1/ai-academy/admin/media", json=body)
    assert result.status_code == 200, result.text
    asset = result.json()
    assert len(list(tmp_path.glob("*.webp"))) == 3
    assert (
        client.post(
            "/api/v1/ai-academy/admin/media/" + asset["id"] + "/review", json={"approved": True}
        ).status_code
        == 200
    )
    assert (
        client.get("/api/v1/ai-academy/media/" + asset["code"] + "?variant=thumbnail").status_code
        == 200
    )
    body["data"] = base64.b64encode(b"<svg><script>bad()</script></svg>").decode()
    assert client.post("/api/v1/ai-academy/admin/media", json=body).status_code == 422
    assert (
        client.get("/api/v1/ai-academy/media/mascot-0").headers["cache-control"]
        == "private, max-age=300"
    )


@pytest.mark.integration
def test_teacher_class_scope_and_guardian_verified_links(client, conn):
    teacher, tname = insert_user(conn, "teacher")
    other, oname = insert_user(conn, "teacher")
    guardian, gname = insert_user(conn, "guardian")
    student, student_name = insert_user(conn, "student", 4)
    classes = db.table("classes")
    class_id = conn.execute(
        classes.insert()
        .values(
            code="AI-TEST-" + uuid4().hex, name="Lớp kiểm thử", grade=4, teacher_user_id=teacher
        )
        .returning(classes.c.id)
    ).scalar_one()
    conn.execute(
        db.table("class_enrollments").insert().values(class_id=class_id, student_id=student)
    )
    login(client, tname, settings().seed_student_password)
    assert (
        client.get("/api/v1/ai-academy/teacher/reports?class_id=" + str(class_id)).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/ai-academy/teacher/assignments",
            json={"class_id": str(class_id), "lesson_id": str(uid("AI4-01"))},
        ).json()["targets"]
        == 1
    )
    login(client, student_name, settings().seed_student_password)
    assigned = client.get("/api/v1/ai-academy/home").json()["assignments"]
    assert len(assigned) == 1 and assigned[0]["lesson_id"] == str(uid("AI4-01"))
    login(client, oname, settings().seed_student_password)
    assert (
        client.get("/api/v1/ai-academy/teacher/reports?class_id=" + str(class_id)).status_code
        == 403
    )
    conn.execute(
        db.table("guardian_students").insert().values(guardian_user_id=guardian, student_id=student)
    )
    login(client, gname, settings().seed_student_password)
    assert client.get("/api/v1/ai-academy/guardian").json() == []
    assert (
        client.post(
            "/api/v1/ai-academy/guardian/consent", json={"student_id": str(student), "given": True}
        ).status_code
        == 403
    )
    conn.execute(
        update(db.table("guardian_students"))
        .where(db.table("guardian_students").c.guardian_user_id == guardian)
        .values(verified_at=now())
    )
    assert len(client.get("/api/v1/ai-academy/guardian").json()) == 1
    assert (
        client.post(
            "/api/v1/ai-academy/guardian/consent", json={"student_id": str(student), "given": True}
        ).status_code
        == 200
    )
