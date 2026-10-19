from xml.etree import ElementTree

import pytest

from app.academy.curriculum import content, records
from app.academy.learning import grade_step
from app.academy.media import ASSETS

# Editorial keys reviewed independently of the activity's stored answers.
CASES = [
    (
        1,
        39,
        ["Có trang để đọc", "Dùng để viết"],
        ["Sách", "Có trang để đọc", "Nhờ người lớn đọc cùng"],
    ),
    (1, 40, ["Gọi tên sách", "Hỏi lại"], ["Không thấy", "Mở phần che", "Có"]),
    (2, 39, ["Đúng cả hai", "Khác màu", "Khác đồ vật"], ["Bút đỏ", "Màu sắc", "Hai: vật và màu"]),
    (
        2,
        40,
        ["Hỏi sách môn nào", "Chọn sách Toán", "Chọn sách Tiếng Việt"],
        ["Sách môn nào?", "Sách Toán", "Để hiểu đúng yêu cầu"],
    ),
    (
        3,
        39,
        ["Nhánh đọc", "Nhánh viết, có mực", "Nhánh viết, không mực"],
        ["Bút mực", "Viết, không có mực", "Không"],
    ),
    (
        3,
        40,
        ["Đủ để theo bảng", "Cần thêm thông tin", "Ngoài bộ quy tắc"],
        ["Bổ sung dòng bị mất", "Bảng này chưa xét cam", "Người thiết kế bảng"],
    ),
    (
        4,
        39,
        ["Căn cứ phù hợp", "Chưa đủ căn cứ", "Chưa đủ căn cứ", "Không đúng chủ đề"],
        ["Nội dung trồng cây", "Không", "Có, đối chiếu nội dung sách"],
    ),
    (
        4,
        40,
        ["Khớp thẻ gốc", "Khác thẻ gốc", "Vẫn phải đối chiếu", "Cần tìm nguồn"],
        ["16 giờ", "Không", "Nhờ người lớn kiểm tra giờ hiện hành"],
    ),
    (
        5,
        39,
        ["Đáp ứng hai tiêu chí", "Khác chủ đề", "Vượt độ dài", "Vẫn cần xét tiêu chí"],
        ["Sách A", "80 trang vượt giới hạn 20 trang", "Xét lại các tiêu chí"],
    ),
    (
        5,
        40,
        ["Bổ sung bối cảnh", "Bổ sung bối cảnh", "Chưa dùng ngay", "Kiểm tra trước khi dùng"],
        [
            "Chưa, cần người phụ trách kiểm tra",
            "Loại cây và độ ẩm đất",
            "Người phụ trách được phân công",
        ],
    ),
]


@pytest.mark.parametrize("grade,number,activity_keys,quiz_keys", CASES)
def test_reasoning_editorial_keys_and_alternative_choices(grade, number, activity_keys, quiz_keys):
    row = next(r for r in records() if r["code"] == f"AI{grade}-{number}")
    payload = content(row)
    exercise, checkpoint = payload["steps"][3:5]
    practice = exercise["activity"]
    assert len(practice["hints"]) == 3
    assert [item["answer"] for item in practice["items"]] == activity_keys
    assert [q["options"][q["answer"]] for q in checkpoint["questions"]] == quiz_keys
    for level in (1, 2, 3):
        limit = level + 1 if level < 3 else len(activity_keys)
        answers = {f"item-{i}": key for i, key in enumerate(activity_keys[:limit], 1)}
        assert grade_step(exercise, answers, level)[0] == 1
    wrong = {
        item["id"]: next(choice for choice in practice["choices"] if choice != item["answer"])
        for item in practice["items"]
    }
    assert grade_step(exercise, wrong, 3)[0] == 0
    answers = {
        q["id"]: str(q["options"].index(key))
        for q, key in zip(checkpoint["questions"], quiz_keys, strict=True)
    }
    assert grade_step(checkpoint, answers)[0] == 1
    if grade <= 2:
        assert all(len(step["text"].split()) <= 18 for step in payload["steps"])


def test_concealed_card_is_visually_covered_instead_of_showing_a_guess():
    root = ElementTree.fromstring((ASSETS / "AI1-40-v2-item-2.svg").read_bytes())
    assert root.find("{http://www.w3.org/2000/svg}title").text == "Thẻ bị che kín"
    assert any(node.text == "?" for node in root.findall(".//{http://www.w3.org/2000/svg}text"))
