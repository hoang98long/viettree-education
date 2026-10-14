"""Read-only inventory and structural checks; semantic review stays explicit."""

from collections import Counter
from uuid import UUID

from app.curriculum.lesson_content import enrich
from app.curriculum.registry import SUBJECT_CODES, SUPPORTED_GRADES, get_pack
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import LessonContent


def sources():
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


def audit_sources():
    counts = Counter()
    issues = []
    dummy = UUID(int=1)
    for grade, subject, plan, code, lessons, questions in sources():
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
    }
