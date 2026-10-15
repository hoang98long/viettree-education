"""Compatibility entry points for the unchanged applied-2026-01 release."""

from app.curriculum.registry import SUPPORTED_GRADES
from app.curriculum.supplements.applied import english, math, vietnamese
from app.curriculum.supplements.release import SupplementPack

RELEASE = "applied-2026-01"


def content(grade):
    if grade not in SUPPORTED_GRADES:
        raise ValueError("Chọn khối lớp 1–5")
    return {
        "MATH": math.content(grade),
        "VIETNAMESE": vietnamese.content(grade),
        "ENGLISH": english.content(grade),
    }


PACK = SupplementPack(RELEASE, "Tình huống gần gũi", content)


def inventory(grades=SUPPORTED_GRADES):
    return PACK.inventory(grades)


def seed(conn, grades=SUPPORTED_GRADES):
    return PACK.seed(conn, grades)


def published_counts(conn, grade):
    return PACK.published_counts(conn, grade)


def verify(conn, grades=SUPPORTED_GRADES):
    return PACK.verify(conn, grades)
