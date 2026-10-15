"""Original short poems, messages and model paragraphs with explicit evidence."""

from app.curriculum.supplements.explorers.builders import cards, pick, unit


def content(grade):
    stories = {
        1: "Nắng lên bên cửa\nMèo nhỏ nằm chơi\nBé mang bát nước\nĐặt cạnh mèo thôi.",
        2: "Nam ơi, chiều nay mẹ về muộn. Con cho chậu cây cạnh cửa sổ một ít nước nhé. Tưới xong, con đặt bình vào kệ. Mẹ cảm ơn con!",
        3: "Mưa vừa ghé qua\nVườn thơm mùi đất\nLá xanh như quạt\nChe mầm non biếc.\nBé đứng bên thềm\nNhìn vườn lấp lánh.",
        4: "Kính gửi bác thủ thư,\nCháu cảm ơn bác đã giúp lớp cháu tìm sách về cây cối. Nhờ bác, chúng cháu biết chọn sách theo chủ đề và giữ sách sạch. Cháu mong sẽ sớm quay lại thư viện.\nCháu kính chúc bác mạnh khỏe!\nHọc sinh lớp 4A\nAn",
        5: "Linh trồng một cây nhỏ bên cửa sổ. Linh tưới cây mỗi sáng. Trời nắng nên Linh chuyển cây vào chỗ có bóng mát. Vài ngày sau, Linh thấy một lá non. Linh vui vì cây đang lớn.",
    }
    titles = {
        1: "Bát nước cho mèo",
        2: "Lời nhắn của mẹ",
        3: "Mầm non sau mưa",
        4: "Lá thư cảm ơn thủ thư",
        5: "Sửa đoạn văn lặp từ",
    }
    rows = {
        1: [
            (
                "Con vật nào nằm chơi?",
                "Mèo nhỏ",
                ["Chó nhỏ", "Chim nhỏ"],
                "Dòng thứ hai nói mèo nhỏ nằm chơi.",
            ),
            (
                "Bé mang gì đến?",
                "Bát nước",
                ["Quả bóng", "Cuốn sách"],
                "Dòng thứ ba nói bé mang bát nước.",
            ),
            (
                "Bé đặt bát nước ở đâu?",
                "Cạnh mèo",
                ["Ngoài cổng", "Dưới gốc cây"],
                "Dòng cuối nói đặt cạnh mèo.",
            ),
            (
                "Điều gì xuất hiện bên cửa?",
                "Nắng",
                ["Tuyết", "Cầu vồng"],
                "Dòng đầu là Nắng lên bên cửa.",
            ),
        ],
        2: [
            ("Mẹ nhắn cho ai?", "Nam", ["Bà", "Cô giáo"], "Lời nhắn mở đầu bằng Nam ơi."),
            (
                "Chiều nay mẹ về thế nào?",
                "Về muộn",
                ["Về sớm", "Không về nữa"],
                "Mẹ nói chiều nay mẹ về muộn; không nói sẽ không về.",
            ),
            (
                "Tưới xong, Nam cần làm gì?",
                "Đặt bình vào kệ",
                ["Đổ bình xuống sân", "Đặt cây vào cặp"],
                "Câu Tưới xong... nêu việc đặt bình vào kệ.",
            ),
            (
                "Mẹ dặn tưới chậu cây nào?",
                "Chậu cạnh cửa sổ",
                ["Chậu ngoài cổng", "Chậu sau bếp"],
                "Lời nhắn xác định chậu cây cạnh cửa sổ.",
            ),
        ],
        3: [
            (
                "Vườn thơm mùi gì?",
                "Mùi đất",
                ["Mùi bánh", "Mùi sơn"],
                "Dòng Vườn thơm mùi đất trả lời trực tiếp câu hỏi.",
            ),
            (
                "Lá xanh được so sánh với gì?",
                "Quạt",
                ["Đèn", "Bóng"],
                "Lá xanh như quạt là hình ảnh so sánh trong bài.",
            ),
            (
                "Từ nào giúp nhận ra phép so sánh ‘Lá xanh như quạt’?",
                "Như",
                ["Lên", "Bên"],
                "Như nối lá xanh với quạt để tạo hình ảnh so sánh.",
            ),
            (
                "Bé đứng ở đâu để nhìn vườn?",
                "Bên thềm",
                ["Ngoài cổng", "Trên cầu"],
                "Dòng Bé đứng bên thềm cho biết vị trí của bé.",
            ),
        ],
        4: [
            (
                "Lá thư gửi cho ai?",
                "Bác thủ thư",
                ["Bác lái xe", "Cô bán hàng"],
                "Lời mở đầu xác định người nhận là bác thủ thư.",
            ),
            (
                "Mục đích chính của lá thư là gì?",
                "Cảm ơn người đã giúp tìm sách",
                ["Xin nghỉ học", "Thông báo mất sách"],
                "An viết rõ lời cảm ơn bác đã giúp lớp tìm sách về cây cối.",
            ),
            (
                "Chi tiết nào nêu việc lớp đã học được?",
                "Chọn sách theo chủ đề và giữ sách sạch",
                ["Chọn sách chỉ theo màu", "Gấp góc sách để đánh dấu"],
                "Đây là hai điều được câu Nhờ bác... nêu rõ.",
            ),
            (
                "Lời kết nào có trong lá thư?",
                "Kính chúc bác mạnh khỏe",
                ["Đừng đến thư viện nữa", "Cháu đã làm mất sách"],
                "An kết thư bằng lời kính chúc lịch sự phù hợp với người nhận.",
            ),
        ],
        5: [
            (
                "Đoạn văn lặp nhiều lần từ nào để gọi nhân vật?",
                "Linh",
                ["Bác", "Bạn Nam"],
                "Tên Linh được nhắc lại trong từng câu.",
            ),
            (
                "Giữ ngôi kể như câu đầu, có thể thay ‘Linh’ ở câu thứ hai bằng cách gọi nào?",
                "Bạn ấy",
                ["Tôi", "Chúng tôi"],
                "Bạn ấy thay cho Linh và giữ cách kể về người khác; tôi đổi ngôi kể.",
            ),
            (
                "Vì sao Linh chuyển cây vào chỗ có bóng mát?",
                "Vì trời nắng",
                ["Vì trời có tuyết", "Vì không còn cửa sổ"],
                "Câu có cặp từ trời nắng nên... nêu rõ nguyên nhân.",
            ),
            (
                "Từ ‘nên’ trong ‘Trời nắng nên Linh chuyển cây...’ nối hai ý theo quan hệ nào?",
                "Nguyên nhân và kết quả",
                ["Hai ý trái ngược", "Hai đồ vật giống nhau"],
                "Trời nắng là nguyên nhân; chuyển cây là việc làm do nguyên nhân ấy.",
            ),
        ],
    }
    goal = (
        "Tìm thông tin trong bài thơ hoặc lời nhắn."
        if grade <= 3
        else "Nhận ra cách viết lịch sự và liên kết ý trong đoạn."
    )
    pictures = {
        1: ("Mèo", "Nước uống"),
        2: ("Cây", "Ngôi nhà"),
        3: ("Mưa", "Cây"),
        4: ("Sách", "Trường học"),
        5: ("Cây", "Mặt trời"),
    }
    return unit(
        grade,
        "reading" if grade <= 3 else "writing",
        "words-around-us-r2" if grade == 3 else "words-around-us",
        titles[grade],
        goal,
        stories[grade],
        "Đọc một câu rồi chỉ ra chi tiết giúp em trả lời.",
        "Trả lời theo điều bài đã cho biết; đọc lại khi chưa chắc.",
        [
            "Tìm người, vật hoặc việc được hỏi.",
            "Đọc lại dòng có chi tiết liên quan.",
            "Nói lại bằng lời của em rồi so với các lựa chọn.",
        ],
        cards(*pictures[grade]),
        [pick(*row) for row in rows[grade]],
        vip=grade <= 2,
        context=stories[grade],
    )
