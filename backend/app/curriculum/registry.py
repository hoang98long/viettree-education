"""One registry for pack selection, expected inventory and admin curriculum maps."""

from dataclasses import dataclass, field
from functools import lru_cache

SUBJECT_CODES = ("MATH", "VIETNAMESE", "ENGLISH")
SUPPORTED_GRADES = (1, 2, 3, 4, 5)
EXPECTED = {
    "MATH": {"topics": 8, "lessons": 25, "questions": 142, "assessments": 21},
    "VIETNAMESE": {"topics": 6, "lessons": 23, "questions": 130, "assessments": 19},
    "ENGLISH": {"topics": 7, "lessons": 20, "questions": 112, "assessments": 16},
}


@dataclass(frozen=True)
class GradePack:
    grade: int
    core: dict
    extensions: tuple[dict, ...]
    topics: dict
    topic_map: dict
    sources: dict
    expected: dict = field(
        default_factory=lambda: {subject: dict(values) for subject, values in EXPECTED.items()}
    )


@lru_cache(maxsize=5)
def get_pack(grade: int) -> GradePack:
    if grade not in SUPPORTED_GRADES:
        raise ValueError("Chưa có bộ học liệu ba môn cho khối này")
    if grade == 5:
        from app.curriculum.grades.grade_05.pack import CORE, EXTENSION, SOURCES, TOPIC_MAP, TOPICS
        from app.curriculum.grades.grade_05.pack import EXPECTED as GRADE5_EXPECTED

        return GradePack(grade, CORE, (EXTENSION,), TOPICS, TOPIC_MAP, SOURCES, GRADE5_EXPECTED)
    if grade in (1, 2):
        from app.curriculum.grades.early_primary.pack import PACKS, SOURCES, TOPICS

        topics = TOPICS[grade]
        topic_map = {
            subject: {
                code: (
                    title,
                    "Học từng bước ngắn với người hướng dẫn; bài vận dụng giữ trong kiến thức của khối.",
                )
                for code, title in rows.items()
            }
            for subject, rows in topics.items()
        }
        return GradePack(
            grade, PACKS[grade]["core"], (PACKS[grade]["extension"],), topics, topic_map, SOURCES
        )
    from app.curriculum.grades.grade_04.map import SOURCES

    if grade == 3:
        from app.curriculum.grades.grade_03.pack import CORE, EXTENSION, FOCUS, TOPICS

        topic_map = {
            subject: {code: (title, FOCUS[subject][code]) for code, title in rows.items()}
            for subject, rows in TOPICS.items()
        }
        return GradePack(grade, CORE, (EXTENSION,), TOPICS, topic_map, SOURCES)
    from app.curriculum.grades.grade_04.advanced import ADVANCED
    from app.curriculum.grades.grade_04.foundation import CURRICULUM
    from app.curriculum.grades.grade_04.map import TOPIC_MAP
    from app.curriculum.grades.grade_04.standard import EXPANDED
    from app.curriculum.grades.grade_04.thinking import GRADE4
    from app.curriculum.grades.grade_04.vip import VIP_EXTENSION

    topics = {
        subject: {code: row[0] for code, row in rows.items()} for subject, rows in TOPIC_MAP.items()
    }
    return GradePack(
        grade, CURRICULUM, (ADVANCED, EXPANDED, VIP_EXTENSION, GRADE4), topics, TOPIC_MAP, SOURCES
    )


def inventory(grade: int) -> dict:
    """Source inventory, without a database or account/membership mutations."""
    pack = get_pack(grade)
    report = {}
    for subject in SUBJECT_CODES:
        core = pack.core[subject]
        units = [row for extension in pack.extensions for row in extension[subject]]
        report[subject] = {
            "topics": len({row["code"] for row in core} | {row["topic"] for row in units}),
            "lessons": sum(len(row["lessons"]) for row in core) + len(units),
            "questions": sum(len(row["questions"]) for row in core + units),
            "assessments": len(core) + len(units),
        }
    return report
