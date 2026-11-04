"""Concrete quantities first; VIP reasoning stays within the grade's arithmetic."""

from app.curriculum.supplements.discovery import cards, pick, unit

DATA = {
    1: [
        (
            "operations",
            "seeds",
            "Đếm hạt để gieo",
            "Gộp hai nhóm hạt. Đếm mỗi hạt một lần.",
            "Có 3 hạt, thêm 2 hạt: có 5 hạt.",
            {"kind": "counters", "count": 5, "caption": "Năm chấm, mỗi chấm là một hạt."},
            [
                ("Có 3 hạt, thêm 2 hạt. Có mấy hạt?", "5 hạt", ["4 hạt", "6 hạt"], "3 + 2 = 5."),
                ("Có 5 hạt, gieo 1 hạt. Còn mấy hạt?", "4 hạt", ["5 hạt", "6 hạt"], "5 − 1 = 4."),
                (
                    "Nhóm A có 3 hạt, nhóm B có 2 hạt. Nhóm nào nhiều hơn?",
                    "Nhóm A",
                    ["Nhóm B"],
                    "3 lớn hơn 2.",
                ),
                (
                    "Muốn có 5 hạt, đã có 4 hạt. Cần thêm mấy hạt?",
                    "1 hạt",
                    ["2 hạt", "4 hạt"],
                    "4 + 1 = 5.",
                ),
            ],
        ),
        (
            "operations",
            "missing-seeds",
            "Ô trống của bạn Ong",
            "Tìm phần còn thiếu. Lấy tất cả bớt phần đã biết.",
            "Cần 7 hạt, đã có 4 hạt. Thêm 3 hạt vì 4 + 3 = 7.",
            cards("Có 4 hạt", "Cần 7 hạt"),
            [
                (
                    "Cần 7 hạt, đã có 4 hạt. Còn thiếu mấy hạt?",
                    "3 hạt",
                    ["2 hạt", "4 hạt"],
                    "7 − 4 = 3.",
                ),
                (
                    "Trong 3 + □ = 8, ô trống là số nào?",
                    "5",
                    ["4", "6"],
                    "8 − 3 = 5; thử lại 3 + 5 = 8.",
                ),
                (
                    "Có 9 que, cất một số que, còn 6 que. Đã cất mấy que?",
                    "3 que",
                    ["2 que", "6 que"],
                    "9 − 6 = 3.",
                ),
                (
                    "Phép tính nào đúng khi ô trống bằng 2?",
                    "5 + □ = 7",
                    ["5 + □ = 8", "5 + □ = 6"],
                    "5 + 2 = 7.",
                ),
            ],
        ),
    ],
    2: [
        (
            "measurement",
            "paper-strips",
            "Đo hai dải giấy",
            "Cộng hai độ dài khi dùng cùng đơn vị. So sánh số đo để tìm dải dài hơn.",
            "Dải đỏ 28 cm, dải xanh 12 cm. Tổng độ dài là 40 cm.",
            {
                "kind": "bars",
                "labels": ["Đỏ", "Xanh"],
                "values": [28, 12],
                "caption": "Độ dài hai dải giấy, đơn vị cm.",
            },
            [
                (
                    "Dải đỏ 28 cm, dải xanh 12 cm. Tổng độ dài là bao nhiêu?",
                    "40 cm",
                    ["30 cm", "16 cm"],
                    "28 + 12 = 40 cm.",
                ),
                (
                    "Dải đỏ 28 cm, dải xanh 12 cm. Đỏ dài hơn xanh bao nhiêu?",
                    "16 cm",
                    ["40 cm", "12 cm"],
                    "28 − 12 = 16 cm.",
                ),
                (
                    "Cắt 5 cm từ dải dài 12 cm. Phần còn lại dài bao nhiêu?",
                    "7 cm",
                    ["17 cm", "5 cm"],
                    "12 − 5 = 7 cm.",
                ),
                (
                    "Một dải dài 40 cm, dải kia 30 cm. Dải nào dài hơn?",
                    "Dải 40 cm",
                    ["Dải 30 cm"],
                    "40 lớn hơn 30; hai số đo cùng đơn vị.",
                ),
            ],
        ),
        (
            "numbers",
            "door-number",
            "Tìm số trên cánh cửa",
            "Xem riêng hàng chục và hàng đơn vị. Đọc đủ điều kiện trước khi chọn số.",
            "Số có 4 chục và 5 đơn vị là 45.",
            cards("Hàng chục", "Hàng đơn vị"),
            [
                (
                    "Số có 4 chục và 5 đơn vị là số nào?",
                    "45",
                    ["54", "40"],
                    "4 chục là 40; thêm 5 được 45.",
                ),
                (
                    "Số có hàng chục là 3, hàng đơn vị hơn hàng chục 2 đơn vị là số nào?",
                    "35",
                    ["32", "53"],
                    "Hàng đơn vị là 3 + 2 = 5; số cần tìm là 35.",
                ),
                (
                    "Trong 47 và 74, số nào có 7 đơn vị?",
                    "47",
                    ["74"],
                    "Chữ số tận cùng bên phải chỉ hàng đơn vị.",
                ),
                (
                    "Số có 6 chục, tổng hai chữ số bằng 8 là số nào?",
                    "62",
                    ["68", "26"],
                    "Hàng đơn vị là 8 − 6 = 2; số đó là 62.",
                ),
            ],
        ),
    ],
    3: [
        (
            "operations",
            "plant-rows",
            "Các hàng cây nhỏ",
            "Các hàng có số cây bằng nhau: nhân số hàng với số cây mỗi hàng.",
            "4 hàng, mỗi hàng 6 cây: có 4 × 6 = 24 cây.",
            {"kind": "garden", "rows": 4, "columns": 6, "caption": "Bốn hàng, mỗi hàng sáu cây."},
            [
                (
                    "4 hàng, mỗi hàng 6 cây. Có tất cả bao nhiêu cây?",
                    "24 cây",
                    ["10 cây", "20 cây"],
                    "4 × 6 = 24.",
                ),
                (
                    "24 cây chia đều thành 4 hàng. Mỗi hàng có bao nhiêu cây?",
                    "6 cây",
                    ["4 cây", "8 cây"],
                    "24 : 4 = 6.",
                ),
                (
                    "Mỗi hàng 6 cây, thêm 1 hàng như vậy. Từ 4 hàng thành 5 hàng có bao nhiêu cây?",
                    "30 cây",
                    ["25 cây", "29 cây"],
                    "5 × 6 = 30.",
                ),
                (
                    "24 cây, chuyển 6 cây sang vườn khác. Còn bao nhiêu cây?",
                    "18 cây",
                    ["20 cây", "30 cây"],
                    "24 − 6 = 18.",
                ),
            ],
        ),
        (
            "wordproblems",
            "step-rule",
            "Bảng số còn thiếu",
            "Theo đúng quy tắc đã nêu. Kiểm tra mỗi bước có làm cùng một việc không.",
            "Bắt đầu từ 12, mỗi bước thêm 4: 12, 16, 20, 24.",
            cards("12", "16", "20", "24"),
            [
                (
                    "Dãy 12, 16, 20, □, mỗi bước thêm 4. Ô trống là gì?",
                    "24",
                    ["22", "28"],
                    "20 + 4 = 24.",
                ),
                ("Từ 12, thêm 4 hai lần. Được số nào?", "20", ["16", "24"], "12 + 4 + 4 = 20."),
                (
                    "Bốn túi, mỗi túi 3 hạt. Thêm 8 hạt rời. Có bao nhiêu hạt?",
                    "20 hạt",
                    ["15 hạt", "24 hạt"],
                    "4 × 3 + 8 = 20.",
                ),
                (
                    "Trong 4 × 3 + □ = 20, ô trống là gì?",
                    "8",
                    ["5", "12"],
                    "4 × 3 = 12; 20 − 12 = 8.",
                ),
            ],
        ),
    ],
    4: [
        (
            "statistics",
            "library-chart",
            "Đọc bảng mượn sách",
            "Đọc nhãn, số liệu rồi chọn phép tính. Trung bình cộng bằng tổng chia số nhóm.",
            "Ba tổ mượn 8, 12, 16 quyển. Tổng 36; trung bình 12 quyển/tổ.",
            {
                "kind": "bars",
                "labels": ["Tổ 1", "Tổ 2", "Tổ 3"],
                "values": [8, 12, 16],
                "caption": "Số quyển sách ba tổ mượn trong tuần.",
            },
            [
                (
                    "Ba tổ mượn 8, 12, 16 quyển. Tổng là bao nhiêu?",
                    "36 quyển",
                    ["26 quyển", "32 quyển"],
                    "8 + 12 + 16 = 36.",
                ),
                (
                    "Ba tổ mượn tổng 36 quyển. Trung bình mỗi tổ mượn bao nhiêu?",
                    "12 quyển",
                    ["18 quyển", "9 quyển"],
                    "36 : 3 = 12.",
                ),
                (
                    "Tổ 3 mượn 16 quyển, tổ 1 mượn 8 quyển. Hơn bao nhiêu quyển?",
                    "8 quyển",
                    ["24 quyển", "6 quyển"],
                    "16 − 8 = 8.",
                ),
                (
                    "Tổ 2 mượn 12 quyển, tổ 3 mượn 16 quyển. Tổ nào mượn nhiều hơn?",
                    "Tổ 3",
                    ["Tổ 2", "Bằng nhau"],
                    "16 lớn hơn 12.",
                ),
            ],
        ),
        (
            "wordproblems",
            "two-teams",
            "Hai đội giữ sân xanh",
            "Biết tổng và hiệu: số lớn bằng (tổng + hiệu) : 2; kiểm tra lại cả hai điều kiện.",
            "Hai đội nhặt 46 lá; đội A hơn đội B 8 lá. A nhặt 27, B nhặt 19 lá.",
            cards("Tổng 46 lá", "A hơn B 8 lá"),
            [
                (
                    "Hai đội nhặt 46 lá, A hơn B 8 lá. Đội A nhặt bao nhiêu?",
                    "27 lá",
                    ["19 lá", "38 lá"],
                    "(46 + 8) : 2 = 27.",
                ),
                (
                    "Hai đội nhặt 46 lá, A nhặt 27 lá. Đội B nhặt bao nhiêu?",
                    "19 lá",
                    ["21 lá", "23 lá"],
                    "46 − 27 = 19.",
                ),
                (
                    "Cặp số nào có tổng 46 và hiệu 8?",
                    "27 và 19",
                    ["26 và 20", "28 và 18"],
                    "27 + 19 = 46; 27 − 19 = 8.",
                ),
                (
                    "Hai hộp có 30 bút, hộp lớn hơn hộp nhỏ 6 bút. Hộp nhỏ có bao nhiêu?",
                    "12 bút",
                    ["18 bút", "24 bút"],
                    "(30 − 6) : 2 = 12.",
                ),
            ],
        ),
    ],
    5: [
        (
            "ratio",
            "sale-card",
            "Giảm giá trong bài toán",
            "Tính số tiền giảm theo phần trăm, rồi lấy giá ban đầu trừ đi. Đây là dữ liệu giả để học Toán.",
            "Giá mẫu 120 000 đồng, giảm 25%: giảm 30 000 đồng, còn 90 000 đồng.",
            {
                "kind": "pie",
                "labels": ["Giảm", "Còn lại"],
                "values": [25, 75],
                "caption": "Giảm 25% giá ban đầu, còn trả 75%.",
            },
            [
                (
                    "Giá mẫu 120 000 đồng, giảm 25%. Giảm bao nhiêu tiền?",
                    "30 000 đồng",
                    ["25 000 đồng", "90 000 đồng"],
                    "120 000 × 25 : 100 = 30 000.",
                ),
                (
                    "Giá 120 000 đồng, giảm 30 000 đồng. Còn trả bao nhiêu?",
                    "90 000 đồng",
                    ["150 000 đồng", "30 000 đồng"],
                    "120 000 − 30 000 = 90 000.",
                ),
                (
                    "Giảm 25% giá ban đầu thì còn trả bao nhiêu phần trăm?",
                    "75%",
                    ["25%", "125%"],
                    "100% − 25% = 75%.",
                ),
                (
                    "Giá mẫu 80 000 đồng, giảm 10%. Còn trả bao nhiêu?",
                    "72 000 đồng",
                    ["70 000 đồng", "88 000 đồng"],
                    "Giảm 8 000 đồng; 80 000 − 8 000 = 72 000.",
                ),
            ],
        ),
        (
            "solids",
            "box-layers",
            "Xếp hộp theo từng lớp",
            "Đếm số khối mỗi lớp rồi nhân số lớp. Các khối đơn vị xếp sát nhau, không có khe hở.",
            "Hộp dài 4 cm, rộng 3 cm, cao 2 cm: thể tích 4 × 3 × 2 = 24 cm³.",
            {
                "kind": "box",
                "length": 4,
                "width": 3,
                "height": 2,
                "caption": "Hộp chữ nhật kích thước 4 cm × 3 cm × 2 cm.",
            },
            [
                (
                    "Hộp dài 4 cm, rộng 3 cm, cao 2 cm có thể tích bao nhiêu?",
                    "24 cm³",
                    ["12 cm³", "9 cm³"],
                    "4 × 3 × 2 = 24 cm³.",
                ),
                (
                    "Một lớp gồm 4 hàng, mỗi hàng 3 khối đơn vị. Lớp đó có mấy khối?",
                    "12 khối",
                    ["7 khối", "24 khối"],
                    "4 × 3 = 12 khối.",
                ),
                (
                    "Giữ đáy 4 cm × 3 cm, tăng chiều cao từ 2 cm lên 3 cm. Thể tích mới là bao nhiêu?",
                    "36 cm³",
                    ["24 cm³", "27 cm³"],
                    "4 × 3 × 3 = 36 cm³.",
                ),
                (
                    "Hộp 24 cm³, đáy rộng 12 cm². Chiều cao là bao nhiêu?",
                    "2 cm",
                    ["12 cm", "288 cm"],
                    "24 : 12 = 2 cm.",
                ),
            ],
        ),
    ],
}


def content(grade):
    result = []
    for index, (topic, code, title, teaching, example, figure, rows) in enumerate(DATA[grade]):
        result.append(
            unit(
                grade,
                topic,
                code,
                title,
                "Đọc dữ kiện và kiểm tra cách tính.",
                teaching,
                example,
                "Đọc lại số và đơn vị. Thử tính ngược để kiểm tra.",
                [
                    "Tìm số đã biết và điều cần tìm.",
                    example,
                    "Làm từng bước rồi kiểm tra với các dữ kiện.",
                ],
                figure,
                [pick(*row) for row in rows],
                vip=bool(index),
            )
        )
    return result
