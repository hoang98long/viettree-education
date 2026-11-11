"""Read-only inventory and structural checks; semantic review stays explicit."""

import re
from collections import Counter
from fractions import Fraction
from unicodedata import normalize
from uuid import UUID

from app.curriculum.lesson_content import enrich
from app.curriculum.registry import SUBJECT_CODES, SUPPORTED_GRADES, get_pack
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import LessonContent

NUMERIC_OPTION = re.compile(
    r"(?P<number>[+−-]?(?:\d{1,3}(?:[ \u00a0\u202f]\d{3})+|\d+)"
    r"(?:[.,]\d+)?(?:\s*/\s*\d+)?)\s*(?P<unit>[^\d+−*/=<>?-]*)\Z"
)


def numeric_option(text):
    """Recognize only a number/fraction and literal unit, never evaluate prose.

    Unit conversion and the teaching intent (for example, simplest form) still
    require review. A dot or comma here is a decimal separator, not a guessed
    thousands separator; only explicit groups of three separated by spaces count.
    """
    match = NUMERIC_OPTION.fullmatch(normalize("NFC", text).strip())
    if match is None:
        return None
    number = "".join(match["number"].split()).replace("−", "-").replace(",", ".")
    try:
        value = Fraction(number)
    except (ValueError, ZeroDivisionError):
        return None
    return value, " ".join(match["unit"].casefold().split())


def equivalent_numeric_choices(question):
    if question["question_type"] != "single_choice":
        return []
    options = question["content"].get("options", [])
    correct = question["grading"].get("correct_option_id")
    grouped = {}
    for option in options:
        value = numeric_option(option["text"])
        if value is not None:
            grouped.setdefault(value, []).append(option["id"])
    return [ids for ids in grouped.values() if len(ids) > 1 and correct in ids]


def sources(include_supplements=False):
    for grade in SUPPORTED_GRADES:
        pack = get_pack(grade)
        for subject in SUBJECT_CODES:
            for topic in pack.core[subject]:
                prefix = f"VT{grade}-{subject}-{topic['code']}"
                yield grade, subject, "free", prefix, topic["lessons"], topic["questions"]
            for extension in pack.extensions:
                for unit in extension[subject]:
                    prefix = f"VT{grade}-{subject}-{unit['code']}"
                    yield (
                        grade,
                        subject,
                        unit.get("minimum_plan_code", "vip"),
                        prefix,
                        [unit["lesson"]],
                        unit["questions"],
                    )
    if include_supplements:
        from app.curriculum.supplements.registry import releases

        for pack in releases().values():
            for grade in SUPPORTED_GRADES:
                for subject, units in pack.content(grade).items():
                    for unit in units:
                        yield (
                            grade,
                            subject,
                            unit["minimum_plan_code"],
                            f"VT{grade}-{subject}-{unit['code']}",
                            [unit["lesson"]],
                            unit["questions"],
                        )


def audit_sources(include_supplements=True):
    counts = Counter()
    issues = []
    warnings = []
    numeric_questions = 0
    dummy = UUID(int=1)
    for grade, subject, plan, code, lessons, questions in sources(include_supplements):
        key = (grade, subject, plan)
        counts[key, "lessons"] += len(lessons)
        counts[key, "questions"] += len(questions)
        counts[key, "assessments"] += 1
        for lesson in lessons:
            try:
                LessonContent.model_validate(enrich(lesson["content"], code))
            except ValueError as error:
                issues.append(
                    {"code": code, "kind": "lesson_schema", "message": str(error).split("\n")[0]}
                )
        for number, question in enumerate(questions, 1):
            if subject == "MATH" and question["question_type"] == "single_choice":
                correct = question["grading"].get("correct_option_id")
                if any(
                    option["id"] == correct and numeric_option(option["text"]) is not None
                    for option in question["content"].get("options", [])
                ):
                    numeric_questions += 1
                for ids in equivalent_numeric_choices(question):
                    warnings.append(
                        {
                            "code": f"{code}-q-{number:02}",
                            "kind": "equivalent_numeric_choices_need_review",
                            "choice_ids": ids,
                        }
                    )
            try:
                QuestionInput.model_validate(
                    {
                        **question,
                        "code": code,
                        "grade": grade,
                        "subject_id": dummy,
                        "topic_id": dummy,
                        "skill_ids": [dummy],
                        "explanation": question["explanation"]["text"],
                    }
                )
            except ValueError as error:
                issues.append(
                    {
                        "code": f"{code}-q-{number:02}",
                        "kind": "question_schema",
                        "message": str(error).split("\n")[0],
                    }
                )
    return {
        "scope": "source_schema_and_inventory",
        "semantic_accuracy": "Use independent answer tests and editorial review; schema validity alone does not prove correctness.",
        "matrix": [
            {
                "grade": g,
                "subject": s,
                "plan": p,
                **{
                    name: counts[(g, s, p), name]
                    for name in ("lessons", "questions", "assessments")
                },
            }
            for g in SUPPORTED_GRADES
            for s in SUBJECT_CODES
            for p in ("free", "vip")
        ],
        "issues": issues,
        "warnings": warnings,
        "semantic_checks": {
            "numeric_literal_questions": numeric_questions,
            "equivalent_correct_choice_groups": len(warnings),
        },
    }
