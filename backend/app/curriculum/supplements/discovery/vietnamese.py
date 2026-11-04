"""Original short passages; every answer has evidence in the supplied text."""

from app.curriculum.supplements.discovery import cards, pick, unit

TEXTS = {
    1: [
        (
            "Chiếc lá bên cửa",
            "Bé Na thấy một chiếc lá ở cửa. Bé nhặt lá, bỏ vào giỏ. Sân nhà lại sạch.",
            [
                (
                    "Bé Na thấy gì ở cửa?",
                    "Chiếc lá",
                    ["Quả bóng", "Quyển sách"],
                    "Câu đầu nói bé thấy một chiếc lá.",
                ),
                ("Bé bỏ lá vào đâu?", "Giỏ", ["Cặp", "Bàn"], "Bé nhặt lá và bỏ vào giỏ."),
                ("Ai nhặt chiếc lá?", "Bé Na", ["Bé An", "Bố"], "Đoạn chỉ kể việc bé Na nhặt lá."),
                (
                    "Sau khi nhặt lá, sân nhà thế nào?",
                    "Sạch",
                    ["Bẩn hơn", "Có tuyết"],
                    "Câu cuối: Sân nhà lại sạch.",
                ),
            ],
        ),
        (
            "Chờ bạn cùng đi",
            "Nam đi ra cổng. Thấy An còn buộc dây giày, Nam đứng chờ. Xong rồi, hai bạn cùng đi học.",
            [
                ("Nam ra đâu trước?", "Ra cổng", ["Ra vườn", "Ra ao"], "Câu đầu: Nam đi ra cổng."),
                (
                    "An đang làm gì khi Nam chờ?",
                    "Buộc dây giày",
                    ["Đọc sách", "Vẽ hoa"],
                    "Nam thấy An còn buộc dây giày.",
                ),
                (
                    "Vì sao Nam đứng chờ trong câu chuyện?",
                    "Để cùng An đi học",
                    ["Để đi một mình", "Để hái cam"],
                    "An buộc giày xong thì hai bạn cùng đi học.",
                ),
                (
                    "Cuối bài, ai cùng đi học?",
                    "Nam và An",
                    ["Nam và bố", "An và mẹ"],
                    "Hai bạn được nhắc tới là Nam và An.",
                ),
            ],
        ),
    ],
    2: [
        (
            "Bình nước của Mai",
            "Mai mang bình nước đến lớp. Sau giờ thể dục, bạn uống nước rồi đậy nắp. Cuối buổi, Mai thấy bình của Lan để quên trên bàn. Mai đưa bình cho cô giáo để cô giữ giúp.",
            [
                (
                    "Mai mang gì đến lớp?",
                    "Bình nước",
                    ["Chậu cây", "Chiếc diều"],
                    "Câu đầu giới thiệu bình nước của Mai.",
                ),
                (
                    "Sau khi uống nước, Mai làm gì?",
                    "Đậy nắp",
                    ["Bỏ bình ở sân", "Xé nhãn"],
                    "Đoạn nói bạn uống nước rồi đậy nắp.",
                ),
                (
                    "Bình để quên trên bàn là của ai?",
                    "Lan",
                    ["Mai", "Cô giáo"],
                    "Đó là bình của Lan.",
                ),
                (
                    "Mai đưa bình để quên cho ai?",
                    "Cô giáo",
                    ["Bác lái xe", "Em bé ngoài cổng"],
                    "Mai đưa bình cho cô giáo giữ giúp.",
                ),
            ],
        ),
        (
            "Góc đọc có chỗ trống",
            "Giờ đọc sách, Huy ngồi cạnh cửa sổ. Thấy Linh chưa có chỗ, Huy dịch ghế sang bên và mời bạn ngồi. Linh cảm ơn rồi đặt sách lên bàn. Hai bạn đọc nhỏ để không làm phiền cả lớp.",
            [
                (
                    "Huy ngồi ở đâu?",
                    "Cạnh cửa sổ",
                    ["Ngoài cổng", "Giữa sân"],
                    "Câu đầu cho biết vị trí của Huy.",
                ),
                (
                    "Huy dịch ghế sang bên để làm gì?",
                    "Nhường chỗ cho Linh",
                    ["Chắn lối đi", "Mang ghế về nhà"],
                    "Thấy Linh chưa có chỗ, Huy mời bạn ngồi.",
                ),
                (
                    "Linh nói gì sau khi được mời ngồi?",
                    "Cảm ơn",
                    ["Tạm biệt", "Chúc ngủ ngon"],
                    "Câu thứ ba ghi Linh cảm ơn.",
                ),
                (
                    "Hai bạn đọc nhỏ vì sao?",
                    "Để không làm phiền cả lớp",
                    ["Vì sách bị ướt", "Vì không có bàn"],
                    "Câu cuối nêu rõ lý do hai bạn đọc nhỏ.",
                ),
            ],
        ),
    ],
    3: [
        (
            "Tấm nhãn ở vườn trường",
            "Tổ Ba chăm một luống rau ở vườn trường. Thu viết nhãn ghi ngày gieo và tên rau. Khi tưới, Minh thấy chữ trên nhãn bị nhòe. Bạn chụp lại nhãn cũ, hỏi Thu rồi cùng viết nhãn mới. Hai bạn đặt nhãn ở đầu luống để các tổ khác dễ đọc.",
            [
                (
                    "Nhãn ban đầu ghi những gì?",
                    "Ngày gieo và tên rau",
                    ["Giá tiền và số ghế", "Giờ tan học"],
                    "Câu thứ hai nêu hai thông tin trên nhãn.",
                ),
                (
                    "Ai phát hiện chữ bị nhòe?",
                    "Minh",
                    ["Thu", "Bác bảo vệ"],
                    "Khi tưới, Minh thấy chữ bị nhòe.",
                ),
                (
                    "Trước khi cùng viết nhãn mới, Minh làm gì?",
                    "Chụp nhãn cũ và hỏi Thu",
                    ["Đoán tên rau", "Bỏ luống rau"],
                    "Đoạn kể đúng hai việc này trước khi viết lại.",
                ),
                (
                    "Nhãn mới được đặt ở đâu?",
                    "Đầu luống",
                    ["Trong hộp bút", "Ngoài cổng"],
                    "Câu cuối cho biết vị trí nhãn mới.",
                ),
            ],
        ),
        (
            "Lời mời trong giờ ra chơi",
            "Tú rủ các bạn chơi chuyền bóng. Hà muốn tham gia nhưng chưa biết luật. Tú giải thích một lượt rồi cho cả nhóm thử chậm. Khi Hà lỡ làm rơi bóng, các bạn nhặt lên và bắt đầu lại. Hết giờ, Hà nói mình đã hiểu cách chơi và hẹn cả nhóm vào giờ ra chơi sau.",
            [
                (
                    "Vì sao Tú giải thích luật cho Hà?",
                    "Hà chưa biết luật",
                    ["Hà muốn đổi bóng", "Cả nhóm đã về nhà"],
                    "Đoạn nói Hà muốn tham gia nhưng chưa biết luật.",
                ),
                (
                    "Cả nhóm thử chơi thế nào sau khi nghe giải thích?",
                    "Thử chậm",
                    ["Chơi thật nhanh ngay", "Không cho Hà thử"],
                    "Tú cho cả nhóm thử chậm.",
                ),
                (
                    "Chi tiết nào cho thấy nhóm giúp Hà tiếp tục tham gia?",
                    "Nhặt bóng và bắt đầu lại",
                    ["Giấu bóng", "Bỏ Hà lại"],
                    "Khi Hà làm rơi bóng, các bạn cùng nhặt và chơi lại.",
                ),
                (
                    "Cuối đoạn, Hà hẹn nhóm lúc nào?",
                    "Giờ ra chơi sau",
                    ["Giữa đêm", "Sáng chủ nhật"],
                    "Lời hẹn được nêu ở câu cuối.",
                ),
            ],
        ),
    ],
    4: [
        (
            "Đọc thông báo đổi lịch",
            "Thông báo của lớp 4A: Buổi trao đổi sách chuyển từ chiều thứ Năm sang chiều thứ Sáu vì phòng đọc cần sửa đèn. Mỗi bạn mang tối đa hai quyển sách còn nguyên trang. Trước buổi trao đổi, tổ trưởng ghi tên sách vào danh sách. Những bạn không có sách mang theo vẫn được dự và cùng đọc tại chỗ.",
            [
                (
                    "Buổi trao đổi sách chuyển sang lúc nào?",
                    "Chiều thứ Sáu",
                    ["Chiều thứ Năm", "Sáng thứ Hai"],
                    "Thông báo nêu lịch mới là chiều thứ Sáu.",
                ),
                (
                    "Vì sao lớp đổi lịch?",
                    "Phòng đọc cần sửa đèn",
                    ["Tất cả sách đã mất", "Cô giáo đổi môn học"],
                    "Lý do được ghi ngay sau lịch mới.",
                ),
                (
                    "Mỗi bạn được mang tối đa bao nhiêu quyển?",
                    "Hai quyển",
                    ["Ba quyển", "Không giới hạn"],
                    "Tối đa hai quyển nghĩa là không quá hai.",
                ),
                (
                    "Bạn không mang sách có được dự không?",
                    "Có, được cùng đọc tại chỗ",
                    ["Không được dự", "Phải mang ba quyển"],
                    "Câu cuối nói rõ các bạn vẫn được dự.",
                ),
            ],
        ),
        (
            "Hai ý kiến cho góc xanh",
            "Nhóm của Vy muốn đặt thêm cây ở lớp. Một bạn đề nghị đặt chậu giữa lối đi để ai cũng nhìn thấy. Vy chỉ vào sơ đồ và đề xuất đặt cạnh cửa sổ, chừa lối đi. Cả nhóm đo khoảng trống, hỏi cô giáo rồi chọn phương án của Vy. Trong bản ghi, nhóm ghi cả ý kiến ban đầu và lý do đổi cách đặt.",
            [
                (
                    "Ý kiến ban đầu muốn đặt chậu ở đâu?",
                    "Giữa lối đi",
                    ["Cạnh cửa sổ", "Trên mái nhà"],
                    "Đây là đề nghị của một bạn trước khi Vy góp ý.",
                ),
                (
                    "Phương án của Vy chú ý điều gì?",
                    "Chừa lối đi",
                    ["Che kín cửa", "Chặn cửa lớp"],
                    "Vy đề xuất cạnh cửa sổ và chừa lối đi.",
                ),
                (
                    "Trước khi quyết định, nhóm đã làm gì?",
                    "Đo khoảng trống và hỏi cô",
                    ["Chỉ bốc thăm", "Bỏ qua mọi ý kiến"],
                    "Hai việc được nêu trước khi nhóm chọn phương án.",
                ),
                (
                    "Vì sao bản ghi giúp hiểu quyết định của nhóm?",
                    "Có ý kiến ban đầu và lý do thay đổi",
                    ["Chỉ có tên Vy", "Không ghi lý do"],
                    "Câu cuối cho thấy bản ghi giữ quá trình cân nhắc.",
                ),
            ],
        ),
    ],
    5: [
        (
            "Đọc bản tin có ngày tháng",
            "Bản tin ngày 3 tháng 10 của trường cho biết thư viện nhận 60 quyển sách mới. Trong đó có 20 quyển truyện, còn lại là sách tìm hiểu khoa học. Bản tin nhắc học sinh xem lịch mượn riêng của từng lớp. Khi kể lại với bạn, Quân nói rõ ngày của bản tin và không gọi số sách mới nhận là tổng số sách của cả thư viện.",
            [
                (
                    "Số 60 trong bản tin chỉ điều gì?",
                    "Số sách mới nhận",
                    ["Toàn bộ sách thư viện", "Số lớp của trường"],
                    "Câu đầu nêu thư viện nhận 60 quyển mới.",
                ),
                (
                    "Có bao nhiêu sách tìm hiểu khoa học mới nhận?",
                    "40 quyển",
                    ["20 quyển", "80 quyển"],
                    "60 − 20 = 40 quyển.",
                ),
                (
                    "Muốn biết lớp mình mượn lúc nào, học sinh cần xem gì?",
                    "Lịch mượn riêng của lớp",
                    ["Số cây trong sân", "Lịch của một trường khác"],
                    "Bản tin nhắc xem lịch mượn từng lớp.",
                ),
                (
                    "Khi kể lại, Quân đã làm rõ thông tin nào?",
                    "Ngày bản tin và ý nghĩa số sách mới",
                    ["Mọi lớp có cùng lịch", "Thư viện chỉ có 60 quyển"],
                    "Câu cuối nêu cách Quân kể lại cẩn thận.",
                ),
            ],
        ),
        (
            "Một đề xuất có căn cứ",
            "Lớp 5B khảo sát cách giữ góc đọc yên tĩnh. Trong 24 phiếu của lớp, 18 phiếu đề nghị có bảng nhắc nói nhỏ, 6 phiếu đề nghị đổi giờ đọc. Nhóm báo cáo viết: Phần lớn phiếu của lớp chọn bảng nhắc. Nhóm chưa kết luận học sinh cả trường đều chọn cách này. Các bạn đề nghị thử bảng trong một tuần rồi ghi nhận thêm ý kiến.",
            [
                (
                    "Lớp 5B thu được bao nhiêu phiếu?",
                    "24 phiếu",
                    ["18 phiếu", "6 phiếu"],
                    "Đoạn nêu rõ khảo sát có 24 phiếu của lớp.",
                ),
                (
                    "18 trong 24 phiếu chọn bảng nhắc. Kết luận nào có căn cứ?",
                    "Phần lớn phiếu của lớp chọn bảng nhắc",
                    ["Cả trường đều chọn bảng", "Không ai muốn bảng"],
                    "18 lớn hơn một nửa 24, nhưng chỉ là phiếu của lớp.",
                ),
                (
                    "Vì sao chưa thể kết luận cho cả trường?",
                    "Khảo sát mới lấy phiếu của lớp 5B",
                    ["Vì 24 bằng 0", "Vì không có phiếu nào"],
                    "Phạm vi dữ liệu chỉ là lớp 5B.",
                ),
                (
                    "Nhóm đề nghị làm gì tiếp theo?",
                    "Thử một tuần và nhận thêm ý kiến",
                    ["Giữ mãi mà không xem lại", "Vứt hết các phiếu"],
                    "Đề nghị nằm ở câu cuối của đoạn.",
                ),
            ],
        ),
    ],
}


def content(grade):
    rows = []
    for index, (title, passage, questions) in enumerate(TEXTS[grade]):
        pictures = {
            1: [("Chiếc lá",), ("Chiếc giày",)],
            2: [("Bình nước",), ("Sách", "Ghế")],
            3: [("Cây",), ("Bóng",)],
            4: [("Sách",), ("Cây",)],
            5: [("Sách",), ("Sách",)],
        }[grade][index]
        rows.append(
            unit(
                grade,
                "reading",
                f"read-{index + 1}",
                title,
                "Đọc, tìm chi tiết và nói điều có căn cứ.",
                "Đọc từng câu. Chạm đáp án rồi tìm lại câu giúp em chọn.",
                passage,
                "Điều bài chưa nói thì chưa đoán chắc.",
                [
                    "Tìm tên người, vật hoặc việc được hỏi.",
                    "Đọc lại câu có chi tiết đó.",
                    "So từng đáp án với đoạn đọc; chọn ý được đoạn đọc ủng hộ.",
                ],
                cards(*pictures),
                [pick(*q) for q in questions],
                vip=bool(index),
                context=passage,
            )
        )
    return rows
