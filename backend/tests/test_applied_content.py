"""Content contracts, independently solved maths and safe additive publishing."""

from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.curriculum.registry import get_pack
from app.curriculum.supplements.applied.pack import content, inventory, seed, verify
from app.db import db
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import LessonContent
from app.services.grading import grade_answer


@pytest.mark.parametrize("grade", range(1, 6))
def test_original_age_appropriate_units_and_valid_answer_keys(grade):
    pack = content(grade)
    assert set(pack) == {"MATH", "VIETNAMESE", "ENGLISH"}
    prompts = set()
    for subject, units in pack.items():
        assert [unit["minimum_plan_code"] for unit in units] == ["free", "vip"]
        for index, unit in enumerate(units):
            assert unit["topic"] in get_pack(grade).topics[subject]
            assert len(unit["questions"]) == (6 if index else 4)
            lesson = LessonContent.model_validate(unit["lesson"]["content"])
            assert len(lesson.hints) == 3 and lesson.free_hint_count == 1
            assert lesson.illustration is not None
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
                assert question["content"]["prompt"] not in prompts
                prompts.add(question["content"]["prompt"])
                outcomes = [
                    grade_answer("single_choice", question["grading"], {"option_id": option["id"]})
                    for option in question["content"]["options"]
                ]
                assert outcomes.count(True) == 1


@pytest.mark.parametrize(
    "grade, expected",
    [
        (
            1,
            [
                5 + 3,
                9 - 4,
                10 - 6,
                7 - 2,
                "Đỏ",
                "Tròn",
                "Xanh",
                2 + 2,
                3,
                "Tròn – vuông – tròn – vuông",
            ],
        ),
        (
            2,
            [
                2 * 4,
                10 // 2,
                5 * 3,
                20 // 5,
                "8 giờ 15 phút",
                "Ăn sáng",
                "8 giờ 30 phút",
                "1 giờ",
                "Thứ Tư",
                "Trước giờ học",
            ],
        ),
        (
            3,
            [
                "Tổ Một",
                12 + 8,
                12 - 8,
                30 // 3,
                (17 + 4) // 5,
                5 * 4,
                20 - 17,
                (23 + 5) // 6,
                24 // 4,
                "Còn 2 bạn chưa có chỗ",
            ],
        ),
        (
            4,
            [
                Fraction(3, 8),
                Fraction(8 - 3, 8),
                Fraction(2 + 3, 8),
                24 // 3,
                (30 - 6) // 2,
                30 - 12,
                (42 - 8) // 2,
                25 - 17,
                36 // 2,
                "30 và 20",
            ],
        ),
        (
            5,
            [
                Decimal("1.5") + Decimal("0.5"),
                Decimal("2.5") * 1000,
                "Bình B",
                3 - Decimal("1.2"),
                50000 * 20 // 100,
                50000 - 10000,
                "75%",
                20000 * 90 // 100,
                60000 - 40000,
                "Giảm 25%",
            ],
        ),
    ],
)
def test_maths_keys_match_independent_solutions(grade, expected):
    questions = [question for unit in content(grade)["MATH"] for question in unit["questions"]]
    for question, answer in zip(questions, expected, strict=True):
        selected = next(
            option["text"]
            for option in question["content"]["options"]
            if option["id"] == question["grading"]["correct_option_id"]
        )
        if isinstance(answer, (int, Decimal, Fraction)):
            numeric = selected.split()[0].replace(",", ".")
            # Thousands are intentionally spaced for primary learners.
            if "đồng" in selected:
                numeric = selected.removesuffix(" đồng").replace(" ", "")
            assert Fraction(numeric) == Fraction(answer)
        else:
            assert selected == answer


def test_inventory_is_equal_for_all_grades_without_changing_baseline():
    report = inventory()
    assert len(report["grades"]) == 5
    assert sum(s["lessons"] for g in report["grades"].values() for s in g.values()) == 30
    assert sum(s["questions"] for g in report["grades"].values() for s in g.values()) == 150


@pytest.mark.integration
def test_additive_seed_preserves_history_accounts_and_teacher_lesson_edits(conn):
    def counts():
        return {
            name: conn.execute(select(func.count()).select_from(db.table(name))).scalar_one()
            for name in ("users", "attempts", "student_memberships", "auth_sessions")
        }

    before = counts()
    seed(conn)
    assert counts() == before
    assert len(verify(conn)["grades"]) == 5
    lessons = db.table("lessons")
    lesson = (
        conn.execute(
            select(lessons).where(lessons.c.code == "VT1-MATH-applied-2026-01-fruit-lesson")
        )
        .mappings()
        .one()
    )
    edited = deepcopy(lesson["content"])
    edited["blocks"][0]["text"] = "Nội dung giáo viên đã chỉnh, cần được giữ nguyên."
    conn.execute(lessons.update().where(lessons.c.id == lesson["id"]).values(content=edited))
    versions = db.table("question_versions")
    count_before = conn.execute(select(func.count()).select_from(versions)).scalar_one()
    seed(conn)
    assert (
        conn.execute(select(lessons.c.content).where(lessons.c.id == lesson["id"])).scalar_one()
        == edited
    )
    assert conn.execute(select(func.count()).select_from(versions)).scalar_one() == count_before
    assert counts() == before


@pytest.mark.integration
@pytest.mark.parametrize("grade", range(1, 6))
def test_new_free_vip_access_and_hint_distribution(logged_student, conn, grade):
    from tests.test_classrooms import grant

    seed(conn, [grade])
    user_id = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == user_id).values(current_grade=grade)
    )
    lessons, assessments = db.table("lessons"), db.table("assessments")
    free_unit, vip_unit = content(grade)["MATH"]
    ids = {}
    for kind, unit in (("free", free_unit), ("vip", vip_unit)):
        prefix = f"VT{grade}-MATH-{unit['code']}"
        ids[kind] = conn.execute(
            select(lessons.c.id).where(lessons.c.code == prefix + "-lesson")
        ).scalar_one()
        assessment = conn.execute(
            select(assessments.c.id).where(assessments.c.code == prefix + "-practice")
        ).scalar_one()
        reply = logged_student.post(f"/api/v1/students/me/assessments/{assessment}/assign-self")
        assert reply.status_code == (200 if kind == "free" else 403)
    free = logged_student.get(f"/api/v1/lessons/{ids['free']}")
    assert free.status_code == 200
    assert len(free.json()["content"]["hints"]) == 1
    assert logged_student.get(f"/api/v1/lessons/{ids['vip']}").status_code == 403
    grant(conn, user_id)
    for identifier in ids.values():
        response = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert response.status_code == 200
        assert len(response.json()["content"]["hints"]) == 3
