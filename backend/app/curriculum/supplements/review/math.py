"""Check operations already introduced in each grade."""

from app.curriculum.supplements.review.builders import cards, pick, unit


def content(grade):
    if grade == 1:
        title, topic = "Đếm lại cho chắc", "operations"
        teaching = "Đếm từng vật. Khi bớt đi, đếm phần còn lại."
        example = "Có 8 que, cất 3 que: còn 5 que. Thử lại: 5 + 3 = 8."
        rows = [
            ("Có 8 que, cất 3 que. Còn mấy que?", "5 que", ["4 que", "6 que"], "8 − 3 = 5."),
            ("Bạn tính 7 − 2 = 6. Kết quả đúng là gì?", "5", ["6", "9"], "Bớt 2 khỏi 7 còn 5."),
            (
                "Phép tính nào giúp kiểm tra 9 − 4 = 5?",
                "5 + 4 = 9",
                ["5 + 3 = 8", "5 − 4 = 1"],
                "Lấy phần còn lại cộng phần đã bớt.",
            ),
            ("Có 6 bút, thêm 3 bút. Có tất cả mấy bút?", "9 bút", ["3 bút", "8 bút"], "6 + 3 = 9."),
        ]
    elif grade == 2:
        title, topic = "Nhớ một chục khi cộng", "operations"
        teaching = "Cộng hàng đơn vị trước. Đủ mười đơn vị thì đổi thành một chục."
        example = "28 + 15: 8 + 5 = 13; viết 3, nhớ 1. Hàng chục: 2 + 1 + 1 = 4. Kết quả 43."
        rows = [
            (
                "Bạn viết 28 + 15 = 33. Kết quả đúng là gì?",
                "43",
                ["33", "53"],
                "Cần cộng 1 chục nhớ: 2 + 1 + 1 = 4 chục.",
            ),
            (
                "Trong phép cộng 28 + 15, 8 + 5 = 13. Nhớ bao nhiêu chục?",
                "1 chục",
                ["3 chục", "Không nhớ"],
                "13 đơn vị = 1 chục và 3 đơn vị.",
            ),
            ("36 + 27 bằng bao nhiêu?", "63", ["53", "73"], "6 + 7 = 13; 3 + 2 + 1 = 6 chục."),
            (
                "Phép tính nào kiểm tra 28 + 15 = 43?",
                "43 − 15 = 28",
                ["43 + 15 = 58", "28 − 15 = 13"],
                "Lấy tổng trừ một số hạng được số hạng kia.",
            ),
        ]
    elif grade == 3:
        title, topic = "Chia đều rồi thử lại", "operations"
        teaching = "Chia đều xong, lấy số của mỗi nhóm nhân số nhóm để kiểm tra."
        example = "42 bút chia đều vào 6 hộp: mỗi hộp 7 bút. Thử: 7 × 6 = 42."
        rows = [
            (
                "42 bút chia đều vào 6 hộp. Mỗi hộp mấy bút?",
                "7 bút",
                ["6 bút", "8 bút"],
                "42 : 6 = 7.",
            ),
            (
                "Bạn tính 42 : 6 = 8. Để thử riêng thương 8, em cần nhân thế nào?",
                "8 × 6 = 48",
                ["7 × 6 = 42", "42 + 6 = 48"],
                "Nếu thương là 8 thì nhân lại phải bằng 42, nhưng được 48.",
            ),
            (
                "Có 56 nhãn chia đều cho 7 bạn. Mỗi bạn được mấy nhãn?",
                "8 nhãn",
                ["7 nhãn", "9 nhãn"],
                "56 : 7 = 8; thử 8 × 7 = 56.",
            ),
            (
                "6 hộp, mỗi hộp 7 bút. Lấy ra 5 bút. Còn mấy bút?",
                "37 bút",
                ["42 bút", "47 bút"],
                "6 × 7 − 5 = 42 − 5 = 37.",
            ),
        ]
    elif grade == 4:
        title, topic = "Cùng một chiếc bánh", "fractions"
        teaching = "Cộng hai phân số cùng mẫu: cộng tử số, giữ mẫu số. Các phần phải chia đều trên cùng một đơn vị."
        example = "Một bánh chia 8 phần bằng nhau. Có 2/8 bánh và thêm 3/8 bánh: được 5/8 bánh."
        rows = [
            (
                "2/8 + 3/8 bằng bao nhiêu?",
                "5/8",
                ["5/16", "6/8"],
                "Cộng tử số 2 + 3 = 5, giữ mẫu số 8.",
            ),
            (
                "Bạn tính 1/6 + 2/6 = 3/12. Cần sửa thế nào?",
                "Giữ mẫu 6: kết quả 3/6",
                ["Giữ kết quả 3/12", "Đổi tử thành 12"],
                "Hai phân số cùng mẫu 6 nên không cộng hai mẫu số.",
            ),
            (
                "7/9 − 4/9 bằng bao nhiêu?",
                "3/9",
                ["3/18", "11/9"],
                "Trừ tử số 7 − 4 = 3, giữ mẫu 9.",
            ),
            (
                "Cùng một bánh, còn 5/8 bánh, ăn thêm 2/8 bánh. Còn bao nhiêu?",
                "3/8 bánh",
                ["7/8 bánh", "3/16 bánh"],
                "5/8 − 2/8 = 3/8.",
            ),
        ]
    else:
        title, topic = "Giảm giá rồi kiểm tra", "ratio"
        teaching = "Tính tiền giảm trước, sau đó lấy giá gốc trừ tiền giảm."
        example = "Sách 80 000 đồng, giảm 25%: giảm 20 000 đồng, còn trả 60 000 đồng."
        rows = [
            (
                "25% của 80 000 đồng là bao nhiêu?",
                "20 000 đồng",
                ["25 000 đồng", "60 000 đồng"],
                "80 000 × 25 : 100 = 20 000.",
            ),
            (
                "Sách 80 000 đồng, giảm 25%. Cần trả bao nhiêu?",
                "60 000 đồng",
                ["20 000 đồng", "55 000 đồng"],
                "80 000 − 20 000 = 60 000.",
            ),
            (
                "Bạn nói giảm 25% nghĩa là chỉ trả 25% giá gốc. Đúng không?",
                "Sai, còn trả 75%",
                ["Đúng, còn trả 25%", "Sai, phải trả 125%"],
                "100% − 25% = 75% giá gốc.",
            ),
            (
                "Vở 50 000 đồng, giảm 10%. Cần trả bao nhiêu?",
                "45 000 đồng",
                ["5 000 đồng", "40 000 đồng"],
                "Giảm 5 000 đồng, còn 50 000 − 5 000 = 45 000 đồng.",
            ),
        ]
    return unit(
        grade,
        topic,
        "check-my-math-r2" if grade == 3 else "check-my-math",
        title,
        "Tìm lỗi và kiểm tra lại một phép tính.",
        teaching,
        example,
        "Đọc lại câu hỏi: cần tìm phần đã bớt hay phần còn lại?",
        [
            "Tìm các số và việc cần tính.",
            "Dùng que, hình hoặc phép tính ngược để kiểm tra.",
            example,
        ],
        {
            "kind": "fraction",
            "numerator": 5,
            "denominator": 8,
            "caption": "Một bánh chia 8 phần bằng nhau, tô 5 phần.",
        }
        if grade == 4
        else cards("Bút chì", "Sách"),
        [pick(*row) for row in rows],
        vip=grade >= 3,
    )
