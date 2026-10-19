from uuid import UUID, uuid4
from xml.etree import ElementTree

import pytest
from sqlalchemy import func, select

from app.academy.curriculum import content, records
from app.academy.learning import grade_step, public_content
from app.academy.media import uid
from app.academy.seed import seed
from app.db import db


def test_counting_pictures_have_no_decorative_extra_dots_and_colors_match_labels():
    from app.academy.media import ASSETS
    from app.academy.visual_art import labelled_picture

    for i in (1, 2):
        root = ElementTree.fromstring((ASSETS / f"AI1-37-v2-item-{i}.svg").read_bytes())
        assert len(root.findall("{http://www.w3.org/2000/svg}circle")) == 2 + 3
    green = labelled_picture("Quả táo xanh", 1)
    red = labelled_picture("Chiếc bút đỏ", 2)
    assert 'fill="#83af56"' in green and 'fill="#e87969"' not in green
    assert 'fill="#e87969"' in red


@pytest.mark.parametrize("grade", range(1, 6))
def test_investigations_have_age_appropriate_hints_and_consistent_grading(grade):
    rows = [row for row in records() if row["grade"] == grade and row["number"] in (37, 38)]
    assert len(rows) == 2
    for row in rows:
        payload = content(row)
        exercise, checkpoint = payload["steps"][3:5]
        assert len(exercise["activity"]["hints"]) == 3
        if grade == 1:
            assert len(exercise["activity"]["items"]) == 2
        for level in (1, 2, 3):
            items = (
                exercise["activity"]["items"][: level + 1]
                if level < 3
                else exercise["activity"]["items"]
            )
            assert grade_step(exercise, {i["id"]: i["answer"] for i in items}, level)[0] == 1
        assert (
            grade_step(checkpoint, {q["id"]: str(q["answer"]) for q in checkpoint["questions"]})[0]
            == 1
        )
        public = public_content(payload)
        assert "teacher_guide" not in public
        assert "standard" not in public and "advanced" not in public
        assert "hints" not in public["steps"][3]["activity"]
        assert all(
            "answer" not in q and "explanation" not in q for q in public["steps"][4]["questions"]
        )
    # Explicit independently reviewed mathematical keys, not just schema checks.
    q = content(rows[0])["steps"][4]["questions"][0]
    assert (
        q["options"][q["answer"]]
        == {1: "5 que", 2: "Cạnh sách", 3: "Mèo C để riêng", 4: "42", 5: "80%"}[grade]
    )


@pytest.mark.integration
@pytest.mark.parametrize("grade", range(1, 6))
@pytest.mark.parametrize("number", (37, 39))
def test_investigation_completion_idempotency_and_live_vip(
    logged_student, conn, grade, number, monkeypatch
):
    from tests.test_classrooms import grant

    monkeypatch.setattr(
        "app.academy.tutor.httpx.post", lambda *a, **k: pytest.fail("No model call")
    )
    seed(conn)
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student).values(current_grade=grade)
    )
    base = "/api/v1/ai-academy/lessons/"
    lesson = uid(f"AI{grade}-{number}")
    path = base + str(lesson)
    result = logged_student.post(path + "/start")
    assert result.status_code == 200 and result.json()["hint_limit"] == 1
    assert "advanced" not in result.json()["content"]
    assert "standard" not in result.json()["content"]
    assert (
        logged_student.post(base + str(uid(f"AI{grade}-{number + 1}")) + "/start").status_code
        == 403
    )
    assert (
        logged_student.get(f"/api/v1/ai-academy/media/AI{grade}-{number + 1}-v2-item-1").status_code
        == 403
    )
    assert (
        logged_student.post(path + "/hints", json={"step_id": "story", "level": 2}).status_code
        == 403
    )
    versions = db.table("ai_lesson_versions")
    payload = conn.execute(
        select(versions.c.payload).where(
            versions.c.lesson_id == lesson, versions.c.status == "published"
        )
    ).scalar_one()
    for step in payload["steps"]:
        if step["kind"] in {"activity", "quiz"}:
            answers = (
                {i["id"]: i["answer"] for i in step["activity"]["items"]}
                if step.get("activity")
                else {q["id"]: str(q["answer"]) for q in step["questions"]}
            )
            request = {
                "step_id": step["id"],
                "answers": answers,
                "level": 3,
                "idempotency_key": str(uuid4()),
            }
            first = logged_student.post(path + "/attempts", json=request)
            retry = logged_student.post(path + "/attempts", json=request)
            assert first.status_code == retry.status_code == 200
            assert first.json()["id"] == retry.json()["id"]
            assert float(first.json()["score"]) == 1
        complete = logged_student.post(path + "/steps", json={"step_id": step["id"]})
        assert complete.status_code == 200
    assert complete.json()["completed_at"]
    grant(conn, student)
    assert logged_student.post(path + "/start").json()["hint_limit"] == 3
    vip = base + str(uid(f"AI{grade}-{number + 1}"))
    assert logged_student.post(vip + "/start").status_code == 200
    assert (
        logged_student.get(f"/api/v1/ai-academy/media/AI{grade}-{number + 1}-v2-item-1").status_code
        == 200
    )
    from app.schemas.memberships import MembershipRevokeInput
    from app.services.memberships import change_membership

    users = db.table("users")
    admin = conn.execute(select(users.c.id).where(users.c.username == "admin")).scalar_one()
    change_membership(
        conn,
        admin,
        student,
        "revoke",
        MembershipRevokeInput(reason="Kiểm thử thu hồi VIP bài mới"),
        uuid4(),
    )
    assert logged_student.post(vip + "/start").status_code == 403
    assert logged_student.post(path + "/start").json()["hint_limit"] == 1
    assert (
        logged_student.post(path + "/hints", json={"step_id": "practice", "level": 2}).status_code
        == 403
    )


@pytest.mark.integration
def test_ai_reseed_preserves_published_versions_and_progress(conn, logged_student):
    seed(conn)
    lesson = uid("AI4-01")
    logged_student.post(f"/api/v1/ai-academy/lessons/{lesson}/start")
    names = ["ai_lesson_versions", "ai_progress", "users", "student_memberships"]
    before = {name: list(conn.execute(select(db.table(name))).mappings()) for name in names}
    counts = {
        name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
        for name in ["ai_lessons", "ai_units", "ai_media_usages"]
    }
    seed(conn)
    for name in names:
        assert list(conn.execute(select(db.table(name))).mappings()) == before[name]
    for name, count in counts.items():
        assert conn.execute(select(func.count()).select_from(db.table(name))).scalar_one() == count
