"""Measure, reason and check; early-primary questions require no typing."""

from app.curriculum.builders import blank
from app.curriculum.supplements.explorers.builders import cards, pick, unit


def content(grade):
    if grade == 1:
        return unit(
            grade,
            "measurement",
            "little-ruler",
            "Thước kẻ tí hon",
            "So sánh hai độ dài đo bằng cm.",
            "Đặt đầu thước ở vạch 0. Đọc vạch ở đầu kia của vật.",
            "Bút chì từ vạch 0 đến vạch 8 dài 8 cm.",
            "So hai độ dài cùng đơn vị: số lớn hơn chỉ vật dài hơn.",
            [
                "Tìm số ghi cùng đơn vị cm.",
                "Đọc vạch bắt đầu và vạch kết thúc.",
                "Đặt hai vật chung một đầu để thử so sánh.",
            ],
            cards("Thước kẻ", "Bút chì"),
            [
                pick(
                    "Bút từ vạch 0 đến vạch 8 trên thước cm. Bút dài bao nhiêu?",
                    "8 cm",
                    ["0 cm", "9 cm"],
                    "Bắt đầu ở 0, kết thúc ở 8 nên dài 8 cm.",
                ),
                pick(
                    "Dây đỏ dài 9 cm, dây xanh dài 6 cm. Dây nào dài hơn?",
                    "Dây đỏ",
                    ["Dây xanh", "Dài bằng nhau"],
                    "9 lớn hơn 6, nên dây đỏ dài hơn.",
                ),
                pick(
                    "Một que dài 5 cm, một que dài 7 cm. Que ngắn hơn dài bao nhiêu?",
                    "5 cm",
                    ["7 cm", "12 cm"],
                    "5 nhỏ hơn 7 nên que ngắn hơn dài 5 cm.",
                ),
                pick(
                    "Hai dải giấy đều dài 6 cm. Hai dải thế nào?",
                    "Dài bằng nhau",
                    ["Dải đầu luôn dài hơn", "Dải sau luôn dài hơn"],
                    "Cùng dài 6 cm nên hai dải dài bằng nhau.",
                ),
            ],
        )
    if grade == 2:
        return unit(
            grade,
            "measurement",
            "ribbon-metre",
            "Một mét ruy băng",
            "Đổi 1 m sang cm và tính độ dài còn lại.",
            "Một mét bằng 100 cm. Đo và tính khi các độ dài cùng đơn vị.",
            "Dây dài 1 m, cắt 20 cm: còn 100 − 20 = 80 cm.",
            "Đổi về cm trước khi cộng hoặc trừ.",
            [
                "Nhớ 1 m = 100 cm.",
                "Đổi độ dài đang ghi bằng m sang cm.",
                "Cộng phần đã cắt và phần còn lại để kiểm tra.",
            ],
            cards("Thước kẻ", "Bút chì"),
            [
                pick(
                    "1 m bằng bao nhiêu cm?",
                    "100 cm",
                    ["10 cm", "1 cm"],
                    "Theo đơn vị đo độ dài, 1 m = 100 cm.",
                ),
                pick(
                    "Dây dài 1 m, cắt 30 cm. Còn bao nhiêu cm?",
                    "70 cm",
                    ["30 cm", "130 cm"],
                    "Đổi 1 m = 100 cm; 100 − 30 = 70 cm.",
                ),
                pick(
                    "Ghép dải dài 40 cm với dải dài 50 cm, không chồng lên nhau. Dài tất cả bao nhiêu?",
                    "90 cm",
                    ["10 cm", "100 cm"],
                    "40 + 50 = 90 cm.",
                ),
                pick(
                    "Có dây dài 80 cm. Cần thêm bao nhiêu cm để đủ 1 m?",
                    "20 cm",
                    ["80 cm", "30 cm"],
                    "1 m = 100 cm; 100 − 80 = 20 cm.",
                ),
            ],
        )
    if grade == 3:
        return unit(
            grade,
            "geometry",
            "paper-frame",
            "Khung giấy có khe hở",
            "Phân biệt chu vi, diện tích và độ dài phần viền.",
            "Mảnh bìa hình chữ nhật dài 12 cm, rộng 8 cm. Chu vi là đường bao; diện tích là phần bìa bên trong.",
            "Chu vi = (12 + 8) × 2 = 40 cm. Chừa khe hở 2 cm thì cần 38 cm dây viền.",
            "Tính chu vi trước, rồi trừ phần khe hở không dán viền.",
            [
                "Cộng chiều dài với chiều rộng.",
                "Chu vi có hai cạnh dài và hai cạnh rộng.",
                "Kiểm tra đơn vị: dây viền tính bằng cm, diện tích tính bằng cm².",
            ],
            cards("Hình chữ nhật", "Thước kẻ"),
            [
                pick(
                    "Mảnh bìa chữ nhật dài 12 cm, rộng 8 cm. Chu vi bao nhiêu?",
                    "40 cm",
                    ["20 cm", "96 cm"],
                    "(12 + 8) × 2 = 40 cm.",
                ),
                blank(
                    "Khung có chu vi 40 cm, chừa khe hở dài 2 cm. Cần bao nhiêu cm dây viền? Chỉ điền số.",
                    ["38"],
                    "40 − 2 = 38 cm dây viền.",
                ),
                pick(
                    "Mảnh bìa chữ nhật dài 12 cm, rộng 8 cm. Diện tích bao nhiêu?",
                    "96 cm²",
                    ["40 cm²", "20 cm²"],
                    "12 × 8 = 96 cm²; không nhầm với chu vi 40 cm.",
                ),
                pick(
                    "Khung có chu vi 40 cm, chừa hai khe hở dài 2 cm và 3 cm. Cần bao nhiêu cm dây viền?",
                    "35 cm",
                    ["38 cm", "45 cm"],
                    "Hai khe dài tổng cộng 2 + 3 = 5 cm; 40 − 5 = 35 cm dây viền.",
                ),
            ],
            vip=True,
        )
    if grade == 4:
        return unit(
            grade,
            "statistics",
            "reading-average",
            "Mục tiêu đọc sách của tổ",
            "Tìm trung bình cộng và số còn thiếu trong bảng.",
            "Ba ngày, tổ đọc được 8, 12 và 10 trang. Muốn tìm trung bình, cộng số trang rồi chia số ngày.",
            "(8 + 12 + 10) : 3 = 10 trang mỗi ngày.",
            "Trung bình không nhất thiết là số đã đọc trong mọi ngày.",
            [
                "Cộng số trang của các ngày đã biết.",
                "Tổng = trung bình × số ngày.",
                "Lấy tổng cần có trừ tổng đã biết để tìm ngày còn thiếu.",
            ],
            {
                "kind": "bars",
                "labels": ["Thứ Hai", "Thứ Ba", "Thứ Tư"],
                "values": [8, 12, 10],
                "tick": 2,
                "caption": "Số trang tổ đọc: thứ Hai 8, thứ Ba 12, thứ Tư 10.",
            },
            [
                pick(
                    "Tổ đọc 8, 12 và 10 trang trong ba ngày. Tổng là bao nhiêu?",
                    "30 trang",
                    ["10 trang", "20 trang"],
                    "8 + 12 + 10 = 30 trang.",
                ),
                blank(
                    "Ba ngày đọc 8, 12 và 10 trang. Trung bình mỗi ngày bao nhiêu trang? Chỉ điền số.",
                    ["10"],
                    "(8 + 12 + 10) : 3 = 10 trang.",
                ),
                pick(
                    "Ba ngày đọc tổng 30 trang. Muốn trung bình 4 ngày là 12 trang, ngày thứ tư cần đọc bao nhiêu?",
                    "18 trang",
                    ["12 trang", "48 trang"],
                    "Bốn ngày cần 12 × 4 = 48 trang; ngày còn lại cần 48 − 30 = 18 trang.",
                ),
                pick(
                    "Trung bình ba ngày là 10 trang. Có chắc ngày nào cũng đọc đúng 10 trang không?",
                    "Không; các ngày có thể khác nhau",
                    ["Có; ngày nào cũng đúng 10 trang", "Có; cả ba ngày chỉ đọc 10 trang"],
                    "8, 12, 10 có trung bình là 10 dù số trang mỗi ngày không giống nhau.",
                ),
            ],
            vip=True,
        )
    return unit(
        grade,
        "solids",
        "gift-box",
        "Hộp quà và khối lập phương",
        "Tính thể tích hộp chữ nhật và giải thích khi đổi kích thước.",
        "Hộp hình hộp chữ nhật có kích thước trong lòng dài 5 cm, rộng 4 cm, cao 3 cm. Bỏ qua độ dày vỏ hộp.",
        "Thể tích = 5 × 4 × 3 = 60 cm³.",
        "Ba kích thước phải cùng đơn vị trước khi nhân.",
        [
            "Xác định dài, rộng và cao.",
            "Nhân diện tích đáy với chiều cao.",
            "Đổi riêng một kích thước rồi so thể tích mới với thể tích cũ.",
        ],
        {
            "kind": "box",
            "length": 5,
            "width": 4,
            "height": 3,
            "caption": "Hộp chữ nhật dài 5 cm, rộng 4 cm, cao 3 cm; kích thước tính trong lòng hộp.",
        },
        [
            pick(
                "Hộp chữ nhật dài 5 cm, rộng 4 cm, cao 3 cm. Thể tích bao nhiêu?",
                "60 cm³",
                ["12 cm³", "20 cm³"],
                "5 × 4 × 3 = 60 cm³.",
            ),
            blank(
                "Hộp chữ nhật dài 5 cm, rộng 4 cm, cao 6 cm. Thể tích bao nhiêu cm³? Chỉ điền số.",
                ["120"],
                "5 × 4 × 6 = 120 cm³; chiều cao gấp đôi thì thể tích gấp đôi.",
            ),
            pick(
                "Xếp kín hộp 5 cm × 4 cm × 3 cm bằng các khối lập phương cạnh 1 cm, không có khoảng trống. Cần mấy khối?",
                "60 khối",
                ["12 khối", "30 khối"],
                "Mỗi khối chiếm 1 cm³; hộp 60 cm³ cần 60 khối.",
            ),
            pick(
                "Hộp chữ nhật rộng 4 cm, cao 3 cm. Tăng chiều dài từ 5 cm lên 6 cm thì thể tích tăng bao nhiêu?",
                "12 cm³",
                ["1 cm³", "72 cm³"],
                "Thêm một lớp dài 1 cm: thể tích tăng 1 × 4 × 3 = 12 cm³.",
            ),
        ],
        vip=True,
    )
