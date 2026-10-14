import re
import unicodedata
from decimal import Decimal

from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas.attempts import BlankAnswer, ChoiceAnswer, MultipleAnswer, OrderAnswer, TextAnswer

ANSWER_MODELS = {
    "single_choice": ChoiceAnswer,
    "multiple_choice": MultipleAnswer,
    "fill_blank": BlankAnswer,
    "ordering": OrderAnswer,
    "free_text": TextAnswer,
}


def normalize(text: str, case_sensitive: bool = False) -> str:
    # Giữ dấu tiếng Việt, chuẩn NFC, chỉ gộp whitespace và tùy chọn casefold.
    text = " ".join(unicodedata.normalize("NFC", text).split())
    return text if case_sensitive else text.casefold()


def numeric_presentation(value: str, decimals=False) -> str:
    """Ignore harmless numeric spacing, without simplifying a requested fraction."""
    if re.fullmatch(r"[+-]?\d{1,3}(?: \d{3})+", value):
        return value.replace(" ", "")
    if re.fullmatch(r"[+-]?\d+\s*/\s*[1-9]\d*", value):
        return value.replace(" ", "")
    if decimals and re.fullmatch(r"[+-]?(?:\d+|\d{1,3}(?: \d{3})+)[.,]\d+", value):
        number = Decimal(value.replace(" ", "").replace(",", "."))
        return format(number, "f").rstrip("0").rstrip(".")
    return value


def safe_content(content: dict) -> dict:
    # Whitelist ở từng tầng, kể cả khi JSONB có chèn đáp án ngoài ý muốn.
    result = {"prompt": str(content.get("prompt", ""))}
    if "options" in content:
        result["options"] = [
            {"id": str(item["id"]), "text": str(item["text"])}
            for item in content["options"]
            if "id" in item and "text" in item
        ]
    return result


def validate_answer(kind: str, content: dict, answer: dict):
    model = ANSWER_MODELS.get(kind)
    if not model:
        raise HTTPException(422, "Dạng câu hỏi này chưa hỗ trợ làm bài")
    try:
        validated = model.model_validate(answer).model_dump()
    except ValidationError:
        raise HTTPException(422, "Câu trả lời chưa đúng định dạng") from None
    allowed = {item["id"] for item in content.get("options", [])}
    if kind == "single_choice" and validated["option_id"] not in allowed:
        raise HTTPException(422, "Lựa chọn không thuộc câu hỏi")
    if kind in ("multiple_choice", "ordering"):
        values = validated["option_ids" if kind == "multiple_choice" else "ordered_ids"]
        if len(values) != len(set(values)) or not set(values) <= allowed:
            raise HTTPException(422, "Các lựa chọn không hợp lệ")
        if kind == "ordering" and set(values) != allowed:
            raise HTTPException(422, "Hãy sắp xếp đủ các phần")
    return validated


def grade_answer(kind: str, grading: dict, answer: dict | None) -> bool | None:
    if kind == "free_text":
        return None
    if answer is None:
        return False
    if kind == "single_choice":
        return answer.get("option_id") == grading["correct_option_id"]
    if kind == "multiple_choice":
        return set(answer.get("option_ids", [])) == set(grading["correct_option_ids"])
    if kind == "fill_blank":
        sensitive = grading.get("case_sensitive", False)
        accepted = [normalize(value, sensitive) for value in grading["accepted_answers"]]
        candidate = normalize(answer.get("text", ""), sensitive)
        if not sensitive:
            decimals = any(re.fullmatch(r"[+-]?\d+[.,]\d+", value) for value in accepted)
            accepted = [numeric_presentation(value, decimals) for value in accepted]
            candidate = numeric_presentation(candidate, decimals)
        return candidate in accepted
    if kind == "ordering":
        return answer.get("ordered_ids") == grading["ordered_ids"]
    raise ValueError("Không có grader hợp lệ")
