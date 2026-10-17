from app.curriculum.registry import SUPPORTED_GRADES
from app.curriculum.supplements.daily import english, math, vietnamese
from app.curriculum.supplements.release import SupplementPack


def content(grade):
    if grade not in SUPPORTED_GRADES:
        raise ValueError("Chọn khối lớp 1–5")
    return {
        "MATH": [math.content(grade)],
        "VIETNAMESE": [vietnamese.content(grade)],
        "ENGLISH": [english.content(grade)],
    }


PACK = SupplementPack("daily-2026-03", "Mỗi ngày một khám phá", content)
