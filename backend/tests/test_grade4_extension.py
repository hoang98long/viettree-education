from copy import deepcopy

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.db import db
from app.grade4_curriculum import GRADE4
from app.lesson_schemas import Illustration, LessonContent
from app.seed import seed_grade4_content
from app.services.grading import grade_answer, validate_answer
from tests.test_memberships import admin_login, identities, membership

# Independently solved answer sheet, deliberately not read from grading metadata.
# Lists mean multiple-choice or ordered ids according to the exercise type.
ANSWERS = {
    "millions": ["300000", "a", ["a", "b"], "c", "1000000", "a"],
    "angles": ["a", "c", "90", "a", ["a", "b"], ["b", "c", "a"]],
    "data": ["48", "16", "a", "c", ["a", "b"], "b"],
    "experiment": ["c", ["a", "b"], "4", "a", "c", ["b", "c", "a"]],
    "sum-difference": ["20", "28", "c", ["a", "b"], ["b", "c", "a"], "b"],
    "area-mass-time": ["235", "305", "b", "25", "c", "b"],
    "fraction-products": ["a", "a", "9", ["a", "b"], ["c", "a", "b"], "b"],
    "interval-riddles": ["20", "6", "b", "5", "b", ["a", "b"]],
    "logic-table": ["c", "a", "b", ["a", "b"], ["b", "c", "a"], "b"],
    "description": ["b", "a", ["a", "b"], ["b", "c", "a"], "b", "b"],
    "recount": ["b", ["b", "c", "a"], "a", ["a", "b"], "b", "a"],
    "discussion": ["b", "b", ["a", "b"], "b", ["b", "c", "a"], "b"],
    "adverbial-punctuation": ["a", "b", "a", ["a", "b"], "a", "a"],
    "information": ["a", "b", ["b", "c", "a"], ["a", "b"], "a", "c"],
    "evidence-riddle": ["c", "a", ["a", "b", "c"], "a", "b", ["b", "c", "a"]],
    "editing": ["b", "a", ["a", "b"], "b", ["b", "c", "a"], "a"],
    "can-cannot": ["b", "can", "a", ["a", "b"], ["c", "b", "a"], "b"],
    "directions": ["a", "a", "b", ["b", "c", "a"], "right", "a"],
    "preferences": ["a", "a", ["a", "b"], "like", ["b", "a", "d", "c"], "a"],
    "schedule-riddle": ["b", "a", "ten", ["a", "b"], ["b", "c", "a"], "b"],
}
PACK = [(subject, unit) for subject, units in GRADE4.items() for unit in units]


def answer(kind, value):
    key = {
        "single_choice": "option_id",
        "multiple_choice": "option_ids",
        "ordering": "ordered_ids",
        "fill_blank": "text",
    }[kind]
    return {key: value}


@pytest.mark.parametrize("subject,unit", PACK, ids=[u["code"] for _, u in PACK])
def test_original_content_has_valid_support_and_independently_solved_answers(subject, unit):
    content = LessonContent.model_validate(unit["lesson"]["content"])
    assert len(content.goals) >= 1 and len(content.hints) >= 2
    expected = ANSWERS[unit["code"].removeprefix("g4-")]
    assert len(unit["questions"]) == len(expected) == 6
    for question, value in zip(unit["questions"], expected, strict=True):
        kind = question["question_type"]
        submitted = validate_answer(kind, question["content"], answer(kind, value))
        assert grade_answer(kind, question["grading"], submitted) is True
        assert len(question["explanation"]["text"]) >= 10
        if kind == "single_choice":
            assert (
                sum(
                    grade_answer(kind, question["grading"], {"option_id": o["id"]})
                    for o in question["content"]["options"]
                )
                == 1
            )


@pytest.mark.parametrize(
    "changes",
    [
        {"values": [101, 2, 3]},
        {"values": [-1, 2, 3]},
        {"values": [1]},
        {"labels": ["", "B", "C"]},
        {"labels": ["a" * 19, "B", "C"]},
        {"values": [1, 2, 3, 4, 5, 6, 7]},
    ],
)
def test_invalid_chart_data_cannot_be_published(changes):
    with pytest.raises(ValidationError):
        Illustration.model_validate({"kind": "bars", "caption": "Số cây của ba tổ", **changes})


def lesson_id(conn, subject, code):
    return conn.execute(
        select(db.table("lessons").c.id).where(
            db.table("lessons").c.code == f"VT4-{subject}-g4-{code}-lesson"
        )
    ).scalar_one()


