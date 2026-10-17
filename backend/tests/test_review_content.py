from uuid import UUID

import pytest
from sqlalchemy import func, select

from app.curriculum.registry import get_pack
from app.curriculum.supplements.review.pack import PACK, content
from app.db import db
from app.schemas.lessons import LessonContent
from app.services.grading import grade_answer


@pytest.mark.parametrize("grade", range(1, 6))
def test_review_structure_age_hints_and_unique_answer(grade):
    for subject, rows in content(grade).items():
        row = rows[0]
        assert row["topic"] in get_pack(grade).topics[subject]
        body = LessonContent.model_validate(row["lesson"]["content"])
        assert len(body.hints) == 3 and body.free_hint_count == 1
        assert body.illustration and len(row["questions"]) == 4
        assert row["lesson"]["estimated_minutes"] <= 8
        if grade <= 2:
            assert sum(len(b.text.split()) for b in body.blocks) <= 90
        for q in row["questions"]:
            assert (
                sum(
                    grade_answer("single_choice", q["grading"], {"option_id": o["id"]})
                    for o in q["content"]["options"]
                )
                == 1
            )


@pytest.mark.parametrize(
    "grade,keys",
    [
        (1, ["5 que", "5", "5 + 4 = 9", "9 bút"]),
        (2, [str(28 + 15), "1 chục", str(36 + 27), "43 − 15 = 28"]),
        (3, ["7 bút", "8 × 6 = 48", "8 nhãn", "37 bút"]),
        (4, ["5/8", "Giữ mẫu 6: kết quả 3/6", "3/9", "3/8 bánh"]),
        (5, ["20 000 đồng", "60 000 đồng", "Sai, còn trả 75%", "45 000 đồng"]),
    ],
)
def test_review_math_independently_checked_answers(grade, keys):
    questions = content(grade)["MATH"][0]["questions"]
    for question, key in zip(questions, keys, strict=True):
        answer = next(
            o["text"]
            for o in question["content"]["options"]
            if o["id"] == question["grading"]["correct_option_id"]
        )
        assert answer == key


@pytest.mark.integration
@pytest.mark.parametrize("grade", range(1, 6))
def test_review_seed_permissions_and_hints(conn, logged_student, grade):
    from tests.test_classrooms import grant

    PACK.seed(conn, [grade])
    versions = db.table("question_versions")
    count = conn.execute(select(func.count()).select_from(versions)).scalar_one()
    PACK.seed(conn, [grade])
    assert conn.execute(select(func.count()).select_from(versions)).scalar_one() == count
    assert PACK.verify(conn, [grade])["grades"]
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student).values(current_grade=grade)
    )
    lessons = db.table("lessons")
    identifiers = []
    for subject, rows in content(grade).items():
        source = rows[0]
        identifier = conn.execute(
            select(lessons.c.id).where(
                lessons.c.code == f"VT{grade}-{subject}-{source['code']}-lesson"
            )
        ).scalar_one()
        identifiers.append(identifier)
        result = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert result.status_code == (403 if source["minimum_plan_code"] == "vip" else 200)
        if result.status_code == 200:
            assert len(result.json()["content"]["hints"]) == 1
    grant(conn, student)
    for identifier in identifiers:
        result = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert result.status_code == 200 and len(result.json()["content"]["hints"]) == 3


def test_review_release_balance():
    inventory = PACK.inventory()["grades"]
    assert sum(s["free_lessons"] for g in inventory.values() for s in g.values()) == 7
    assert sum(s["vip_lessons"] for g in inventory.values() for s in g.values()) == 8
    assert all(
        PACK.expected(g) == {"lessons": 3, "questions": 12, "assessments": 3} for g in range(1, 6)
    )
