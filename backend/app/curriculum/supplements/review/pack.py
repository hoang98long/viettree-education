from app.curriculum.registry import SUPPORTED_GRADES
from app.curriculum.supplements.release import SupplementPack
from app.curriculum.supplements.review import english, math, vietnamese


def content(grade):
    if grade not in SUPPORTED_GRADES:
        raise ValueError("Chọn khối lớp 1–5")
    return {
        "MATH": [math.content(grade)],
        "VIETNAMESE": [vietnamese.content(grade)],
        "ENGLISH": [english.content(grade)],
    }


PACK = SupplementPack("review-2026-02", "Đọc kỹ · Thử lại · Tự kiểm tra", content)
