from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.curriculum.registry import get_pack
from app.curriculum.supplements.discovery.pack import PACK, content
from app.db import db
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import LessonContent
from app.services.grading import grade_answer


@pytest.mark.parametrize("grade", range(1, 6))
def test_discovery_content_has_short_guidance_and_unique_correct_choices(grade):
    for subject, units in content(grade).items():
        assert len(units) == 2
        assert [unit["minimum_plan_code"] for unit in units] == ["free", "vip"]
        for row in units:
            assert row["topic"] in get_pack(grade).topics[subject]
            body = LessonContent.model_validate(row["lesson"]["content"])
            assert body.illustration and len(body.hints) == 3 and body.free_hint_count == 1
            assert len(row["questions"]) == 4
            if grade <= 2:
                assert sum(len(block.text.split()) for block in body.blocks) < 130
            for question in row["questions"]:
                QuestionInput.model_validate(
                    {
                        **question,
                        "code": row["code"],
                        "grade": grade,
                        "subject_id": uuid4(),
                        "topic_id": uuid4(),
                        "skill_ids": [uuid4()],
                        "explanation": question["explanation"]["text"],
                    }
                )
                assert (
                    sum(
                        grade_answer(
                            question["question_type"],
                            question["grading"],
                            {"option_id": option["id"]},
                        )
                        for option in question["content"]["options"]
                    )
                    == 1
                )
                if subject in ("VIETNAMESE", "ENGLISH"):
                    assert body.blocks[1].text in question["content"]["prompt"]


@pytest.mark.parametrize(
    "grade,keys",
    [
        (1, [["5 hạt", "4 hạt", "Nhóm A", "1 hạt"], ["3 hạt", "5", "3 que", "5 + □ = 7"]]),
        (2, [["40 cm", "16 cm", "7 cm", "Dải 40 cm"], ["45", "35", "47", "62"]]),
        (3, [["24 cây", "6 cây", "30 cây", "18 cây"], ["24", "20", "20 hạt", "8"]]),
        (
            4,
            [["36 quyển", "12 quyển", "8 quyển", "Tổ 3"], ["27 lá", "19 lá", "27 và 19", "12 bút"]],
        ),
        (
            5,
            [
                ["30 000 đồng", "90 000 đồng", "75%", "72 000 đồng"],
                ["24 cm³", "12 khối", "36 cm³", "2 cm"],
            ],
        ),
    ],
)
def test_math_answer_keys_reviewed_independently(grade, keys):
    for row, expected in zip(content(grade)["MATH"], keys, strict=True):
        actual = [
            next(
                option["text"]
                for option in q["content"]["options"]
                if option["id"] == q["grading"]["correct_option_id"]
            )
            for q in row["questions"]
        ]
        assert actual == expected


def test_discovery_inventory_and_invalid_grade():
    assert all(
        PACK.expected(grade) == {"lessons": 6, "questions": 24, "assessments": 6}
        for grade in range(1, 6)
    )
    with pytest.raises(ValueError):
        content(6)


@pytest.mark.integration
@pytest.mark.parametrize("grade", range(1, 6))
def test_release_filters_and_live_hints_follow_profile_and_membership(conn, logged_student, grade):
    from tests.test_classrooms import grant

    PACK.seed(conn, [grade])
    user = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    profile = db.table("student_profiles")
    conn.execute(profile.update().where(profile.c.student_id == user).values(current_grade=grade))
    for library in ("lesson", "practice"):
        path = f"/api/v1/students/me/{library}-library"
        result = logged_student.get(path, params={"release_code": PACK.code}).json()
        assert result["grade"] == grade and result["summary"]["total"] == 6
        assert len(result["items"]) == 6
        assert sum(row["locked"] for row in result["items"]) == 3
        assert {"code": PACK.code, "title": PACK.title} in result["releases"]
        free = logged_student.get(path, params={"release_code": PACK.code, "plan": "free"}).json()
        assert free["summary"]["total"] == 3 and all(not row["locked"] for row in free["items"])
        maths = logged_student.get(
            path, params={"release_code": PACK.code, "subject_code": "MATH"}
        ).json()
        assert maths["summary"]["total"] == 2
        assert (
            logged_student.get(path, params={"release_code": PACK.code + "%_"}).status_code == 422
        )
    lessons = db.table("lessons")
    ids = []
    for subject, rows in content(grade).items():
        for row in rows:
            identifier = conn.execute(
                select(lessons.c.id).where(
                    lessons.c.code == f"VT{grade}-{subject}-{row['code']}-lesson"
                )
            ).scalar_one()
            ids.append(identifier)
            response = logged_student.get(f"/api/v1/lessons/{identifier}")
            assert response.status_code == (403 if row["minimum_plan_code"] == "vip" else 200)
            if response.status_code == 200:
                assert len(response.json()["content"]["hints"]) == 1
    versions = db.table("question_versions")
    before = {row["id"]: dict(row) for row in conn.execute(select(versions)).mappings()}
    PACK.seed(conn, [grade])
    assert {row["id"]: dict(row) for row in conn.execute(select(versions)).mappings()} == before
    grant(conn, user)
    for identifier in ids:
        response = logged_student.get(f"/api/v1/lessons/{identifier}")
        assert response.status_code == 200 and len(response.json()["content"]["hints"]) == 3
        assessments = db.table("assessments")
        own_practice = conn.execute(
            select(assessments.c.id).where(assessments.c.lesson_id == identifier)
        ).scalar_one()
        assert response.json()["practice"][0]["id"] == str(own_practice)
