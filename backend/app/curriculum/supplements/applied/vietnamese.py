"""Original mini-stories with literal, sequencing and evidence-based questions."""

from app.curriculum.supplements.applied.builders import cards, unit


def content(grade):
    free_contexts = {
        1: "Na có một chậu hoa. Sáng nay, Na tưới nước. Mẹ khen Na chăm chỉ.",
        2: "Giờ ra chơi, Bình thấy một chiếc bút dưới ghế. Bình mang bút đến cô giáo. Cô hỏi cả lớp và trả bút cho Hà. Hà cảm ơn Bình.",
        3: "THƯ VIỆN XANH\nThứ Sáu, từ 8 giờ đến 9 giờ, lớp 3A đọc sách ở sân trường. Mỗi bạn mang một cuốn sách yêu thích. Nếu trời mưa, cả lớp đọc ở phòng học. Đọc xong, các bạn đổi sách cho nhau khi đã được chủ sách đồng ý.",
        4: "Lớp 4B làm một góc đổi sách. Ban đầu, sách chỉ được xếp theo màu bìa nên các bạn khó tìm truyện. Mai đề nghị gắn nhãn: truyện, thơ, khoa học. Cả lớp thử cách ấy. Một tuần sau, các bạn tìm sách nhanh hơn. Mai nói: ‘Mình sẽ hỏi thêm ý kiến để góc sách ngày càng dễ dùng.’",
        5: "Nhóm của Linh muốn giảm giấy bỏ phí. Trong một tuần, nhóm đặt khay giấy mới và khay giấy đã dùng một mặt. Các bạn dùng giấy một mặt để nháp, nhưng vẫn dùng giấy mới khi cần nộp bài sạch đẹp. Cuối tuần, nhóm ghi nhận số tờ giấy mới đã dùng ít hơn tuần trước. Linh đề nghị tiếp tục theo dõi vì số bài học mỗi tuần có thể khác nhau.",
    }
    vip_contexts = {
        1: "Mẹ dặn: ‘Con cất bút vào hộp, rồi đặt hộp lên bàn.’ An làm đúng lời mẹ.",
        2: "Minh mượn truyện của Lan, hẹn thứ Sáu trả. Thứ Năm, Minh đọc xong. Minh cất truyện vào cặp để mai mang trả. Lan vui vì Minh giữ lời.",
        3: "Trước khi trồng hạt, cô dặn: ‘Mỗi cốc cho hai hạt, ghi tên cây rồi tưới ít nước.’ Nam cho hạt vào cốc nhưng quên ghi tên. Lan chưa tưới, đã nhắc Nam làm nốt bước còn thiếu. Hai bạn sửa xong rồi mới tưới.",
        4: "Huy đề nghị: ‘Lớp mình nên có mười phút đọc sách đầu giờ. Mỗi bạn có thể chọn sách mình thích.’ An hỏi: ‘Nếu bạn quên sách thì sao?’ Huy đáp: ‘Góc sách chung có thể cho bạn mượn.’ Cô giáo đề nghị lớp thử trong một tuần rồi trao đổi kết quả, thay vì kết luận ngay rằng mọi bạn đều thích cách này.",
        5: "Một áp phích viết: ‘Uống nước trong chai X giúp mọi bạn học giỏi ngay!’ Bên dưới chỉ có hình một học sinh cầm chai nước, không có thông tin kiểm chứng. Vy nhận xét rằng hình ảnh ấy cho thấy một bạn đang cầm chai, chưa chứng minh việc học giỏi là do loại nước đó. Nhóm quyết định hỏi người lớn và tìm nguồn đáng tin cậy, không chia sẻ lời quảng cáo như một sự thật đã được xác nhận.",
    }
    free_rows = {
        1: [
            ("Ai có chậu hoa?", "Na", ["Mẹ", "Cô giáo"], "Câu đầu cho biết: Na có một chậu hoa."),
            (
                "Na làm gì vào sáng nay?",
                "Tưới nước",
                ["Đá bóng", "Đọc sách"],
                "Bài đọc nói: Sáng nay, Na tưới nước.",
            ),
            ("Ai khen Na?", "Mẹ", ["Bạn Nam", "Cô giáo"], "Câu cuối nói mẹ khen Na."),
            (
                "Mẹ khen Na thế nào?",
                "Chăm chỉ",
                ["Vội vàng", "Buồn ngủ"],
                "Từ chăm chỉ xuất hiện trong lời khen của mẹ.",
            ),
        ],
        2: [
            (
                "Bình thấy chiếc bút ở đâu?",
                "Dưới ghế",
                ["Trên bàn", "Trong cặp"],
                "Câu đầu nêu rõ chiếc bút ở dưới ghế.",
            ),
            (
                "Bình mang bút đến cho ai?",
                "Cô giáo",
                ["Người bán hàng", "Bác bảo vệ"],
                "Bình nhờ cô giáo tìm chủ của chiếc bút.",
            ),
            ("Chiếc bút được trả cho ai?", "Hà", ["Bình", "Lan"], "Bài đọc nói cô trả bút cho Hà."),
            (
                "Hà nói lời nào phù hợp với việc Bình đã làm?",
                "Cảm ơn bạn!",
                ["Tạm biệt chiếc ghế!", "Chúc mừng sinh nhật!"],
                "Lời cảm ơn phù hợp khi nhận lại đồ vật nhờ bạn giúp.",
            ),
        ],
        3: [
            (
                "Lớp 3A đọc sách vào ngày nào?",
                "Thứ Sáu",
                ["Thứ Hai", "Chủ nhật"],
                "Dòng thời gian của thông báo ghi thứ Sáu.",
            ),
            (
                "Nếu trời mưa, lớp đọc sách ở đâu?",
                "Phòng học",
                ["Sân trường", "Nhà của Mai"],
                "Thông báo nêu phương án trời mưa là đọc ở phòng học.",
            ),
            (
                "Mỗi bạn cần mang gì?",
                "Một cuốn sách yêu thích",
                ["Một quả bóng", "Một chậu cây"],
                "Đây là vật được yêu cầu trực tiếp trong thông báo.",
            ),
            (
                "Khi muốn đổi sách, em cần làm gì?",
                "Xin chủ sách đồng ý",
                ["Tự lấy sách của bạn", "Giấu sách vào cặp"],
                "Thông báo yêu cầu chủ sách đồng ý trước khi đổi.",
            ),
        ],
        4: [
            (
                "Ban đầu, lớp xếp sách theo cách nào?",
                "Theo màu bìa",
                ["Theo tên tác giả", "Theo số trang"],
                "Câu thứ hai nêu cách xếp ban đầu.",
            ),
            (
                "Mai đề nghị thay đổi điều gì?",
                "Gắn nhãn theo loại sách",
                ["Bỏ hết sách khoa học", "Chỉ giữ sách bìa xanh"],
                "Mai đề nghị các nhãn truyện, thơ, khoa học.",
            ),
            (
                "Chi tiết nào cho thấy cách mới có ích?",
                "Các bạn tìm sách nhanh hơn",
                ["Sách có nhiều màu bìa", "Mai đứng cạnh góc sách"],
                "Tìm sách nhanh hơn là kết quả được quan sát sau khi thay đổi.",
            ),
            (
                "Vì sao Mai muốn hỏi thêm ý kiến?",
                "Để góc sách dễ dùng hơn",
                ["Để ngừng cho mượn sách", "Để đổi tên cả lớp"],
                "Lời cuối của Mai nói rõ mục đích cải thiện góc sách.",
            ),
        ],
        5: [
            (
                "Nhóm dùng giấy đã viết một mặt vào việc gì?",
                "Làm giấy nháp",
                ["Thay tất cả bài nộp", "Bỏ ngay vào thùng rác"],
                "Bài đọc nêu rõ dùng giấy một mặt để nháp.",
            ),
            (
                "Khi nào nhóm vẫn dùng giấy mới?",
                "Khi cần nộp bài sạch đẹp",
                ["Mọi lúc, kể cả nháp", "Không bao giờ"],
                "Nhóm chọn loại giấy phù hợp với từng việc.",
            ),
            (
                "Kết quả nào thực sự được bài đọc nêu?",
                "Dùng ít tờ giấy mới hơn tuần trước",
                ["Không còn dùng giấy mới", "Mọi lớp đều đã tiết kiệm như nhau"],
                "Chỉ số được ghi nhận là số tờ giấy mới của nhóm so với tuần trước.",
            ),
            (
                "Vì sao Linh muốn theo dõi thêm?",
                "Số bài học mỗi tuần có thể khác",
                ["Vì không cần ghi số liệu", "Vì giấy nháp luôn vô dụng"],
                "Theo dõi thêm giúp xem kết quả qua các tuần có lượng bài học khác nhau.",
            ),
        ],
    }
    vip_rows = {
        1: [
            ("An cần cất gì vào hộp?", "Bút", ["Bàn", "Ghế"], "Mẹ dặn cất bút vào hộp."),
            (
                "An cất bút vào đâu?",
                "Vào hộp",
                ["Dưới ghế", "Ngoài sân"],
                "Lời mẹ nêu rõ vị trí là vào hộp.",
            ),
            (
                "An làm việc nào trước?",
                "Cất bút vào hộp",
                ["Đặt hộp lên bàn", "Mang hộp ra sân"],
                "Từ rồi cho biết đặt hộp lên bàn là việc làm sau.",
            ),
            (
                "Sau khi cất bút, An làm gì?",
                "Đặt hộp lên bàn",
                ["Lấy bút ra sân", "Đặt bàn vào hộp"],
                "Đây là bước thứ hai trong lời mẹ dặn.",
            ),
            (
                "Hộp được đặt ở đâu?",
                "Trên bàn",
                ["Dưới bàn", "Trên ghế"],
                "Mẹ dặn đặt hộp lên bàn.",
            ),
            (
                "Câu nào đúng lời mẹ dặn?",
                "Cất bút rồi đặt hộp lên bàn",
                ["Đặt bút dưới bàn", "Cất bàn vào hộp"],
                "Câu đúng giữ cả hai việc và đúng thứ tự.",
            ),
        ],
        2: [
            (
                "Minh mượn truyện của ai?",
                "Lan",
                ["Cô giáo", "Bình"],
                "Câu đầu cho biết chủ cuốn truyện là Lan.",
            ),
            (
                "Minh hẹn trả truyện vào ngày nào?",
                "Thứ Sáu",
                ["Thứ Tư", "Chủ nhật"],
                "Ngày hẹn trả được ghi rõ là thứ Sáu.",
            ),
            (
                "Minh đọc xong vào ngày nào?",
                "Thứ Năm",
                ["Thứ Hai", "Thứ Bảy"],
                "Câu thứ hai cho biết Minh đọc xong vào thứ Năm.",
            ),
            (
                "Trong câu ‘để mai mang trả’, mai là ngày nào?",
                "Thứ Sáu",
                ["Thứ Tư", "Thứ Năm"],
                "Minh cất truyện vào thứ Năm; ngày mai là thứ Sáu.",
            ),
            (
                "Vì sao Minh cất truyện vào cặp?",
                "Để hôm sau mang trả",
                ["Để giấu không trả", "Để mang đi bán"],
                "Bài đọc nói rõ mục đích là mai mang trả.",
            ),
            (
                "Việc nào giúp Minh giữ lời hẹn?",
                "Mang trả truyện vào thứ Sáu",
                ["Giữ truyện đến tháng sau", "Làm mất truyện"],
                "Trả vào đúng ngày đã hẹn là giữ lời.",
            ),
        ],
        3: [
            (
                "Mỗi cốc cần bao nhiêu hạt?",
                "Hai hạt",
                ["Một hạt", "Bốn hạt"],
                "Lời cô dặn nêu rõ mỗi cốc cho hai hạt.",
            ),
            (
                "Nam quên bước nào?",
                "Ghi tên cây",
                ["Cho hạt vào cốc", "Lấy cốc"],
                "Bài đọc nói Nam đã cho hạt nhưng quên ghi tên.",
            ),
            (
                "Sau khi cho hạt, bước tiếp theo theo lời cô là gì?",
                "Ghi tên cây",
                ["Tưới thật nhiều nước", "Bỏ cốc đi"],
                "Thứ tự là cho hạt, ghi tên rồi tưới ít nước.",
            ),
            (
                "Chi tiết nào cho thấy Lan làm cẩn thận?",
                "Nhắc Nam sửa trước khi tưới",
                ["Tưới ngay khi chưa ghi tên", "Bỏ qua lời cô"],
                "Lan kiểm tra bước còn thiếu và nhắc sửa trước bước tiếp theo.",
            ),
            (
                "Cô dặn tưới lượng nước thế nào?",
                "Ít nước",
                ["Thật đầy cốc", "Không tưới bao giờ"],
                "Lời dặn cuối là tưới ít nước.",
            ),
            (
                "Trình tự nào đúng?",
                "Cho hạt → ghi tên → tưới",
                ["Tưới → bỏ cốc → ghi tên", "Ghi tên → bỏ hạt đi → tưới"],
                "Dãy đúng giữ đủ ba bước theo lời cô.",
            ),
        ],
        4: [
            (
                "Huy đề nghị dành bao lâu để đọc sách?",
                "Mười phút đầu giờ",
                ["Cả buổi học", "Một phút cuối tuần"],
                "Đề nghị của Huy ghi rõ mười phút đọc sách đầu giờ.",
            ),
            (
                "An nêu băn khoăn gì?",
                "Có bạn quên mang sách",
                ["Không ai biết đọc", "Sách đều bị mất"],
                "Câu hỏi của An là nếu bạn quên sách thì sao.",
            ),
            (
                "Huy giải quyết băn khoăn bằng cách nào?",
                "Cho mượn từ góc sách chung",
                ["Yêu cầu bạn nghỉ học", "Hủy tất cả giờ đọc"],
                "Huy đề xuất dùng góc sách chung cho bạn mượn.",
            ),
            (
                "Vì sao cô đề nghị thử một tuần?",
                "Để có kết quả trước khi nhận xét",
                ["Để khẳng định ngay mọi bạn thích", "Để không ai được góp ý"],
                "Thử rồi trao đổi giúp nhận xét dựa vào trải nghiệm.",
            ),
            (
                "Thông tin nào chưa được bài đọc chứng minh?",
                "Mọi bạn đều thích cách đọc này",
                ["Huy đưa ra đề nghị", "An nêu một câu hỏi"],
                "Cô nhắc không kết luận ngay rằng mọi bạn đều thích.",
            ),
            (
                "Lời góp ý nào giúp buổi thảo luận tiếp tục?",
                "Mình thử rồi hỏi ý kiến các bạn nhé",
                ["Không cần nghe ai nữa", "Ai hỏi là làm sai"],
                "Lời góp ý này tôn trọng việc thử và lắng nghe phản hồi.",
            ),
        ],
        5: [
            (
                "Áp phích đưa ra lời khẳng định nào?",
                "Nước X giúp mọi bạn học giỏi ngay",
                ["Nước X có chai màu xanh", "Nước X được miễn phí"],
                "Đây là lời quảng cáo xuất hiện trực tiếp trong đoạn.",
            ),
            (
                "Hình trong áp phích thực sự cho thấy điều gì?",
                "Một học sinh cầm chai nước",
                ["Tất cả học sinh đều học giỏi", "Kết quả kiểm chứng của chuyên gia"],
                "Bức hình chỉ ghi lại việc cầm chai; không chứng minh tác dụng học tập.",
            ),
            (
                "Lời quảng cáo còn thiếu điều gì để được tin là đã kiểm chứng?",
                "Thông tin kiểm chứng đáng tin cậy",
                ["Thêm chữ thật to", "Thêm nhiều màu nền"],
                "Cỡ chữ và màu không thay thế được thông tin kiểm chứng.",
            ),
            (
                "Vy phân biệt hai điều gì?",
                "Điều nhìn thấy và kết luận chưa đủ chứng cứ",
                ["Chai cao và chai thấp", "Giấy trắng và giấy màu"],
                "Vy chỉ ra ảnh cầm chai chưa chứng minh nguyên nhân học giỏi.",
            ),
            (
                "Nhóm chọn làm gì tiếp theo?",
                "Hỏi người lớn, tìm nguồn đáng tin cậy",
                ["Chia sẻ ngay như sự thật", "Mua ngay vì hình đẹp"],
                "Đây là hành động kiểm tra thông tin của nhóm trong đoạn.",
            ),
            (
                "Câu nào nhận xét đúng mức bằng chứng trong bài?",
                "Chưa đủ thông tin để xác nhận lời quảng cáo",
                ["Ảnh đã chứng minh mọi bạn học giỏi", "Chữ lớn luôn là thông tin đúng"],
                "Không có kiểm chứng nên chưa thể xác nhận lời quảng cáo, cũng không suy diễn thêm từ bức ảnh.",
            ),
        ],
    }
    free_titles = {
        1: "Na chăm chậu hoa",
        2: "Chiếc bút tìm được chủ",
        3: "Đọc thông báo thư viện",
        4: "Góc sách dễ tìm",
        5: "Đọc số liệu, nghĩ cẩn thận",
    }
    vip_titles = {
        1: "Làm đúng hai lời dặn",
        2: "Lời hẹn trả truyện",
        3: "Tìm bước còn thiếu",
        4: "Góp ý có lí do",
        5: "Thám tử lời quảng cáo",
    }
    free_pictures = {
        1: ("Bông hoa", "Cây"),
        2: ("Bút mực", "Ghế"),
        3: ("Sách", "Trường học"),
        4: ("Sách", "Trường học"),
        5: ("Bút chì", "Trường học"),
    }
    vip_pictures = {
        1: ("Bút mực", "Bàn học"),
        2: ("Sách", "Cặp"),
        3: ("Cây", "Cây"),
        4: ("Sách", "Trường học"),
        5: ("Nước uống", "Trường học"),
    }
    return [
        unit(
            grade,
            "reading",
            "reading-everyday",
            free_titles[grade],
            free_contexts[grade],
            "Tìm câu trong bài cho biết ai làm việc gì.",
            "Chọn điều bài đọc thực sự cho biết.",
            [
                "Đọc từng câu ngắn, có thể nhờ người lớn đọc cùng.",
                "Tìm tên người, thời gian hoặc việc được hỏi.",
                "Đọc lại câu có thông tin trước khi chọn.",
            ],
            cards(*free_pictures[grade]),
            free_rows[grade],
            context=free_contexts[grade],
        ),
        unit(
            grade,
            "reading",
            "reading-detective",
            vip_titles[grade],
            vip_contexts[grade],
            "Từ rồi giúp em biết việc làm sau. Một chi tiết rõ ràng giúp em giải thích lựa chọn.",
            "Tìm bằng chứng trong bài, đừng đoán thêm.",
            [
                "Xác định câu hỏi đang hỏi điều gì.",
                "Gạch ý hoặc nói lại chi tiết liên quan.",
                "So từng lựa chọn với chi tiết; bỏ ý không có căn cứ.",
            ],
            cards(*vip_pictures[grade]),
            vip_rows[grade],
            vip=True,
            context=vip_contexts[grade],
        ),
    ]
