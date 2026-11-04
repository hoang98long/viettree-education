from app.curriculum.registry import SUPPORTED_GRADES
from app.curriculum.supplements.discovery import CODE, TITLE, english, math, vietnamese
from app.curriculum.supplements.release import SupplementPack


def content(grade):
    if grade not in SUPPORTED_GRADES:
        raise ValueError("Chọn khối lớp 1–5")
    subjects = {
        "MATH": math.content(grade),
        "VIETNAMESE": vietnamese.content(grade),
        "ENGLISH": english.content(grade),
    }
    for units in subjects.values():
        for row in units:
            row["sort_order"] = 251 if row["minimum_plan_code"] == "vip" else 250
            for question in row["questions"]:
                question["difficulty"] = (
                    3 if row["minimum_plan_code"] == "vip" else 1 if grade <= 2 else 2
                )
    return subjects


PACK = SupplementPack(CODE, TITLE, content)
