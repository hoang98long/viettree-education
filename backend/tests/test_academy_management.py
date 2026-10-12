from uuid import uuid4

import pytest
from sqlalchemy import func, select, update

from app.academy.media import uid
from app.academy.safety import moderation_reason
from app.core.config import settings
from app.core.security import now
from app.db import db
from tests.test_academy import insert_user, login


def confirmed(**values):
    return {
        "actor_password": settings().seed_admin_password,
        "reason": "Kiểm thử quản trị theo chính sách",
        **values,
    }


@pytest.mark.integration
def test_projects_revision_rubric_and_enrollment_boundaries(client, conn):
    teacher, teacher_name = insert_user(conn, "teacher")
    other_teacher, other_name = insert_user(conn, "teacher")
    student, student_name = insert_user(conn, "student", 4)
    classroom = uuid4()
    conn.execute(
        db.table("classes")
        .insert()
        .values(
            id=classroom,
            code="TEST-" + classroom.hex,
            name="Lớp kiểm thử",
            grade=4,
            teacher_user_id=teacher,
        )
    )
    conn.execute(
        db.table("class_enrollments").insert().values(class_id=classroom, student_id=student)
    )
    login(client, student_name, settings().seed_student_password)
    project = client.get("/api/v1/ai-academy/projects").json()[0]["id"]
    body = {
        "project_id": project,
        "class_id": str(classroom),
        "artifact": {
            "kind": "poster",
            "title": "Poster an toàn",
            "frame1": "Dùng dữ liệu mẫu và kiểm tra nguồn",
            "reflection": "Em đã kiểm tra nguồn và dùng nhân vật mẫu",
        },
        "submit": True,
    }
    response = client.post("/api/v1/ai-academy/projects/submissions", json=body)
    assert response.status_code == 200, response.text
    saved = response.json()
    assert client.post("/api/v1/ai-academy/projects/submissions", json=body).status_code == 409
    login(client, other_name, settings().seed_student_password)
    review = {
        "revision": saved["revision"],
        "feedback": "Cần thêm cách kiểm tra kết quả",
        "scores": {"understanding": 4, "practice": 3, "creativity": 2, "safety": 4},
    }
    path = f"/api/v1/ai-academy/teacher/submissions/{saved['id']}/review"
    assert client.post(path, json=review).status_code == 403
    login(client, teacher_name, settings().seed_student_password)
    result = client.post(path, json=review)
    assert result.status_code == 200, result.text
    assert result.json()["total"] == 77.5
    assert client.post(path, json=review).status_code == 409
    enrollment = db.table("class_enrollments")
    conn.execute(update(enrollment).where(enrollment.c.class_id == classroom).values(left_at=now()))
    review["revision"] = result.json()["revision"]
    assert client.post(path, json=review).status_code == 403
    assert other_teacher != teacher


@pytest.mark.integration
def test_privacy_export_and_project_text_removal_preserve_records(client, conn):
    student, name = insert_user(conn, "student", 4)
    stranger, stranger_name = insert_user(conn, "student", 4)
    guardian, guardian_name = insert_user(conn, "guardian")
    login(client, name, settings().seed_student_password)
    project = client.get("/api/v1/ai-academy/projects").json()[0]["id"]
    saved = client.post(
        "/api/v1/ai-academy/projects/submissions",
        json={"project_id": project, "artifact": {"title": "Nháp riêng", "frame1": "Dữ liệu mẫu"}},
    ).json()
    assert client.get(f"/api/v1/ai-academy/privacy/{student}/export").status_code == 200
    login(client, stranger_name, settings().seed_student_password)
    assert client.get(f"/api/v1/ai-academy/privacy/{student}/export").status_code == 403
    assert (
        client.post(
            "/api/v1/ai-academy/privacy/project-text-removal", json={"student_id": str(student)}
        ).status_code
        == 403
    )
    login(client, guardian_name, settings().seed_student_password)
    assert client.get(f"/api/v1/ai-academy/privacy/{student}/export").status_code == 403
    login(client)
    linked = client.post(
        "/api/v1/ai-academy/admin/guardian-links",
        json=confirmed(guardian_id=str(guardian), student_id=str(student), verified=True),
    )
    assert linked.status_code == 200, linked.text
    login(client, guardian_name, settings().seed_student_password)
    assert client.get(f"/api/v1/ai-academy/privacy/{student}/export").status_code == 200
    assert (
        client.post(
            "/api/v1/ai-academy/privacy/project-text-removal", json={"student_id": str(student)}
        ).status_code
        == 200
    )
    login(client)
    request = client.get("/api/v1/ai-academy/admin/privacy-requests").json()[0]
    path = f"/api/v1/ai-academy/admin/privacy-requests/{request['id']}/resolve"
    assert client.post(path, json=confirmed(approved=True)).status_code == 200
    assert client.post(path, json=confirmed(approved=True)).status_code == 409
    table = db.table("ai_project_submissions")
    record = conn.execute(select(table).where(table.c.id == saved["id"])).mappings().one()
    assert record["artifact"] == {} and record["student_id"] == student
    users = db.table("users")
    assert conn.execute(
        select(users.c.id).where(users.c.id.in_([student, stranger, guardian]))
    ).all()


