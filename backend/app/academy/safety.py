import re
import unicodedata


def normalized(value):
    return "".join(
        c for c in unicodedata.normalize("NFD", value.casefold()) if not unicodedata.combining(c)
    )


def moderation_reason(text):
    value = normalized(text).replace("đ", "d")
    if re.search(r"(?:\d[\s().-]*){8,}|[\w.+-]+@[\w.-]+\.[a-z]{2,}|https?://", text, re.I):
        return "personal_data"
    if re.search(
        r"(?:mat khau|password|dia chi nha|so dien thoai)\s*(?:cua (?:em|toi))?\s*(?:la|:|=)\s*\S+",
        value,
    ) or any(part in value for part in ["em ten la", "toi ten la", "truong em la", "lop em la"]):
        return "personal_data"
    if any(
        part in value
        for part in [
            "ignore previous",
            "ignore all",
            "bo qua huong dan",
            "system prompt",
            "jailbreak",
            "api key",
            "secret token",
        ]
    ):
        return "injection"
    if any(
        part in value
        for part in [
            "khieu dam",
            "tinh duc",
            "che bom",
            "tu tu",
            "giet nguoi",
            "lam hai ban",
            "ma tuy",
            "hack tai khoan",
        ]
    ):
        return "unsafe_content"
    return None
