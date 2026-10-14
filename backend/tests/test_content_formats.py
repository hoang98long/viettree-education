import pytest

from app.services.grading import grade_answer


@pytest.mark.parametrize(
    "expected,typed",
    [
        ("12000", "12 000"),
        ("12000", "12\u00a0000"),
        ("12000", "12\u202f000"),
        ("3/8", "3 / 8"),
        ("4.75", "4,750"),
        ("12000.5", "12 000,50"),
    ],
)
def test_numeric_spacing_and_explicit_decimal_answers(expected, typed):
    assert grade_answer("fill_blank", {"accepted_answers": [expected]}, {"text": typed})


@pytest.mark.parametrize(
    "expected,typed",
    [
        ("12000", "1 200"),
        ("12000", "12 00"),
        ("1000", "1.000"),
        ("1/2", "2 / 4"),
        ("3/8", "3 / 0"),
        ("12000", "12 000 đồng"),
        ("cá", "ca"),
        ("Có", "Không"),
        ("4.75", "4.75000000000000000000000000001"),
    ],
)
def test_friendly_grading_does_not_change_mathematical_or_language_meaning(expected, typed):
    assert not grade_answer("fill_blank", {"accepted_answers": [expected]}, {"text": typed})


def test_case_sensitive_spelling_keeps_exact_format():
    assert not grade_answer(
        "fill_blank", {"accepted_answers": ["Hà Nội"], "case_sensitive": True}, {"text": "hà nội"}
    )
