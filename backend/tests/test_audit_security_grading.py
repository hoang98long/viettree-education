"""Regressions found during the November system audit."""

import pytest

from app.services.grading import grade_answer


@pytest.mark.parametrize(
    "accepted,typed",
    [
        ("12 000,50", "12000.5"),
        ("1\u202f234,50", "1 234.500"),
        ("-12 000.50", "-12000,500"),
    ],
)
def test_teacher_grouped_decimal_key_accepts_equivalent_decimal_presentation(accepted, typed):
    assert grade_answer("fill_blank", {"accepted_answers": [accepted]}, {"text": typed})


@pytest.mark.parametrize(
    "accepted,typed",
    [
        ("12 000,50", "1200.5"),
        ("12 000,50", "12000.500000000000000000000001"),
        ("12 00,50", "1200.5"),
        ("12 000", "12.000"),
        ("1/2", "2/4"),
    ],
)
def test_grouped_decimal_support_does_not_relax_quantity_or_fraction_form(accepted, typed):
    assert not grade_answer("fill_blank", {"accepted_answers": [accepted]}, {"text": typed})


def test_explicit_case_sensitive_format_is_retained():
    assert not grade_answer(
        "fill_blank",
        {"accepted_answers": ["12 000,50"], "case_sensitive": True},
        {"text": "12000.5"},
    )


@pytest.mark.integration
def test_grouped_decimal_is_graded_by_server_without_rewriting_the_answer(logged_student, conn):
    from sqlalchemy import select

    from app.db import db
    from tests.test_integration import start

    attempt_id, _, _ = start(logged_student)
    items = logged_student.get(f"/api/v1/attempts/{attempt_id}").json()["items"]
    target = next(item for item in items if item["question_type"] == "fill_blank")
    versions = db.table("question_versions")
    # An isolated fixture represents an administrator's valid grouped decimal key.
    conn.execute(
        versions.update()
        .where(versions.c.id == target["question_version_id"])
        .values(grading={"accepted_answers": ["12 000,50"], "case_sensitive": False})
    )
    answer = {"text": "12000.5"}
    saved = logged_student.put(
        f"/api/v1/attempts/{attempt_id}/answers/{target['id']}", json={"answer": answer}
    )
    assert saved.status_code == 200
    result = logged_student.post(f"/api/v1/attempts/{attempt_id}/submit")
    assert result.status_code == 200
    graded = next(item for item in result.json()["items"] if item["id"] == target["id"])
    assert graded["is_correct"] is True and graded["score"] == target["points"]
    assert graded["student_answer"] == answer
    assert result.json()["total_score"] == target["points"]
    assert conn.execute(
        select(versions.c.grading).where(versions.c.id == target["question_version_id"])
    ).scalar_one()["accepted_answers"] == ["12 000,50"]