@pytest.mark.integration
def test_thinking_catalog_metadata_only_live_access_own_progress_and_grade(logged_student, conn):
    client = logged_student
    student, admin = identities(client, conn)
    response = client.get("/api/v1/students/me/thinking")
    assert response.status_code == 200, response.text
    assert response.headers["cache-control"] == "no-store"
    data = response.json()
    assert data["total"] >= 4
    assert all(key not in response.text for key in ("blocks", "grading", "hints", "explanation"))
    free = str(lesson_id(conn, "MATH", "interval-riddles"))
    vip = str(lesson_id(conn, "MATH", "logic-table"))
    catalog = {item["id"]: item for item in data["items"]}
    assert catalog[free]["locked"] is False and catalog[vip]["locked"] is True
    assert client.get(f"/api/v1/lessons/{vip}").status_code == 403
    assert client.get("/api/v1/admin/curriculum-map").status_code == 403
    assert client.post(f"/api/v1/lessons/{free}/complete").status_code == 200
    catalog = {
        item["id"]: item for item in client.get("/api/v1/students/me/thinking").json()["items"]
    }
    assert catalog[free]["progress_status"] == "completed"
    assert catalog[vip]["progress_status"] is None
    membership(conn, student, admin)
    assert client.get(f"/api/v1/lessons/{vip}").json()["content"]["category"] == "thinking"
    membership(conn, student, admin, "revoke")
    assert client.get(f"/api/v1/lessons/{vip}").status_code == 403
    assert client.get("/api/v1/students/me/thinking?subject_code=UNKNOWN").status_code == 422
    assert client.get("/api/v1/students/me/thinking?page=0").status_code == 422
    conn.execute(
        db.table("student_profiles")
        .update()
        .where(db.table("student_profiles").c.student_id == student)
        .values(current_grade=3)
    )
    grade3 = client.get("/api/v1/students/me/thinking").json()
    assert grade3["grade"] == 3 and grade3["total"] > 0
    assert all(item["id"] not in (free, vip) for item in grade3["items"])


@pytest.mark.integration
def test_curriculum_map_reports_actual_publication_not_drafts_or_version_duplicates(
    logged_student, conn
):
    client = logged_student
    admin_login(client)
    response = client.get("/api/v1/admin/curriculum-map")
    assert response.status_code == 200, response.text
    rows = {row["code"]: row for row in response.json()["rows"]}
    key = "VT4-MATH-chance"
    assert rows[key]["free_lessons"] == 1 and rows[key]["questions"] == 6
    assert rows["VT4-ENGLISH-listening"]["free_lessons"] == 0
    assert rows["VT4-ENGLISH-listening"]["active"] is False
    lessons, questions, versions = (
        db.table(n) for n in ("lessons", "questions", "question_versions")
    )
    identifier = lesson_id(conn, "MATH", "experiment")
    conn.execute(lessons.update().where(lessons.c.id == identifier).values(status="draft"))
    qid = conn.execute(
        select(questions.c.id).where(questions.c.code == "VT4-MATH-g4-experiment-q-01")
    ).scalar_one()
    version = dict(
        conn.execute(select(versions).where(versions.c.question_id == qid)).mappings().one()
    )
    for column in ("id", "created_at"):
        version.pop(column)
    version["version"] = 2
    version["status"] = "draft"
    conn.execute(versions.insert().values(**version))
    row = next(
        r for r in client.get("/api/v1/admin/curriculum-map").json()["rows"] if r["code"] == key
    )
    assert row["free_lessons"] == 0 and row["questions"] == 6
    subjects = db.table("subjects")
    conn.execute(subjects.update().where(subjects.c.code == "MATH").values(is_active=False))
    rows = client.get("/api/v1/admin/curriculum-map").json()["rows"]
    assert all(not r["active"] for r in rows if r["subject_code"] == "MATH")
    assert client.get("/api/v1/students/me/thinking").status_code == 403


@pytest.mark.integration
def test_content_only_seed_is_idempotent_preserves_existing_rows_and_admin_lesson_edits(conn):
    lessons = db.table("lessons")
    identifier = lesson_id(conn, "MATH", "angles")
    content = deepcopy(
        conn.execute(select(lessons.c.content).where(lessons.c.id == identifier)).scalar_one()
    )
    content["goals"] = ["Mục tiêu đã được giáo viên điều chỉnh"]
    conn.execute(lessons.update().where(lessons.c.id == identifier).values(content=content))
    names = [
        "users",
        "auth_sessions",
        "student_memberships",
        "attempts",
        "attempt_answers",
        "student_lesson_progress",
        "lessons",
        "questions",
        "question_versions",
        "assessments",
        "topics",
        "skills",
    ]
    before = {name: list(conn.execute(select(db.table(name))).mappings()) for name in names}
    seed_grade4_content(conn)
    after = {name: list(conn.execute(select(db.table(name))).mappings()) for name in names}
    assert before == after
    assert (
        conn.execute(select(lessons.c.content).where(lessons.c.id == identifier)).scalar_one()
        == content
    )


@pytest.mark.integration
def test_twenty_assessments_end_to_end_with_independent_answers(logged_student, conn):
    client = logged_student
    student, admin = identities(client, conn)
    membership(conn, student, admin)
    for subject, unit in PACK:
        code = f"VT4-{subject}-{unit['code']}-practice"
        assessment = conn.execute(
            select(db.table("assessments").c.id).where(db.table("assessments").c.code == code)
        ).scalar_one()
        assignment = client.post(f"/api/v1/students/me/assessments/{assessment}/assign-self")
        assert assignment.status_code == 200, assignment.text
        started = client.post("/api/v1/attempts", json={"assignment_id": assignment.json()["id"]})
        assert started.status_code == 200, started.text
        aid = started.json()["id"]
        active = client.get(f"/api/v1/attempts/{aid}")
        assert all(
            secret not in active.text for secret in ("grading", "explanation", "correct_option")
        )
        sheet = ANSWERS[unit["code"].removeprefix("g4-")]
        for item, value in zip(active.json()["items"], sheet, strict=True):
            saved = client.put(
                f"/api/v1/attempts/{aid}/answers/{item['id']}",
                json={"answer": answer(item["question_type"], value)},
            )
            assert saved.status_code == 200, saved.text
        result = client.post(f"/api/v1/attempts/{aid}/submit")
        assert result.status_code == 200, result.text
        assert result.json()["total_score"] == result.json()["max_score"] == 6, code
