import re
import unicodedata


def _visible(value):
    # Compatibility glyphs and invisible format characters must not hide a
    # disclosure. Keep the original accented text separately for ambiguous words.
    return "".join(
        c for c in unicodedata.normalize("NFKC", value) if unicodedata.category(c) != "Cf"
    )


def normalized(value):
    value = _visible(value)
    return "".join(
        c for c in unicodedata.normalize("NFD", value.casefold()) if not unicodedata.combining(c)
    )


def moderation_reason(text):
    value = " ".join(normalized(text).replace("đ", "d").split())
    if re.search(r"(?:\d[\s().-]*){8,}|[\w.+-]+@[\w.-]+\.[a-z]{2,}|https?://", value, re.I):
        return "personal_data"
    if re.search(
        r"\b(?:mat khau|password|dia chi(?: nha)?|(?:home|my) address|so dien thoai|phone(?: number)?)"
        r"\s*(?:cua (?:em|toi))?\s*(?:la\b|is\b|:|=)\s*\S+",
        value,
    ) or re.search(
        r"\b(?:em ten la|toi ten la|ten (?:em|toi) la|truong em la|lop em la|my name is|i live at|i go to school at)\s+\S",
        value,
    ):
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
    # Stripping tones makes "tự tử", "từ từ" and "tự tư duy" collide.
    # Match accented self-harm language as written, or unaccented intent phrases.
    accented = " ".join(_visible(text).casefold().split())
    if (
        re.search(r"\b(?:tự tử|tự hại|tự làm đau|cắt tay)\b", accented)
        or re.search(
            r"\b(?:muon tu tu|dinh tu tu|cach tu tu|muon chet|khong muon song|"
            r"(?:tu )?lam dau ban than|kill myself|hurt myself|self[- ]harm)\b",
            value,
        )
        or accented == "tu tu"
        or re.search(
            r"\b(?:khieu dam|tinh duc|che bom|che sung|giet nguoi|lam hai ban|ma tuy|"
            r"hack tai khoan|bat nat|danh ban|porn|sexual|sex|make a bomb|build a bomb|"
            r"bully|bullying|steal passwords?)\b",
            value,
        )
    ):
        return "unsafe_content"
    return None


def moderation_message(reason):
    if reason == "unsafe_content":
        return (
            "Mình dừng nội dung này nhé. Nếu em thấy buồn, bị bắt nạt hoặc muốn làm đau mình, "
            "hãy nhờ bố mẹ, thầy cô hoặc một người lớn em tin cậy ở bên và giúp em ngay."
        )
    if reason == "personal_data":
        return "Em giữ tên thật, địa chỉ, số điện thoại và mật khẩu riêng nhé. Hãy dùng dữ liệu mẫu của bài."
    return "Em dùng yêu cầu và dữ liệu mẫu của bài, rồi nhờ thầy cô nếu cần giúp nhé."
