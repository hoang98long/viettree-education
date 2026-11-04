"""Search and release filters shared by lesson and practice discovery."""

import unicodedata

from fastapi import HTTPException

from app.curriculum.supplements.registry import releases

ACCENTS = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"


def fold(value):
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value.lower().replace("đ", "d"))
        if not unicodedata.combining(char)
    )


BASE_LETTERS = "".join(fold(char) for char in ACCENTS)


def release_options():
    return [{"code": pack.code, "title": pack.title} for pack in releases().values()]


def release_predicate(column, code):
    if code not in releases():
        raise HTTPException(422, "Chọn bộ học liệu có trong danh sách")
    escaped = code.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return column.like("VT%-" + escaped + "-%", escape="\\")
