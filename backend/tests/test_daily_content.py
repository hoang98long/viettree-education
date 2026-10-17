from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.curriculum.registry import get_pack
from app.curriculum.supplements.daily.pack import PACK, content
from app.db import db
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import LessonContent
from app.services.grading import grade_answer


@pytest.mark.parametrize("grade", range(1, 6))
def test_daily_content_structure_evidence_and_single_correct_option(grade):
    for subject, units in content(grade).items():
        row = units[0]
        assert row["topic"] in get_pack(grade).topics[subject]
        body = LessonContent.model_validate(row["lesson"]["content"])
        assert body.illustration and len(body.hints) == 3 and body.free_hint_count == 1
        assert len(row["questions"]) == 4
        assert row["lesson"]["estimated_minutes"] <= 8
        if grade <= 2:
            assert sum(len(b.text.split()) for b in body.blocks) <= 90
        for q in row["questions"]:
            QuestionInput.model_validate(
                {
                    **q,
                    "explanation": q["explanation"]["text"],
                    "code": row["code"],
                    "grade": grade,
                    "subject_id": uuid4(),
                    "topic_id": uuid4(),
                    "skill_ids": [uuid4()],
                }
            )
            assert (
                sum(
                    grade_answer(q["question_type"], q["grading"], {"option_id": option["id"]})
                    for option in q["content"]["options"]
                )
                == 1
            )
            if subject == "VIETNAMESE":
                assert body.blocks[1].text in q["content"]["prompt"]


@pytest.mark.parametrize(
    "grade,answers",
    [
        (1, ["12", "7", "6 giờ", "Buổi sáng"]),
        (2, ["7 giờ 30 phút", "30 phút", "7 giờ 30 phút", "6"]),
        (3, ["25 phút", "9 giờ 35 phút", "8 giờ 5 phút", "60 phút"]),
        (4, ["40 phút", "14 giờ 15 phút", "14 giờ 20 phút", "5 phút"]),
        (5, ["6 km", "18 km", "7 giờ 45 phút", "30 phút"]),
    ],
)
def test_clock_duration_motion_answers_reviewed_independently(grade, answers):
    for q, expected in zip(content(grade)["MATH"][0]["questions"], answers, strict=True):
        assert (
            next(
                o["text"]
                for o in q["content"]["options"]
                if o["id"] == q["grading"]["correct_option_id"]
            )
            == expected
        )


def test_daily_inventory_balance_and_invalid_grade():
    inventory = PACK.inventory()["grades"]
    assert sum(s["free_lessons"] for g in inventory.values() for s in g.values()) == 7
    assert sum(s["vip_lessons"] for g in inventory.values() for s in g.values()) == 8
    assert all(
        PACK.expected(g) == {"lessons": 3, "questions": 12, "assessments": 3} for g in range(1, 6)
    )
    with pytest.raises(ValueError):
        content(6)


@pytest.mark.integration
@pytest.mark.parametrize("grade", range(1, 6))
def test_daily_publishing_permissions_hints_and_admin_counts(conn, logged_student, grade):
    from tests.test_academy import login
    from tests.test_classrooms import grant

    PACK.seed(conn, [grade])
    versions = db.table("question_versions")
    total = conn.execute(select(func.count()).select_from(versions)).scalar_one()
    PACK.seed(conn, [grade])
    assert conn.execute(select(func.count()).select_from(versions)).scalar_one() == total
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student).values(current_grade=grade)
    )
    lessons = db.table("lessons")
    ids = []
    for subject, units in content(grade).items():
        row = units[0]
        identifier = conn.execute(
            select(lessons.c.id).where(
                lessons.c.code == f"VT{grade}-{subject}-{row['code']}-lesson"
            )
        ).scalar_one()
        ids.append(identifier)
        response = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert response.status_code == (200 if row["minimum_plan_code"] == "free" else 403)
        if response.status_code == 200:
            assert len(response.json()["content"]["hints"]) == 1
    grant(conn, student)
    for identifier in ids:
        response = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert response.status_code == 200 and len(response.json()["content"]["hints"]) == 3
    login(logged_student, "admin")
    response = logged_student.get(f"/api/v1/admin/curriculum-map?grade={grade}")
    assert response.status_code == 200
    release = next(row for row in response.json()["supplements"] if row["release"] == PACK.code)
    assert release["expected"] == release["published"] == PACK.expected(grade)
