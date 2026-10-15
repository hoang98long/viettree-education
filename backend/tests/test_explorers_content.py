from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.curriculum.registry import get_pack
from app.curriculum.supplements.explorers.pack import PACK, content
from app.db import db
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import LessonContent
from app.services.grading import grade_answer


@pytest.mark.parametrize("grade", range(1, 6))
def test_short_lessons_have_supported_topics_illustrations_hints_and_valid_keys(grade):
    units = content(grade)
    assert set(units) == {"MATH", "VIETNAMESE", "ENGLISH"}
    for subject, rows in units.items():
        assert len(rows) == 1
        unit = rows[0]
        assert unit["topic"] in get_pack(grade).topics[subject]
        lesson = LessonContent.model_validate(unit["lesson"]["content"])
        assert len(lesson.hints) == 3 and lesson.free_hint_count == 1 and lesson.illustration
        assert len(unit["questions"]) == 4
        assert unit["lesson"]["estimated_minutes"] <= 8
        if grade <= 2:
            assert sum(len(block.text.split()) for block in lesson.blocks) <= 90
        for question in unit["questions"]:
            QuestionInput.model_validate(
                {
                    **question,
                    "code": unit["code"],
                    "grade": grade,
                    "subject_id": uuid4(),
                    "topic_id": uuid4(),
                    "skill_ids": [uuid4()],
                    "explanation": question["explanation"]["text"],
                }
            )
            if question["question_type"] == "single_choice":
                assert (
                    sum(
                        grade_answer(
                            "single_choice", question["grading"], {"option_id": option["id"]}
                        )
                        for option in question["content"]["options"]
                    )
                    == 1
                )


@pytest.mark.parametrize(
    "grade,expected",
    [
        (1, [8, "Dây đỏ", 5, "Dài bằng nhau"]),
        (2, [100, 100 - 30, 40 + 50, 100 - 80]),
        (3, [(12 + 8) * 2, 40 - 2, 12 * 8, 40 - 2 - 3]),
        (4, [8 + 12 + 10, (8 + 12 + 10) // 3, 12 * 4 - 30, "Không; các ngày có thể khác nhau"]),
        (5, [5 * 4 * 3, 5 * 4 * 6, 5 * 4 * 3, (6 - 5) * 4 * 3]),
    ],
)
def test_math_answers_match_independent_calculation(grade, expected):
    for question, value in zip(content(grade)["MATH"][0]["questions"], expected, strict=True):
        if question["question_type"] == "fill_blank":
            assert grade_answer("fill_blank", question["grading"], {"text": str(value)})
        else:
            correct = next(
                o["text"]
                for o in question["content"]["options"]
                if o["id"] == question["grading"]["correct_option_id"]
            )
            assert (
                Decimal(correct.split()[0]) == value if isinstance(value, int) else correct == value
            )


def test_inventory_and_access_balance():
    report = PACK.inventory()["grades"]
    assert sum(s["questions"] for g in report.values() for s in g.values()) == 60
    assert sum(s["free_lessons"] for g in report.values() for s in g.values()) == 7
    assert sum(s["vip_lessons"] for g in report.values() for s in g.values()) == 8
    for grade in range(1, 6):
        assert PACK.expected(grade) == {"lessons": 3, "questions": 12, "assessments": 3}


@pytest.mark.integration
def test_idempotent_publishing_and_admin_release_inventory(conn, logged_student):
    from tests.test_academy import login

    PACK.seed(conn)
    tables = (
        "lessons",
        "questions",
        "question_versions",
        "assessments",
        "users",
        "student_memberships",
        "attempts",
    )
    before = {
        name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
        for name in tables
    }
    PACK.seed(conn)
    assert {
        name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
        for name in tables
    } == before
    assert len(PACK.verify(conn)["grades"]) == 5
    login(logged_student, "admin")
    for grade in range(1, 6):
        response = logged_student.get(f"/api/v1/admin/curriculum-map?grade={grade}")
        assert response.status_code == 200
        release = next(row for row in response.json()["supplements"] if row["release"] == PACK.code)
        assert release["published"] == release["expected"] == PACK.expected(grade)


@pytest.mark.integration
@pytest.mark.parametrize("grade", range(1, 6))
def test_new_pack_free_vip_and_hints_are_enforced(logged_student, conn, grade):
    from tests.test_classrooms import grant

    PACK.seed(conn, [grade])
    student = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student).values(current_grade=grade)
    )
    lessons = db.table("lessons")
    ids = []
    for subject, rows in content(grade).items():
        unit = rows[0]
        identifier = conn.execute(
            select(lessons.c.id).where(
                lessons.c.code == f"VT{grade}-{subject}-{unit['code']}-lesson"
            )
        ).scalar_one()
        ids.append(identifier)
        response = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert response.status_code == (403 if unit["minimum_plan_code"] == "vip" else 200)
        if response.status_code == 200:
            assert len(response.json()["content"]["hints"]) == 1
    grant(conn, student)
    for identifier in ids:
        response = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert response.status_code == 200 and len(response.json()["content"]["hints"]) == 3
