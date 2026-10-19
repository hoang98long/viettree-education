"""Original card-based reasoning lessons; no inference service or personal data."""

from app.academy.curriculum import activity, lesson, quiz


def reasoning(grade, number, title, scene, concept, pairs, questions, hints, application):
    row = lesson(
        number,
        title,
        scene,
        concept,
        activity(
            "fact_check",
            "Xem từng thẻ. Chọn lời giải thích hoặc bước tiếp theo.",
            pairs,
            concept,
            hints=hints,
        ),
        [quiz(*question) for question in questions],
        "Dùng tình huống và dữ liệu giả trong bài. Đọc cùng trẻ lớp 1–2; cho trẻ chỉ tranh "
        "hoặc nói thay cho viết. Hỏi: Vì sao em chọn? Chấp nhận chưa đủ thông tin và "
        "hướng dẫn hỏi lại. Đây là thẻ mô phỏng, không chạy mô hình AI thật.",
        "Đổi một chi tiết trên thẻ. Nói lựa chọn có đổi không và vì sao. "
        "Nhờ người lớn kiểm tra cách giải thích của em.",
        application,
    )
    row.update(
        grade=grade,
        code=f"AI{grade}-{number}",
        unit_code=f"AI{grade}-reason",
        unit_title="Giải thích lựa chọn",
        unit_position=11,
        position=number - 38,
        objectives=[
            "Tìm chi tiết giúp em lựa chọn.",
            "Giải thích bằng tranh hoặc lời ngắn.",
            "Hỏi lại khi thông tin chưa đủ.",
        ],
    )
    return row


