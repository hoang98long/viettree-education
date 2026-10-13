from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.curriculum.grades.grade_04.foundation import CURRICULUM
from app.personalization.engine import evidence_update
from app.services.grading import grade_answer, normalize, safe_content, validate_answer


def correct_answer(question):
    key = question["grading"]
    kind = question["question_type"]
    if kind == "single_choice":
        return {"option_id": key["correct_option_id"]}
    if kind == "multiple_choice":
        return {"option_ids": key["correct_option_ids"]}
    if kind == "ordering":
        return {"ordered_ids": key["ordered_ids"]}
    return {"text": key["accepted_answers"][0]}


QUESTIONS = [
    (subject, q)
    for subject, topics in CURRICULUM.items()
    for topic in topics
    for q in topic["questions"]
]


@pytest.mark.parametrize("subject,question", QUESTIONS)
def test_curriculum_grading(subject, question):
    answer = correct_answer(question)
    validate_answer(question["question_type"], question["content"], answer)
    assert grade_answer(question["question_type"], question["grading"], answer)
    assert not grade_answer(question["question_type"], question["grading"], None)
    assert question["explanation"]["text"]


def test_subject_counts_and_types():
    for subject, topics in CURRICULUM.items():
        assert len(topics) >= 4
        assert sum(len(topic["lessons"]) for topic in topics) >= 8
        assert sum(len(topic["questions"]) for topic in topics) >= 30
        for topic in topics:
            assert 8 <= len(topic["questions"]) <= 10
            assert {q["question_type"] for q in topic["questions"]} == {
                "single_choice",
                "multiple_choice",
                "fill_blank",
                "ordering",
            }
            for lesson in topic["lessons"]:
                assert len(lesson["content"]["blocks"]) >= 4
                assert len(lesson["content"]["blocks"][0]["text"]) > 80


def test_normalization_preserves_vietnamese_accents():
    assert normalize("  NGỌT  ") == "ngọt"
    assert normalize("ngo\u0323t") == "ngọt"
    assert not grade_answer("fill_blank", {"accepted_answers": ["ngọt"]}, {"text": "ngot"})
    assert grade_answer("fill_blank", {"accepted_answers": ["ngọt"]}, {"text": " NGỌT "})


def test_multiple_choice_sets_and_ordering_sequence():
    assert grade_answer(
        "multiple_choice", {"correct_option_ids": ["a", "c"]}, {"option_ids": ["c", "a"]}
    )
    assert not grade_answer(
        "multiple_choice", {"correct_option_ids": ["a", "c"]}, {"option_ids": ["a", "b", "c"]}
    )
    assert not grade_answer("ordering", {"ordered_ids": ["a", "c"]}, {"ordered_ids": ["c", "a"]})
    assert grade_answer("free_text", {}, {"text": "bất kỳ"}) is None


def test_answer_input_rejects_score_and_invalid_options():
    content = {"prompt": "Chọn", "options": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}]}
    for kind, answer in [
        ("single_choice", {"option_id": "c"}),
        ("single_choice", {"option_id": "a", "score": 100}),
        ("multiple_choice", {"option_ids": ["a", "a"]}),
        ("ordering", {"ordered_ids": ["a"]}),
    ]:
        with pytest.raises(HTTPException):
            validate_answer(kind, content, answer)


def test_public_content_whitelist_deep():
    assert safe_content(
        {
            "prompt": "Hi",
            "answer_key": "a",
            "grading": {},
            "explanation": "secret",
            "options": [{"id": "a", "text": "A", "is_correct": True}],
        }
    ) == {"prompt": "Hi", "options": [{"id": "a", "text": "A"}]}


def test_mastery_confidence_and_review_intervals():
    at = datetime(2026, 10, 9, tzinfo=timezone.utc)
    state = evidence_update({}, False, 3, 1, at)
    assert state["confidence"] == 0.05 and state["mastery_score"] == 0
    assert (state["next_review_at"] - at).days == 1
    for _ in range(24):
        state = evidence_update(state, True, 3, 1, at)
    assert 0 <= state["mastery_score"] <= 1 and state["confidence"] == 1
    assert state["questions_attempted"] == 25 and state["correct_count"] == 24
    assert (state["next_review_at"] - at).days == 7


def test_math_answers_independently():
    assert MATH_ANSWER("operations", 0) == str(4508 + 2315)
    assert MATH_ANSWER("operations", 1) == str(8000 - 2475)
    assert MATH_ANSWER("operations", 6) == str(156 // 6)
    assert MATH_ANSWER("measurement", 6) == str(7 * 3)


def MATH_ANSWER(topic_code, index):
    question = next(topic for topic in CURRICULUM["MATH"] if topic["code"] == topic_code)[
        "questions"
    ][index]
    if question["question_type"] == "single_choice":
        value = next(
            o["text"]
            for o in question["content"]["options"]
            if o["id"] == question["grading"]["correct_option_id"]
        )
        return value.replace(" ", "")
    return question["grading"]["accepted_answers"][0]
