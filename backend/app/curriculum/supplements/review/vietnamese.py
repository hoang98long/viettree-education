"""Original mini texts with explicit evidence for each answer."""

from app.curriculum.supplements.review.builders import cards, pick, unit

TEXTS = {
    1: (
        "Bút của Hà",
        "Hà có bút đỏ. Bút rơi ở sân. Nam nhặt bút, đưa cho Hà. Hà cảm ơn Nam.",
        [
            ("Hà có bút màu gì?", "Đỏ", ["Xanh", "Vàng"], "Câu đầu: Hà có bút đỏ."),
            ("Bút rơi ở đâu?", "Ở sân", ["Ở nhà", "Ở lớp"], "Câu thứ hai cho biết bút rơi ở sân."),
            ("Ai nhặt bút?", "Nam", ["Hà", "Cô giáo"], "Bài viết: Nam nhặt bút."),
            (
                "Hà nói gì khi nhận lại bút?",
                "Cảm ơn Nam",
                ["Chào mẹ", "Xin lỗi cô"],
                "Câu cuối: Hà cảm ơn Nam.",
            ),
        ],
    ),
    2: (
        "Chiếc cốc dùng lại",
        "Giờ ra chơi, Mai lấy cốc của mình để uống nước. Uống xong, Mai rửa cốc rồi úp lên giá. Mai dùng chiếc cốc ấy mỗi ngày.",
        [
            (
                "Mai uống nước lúc nào?",
                "Giờ ra chơi",
                ["Trước khi ngủ", "Buổi tối"],
                "Thông tin ở đầu bài: giờ ra chơi.",
            ),
            (
                "Uống xong, Mai làm gì trước?",
                "Rửa cốc",
                ["Úp cốc ngay", "Vứt cốc đi"],
                "Mai rửa cốc rồi mới úp lên giá.",
            ),
            ("Mai úp cốc ở đâu?", "Trên giá", ["Dưới sân", "Trong cặp"], "Bài ghi rõ: úp lên giá."),
            (
                "Chi tiết nào cho thấy cốc được dùng lại?",
                "Mai dùng chiếc cốc ấy mỗi ngày",
                ["Giờ ra chơi", "Mai uống nước"],
                "Cụm 'mỗi ngày' cho biết Mai dùng lại chiếc cốc.",
            ),
        ],
    ),
    3: (
        "Giỏ sách lớp em",
        "Lớp 3A đặt một giỏ sách cạnh cửa sổ. Mỗi thứ Sáu, các bạn đổi sách đã đọc. Tuần này, Bình mang truyện về biển. An chọn cuốn ấy và hẹn giữ sách sạch để bạn khác đọc tiếp.",
        [
            (
                "Giỏ sách được đặt ở đâu?",
                "Cạnh cửa sổ",
                ["Ngoài cổng", "Dưới sân"],
                "Câu đầu nêu vị trí giỏ sách.",
            ),
            (
                "Các bạn đổi sách vào ngày nào?",
                "Thứ Sáu",
                ["Thứ Hai", "Chủ nhật"],
                "Câu thứ hai có cụm 'Mỗi thứ Sáu'.",
            ),
            (
                "Bình mang truyện về điều gì?",
                "Biển",
                ["Núi", "Vũ trụ"],
                "Bài viết: Bình mang truyện về biển.",
            ),
            (
                "Vì sao An hẹn giữ sách sạch?",
                "Để bạn khác đọc tiếp",
                ["Để cất sách mãi", "Để đổi lấy đồ chơi"],
                "Mục đích được nêu ở câu cuối.",
            ),
        ],
    ),
    4: (
        "Tấm bảng nhắc tưới cây",
        "Sáng thứ Hai, nhóm Lan thấy đất trong chậu đã khô. Các bạn tưới vừa đủ nước rồi đặt bảng nhắc lịch tưới cạnh chậu. Hôm sau trời mưa, đất vẫn ẩm. Nhóm kiểm tra đất trước và quyết định chưa tưới thêm.",
        [
            (
                "Dấu hiệu nào khiến nhóm tưới cây sáng thứ Hai?",
                "Đất trong chậu đã khô",
                ["Có bảng mới", "Trời đang mưa"],
                "Nhóm quan sát đất khô trước khi tưới.",
            ),
            (
                "Tấm bảng được đặt ở đâu?",
                "Cạnh chậu",
                ["Trên mái", "Ngoài cổng"],
                "Vị trí được nêu ở câu thứ hai.",
            ),
            (
                "Vì sao hôm sau nhóm chưa tưới thêm?",
                "Đất vẫn ẩm sau mưa",
                ["Các bạn quên cây", "Bảng bị mất"],
                "Nhóm kiểm tra và thấy đất vẫn ẩm.",
            ),
            (
                "Nhận xét nào có căn cứ từ bài?",
                "Nhóm quan sát trước khi quyết định tưới",
                ["Nhóm luôn tưới bất kể đất", "Cây không bao giờ cần nước"],
                "Cả hai ngày, nhóm đều dựa vào tình trạng đất.",
            ),
        ],
    ),
    5: (
        "Đọc bảng tin cho đúng",
        "Bảng tin thư viện ghi: 'Tuần này có 40 lượt mượn sách khoa học, tăng 10 lượt so với tuần trước.' Minh cho rằng số học sinh mượn sách khoa học tuần này là 40. Thủ thư giải thích: một học sinh có thể mượn nhiều lần, nên số lượt chưa cho biết số người.",
        [
            (
                "Tuần này có bao nhiêu lượt mượn sách khoa học?",
                "40 lượt",
                ["30 lượt", "50 lượt"],
                "Bảng tin ghi 40 lượt.",
            ),
            (
                "Tuần trước có bao nhiêu lượt mượn sách khoa học?",
                "30 lượt",
                ["40 lượt", "50 lượt"],
                "Tuần này tăng 10 lượt: 40 − 10 = 30.",
            ),
            (
                "Có thể kết luận đúng 40 học sinh đã mượn không?",
                "Không, một người có thể mượn nhiều lần",
                ["Có, lượt luôn bằng người", "Có, vì số 40 lớn"],
                "Thủ thư phân biệt lượt mượn với số người mượn.",
            ),
            (
                "Muốn biết số người mượn, cần thêm gì?",
                "Số người khác nhau đã mượn",
                ["Màu bảng tin", "Số trang sách"],
                "Phải đếm người khác nhau, không cộng tất cả lượt.",
            ),
        ],
    ),
}


def content(grade):
    title, text, rows = TEXTS[grade]
    return unit(
        grade,
        "reading",
        "read-for-evidence",
        title,
        "Tìm chi tiết làm căn cứ cho câu trả lời.",
        "Đọc từng câu ngắn. Tìm từ hoặc câu trả lời đúng điều được hỏi.",
        text,
        "Bài không nói thì em chưa vội đoán thêm.",
        [
            "Tìm tên, nơi chốn hoặc việc được hỏi.",
            "Đọc câu chứa từ khóa và câu bên cạnh.",
            "Đối chiếu lựa chọn với lời trong bài, đừng thêm chi tiết chưa có.",
        ],
        cards("Bút chì", "Sách") if grade in (1, 3, 5) else cards("Cốc", "Cây"),
        [pick(*row) for row in rows],
        context=text,
    )
