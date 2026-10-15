from app.curriculum.registry import SUPPORTED_GRADES
from app.curriculum.supplements.explorers import english, math, vietnamese
from app.curriculum.supplements.release import SupplementPack


def content(grade):
    if grade not in SUPPORTED_GRADES:
        raise ValueError("Chọn khối lớp 1–5")
    return {
        "MATH": [math.content(grade)],
        "VIETNAMESE": [vietnamese.content(grade)],
        "ENGLISH": [english.content(grade)],
    }


PACK = SupplementPack("explorers-2026-01", "Khám phá và luyện ngắn", content)
