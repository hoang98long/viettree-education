from collections import Counter
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.academy import baseline_upgrade
from app.academy.access import FREE_CODES
from app.academy.curriculum import content, records
from app.academy.media import uid
from app.db import db


@pytest.mark.integration
def test_archiving_a_vip_version_does_not_make_its_illustrations_free(logged_student, conn):
    versions = db.table("ai_lesson_versions")
    conn.execute(
        versions.update().where(versions.c.lesson_id == uid("AI1-08")).values(status="archived")
    )
    response = logged_student.get("/api/v1/ai-academy/media/AI1-08-v2-item-2")
    assert response.status_code == 403


def test_every_grade_has_full_distinct_course_with_free_introduction():
    rows = records()
    assert Counter(row["grade"] for row in rows) == {grade: 40 for grade in range(1, 6)}
    for grade in range(1, 6):
        selected = [row for row in rows if row["grade"] == grade]
        assert len({row["unit_code"] for row in selected}) == 11
        assert len({row["title"] for row in selected}) == 40
        assert sum(row["code"] in FREE_CODES for row in selected) == 5
    young = [content(row) for row in rows if row["grade"] <= 2]
    assert all(payload["estimated_minutes"] == 10 for payload in young)
    assert all(
        len(payload["steps"][3]["activity"]["items"]) == 2
        for row, payload in zip(
            [r for r in rows if r["grade"] == 1], [content(r) for r in rows if r["grade"] == 1]
        )
    )


@pytest.mark.integration
def test_no_typing_hints_are_pinned_and_vip_levels_are_enforced(logged_student, conn, monkeypatch):
    user_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    lesson_id = uid("AI4-01")
    path = f"/api/v1/ai-academy/lessons/{lesson_id}/hints"
    monkeypatch.setattr(
        "app.academy.tutor.httpx.post",
        lambda *args, **kwargs: pytest.fail("Must not call a provider"),
    )
    result = logged_student.post(path, json={"step_id": "story", "level": 1})
    assert result.status_code == 200 and result.json()["message"]
    assert logged_student.post(path, json={"step_id": "finish", "level": 1}).status_code == 409
    assert logged_student.post(path, json={"step_id": "story", "level": 2}).status_code == 403
    from tests.test_classrooms import grant

    grant(conn, user_id)
    assert logged_student.post(path, json={"step_id": "story", "level": 3}).status_code == 200
    assert logged_student.post(path, json={"step_id": "story", "level": 4}).status_code == 422
    token = logged_student.headers.pop("X-CSRF-Token")
    assert logged_student.post(path, json={"step_id": "story", "level": 1}).status_code == 403
    logged_student.headers["X-CSRF-Token"] = token


@pytest.mark.integration
def test_visual_revision_retains_old_payload_progress_and_teacher_work(
    logged_student, conn, monkeypatch
):
    versions, lessons, progress = (
        db.table(name) for name in ["ai_lesson_versions", "ai_lessons", "ai_progress"]
    )
    source = records()[0]
    user_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    for edited in [False, True]:
        row = {**source, "code": "regression-" + uuid4().hex, "title": "Bản học bằng tranh"}
        lesson_id, version_id = uid(row["code"]), uuid4()
        original = content(source)
        original["steps"][0]["text"] = "Câu chuyện cũ vẫn cần giữ cho học sinh đang học."
        conn.execute(
            lessons.insert().values(
                id=lesson_id,
                code=row["code"],
                unit_id=uid(source["unit_code"]),
                position=1000 if not edited else 1001,
                title="Bài cũ",
                minimum_plan_code="vip",
            )
        )
        conn.execute(
            versions.insert().values(
                id=version_id, lesson_id=lesson_id, version=1, status="published", payload=original
            )
        )
        monkeypatch.setitem(
            baseline_upgrade.BASELINE,
            row["code"],
            {
                "sha256": baseline_upgrade.fingerprint(original),
                "title": "Bài cũ",
                "unit_code": source["unit_code"],
                "position": 1000 if not edited else 1001,
            },
        )
        conn.execute(
            progress.insert().values(
                student_id=user_id, lesson_id=lesson_id, version_id=version_id, next_step=1
            )
        )
        if edited:
            conn.execute(
                lessons.update()
                .where(lessons.c.id == lesson_id)
                .values(title="Tên riêng của giáo viên")
            )
        new_id = baseline_upgrade.publish_visual_revision(conn, row, content(source))
        assert (new_id is None) == edited
        assert (
            conn.execute(
                select(progress.c.version_id).where(progress.c.lesson_id == lesson_id)
            ).scalar_one()
            == version_id
        )
        stored = conn.execute(select(versions).where(versions.c.id == version_id)).mappings().one()
        assert stored["payload"] == original
        assert stored["status"] == ("published" if edited else "archived")
        assert baseline_upgrade.publish_visual_revision(conn, row, content(source)) is None


@pytest.mark.integration
@pytest.mark.parametrize("grade", [1, 2, 3, 5])
def test_free_visual_course_can_be_completed_and_vip_content_stays_locked(
    logged_student, conn, grade
):
    client = logged_student
    student_id = UUID(client.get("/api/v1/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student_id).values(current_grade=grade)
    )
    catalog = client.get(f"/api/v1/ai-academy/catalog?grade={grade}").json()
    assert len(catalog) == 40
    lesson_id = uid(f"AI{grade}-01")
    result = client.post(f"/api/v1/ai-academy/lessons/{lesson_id}/start")
    assert result.status_code == 200, result.text
    assert all(
        "answer" not in item for item in result.json()["content"]["steps"][3]["activity"]["items"]
    )
    payload = conn.execute(
        select(db.table("ai_lesson_versions").c.payload).where(
            db.table("ai_lesson_versions").c.lesson_id == lesson_id,
            db.table("ai_lesson_versions").c.status == "published",
        )
    ).scalar_one()
    for step in payload["steps"]:
        if step["kind"] in {"activity", "quiz"}:
            answers = (
                {item["id"]: item["answer"] for item in step["activity"]["items"]}
                if step["kind"] == "activity"
                else {q["id"]: str(q["answer"]) for q in step["questions"]}
            )
            response = client.post(
                f"/api/v1/ai-academy/lessons/{lesson_id}/attempts",
                json={
                    "step_id": step["id"],
                    "level": 3,
                    "idempotency_key": str(uuid4()),
                    "answers": answers,
                },
            )
            assert response.status_code == 200 and float(response.json()["score"]) == 1
        assert (
            client.post(
                f"/api/v1/ai-academy/lessons/{lesson_id}/steps", json={"step_id": step["id"]}
            ).status_code
            == 200
        )
    assert (
        client.post(f"/api/v1/ai-academy/lessons/{uid(f'AI{grade}-10')}/start").status_code == 403
    )
