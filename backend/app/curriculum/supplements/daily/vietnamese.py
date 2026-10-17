from app.curriculum.supplements.daily.builders import cards, pick, unit

TEXTS = {
    1: (
        "Sách đặt lên bàn",
        "Bé An mở cặp. Bé lấy sách, đặt lên bàn. Bé cất cặp vào ngăn bàn.",
        [
            (
                "Trước khi lấy sách, bé An làm gì?",
                "Mở cặp",
                ["Cất cặp", "Đóng sách"],
                "Câu đầu cho biết bé An mở cặp.",
            ),
            ("Bé An lấy gì ra khỏi cặp?", "Sách", ["Cốc", "Bóng"], "Câu thứ hai: bé lấy sách."),
            (
                "Bé đặt sách ở đâu?",
                "Trên bàn",
                ["Ở sân", "Trong hộp"],
                "Bé lấy sách và đặt lên bàn.",
            ),
            (
                "Cuối bài, bé cất cặp vào đâu?",
                "Ngăn bàn",
                ["Sân nhà", "Hộp bút"],
                "Câu cuối: bé cất cặp vào ngăn bàn.",
            ),
        ],
    ),
    2: (
        "Góc bàn gọn gàng",
        "Trước giờ học, My xếp sách thành một chồng. Bạn bỏ bút vào hộp. Sau đó, My lau mặt bàn. Cuối cùng, bạn đặt hộp bút cạnh chồng sách.",
        [
            (
                "Việc đầu tiên My làm trong bài là gì?",
                "Xếp sách thành chồng",
                ["Lau mặt bàn", "Đặt hộp bút"],
                "Câu đầu kể việc My xếp sách.",
            ),
            (
                "Sau khi bỏ bút vào hộp, My làm gì?",
                "Lau mặt bàn",
                ["Mở cặp", "Đi ra sân"],
                "Câu tiếp theo: Sau đó, My lau mặt bàn.",
            ),
            (
                "My đặt hộp bút ở đâu?",
                "Cạnh chồng sách",
                ["Dưới gầm giường", "Ngoài cửa"],
                "Câu cuối cho biết hộp bút ở cạnh chồng sách.",
            ),
            (
                "Từ nào báo hiệu việc sau hết trong bài?",
                "Cuối cùng",
                ["Trước giờ học", "Sau đó"],
                "Cuối cùng đánh dấu việc cuối của chuỗi được kể.",
            ),
        ],
    ),
    3: (
        "Chia việc làm thẻ sách",
        "Nhóm làm thẻ giới thiệu sách. Phương vẽ hình, Đạt viết tên sách, Lan xếp thẻ. Trước khi cắt thẻ, các bạn kẻ khung. Nhóm kiểm tra chữ rồi mới nộp. Nhờ chia việc, ai cũng biết việc của mình.",
        [
            ("Ai viết tên sách?", "Đạt", ["Phương", "Lan"], "Bài nêu rõ: Đạt viết tên sách."),
            (
                "Trước khi cắt thẻ, nhóm làm gì?",
                "Kẻ khung",
                ["Nộp thẻ", "Xếp thẻ vào cặp"],
                "Bài ghi rõ nhóm kẻ khung trước khi cắt.",
            ),
            (
                "Nhóm làm gì ngay trước khi nộp?",
                "Kiểm tra chữ",
                ["Đi ra sân", "Mua sách mới"],
                "Nhóm kiểm tra chữ rồi mới nộp.",
            ),
            (
                "Theo bài, chia việc giúp điều gì?",
                "Ai cũng biết việc của mình",
                ["Không cần kiểm tra chữ", "Không cần làm thẻ"],
                "Lợi ích được nêu ở câu cuối.",
            ),
        ],
    ),
    4: (
        "Đọc kỹ hướng dẫn làm hộp bút",
        "Bảng hướng dẫn ghi: 1. Chuẩn bị một cốc giấy sạch. 2. Dán nhãn lên cốc. 3. Xếp bút vào cốc. Thảo dùng mảnh giấy nhỏ viết tên nhóm để làm nhãn. Cô nhắc: cốc phải khô trước khi xếp bút.",
        [
            (
                "Theo hướng dẫn, bước đầu tiên là gì?",
                "Chuẩn bị cốc giấy sạch",
                ["Xếp bút vào cốc", "Dán nhãn lên cốc"],
                "Đó là việc được đánh số 1.",
            ),
            (
                "Thảo dùng vật gì để làm nhãn?",
                "Mảnh giấy nhỏ",
                ["Chiếc bút chì", "Một quyển sách"],
                "Thảo dùng mảnh giấy nhỏ viết tên nhóm.",
            ),
            (
                "Trước khi xếp bút, cốc cần thế nào?",
                "Sạch và khô",
                ["Đầy nước", "Bị rách"],
                "Bước 1 cần cốc sạch; lời nhắc yêu cầu cốc khô.",
            ),
            (
                "Theo các bước đánh số, sau dán nhãn cần làm gì?",
                "Xếp bút vào cốc",
                ["Chuẩn bị một cốc khác", "Bỏ nhãn đi"],
                "Dán nhãn là bước 2, xếp bút là bước 3.",
            ),
        ],
    ),
    5: (
        "Đọc thông báo trước khi đi",
        "Thông báo tổ đọc sách: Thứ Bảy, từ 14 giờ đến 15 giờ, tại thư viện. Mỗi bạn mang một cuốn sách yêu thích. Nếu trời mưa, buổi đọc vẫn tổ chức bên trong thư viện, giờ không đổi.",
        [
            (
                "Buổi đọc sách diễn ra ngày nào?",
                "Thứ Bảy",
                ["Thứ Sáu", "Chủ nhật"],
                "Ngày được ghi ngay đầu thông báo.",
            ),
            (
                "Buổi đọc dự kiến kéo dài bao lâu?",
                "1 giờ",
                ["2 giờ", "100 phút"],
                "Từ 14 giờ đến 15 giờ là một giờ.",
            ),
            (
                "Mỗi bạn cần mang gì theo thông báo?",
                "Một cuốn sách yêu thích",
                ["Hai bộ đồ chơi", "Một chậu cây"],
                "Thông báo ghi mỗi bạn mang một cuốn sách yêu thích.",
            ),
            (
                "Bạn nói trời mưa thì buổi đọc bị hủy. Chi tiết nào bác bỏ nhận xét đó?",
                "Buổi đọc vẫn tổ chức bên trong thư viện",
                ["Mỗi bạn mang một cuốn sách", "Buổi đọc bắt đầu lúc 14 giờ"],
                "Thông báo nói rõ nếu mưa vẫn tổ chức, giờ không đổi.",
            ),
        ],
    ),
}


def content(grade):
    title, text, rows = TEXTS[grade]
    return unit(
        grade,
        "reading",
        "read-the-steps",
        title,
        "Tìm đúng việc, thứ tự và điều kiện trong văn bản.",
        "Đọc từng câu. Tìm ai làm gì, việc nào trước, việc nào sau.",
        text,
        "Đọc lại chi tiết trong bài trước khi chọn.",
        [
            "Tìm câu chứa người, việc hoặc thời gian được hỏi.",
            "Chú ý: trước, sau đó, cuối cùng, nếu.",
            "Đối chiếu thứ tự và điều kiện, không thêm việc bài chưa kể.",
        ],
        cards("Sách", "Bút chì") if grade != 4 else cards("Cốc", "Bút chì"),
        [pick(*row) for row in rows],
        vip=grade >= 3,
        context=text,
    )