@pytest.mark.integration
def test_new_unit_prompt_versions_and_private_teacher_guidance(client, conn):
    login(client)
    unit = client.post(
        "/api/v1/ai-academy/admin/units",
        json={
            "grade": 4,
            "code": "TEST-" + uuid4().hex,
            "title": "Chủ đề mới",
            "description": "Chủ đề mẫu có mục tiêu rõ ràng",
        },
    )
    assert unit.status_code == 200, unit.text
    assert any(
        r["id"] == unit.json()["id"]
        for r in client.get("/api/v1/ai-academy/admin/units?grade=4").json()
    )
    draft = client.post(
        "/api/v1/ai-academy/admin/prompts",
        json={
            "mode": "GiveHint",
            "template": "Chỉ dùng ngữ liệu đã duyệt; đưa gợi ý để học sinh tự thử, kiểm tra dữ kiện và không cung cấp đáp án thay em.",
        },
    )
    assert draft.status_code == 200, draft.text
    path = f"/api/v1/ai-academy/admin/prompts/GiveHint/{draft.json()['version']}/approve"
    assert client.post(path, json=confirmed()).status_code == 200
    prompts = client.get("/api/v1/ai-academy/admin/prompts").json()
    assert len([p for p in prompts if p["mode"] == "GiveHint" and p["status"] == "approved"]) == 1
    response = client.post(f"/api/v1/ai-academy/admin/lessons/{uid('AI4-01')}/teacher-draft")
    assert response.status_code == 200, response.text
    assert response.json()["mode"] == "simulation" and response.json()["teacher_guide"]


@pytest.mark.integration
def test_archive_current_publication_with_newer_draft_and_media_guard(client, conn):
    login(client)
    identifier = str(uid("AI4-02"))
    source = client.get("/api/v1/ai-academy/admin/lessons/" + identifier).json()
    row = source["lesson"]
    draft = client.put(
        "/api/v1/ai-academy/admin/lessons/" + identifier,
        json={
            "unit_id": row["unit_id"],
            "code": row["code"],
            "title": row["title"],
            "position": row["position"],
            "revision": row["revision"],
            "content": source["versions"][0]["payload"],
        },
    )
    assert draft.status_code == 200, draft.text
    media = db.table("ai_media_assets")
    asset = conn.execute(
        select(media.c.id).where(media.c.code == source["versions"][0]["payload"]["hero"])
    ).scalar_one()
    assert (
        client.post(
            f"/api/v1/ai-academy/admin/media/{asset}/review", json={"approved": False}
        ).status_code
        == 409
    )
    archived = client.post(
        f"/api/v1/ai-academy/admin/lessons/{identifier}/archive",
        json={"revision": draft.json()["revision"]},
    )
    assert archived.status_code == 200, archived.text
    versions = db.table("ai_lesson_versions")
    assert (
        conn.execute(
            select(func.count())
            .select_from(versions)
            .where(versions.c.lesson_id == identifier, versions.c.status == "published")
        ).scalar_one()
        == 0
    )
    assert (
        conn.execute(
            select(func.count())
            .select_from(versions)
            .where(versions.c.lesson_id == identifier, versions.c.status == "draft")
        ).scalar_one()
        == 1
    )


@pytest.mark.integration
def test_dormant_editor_grant_does_not_authorize_student(client, conn):
    student, name = insert_user(conn, "student", 4)
    login(client)
    assert (
        client.post(
            "/api/v1/ai-academy/admin/staff",
            json=confirmed(user_id=str(student), role="editor", grant=True),
        ).status_code
        == 422
    )
    conn.execute(
        db.table("ai_staff_roles")
        .insert()
        .values(user_id=student, role="editor", assigned_by=student)
    )
    login(client, name, settings().seed_student_password)
    assert client.get("/api/v1/ai-academy/admin/lessons?grade=4").status_code == 403


@pytest.mark.integration
def test_published_quality_reports_corrupt_content_and_missing_assets(conn):
    from copy import deepcopy

    from app.academy.quality import report

    assert report(conn)["issues"] == []
    versions = db.table("ai_lesson_versions")
    row = (
        conn.execute(
            select(versions).where(
                versions.c.lesson_id == uid("AI4-03"), versions.c.status == "published"
            )
        )
        .mappings()
        .one()
    )
    payload = deepcopy(row["payload"])
    payload["steps"][3]["activity"]["items"][0]["asset"] = "missing-artifact"
    conn.execute(update(versions).where(versions.c.id == row["id"]).values(payload=payload))
    assert {"code": "AI4-03", "reason": "missing_approved_media"} in report(conn)["issues"]
    payload["steps"][4]["questions"] = []
    conn.execute(update(versions).where(versions.c.id == row["id"]).values(payload=payload))
    assert {"code": "AI4-03", "reason": "invalid_lesson_structure"} in report(conn)["issues"]


@pytest.mark.integration
def test_svg_generation_job_writes_asset_and_requires_review(client, conn, monkeypatch, tmp_path):
    monkeypatch.setattr(settings(), "ai_media_root", tmp_path)
    login(client)
    created = client.post("/api/v1/ai-academy/admin/jobs", json={"template": "robot", "palette": 2})
    assert created.status_code == 200, created.text
    response = client.post(f"/api/v1/ai-academy/admin/jobs/{created.json()['id']}/run")
    assert response.status_code == 200, response.text
    assert list(tmp_path.glob("*.svg"))
    jobs = client.get("/api/v1/ai-academy/admin/jobs").json()
    job = next(j for j in jobs if j["id"] == created.json()["id"])
    assert job["status"] == "review"
    assert (
        client.post(
            f"/api/v1/ai-academy/admin/media/{job['asset_id']}/review", json={"approved": True}
        ).status_code
        == 200
    )


@pytest.mark.parametrize(
    "text,reason",
    [
        ("Giữ mật khẩu riêng và hỏi người lớn", None),
        ("Mật khẩu của em là abc123xyz", "personal_data"),
        ("Em gửi mail a@example.com", "personal_data"),
    ],
)
def test_moderation_distinguishes_safety_lesson_from_disclosure(text, reason):
    assert moderation_reason(text) == reason
