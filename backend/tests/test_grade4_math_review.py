"""Independent solutions from the Free/VIP exercise statements, October 2026.

The 54 newer thinking questions have their own independent answer sheet in
test_grade4_extension.py. These 88 questions cover the remaining mathematics.
"""

import pytest

from app.curriculum.quality import sources
from app.services.grading import grade_answer, validate_answer

ANSWERS = {
    "numbers": [
        "70 000",
        "90 010",
        "42005",
        "37 000",
        ["49 999", "40 500"],
        ["20 999", "21 003", "21 030", "21 300"],
        "100000",
        "600 000 + 8 000 + 40 + 2",
    ],
    "operations": [
        "6 823",
        "5525",
        "1 000",
        "18",
        ["6 × 4", "96 : 4", "30 − 6"],
        ["Tính số bi ban đầu: 5 × 12", "Tính số bi còn lại: 60 − 18", "Kết luận còn 42 viên bi"],
        "26",
        "135 kg",
    ],
    "fractions": [
        "8",
        "2/6",
        "6",
        "5/7",
        ["2/4", "3/6", "4/8"],
        ["1/8", "3/8", "5/8", "7/8"],
        "4",
        "6/6",
    ],
    "measurement": [
        "3000",
        "135",
        "26 cm",
        "25 cm²",
        ["1 km = 1 000 m", "1 giờ = 60 phút"],
        ["50 cm", "150 cm", "2 m", "3 m"],
        "21",
        "Vuông góc",
    ],
    "vip-multi-step": [
        "87",
        "10",
        "80",
        ["5 × 12 − 17", "60 − 17"],
        ["Tính 3 × 20 = 60 chai", "Tính 60 − 15 = 45 chai", "Kiểm tra 45 + 15 = 60"],
        "48",
        "21",
        "160 + 40 = 8 × 25",
    ],
    "vip-fraction-reasoning": [
        "9",
        "15",
        "3/4 = 6/8 và 6/8 > 5/8",
        ["2/4", "3/6", "4/8"],
        "32",
        "7/8 km",
        ["1/4", "1/2", "3/4"],
        "2/6",
    ],
    "extend-rounding": [
        "13 000",
        "4000",
        "7 900",
        ["5 600", "6 200"],
        ["Xác định hàng nghìn", "Nhìn hàng trăm là 4", "Giữ 8 và thay phần sau bằng 0"],
        "Số đếm thực tế",
    ],
    "extend-area": [
        "26 m",
        "40",
        "cm²",
        ["Chu vi đo đường bao", "Diện tích đo phần bên trong"],
        ["Đổi 2 m = 200 cm", "Tính 200 × 50", "Ghi 10 000 cm²"],
        "26",
    ],
    "extend-reasoning": [
        "77",
        "18",
        "5 thùng và 18 chai mỗi thùng",
        ["3 × 12 + 4", "36 + 4"],
        ["4 × 25 = 100", "100 − 36 = 64", "64 + 36 = 100 để kiểm tra"],
        "77 + 37 = 90 + 24",
    ],
    "extend-fraction-total": [
        "12",
        "16",
        "5/8",
        ["2/4", "3/6"],
        ["28 : 4 = 7", "7 × 3 = 21", "28 − 21 = 7"],
        "Còn 1/3 của tổng",
    ],
    "vip-fraction-project": [
        "5/8",
        "3/8",
        ["2/4", "4/8"],
        "2",
        "5/8",
        ["Đổi 1/4 = 2/8", "Cộng 2/8 + 3/8 = 5/8", "Lấy 8/8 − 5/8 = 3/8"],
        "Sai vì cùng mẫu số thì giữ mẫu số 8",
        "3/8",
    ],
    "vip-garden-design": [
        "26 m",
        "40 m²",
        "24",
        ["Cùng chu vi 26 m", "Diện tích lần lượt 40 m² và 36 m²"],
        "24 m²",
        ["Đổi 500 cm = 5 m", "Tính 5 × 3 = 15", "Viết đáp số 15 m²"],
        "9",
        "Không, phần đất bên trong vẫn giữ nguyên",
    ],
}
UNITS = {
    code.removeprefix("VT4-MATH-"): questions
    for grade, subject, _, code, _, questions in sources()
    if grade == 4 and subject == "MATH"
}


@pytest.mark.parametrize("code", ANSWERS)
def test_free_and_vip_math_with_independent_solutions(code):
    questions, sheet = UNITS[code], ANSWERS[code]
    assert len(questions) == len(sheet)
    for question, solution in zip(questions, sheet, strict=True):
        kind = question["question_type"]
        options = {o["text"]: o["id"] for o in question["content"].get("options", [])}
        if kind == "fill_blank":
            answer = {"text": solution}
        elif kind == "single_choice":
            answer = {"option_id": options[solution]}
        else:
            key = "ordered_ids" if kind == "ordering" else "option_ids"
            answer = {key: [options[text] for text in solution]}
        validate_answer(kind, question["content"], answer)
        assert grade_answer(kind, question["grading"], answer), question["content"]["prompt"]