def records():
    return [
        reasoning(
            1,
            39,
            "Robot tìm sách",
            "Robot cần tìm sách. Sách có nhiều trang để đọc. Em chỉ đúng thẻ giúp robot.",
            "Sách có trang để đọc. Bút dùng để viết. Ta chọn theo đặc điểm, không theo màu.",
            [("Quyển sách", "Có trang để đọc"), ("Chiếc bút", "Dùng để viết")],
            [
                ("Vật nào có nhiều trang để đọc?", "Sách", "Bút", "Sách có các trang để đọc."),
                (
                    "Robot cần sách. Em dựa vào điều gì?",
                    "Có trang để đọc",
                    "Chỉ nhìn màu",
                    "Nhiều vật cùng màu nhưng dùng khác nhau.",
                ),
                (
                    "Chưa hiểu thẻ yêu cầu, em làm gì?",
                    "Nhờ người lớn đọc cùng",
                    "Chọn bừa",
                    "Em có thể hỏi lại để hiểu yêu cầu.",
                ),
            ],
            [
                "Nhìn vật trong tranh.",
                "Sách có các trang; bút có đầu để viết.",
                "Chỉ sách và nói: Có trang để đọc.",
            ],
            "Chỉ vào sách và bút của em. Nói mỗi vật dùng làm gì.",
        ),
        reasoning(
            1,
            40,
            "Thẻ bị che kín",
            "Một thẻ là sách. Thẻ kia bị che kín. Robot chưa nhìn được vật bên dưới.",
            "Thấy rõ sách thì gọi tên sách. Bị che kín thì hỏi lại, không đoán chắc.",
            [("Quyển sách", "Gọi tên sách"), ("Thẻ bị che kín", "Hỏi lại")],
            [
                (
                    "Thẻ bị che kín, robot có thấy vật không?",
                    "Không thấy",
                    "Thấy rõ",
                    "Phần che kín không cho biết vật bên dưới.",
                ),
                (
                    "Muốn biết vật bị che, em đề nghị gì?",
                    "Mở phần che",
                    "Đoán chắc là mèo",
                    "Cần thêm thông tin trước khi gọi tên.",
                ),
                (
                    "Nói chưa biết khi thiếu thông tin có được không?",
                    "Có",
                    "Không",
                    "Nói chưa biết giúp tránh khẳng định sai.",
                ),
            ],
            [
                "Thẻ nào nhìn thấy vật?",
                "Thẻ kín chưa cho em thấy vật.",
                "Hỏi: Cho em xem vật bên dưới được không?",
            ],
            "Nhờ người lớn che một đồ vật bằng khăn. Xin xem thêm rồi mới gọi tên.",
        ),
        reasoning(
            2,
            39,
            "Không chỉ nhìn màu",
            "Robot cần chọn bút đỏ. Có bút đỏ, bút xanh và táo đỏ trên bàn.",
            "Phải đúng cả hai: là bút và có màu đỏ. Chỉ cùng màu chưa đủ.",
            [("Bút đỏ", "Đúng cả hai"), ("Bút xanh", "Khác màu"), ("Táo đỏ", "Khác đồ vật")],
            [
                (
                    "Thẻ nào đúng yêu cầu bút đỏ?",
                    "Bút đỏ",
                    "Táo đỏ",
                    "Táo đỏ đúng màu nhưng không phải bút.",
                ),
                (
                    "Bút xanh chưa đúng ở điểm nào?",
                    "Màu sắc",
                    "Không phải bút",
                    "Bút xanh là bút nhưng không có màu đỏ.",
                ),
                (
                    "Chọn bút đỏ cần xem mấy điều?",
                    "Hai: vật và màu",
                    "Chỉ màu",
                    "Cần kiểm tra cả tên vật và màu sắc.",
                ),
            ],
            ["Đọc hai từ: bút, đỏ.", "Tìm bút trước, rồi xem màu.", "Chỉ thẻ vừa là bút vừa đỏ."],
            "Vẽ bút xanh và táo xanh. Nhờ người lớn chọn táo xanh và giải thích.",
        ),
        reasoning(
            2,
            40,
            "Hỏi rõ trước khi làm",
            "Robot nghe: Lấy sách nhé. Có sách Toán và sách Tiếng Việt. Robot cần hỏi rõ.",
            "Lời yêu cầu chưa rõ thì hỏi thêm. Đã nêu sách Toán thì chọn sách Toán.",
            [
                ("Sách: chưa nói môn", "Hỏi sách môn nào"),
                ("Sách Toán: đã nói rõ", "Chọn sách Toán"),
                ("Sách Tiếng Việt: đã nói rõ", "Chọn sách Tiếng Việt"),
            ],
            [
                (
                    "Có hai sách khác môn, chỉ nghe lấy sách, em hỏi gì?",
                    "Sách môn nào?",
                    "Sách màu gì cũng được?",
                    "Tên môn giúp phân biệt hai sách trong tình huống.",
                ),
                (
                    "Đã yêu cầu sách Toán, robot nên chọn gì?",
                    "Sách Toán",
                    "Sách Tiếng Việt",
                    "Chọn đúng môn đã được nêu.",
                ),
                (
                    "Vì sao robot nên hỏi khi chưa rõ?",
                    "Để hiểu đúng yêu cầu",
                    "Vì mọi câu đều sai",
                    "Hỏi lại giúp làm đúng điều người dùng cần.",
                ),
            ],
            [
                "Tìm tên môn trong lời yêu cầu.",
                "Chưa có tên môn thì chưa biết chọn sách nào.",
                "Hỏi tên môn; nghe câu trả lời rồi mới chọn.",
            ],
            "Đóng vai với người lớn: yêu cầu lấy sách, hỏi môn, rồi chọn đúng sách.",
        ),
        reasoning(
            3,
            39,
            "Hai câu hỏi tìm đồ vật",
            "Robot làm theo bảng: vật để đọc là sách; vật để viết thì xem có mực không. Có mực là bút mực, không có mực là bút chì.",
            "Bảng này là quy tắc do người viết sẵn. Theo từng nhánh để tìm tên vật trong bộ thẻ.",
            [
                ("Sách: để đọc", "Nhánh đọc"),
                ("Bút mực: để viết, có mực", "Nhánh viết, có mực"),
                ("Bút chì: để viết, không có mực", "Nhánh viết, không mực"),
            ],
            [
                (
                    "Vật để viết và có mực là gì theo bảng?",
                    "Bút mực",
                    "Sách",
                    "Theo nhánh viết rồi nhánh có mực.",
                ),
                (
                    "Theo bảng, bút chì đi qua nhánh nào?",
                    "Viết, không có mực",
                    "Đọc",
                    "Bút chì viết bằng lõi chì, không dùng mực.",
                ),
                (
                    "Bảng quy tắc viết sẵn có tự chứng minh dùng học máy không?",
                    "Không",
                    "Có",
                    "Làm theo nhánh viết sẵn chưa có nghĩa học từ dữ liệu.",
                ),
            ],
            [
                "Tìm việc dùng đồ vật: đọc hay viết.",
                "Nếu để viết, xem thẻ có ghi mực không.",
                "Đi từ câu hỏi đầu sang nhánh phù hợp, không nhảy bước.",
            ],
            "Vẽ hai nhánh đọc và viết. Gắn ba đồ vật mẫu vào đúng nhánh.",
        ),
        reasoning(
            3,
            40,
            "Dừng ở chỗ chưa biết",
            "Bảng mẫu hỏi công dụng trước: sách để đọc, bút mực và bút chì để viết. Một thẻ mất công dụng. Cam nằm ngoài bộ ba vật.",
            "Thiếu công dụng thì cần bổ sung. Vật ngoài bộ quy tắc thì chưa kết luận theo bảng này.",
            [
                ("Sách: để đọc", "Đủ để theo bảng"),
                ("Bút: mất dòng công dụng", "Cần thêm thông tin"),
                ("Cam: ngoài bộ ba vật", "Ngoài bộ quy tắc"),
            ],
            [
                (
                    "Thẻ mất dòng công dụng cần làm gì trước?",
                    "Bổ sung dòng bị mất",
                    "Tự bịa công dụng",
                    "Cần có thông tin của câu hỏi đầu trước khi theo nhánh.",
                ),
                (
                    "Cam không có trong bảng ba vật, nên nói gì?",
                    "Bảng này chưa xét cam",
                    "Cam chắc chắn là sách",
                    "Giới hạn của bảng không làm cam trở thành sách.",
                ),
                (
                    "Muốn thêm cam vào bảng, ai cần xem lại quy tắc?",
                    "Người thiết kế bảng",
                    "Màu nền của thẻ",
                    "Người thiết kế cần bổ sung và thử lại quy tắc.",
                ),
            ],
            [
                "Xem thẻ có đủ mô tả không.",
                "Xem vật có thuộc ba vật của bảng không.",
                "Thiếu thông tin thì hỏi thêm; ngoài bảng thì báo giới hạn.",
            ],
            "Thêm thẻ thước kẻ vào bộ mẫu. Nói vì sao cần mở rộng bảng trước khi dùng.",
        ),
        reasoning(
            4,
            39,
            "Lời giải thích có đúng căn cứ?",
            "Người dùng yêu cầu sách về cây. Thẻ A: sách trồng cây, bìa xanh. Thẻ B: sách hình học, bìa xanh. Robot cần giải thích vì sao chọn A.",
            "Căn cứ cần liên quan yêu cầu. Nội dung về cây phù hợp; màu bìa và tốc độ trả lời không giải thích được lựa chọn.",
            [
                ("Sách A: nội dung trồng cây", "Căn cứ phù hợp"),
                ("Sách A: bìa màu xanh", "Chưa đủ căn cứ"),
                ("Robot: trả lời rất nhanh", "Chưa đủ căn cứ"),
                ("Sách B: nội dung hình học", "Không đúng chủ đề"),
            ],
            [
                (
                    "Căn cứ nào giúp chọn sách về cây?",
                    "Nội dung trồng cây",
                    "Bìa xanh",
                    "Cần đối chiếu nội dung với điều người đọc cần.",
                ),
                (
                    "Hai sách cùng bìa xanh có chắc cùng chủ đề không?",
                    "Không",
                    "Có",
                    "Trong tình huống, hai sách có nội dung khác nhau.",
                ),
                (
                    "Robot giải thích rất tự tin thì có cần kiểm tra không?",
                    "Có, đối chiếu nội dung sách",
                    "Không, giọng tự tin là đủ",
                    "Lời giải thích vẫn có thể sai hoặc không liên quan.",
                ),
            ],
            [
                "Gạch chân yêu cầu: sách về cây.",
                "Đối chiếu từng căn cứ với chủ đề cây.",
                "Giữ căn cứ nội dung; màu bìa hay tốc độ chưa chứng minh phù hợp.",
            ],
            "Chọn một sách mẫu. Nói người đọc cần gì và chi tiết nào khiến sách phù hợp.",
        ),
        reasoning(
            4,
            40,
            "Hai công cụ nói khác nhau",
            "Thẻ gốc: thư viện mở 8 giờ, đóng 16 giờ. Công cụ A nói đóng 16 giờ; B nói 18 giờ. Đây là giờ giả trong bài.",
            "Đối chiếu nguồn gốc, không biểu quyết theo số công cụ. Chưa có nguồn thì cần tìm nguồn trước khi kết luận.",
            [
                ("A: đóng 16 giờ", "Khớp thẻ gốc"),
                ("B: đóng 18 giờ", "Khác thẻ gốc"),
                ("Hai công cụ cùng nói 18 giờ", "Vẫn phải đối chiếu"),
                ("Không có thẻ giờ mở cửa", "Cần tìm nguồn"),
            ],
            [
                (
                    "Theo thẻ gốc trong bài, thư viện đóng lúc nào?",
                    "16 giờ",
                    "18 giờ",
                    "Thẻ gốc ghi đóng 16 giờ.",
                ),
                (
                    "Hai công cụ cùng nói 18 giờ có đủ để bỏ thẻ gốc không?",
                    "Không",
                    "Có",
                    "Nhiều công cụ có thể lặp cùng một lỗi.",
                ),
                (
                    "Muốn đi thư viện thật, nên làm gì?",
                    "Nhờ người lớn kiểm tra giờ hiện hành",
                    "Dùng luôn giờ giả của bài",
                    "Giờ trong bài là dữ liệu giả, không phải thông báo thư viện thật.",
                ),
            ],
            [
                "Tìm dòng đóng cửa trên thẻ gốc.",
                "So 16 giờ với từng câu trả lời.",
                "Khi các công cụ khác nhau, kiểm nguồn; không chọn theo số đông.",
            ],
            "Vẽ thẻ giờ mở cửa giả và hai câu trả lời. Đổi thẻ gốc rồi kiểm tra lại.",
        ),
        reasoning(
            5,
            39,
            "Gợi ý nhiều chưa chắc phù hợp",
            "Mai cần sách khoa học ngắn. Bảng mẫu: A là khoa học 12 trang; B là truyện 12 trang; C là khoa học 80 trang. Trong bài, ngắn là không quá 20 trang.",
            "Chọn theo nhu cầu đã nêu. Lượt xem cao hay vị trí đầu danh sách không thay cho kiểm tra chủ đề và độ dài.",
            [
                ("Sách A: khoa học, 12 trang", "Đáp ứng hai tiêu chí"),
                ("Sách B: truyện, 12 trang", "Khác chủ đề"),
                ("Sách C: khoa học, 80 trang", "Vượt độ dài"),
                ("Sách B: đứng đầu gợi ý", "Vẫn cần xét tiêu chí"),
            ],
            [
                (
                    "Sách nào phù hợp cả hai tiêu chí trong bài?",
                    "Sách A",
                    "Sách C",
                    "A đúng chủ đề khoa học và không quá 20 trang.",
                ),
                (
                    "Vì sao C chưa phù hợp nhu cầu đã nêu?",
                    "80 trang vượt giới hạn 20 trang",
                    "Khoa học không thể ngắn",
                    "Tiêu chí độ dài là điều kiện riêng của tình huống này.",
                ),
                (
                    "Nếu Mai đổi nhu cầu, em làm gì?",
                    "Xét lại các tiêu chí",
                    "Giữ A cho mọi nhu cầu",
                    "Một lựa chọn phù hợp trong tình huống này chưa phù hợp mọi lúc.",
                ),
            ],
            [
                "Tìm hai tiêu chí: khoa học và không quá 20 trang.",
                "Kiểm riêng chủ đề và số trang từng sách.",
                "Chỉ A đạt cả hai; đứng đầu gợi ý chưa đủ chứng minh phù hợp.",
            ],
            "Đổi giới hạn sang 100 trang. Nói sách nào đáp ứng và còn cần hỏi thêm sở thích gì.",
        ),
        reasoning(
            5,
            40,
            "Con người duyệt trước khi dùng",
            "Lớp làm bảng nhắc tưới cây. Công cụ gợi ý: tưới cây mỗi giờ. Người phụ trách vườn cần xem loại cây, đất và thời tiết trước khi duyệt.",
            "Gợi ý có thể thiếu bối cảnh. Khi quyết định ảnh hưởng người hoặc cây, cần người phù hợp kiểm tra; chưa duyệt thì chưa đem làm theo.",
            [
                ("Cây: chưa biết loại", "Bổ sung bối cảnh"),
                ("Đất: chưa kiểm tra độ ẩm", "Bổ sung bối cảnh"),
                ("Robot: tưới mỗi giờ", "Chưa dùng ngay"),
                ("Người phụ trách vườn: xem và duyệt", "Kiểm tra trước khi dùng"),
            ],
            [
                (
                    "Có nên làm theo lịch tưới mỗi giờ ngay không?",
                    "Chưa, cần người phụ trách kiểm tra",
                    "Có, mọi cây đều cần vậy",
                    "Lịch tưới còn phụ thuộc loại cây và điều kiện cụ thể.",
                ),
                (
                    "Thông tin nào cần bổ sung trước khi duyệt?",
                    "Loại cây và độ ẩm đất",
                    "Màu vỏ robot",
                    "Thông tin liên quan giúp người phụ trách xem lịch có phù hợp không.",
                ),
                (
                    "Ai chịu trách nhiệm duyệt bảng nhắc của lớp?",
                    "Người phụ trách được phân công",
                    "Công cụ tự chịu mọi trách nhiệm",
                    "Công cụ hỗ trợ đề xuất; người được phân công kiểm tra trước khi dùng.",
                ),
            ],
            [
                "Tìm điều chưa biết về cây và đất.",
                "Phân biệt gợi ý với lịch đã được duyệt.",
                "Đưa gợi ý và bối cảnh cho người phụ trách; chờ kiểm tra trước khi dùng.",
            ],
            "Làm thẻ giấy gồm: đề xuất, điều chưa biết, người cần kiểm tra. Không thử lịch tưới giả lên cây thật.",
        ),
    ]
