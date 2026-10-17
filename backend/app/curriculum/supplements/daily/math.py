"""Clocks and duration; numerical assumptions are included in each problem."""

from app.curriculum.supplements.daily.builders import pick, unit


def content(grade):
    if grade == 1:
        title, topic = "Bảy giờ sáng rồi!", "time"
        teaching = "Giờ đúng: kim dài chỉ số 12. Kim ngắn chỉ số giờ."
        example = "7 giờ sáng: kim ngắn chỉ 7, kim dài chỉ 12."
        remember = "Nhìn kim ngắn để đọc giờ; xem thêm đó là buổi nào."
        figure = {
            "kind": "clock",
            "hour": 7,
            "minute": 0,
            "caption": "7 giờ sáng: kim ngắn chỉ 7, kim dài chỉ 12.",
        }
        rows = [
            (
                "Lúc 7 giờ đúng, kim dài chỉ số mấy?",
                "12",
                ["7", "6"],
                "Vào giờ đúng, kim dài chỉ số 12.",
            ),
            ("Lúc 7 giờ đúng, kim ngắn chỉ số mấy?", "7", ["12", "6"], "Kim ngắn chỉ số giờ là 7."),
            (
                "Trong cùng buổi sáng, 6 giờ và 8 giờ, giờ nào đến trước?",
                "6 giờ",
                ["8 giờ", "Cùng lúc"],
                "Trong buổi sáng, 6 giờ đến trước 8 giờ.",
            ),
            (
                "Đồng hồ chỉ 8 giờ sáng. Đó là buổi nào?",
                "Buổi sáng",
                ["Buổi tối", "Buổi chiều"],
                "Đề đã cho biết là 8 giờ sáng.",
            ),
        ]
    elif grade == 2:
        title, topic = "Nửa giờ trên đồng hồ", "time"
        teaching = "Một giờ có 60 phút. Nửa giờ là 30 phút, kim dài chỉ số 6."
        example = "7 giờ 30 phút: kim dài chỉ 6, kim ngắn ở giữa 7 và 8."
        remember = "Đọc số giờ trước, số phút sau."
        figure = {
            "kind": "clock",
            "hour": 7,
            "minute": 30,
            "caption": "7 giờ 30 phút, kim ngắn ở giữa 7 và 8.",
        }
        rows = [
            (
                "Đồng hồ điện tử ghi 07:30. Đọc thế nào?",
                "7 giờ 30 phút",
                ["7 giờ 15 phút", "8 giờ 30 phút"],
                "07 là giờ, 30 là phút.",
            ),
            (
                "Nửa giờ là bao nhiêu phút?",
                "30 phút",
                ["15 phút", "60 phút"],
                "Một giờ 60 phút; một nửa là 30 phút.",
            ),
            (
                "7 giờ 15 phút, sau thêm 15 phút là mấy giờ?",
                "7 giờ 30 phút",
                ["7 giờ đúng", "8 giờ 15 phút"],
                "15 + 15 = 30 phút, vẫn trong giờ 7.",
            ),
            (
                "Lúc 7 giờ 30 phút, kim dài chỉ số nào?",
                "6",
                ["7", "12"],
                "30 phút ứng với vị trí số 6 của kim dài.",
            ),
        ]
    elif grade == 3:
        title, topic = "Đọc sách trong bao lâu?", "measurement"
        teaching = "Tính khoảng thời gian bằng cách đếm số phút từ lúc bắt đầu đến lúc kết thúc."
        example = "Đọc từ 8 giờ 10 đến 8 giờ 35: 35 − 10 = 25 phút."
        remember = "Qua giờ mới, đếm tới phút 60 rồi đếm tiếp."
        figure = {
            "kind": "clock",
            "hour": 8,
            "minute": 10,
            "caption": "Bắt đầu đọc lúc 8 giờ 10 phút.",
        }
        rows = [
            (
                "Đọc từ 8 giờ 10 đến 8 giờ 35 cùng sáng. Đọc bao lâu?",
                "25 phút",
                ["45 phút", "35 phút"],
                "Cùng giờ 8: 35 − 10 = 25 phút.",
            ),
            (
                "Bắt đầu lúc 9 giờ 20, đọc 15 phút. Kết thúc lúc nào?",
                "9 giờ 35 phút",
                ["9 giờ 5 phút", "10 giờ 20 phút"],
                "20 + 15 = 35, nên kết thúc lúc 9 giờ 35.",
            ),
            (
                "Từ 7 giờ 45, sau 20 phút là mấy giờ?",
                "8 giờ 5 phút",
                ["7 giờ 65 phút", "8 giờ 20 phút"],
                "15 phút tới 8 giờ, còn 5 phút: 8 giờ 5 phút.",
            ),
            (
                "Từ 8 giờ đến 9 giờ cùng sáng có bao nhiêu phút?",
                "60 phút",
                ["30 phút", "100 phút"],
                "Khoảng này là một giờ, bằng 60 phút.",
            ),
        ]
    elif grade == 4:
        title, topic = "Xếp lịch học và nghỉ", "measurement"
        teaching = "Cộng thời gian từng hoạt động. Nhớ tính cả thời gian nghỉ."
        example = "Bắt đầu 14 giờ: đọc 15 phút, nghỉ 5 phút, làm Toán 20 phút. Tổng 40 phút, xong lúc 14 giờ 40."
        remember = "Kiểm tra tổng các phần có bằng thời gian đã dùng không."
        figure = {
            "kind": "clock",
            "hour": 14,
            "minute": 0,
            "caption": "14 giờ là lúc bắt đầu; sau ba hoạt động là 14 giờ 40.",
        }
        rows = [
            (
                "Đọc 15 phút, nghỉ 5 phút, làm Toán 20 phút. Dùng tất cả bao nhiêu phút?",
                "40 phút",
                ["35 phút", "45 phút"],
                "15 + 5 + 20 = 40 phút, đã tính cả lúc nghỉ.",
            ),
            (
                "Bắt đầu đọc lúc 14 giờ, đọc 15 phút. Đọc xong lúc nào?",
                "14 giờ 15 phút",
                ["14 giờ 5 phút", "15 giờ"],
                "14 giờ thêm 15 phút là 14 giờ 15.",
            ),
            (
                "Đọc xong 14 giờ 15, nghỉ 5 phút rồi làm Toán. Bắt đầu Toán lúc nào?",
                "14 giờ 20 phút",
                ["14 giờ 10 phút", "14 giờ 40 phút"],
                "15 + 5 = 20 phút: bắt đầu lúc 14 giờ 20.",
            ),
            (
                "Có 45 phút, ba hoạt động dùng 40 phút. Còn mấy phút?",
                "5 phút",
                ["10 phút", "85 phút"],
                "45 − 40 = 5 phút.",
            ),
        ]
    else:
        title, topic = "Chuyến đi trong bài toán", "motion"
        teaching = (
            "Quãng đường bằng vận tốc nhân thời gian. Đổi thời gian về cùng đơn vị với vận tốc."
        )
        example = "Trong bài toán, xe đi đều 12 km/giờ, không nghỉ. 30 phút = 0,5 giờ; đi được 12 × 0,5 = 6 km."
        remember = "Vận tốc km/giờ thì thời gian cần tính bằng giờ."
        figure = {
            "kind": "bars",
            "labels": ["30 phút", "1 giờ", "1,5 giờ"],
            "values": [6, 12, 18],
            "caption": "Xe đi đều 12 km/giờ, không nghỉ: quãng đường theo km.",
        }
        rows = [
            (
                "Xe đi đều 12 km/giờ, không nghỉ trong 30 phút. Đi bao nhiêu km?",
                "6 km",
                ["24 km", "360 km"],
                "30 phút = 0,5 giờ; 12 × 0,5 = 6 km.",
            ),
            (
                "Xe đi đều 12 km/giờ, không nghỉ trong 1,5 giờ. Đi bao nhiêu km?",
                "18 km",
                ["8 km", "13,5 km"],
                "12 × 1,5 = 18 km.",
            ),
            (
                "Khởi hành 7 giờ 15, đi hết 30 phút. Đến lúc nào cùng sáng?",
                "7 giờ 45 phút",
                ["8 giờ 15 phút", "7 giờ 30 phút"],
                "15 + 30 = 45 phút, nên đến lúc 7 giờ 45.",
            ),
            (
                "Đi đều 12 km/giờ, không nghỉ. Đi 6 km mất bao lâu?",
                "30 phút",
                ["2 giờ", "6 phút"],
                "6 : 12 = 0,5 giờ = 30 phút.",
            ),
        ]
    return unit(
        grade,
        topic,
        "time-in-my-day",
        title,
        "Đọc thời gian và giải thích cách kiểm tra.",
        teaching,
        example,
        remember,
        ["Tìm giờ bắt đầu, số phút hoặc quãng đường được hỏi.", remember, example],
        figure,
        [pick(*row) for row in rows],
    )
