"""Giáo trình nguyên bản; thông tin AI được diễn giải ở mức phù hợp tiểu học."""

UNITS = [
    ("around", "AI quanh em", 3),
    ("data", "Máy tính học từ dữ liệu", 3),
    ("prompt", "Giao tiếp với AI", 4),
    ("math", "AI hỗ trợ Toán", 4),
    ("vietnamese", "AI hỗ trợ Tiếng Việt", 4),
    ("english", "AI hỗ trợ Tiếng Anh", 4),
    ("creative", "Sáng tạo cùng AI", 4),
    ("safety", "AI an toàn và thông minh", 4),
    ("project", "Dự án AI của em", 6),
]
COMPETENCIES = {
    "around": "Nhận biết khả năng và giới hạn AI",
    "data": "Thu thập và kiểm tra dữ liệu mẫu",
    "prompt": "Đặt câu hỏi và kiểm chứng",
    "math": "Giải thích và kiểm tra lập luận Toán",
    "vietnamese": "Tìm ý, đọc hiểu và giữ giọng văn",
    "english": "Thực hành tiếng Anh theo tình huống",
    "creative": "Thiết kế và cải tiến sản phẩm",
    "safety": "Bảo vệ thông tin và tôn trọng nguồn",
    "project": "Hợp tác, thử nghiệm và trình bày",
}


def quiz(prompt, correct, wrong, explanation):
    return {"prompt": prompt, "options": [correct, wrong], "answer": 0, "explanation": explanation}


def activity(kind, instruction, pairs, explanation, hints=()):
    return {
        "kind": kind,
        "instruction": instruction,
        "items": [
            {"id": f"item-{i}", "text": text, "answer": answer}
            for i, (text, answer) in enumerate(pairs, 1)
        ],
        "choices": list(dict.fromkeys(answer for _, answer in pairs)),
        "explanation": explanation,
        "hints": list(hints),
    }


def lesson(number, title, scene, concept, practice, questions, teacher, advanced, application):
    return dict(
        number=number,
        title=title,
        scene=scene,
        concept=concept,
        activity=practice,
        questions=questions,
        teacher=teacher,
        advanced=advanced,
        application=application,
    )


LESSONS = [
    lesson(
        1,
        "AI là gì và AI không phải là gì?",
        "Ở góc lớp có quạt bật bằng công tắc và ứng dụng nhận dạng hình con mèo. Hai thiết bị đều dùng điện. Em thử tìm điểm khác nhau.",
        "AI là các hệ thống máy tính làm một số nhiệm vụ như nhận dạng, dự đoán hoặc tạo nội dung. Nhiều AI tìm quy luật từ dữ liệu mẫu. Quạt chỉ bật bằng công tắc không vì thế trở thành AI. AI không có cảm xúc thật và vẫn có thể sai.",
        activity(
            "classify",
            "Xếp tình huống vào AI hoặc thiết bị hoạt động theo lệnh thông thường.",
            [
                ("Ứng dụng đoán tên con vật từ ảnh", "Có dùng AI"),
                ("Quạt bật bằng công tắc", "Thiết bị thông thường"),
                ("Máy tính tạo đoạn gợi ý từ yêu cầu", "Có dùng AI"),
                ("Đèn bật khi em nhấn nút", "Thiết bị thông thường"),
            ],
            "Tính tự động hoặc dùng điện chưa đủ để kết luận một thiết bị dùng AI.",
        ),
        [
            quiz(
                "Vì sao quạt bật bằng công tắc chưa phải ví dụ AI?",
                "Nó làm theo lệnh bật/tắt đã định",
                "Vì quạt không có màn hình",
                "Cần xét cách hoạt động, không xét hình dáng.",
            ),
            quiz(
                "AI nhận dạng có thể làm gì?",
                "Ước đoán nhãn từ dữ liệu",
                "Luôn hiểu đúng mọi bức ảnh",
                "Kết quả nhận dạng là dự đoán, cần kiểm tra.",
            ),
            quiz(
                "Robot nói 'rất vui' có nghĩa gì?",
                "Câu được hệ thống tạo hoặc lập trình",
                "Robot có cảm xúc như con người",
                "Lời nói thân thiện không chứng minh có cảm xúc thật.",
            ),
        ],
        "Đưa hai thẻ quạt và nhận dạng ảnh. Hỏi trẻ thiết bị nhận thông tin gì và tạo kết quả gì; chấp nhận 'chưa biết' khi thiếu mô tả cách hoạt động.",
        "Tìm một thiết bị tự động chưa dùng AI và giải thích vì sao không thể kết luận chỉ qua vẻ ngoài.",
        "Khi gặp thiết bị mới, hỏi người lớn về chức năng trước khi gọi nó là AI.",
    ),
    lesson(
        2,
        "AI ở nhà, ở trường và trong cuộc sống",
        "Một bạn đọc phụ đề tự động, một cô giáo dùng công cụ gợi ý tài liệu và một gia đình xem bản đồ đường đi. Ta tìm AI trong các tình huống gần gũi.",
        "Nhận giọng nói thành chữ, gợi ý học liệu và nhận dạng đồ vật là những nhiệm vụ có thể dùng AI. Ta mô tả nhiệm vụ cụ thể, không gọi mọi ứng dụng bản đồ hay mọi máy giặt là AI. Dữ liệu và thiết kế quyết định chức năng.",
        activity(
            "match",
            "Ghép nhiệm vụ với nơi sử dụng phù hợp trong câu chuyện.",
            [
                ("Tạo phụ đề bài giảng", "Ở trường"),
                ("Gợi ý món ăn từ đồ có sẵn", "Ở nhà"),
                ("Nhận dạng biển báo trong thử nghiệm", "Ngoài đường"),
                ("Gợi ý ôn từ vựng của lớp", "Ở trường"),
            ],
            "Một nhiệm vụ có thể xuất hiện ở nhiều nơi; ở đây ghép theo tình huống đã mô tả.",
        ),
        [
            quiz(
                "Khi phụ đề khác lời cô giáo, em nên làm gì?",
                "Nghe lại và nhờ cô xác nhận",
                "Tin phụ đề hơn mọi người",
                "Công cụ nhận giọng nói có thể nghe nhầm.",
            ),
            quiz(
                "Thông tin nào đủ để mô tả ứng dụng?",
                "Nhiệm vụ và đầu vào/đầu ra của nó",
                "Màu vỏ thiết bị",
                "Cần biết chức năng thay vì suy đoán qua màu sắc.",
            ),
            quiz(
                "Có nên nhập địa chỉ nhà để chơi nhận dạng?",
                "Không, dùng ví dụ giả",
                "Có, vì trò chơi nào cũng an toàn",
                "Không cần thông tin riêng để học nhiệm vụ nhận dạng.",
            ),
        ],
        "Cho nhóm gắn thẻ vào tranh nhà/lớp/đường. Mời giải thích lựa chọn; tách tác dụng của công cụ với quyền quyết định của người dùng.",
        "Đề xuất tình huống AI giúp trường học nhưng vẫn cần người lớn kiểm tra.",
        "Vẽ sơ đồ một nhiệm vụ AI giúp em học; dùng dữ liệu mẫu.",
    ),
    lesson(
        3,
        "Con người giỏi gì, AI giỏi gì?",
        "Lớp muốn gửi lời cảm ơn bác bảo vệ. Công cụ gợi ý câu chữ, còn các bạn nhớ những việc bác đã giúp và chọn lời nói phù hợp.",
        "AI có thể xử lý nhiều mẫu nhanh, nhưng con người đặt mục tiêu, hiểu tình huống, quan tâm người khác và chịu trách nhiệm. Kết quả do AI tạo không tự thay thế nhận xét hoặc quyết định của em.",
        activity(
            "classify",
            "Chọn ai cần chịu trách nhiệm trong từng việc của lớp.",
            [
                ("Quyết định lời cảm ơn có lịch sự không", "Con người quyết định"),
                ("Tạo nhiều cách mở đầu để tham khảo", "Công cụ hỗ trợ"),
                ("Kiểm tra dữ kiện có thật không", "Con người quyết định"),
                ("Sắp xếp các thẻ theo quy tắc đã cho", "Công cụ hỗ trợ"),
            ],
            "Công cụ hỗ trợ thao tác; người sử dụng vẫn kiểm tra và chịu trách nhiệm.",
        ),
        [
            quiz(
                "Ai quyết định câu văn cuối cùng của em?",
                "Em, với hướng dẫn phù hợp",
                "Công cụ vì gõ nhanh hơn",
                "Tốc độ không thay thế trách nhiệm.",
            ),
            quiz(
                "AI tạo lời cảm ơn sai tên thì sao?",
                "Sửa và kiểm tra trước khi dùng",
                "Giữ vì AI không thể sai",
                "Người viết cần xác minh nội dung.",
            ),
            quiz(
                "AI có thật sự quý bác bảo vệ không?",
                "Không có bằng chứng về cảm xúc thật",
                "Có, vì nó dùng lời thân thiện",
                "Không gán cảm xúc con người cho hệ thống máy tính.",
            ),
        ],
        "Tổ chức đóng vai người biên tập và công cụ gợi ý. Đánh giá lý do chọn lời cảm ơn, không đánh giá độ dài văn bản.",
        "Nêu một việc nên nhờ công cụ và một việc cần người lớn quyết định, giải thích từng lựa chọn.",
        "Viết một câu cảm ơn bằng lời của em sau khi đọc gợi ý.",
    ),
    lesson(
        4,
        "Dữ liệu là gì?",
        "Trên bàn có bút, quả cam và thẻ hình mèo. Ta ghi màu, hình dạng và nhóm đồ vật thành những thông tin quan sát được.",
        "Dữ liệu là thông tin được ghi lại: hình, âm thanh, số đo hoặc từ ngữ. Nhãn cho biết nhóm của một mẫu. Cùng vật có nhiều đặc điểm; màu đỏ không đủ phân biệt quả táo với chiếc bút đỏ.",
        activity(
            "classify",
            "Xếp các mẫu theo loại dữ liệu được mô tả.",
            [
                ("Bức vẽ quả cam", "Hình ảnh"),
                ("Tiếng chim trong bản ghi mẫu", "Âm thanh"),
                ("Số lượng 5 chiếc bút", "Số"),
                ("Từ 'mèo' trên thẻ", "Từ ngữ"),
            ],
            "Chọn loại thông tin được ghi lại, không đoán vật qua một màu duy nhất.",
        ),
        [
            quiz(
                "Nhãn 'trái cây' cho biết gì?",
                "Nhóm của mẫu",
                "Tên thật của người chụp",
                "Nhãn mô tả nhóm dữ liệu, không cần danh tính.",
            ),
            quiz(
                "Hai đồ vật đều đỏ có cùng loại không?",
                "Chưa đủ thông tin",
                "Luôn cùng loại",
                "Một đặc điểm không đủ phân loại mọi đồ vật.",
            ),
            quiz(
                "Dữ liệu phù hợp trò chơi của lớp là gì?",
                "Thẻ đồ vật tự vẽ",
                "Ảnh kèm số điện thoại bạn",
                "Dùng thẻ mẫu tránh thông tin nhận dạng.",
            ),
        ],
        "Cho trẻ quan sát một vật qua hai tiêu chí. Ghi bảng loại dữ liệu/nhãn; nhấn mạnh không thu ảnh hoặc giọng nói học sinh.",
        "Tạo hai quy tắc phân loại cùng một bộ thẻ và nêu điểm khác nhau.",
        "Lập bảng dữ liệu 4 đồ vật bằng đặc điểm quan sát được.",
    ),
    lesson(
        5,
        "Dạy máy phân loại động vật",
        "Mầm AI đã xem một số thẻ mèo và chim. Em bổ sung ví dụ rồi thử thẻ mới có đặc điểm gần giống. Đây là trò mô phỏng phân loại.",
        "Mô hình học từ các ví dụ có nhãn. Tập huấn luyện giúp tìm quy luật, tập thử dùng để xem quy luật có áp dụng được cho mẫu mới. Trò này dùng so khớp đặc điểm đơn giản, không phải mô hình AI lớn.",
        activity(
            "train",
            "Quan sát đặc điểm và chọn nhãn cho từng con vật; thử lại sau khi kiểm tra lỗi.",
            [
                ("Mèo: bốn chân, có lông", "Mèo"),
                ("Chim: hai chân, có cánh", "Chim"),
                ("Mèo nằm cuộn tròn", "Mèo"),
                ("Chim đậu trên cành", "Chim"),
            ],
            "Tư thế khác nhau vẫn có thể thuộc cùng nhãn; hãy chọn nhiều mẫu đa dạng.",
        ),
        [
            quiz(
                "Tập thử có nên chỉ lặp lại toàn bộ tập học?",
                "Không, cần mẫu mới để kiểm tra",
                "Có, để luôn đạt điểm cao",
                "Mẫu mới giúp thấy giới hạn của quy luật.",
            ),
            quiz(
                "Nhãn sai có ảnh hưởng gì?",
                "Có thể làm dự đoán sai",
                "Không ảnh hưởng cách học",
                "Ví dụ có nhãn là thông tin mô hình sử dụng.",
            ),
            quiz(
                "Mèo nằm có còn là mèo không?",
                "Có, tư thế không đổi nhóm",
                "Không vì không thấy đủ chân",
                "Cần xét nhiều đặc điểm, không chỉ tư thế.",
            ),
        ],
        "Dùng thẻ minh họa có nhãn; một nhóm chọn tập học, nhóm kia giữ tập thử. Mời trẻ sửa nhãn trước khi thêm nhiều mẫu.",
        "Tìm mẫu mà quy tắc bốn chân nhận nhầm, rồi đề xuất đặc điểm bổ sung.",
        "Thử bộ phân loại ở Phòng thí nghiệm với tập học và tập thử tách biệt.",
    ),
    lesson(
        6,
        "Khi dữ liệu thiếu hoặc sai",
        "Một bộ thẻ chỉ có mèo màu vàng. Khi gặp mèo màu đen, bộ phân loại theo màu nhầm nhãn. Vấn đề nằm ở quy tắc và bộ mẫu.",
        "Dữ liệu thiếu đa dạng hoặc gắn nhãn sai có thể dẫn tới kết quả kém. Cần bổ sung ví dụ khác màu, góc nhìn, kích thước; sửa nhãn và kiểm thử lại. Thêm nhiều bản sao một mẫu không thay thế sự đa dạng.",
        activity(
            "bias",
            "Chọn cách sửa phù hợp cho từng lỗi của bộ dữ liệu.",
            [
                ("Chỉ có mèo vàng", "Thêm mẫu đa dạng"),
                ("Nhãn chim đặt cho ảnh mèo", "Sửa nhãn"),
                ("Chỉ thử đúng mẫu đã học", "Dùng mẫu thử mới"),
                ("Thiếu hình ở góc nhìn khác", "Thêm mẫu đa dạng"),
            ],
            "Kiểm tra nguồn lỗi trước khi bổ sung dữ liệu; số lượng và sự đa dạng là hai điều khác nhau.",
        ),
        [
            quiz(
                "Một trăm bản sao cùng ảnh có đa dạng không?",
                "Không",
                "Có vì có nhiều ảnh",
                "Đa dạng nói về khác biệt có ý nghĩa giữa các mẫu.",
            ),
            quiz(
                "Cách sửa nhãn sai tốt nhất là gì?",
                "Xác nhận rồi sửa nhãn",
                "Thêm bản sao của nhãn sai",
                "Nhân bản lỗi sẽ không giải quyết lỗi.",
            ),
            quiz(
                "Có nên kết luận nhóm người kém từ lỗi mô hình?",
                "Không, kiểm tra dữ liệu và thiết kế",
                "Có, vì máy đã nói",
                "Lỗi dữ liệu không chứng minh năng lực hoặc giá trị của con người.",
            ),
        ],
        "Cho lớp so hai tập thẻ có cùng số lượng nhưng độ đa dạng khác nhau. Hỏi 'còn thiếu trường hợp nào' thay vì chỉ hỏi 'có bao nhiêu'.",
        "Thiết kế một tập thử có mẫu khác màu mà vẫn cùng nhãn để kiểm tra thiên lệch.",
        "So sánh dự đoán trước và sau khi cân bằng mẫu trong mô phỏng.",
    ),
    lesson(
        7,
        "Câu hỏi rõ ràng và câu hỏi mơ hồ",
        "Hai yêu cầu xuất hiện: 'Giúp em với' và 'Gợi ý bước đầu bài tìm chu vi hình chữ nhật có dài 8 cm, rộng 3 cm'. Em chọn yêu cầu dễ hiểu hơn.",
        "Câu hỏi rõ nêu việc cần làm và thông tin cần thiết. Không cần câu dài; cần đủ dữ kiện đúng và không kèm thông tin riêng. Khi chưa rõ nhiệm vụ, nên hỏi lại thay vì đoán.",
        activity(
            "classify",
            "Phân loại yêu cầu theo độ rõ ràng.",
            [
                ("Giúp em với", "Cần bổ sung"),
                ("Gợi ý 2 ý cho đoạn văn về cây ở sân trường", "Đã rõ"),
                ("Làm cái đó", "Cần bổ sung"),
                ("Giải thích từ 'library' bằng một câu ngắn", "Đã rõ"),
            ],
            "Từ 'cái đó' không cho biết nhiệm vụ; mục tiêu và ngữ cảnh giúp hiểu đúng.",
        ),
        [
            quiz(
                "Cần thêm gì cho yêu cầu 'Sửa giúp'?",
                "Đoạn cần sửa và mục tiêu sửa",
                "Mật khẩu của em",
                "Thông tin nhiệm vụ có ích; mật khẩu không liên quan.",
            ),
            quiz(
                "Yêu cầu rõ có phải luôn thật dài?",
                "Không, đủ ý cần thiết",
                "Có, càng dài càng đúng",
                "Độ rõ không phụ thuộc riêng số chữ.",
            ),
            quiz(
                "Khi không hiểu câu hỏi, nên làm gì?",
                "Hỏi thêm một điều cụ thể",
                "Tự bịa dữ kiện",
                "Hỏi lại giúp tránh làm sai nhiệm vụ.",
            ),
        ],
        "Cho nhóm cải thiện một yêu cầu mơ hồ bằng hai thông tin. Đánh giá sự phù hợp của thông tin thêm, không chấm theo độ dài.",
        "Rút một câu hỏi dài thành câu ngắn vẫn đủ mục tiêu, dữ kiện và định dạng.",
        "Viết lại một câu hỏi em từng dùng khi nhờ người khác giúp.",
    ),
    lesson(
        8,
        "Công thức hỏi AI: mục tiêu + ngữ cảnh + yêu cầu + định dạng",
        "Em muốn ôn phân số bằng hình chiếc bánh. Ta ghép bốn mảnh để công cụ hiểu việc cần giúp và cách trả lời.",
        "Mục tiêu: em muốn hiểu điều gì. Ngữ cảnh: bài đang học và dữ kiện mẫu. Yêu cầu: cách hỗ trợ, ví dụ chỉ gợi ý. Định dạng: câu ngắn, bảng hoặc ba bước. Công thức giúp rõ ràng nhưng không bảo đảm câu trả lời luôn đúng.",
        activity(
            "prompt",
            "Ghép từng mảnh vào phần của công thức câu hỏi.",
            [
                ("Em muốn hiểu 1/4", "Mục tiêu"),
                ("Bánh chia 4 phần bằng nhau", "Ngữ cảnh"),
                ("Gợi ý để em tự tô màu", "Yêu cầu"),
                ("Trả lời bằng 2 câu ngắn", "Định dạng"),
            ],
            "Bốn phần giúp nêu nhiệm vụ; vẫn cần tự kiểm tra phản hồi.",
        ),
        [
            quiz(
                "'Dùng bảng hai cột' thuộc phần nào?",
                "Định dạng",
                "Mật khẩu",
                "Định dạng mô tả cách trình bày.",
            ),
            quiz(
                "'Chỉ gợi ý bước đầu' có tác dụng gì?",
                "Giữ việc suy nghĩ cho em",
                "Bảo đảm mọi kết quả đúng",
                "Cách hỏi không thay thế kiểm chứng.",
            ),
            quiz(
                "Ngữ cảnh phù hợp là gì?",
                "Dữ kiện của bài mẫu",
                "Địa chỉ nhà riêng",
                "Dữ kiện bài đủ giúp hiểu nhiệm vụ mà không cần thông tin riêng.",
            ),
        ],
        "Dùng bốn thẻ màu có cả biểu tượng và chữ. Mời trẻ ghép câu rồi bỏ thông tin không cần thiết; không yêu cầu nhập tên thật.",
        "Tạo hai yêu cầu cho cùng mục tiêu nhưng có định dạng khác, nêu khi nào dùng mỗi dạng.",
        "Dùng Prompt Builder tạo câu hỏi xin gợi ý cho bài đang học.",
    ),
    lesson(
        9,
        "Hỏi tiếp và cải thiện câu trả lời",
        "Công cụ gợi ý một đoạn quá dài về tiết kiệm nước. Em cần poster bốn dòng và có thể yêu cầu rút gọn mà không thêm dữ kiện bịa.",
        "Đọc phản hồi, xác định điểm chưa phù hợp và hỏi tiếp cụ thể. Có thể yêu cầu giải thích từ khó, đưa ví dụ hoặc đổi định dạng. Không lặp 'sai rồi' mà không nêu cần sửa điều gì.",
        activity(
            "match",
            "Ghép vấn đề với yêu cầu hỏi tiếp giúp cải thiện.",
            [
                ("Câu trả lời quá dài", "Rút còn 3 câu"),
                ("Có từ em chưa hiểu", "Giải thích từ khó"),
                ("Thiếu ví dụ", "Thêm ví dụ mẫu"),
                ("Chưa theo dạng bảng", "Trình bày lại thành bảng"),
            ],
            "Yêu cầu tiếp theo cần chỉ rõ vấn đề và giới hạn mới.",
        ),
        [
            quiz(
                "Sau khi nhận phản hồi, bước đầu là gì?",
                "Đọc và xác định chỗ cần cải thiện",
                "Chép ngay toàn bộ",
                "Hiểu phản hồi giúp đặt câu hỏi tiếp đúng mục tiêu.",
            ),
            quiz(
                "Hỏi tiếp có làm dữ kiện bịa thành thật không?",
                "Không, vẫn cần bằng chứng",
                "Có nếu hỏi nhiều lần",
                "Sự lặp lại không chứng minh tính đúng.",
            ),
            quiz(
                "Câu nào giúp rút gọn tốt hơn?",
                "Giữ 2 ý chính trong 3 câu",
                "Làm tốt hơn đi",
                "Yêu cầu cụ thể có tiêu chí để kiểm tra.",
            ),
        ],
        "Cho trẻ nhận bản nháp cố tình quá dài, chọn một cải tiến rồi so với tiêu chí ban đầu. Không xem phản hồi thứ hai là mặc nhiên chính xác.",
        "Viết câu hỏi tiếp yêu cầu nêu chỗ chưa chắc chắn và cách kiểm tra.",
        "Sửa câu hỏi của bài trước để phản hồi dễ đọc hơn.",
    ),
    lesson(
        10,
        "Kiểm chứng: AI có thể trả lời sai",
        "Một thẻ nói 7 × 8 = 54, thẻ khác có bảy nhóm tám chấm. Em kiểm tra bằng phép tính và hình trước khi chọn thông tin.",
        "AI có thể trả lời tự tin nhưng sai. Kiểm chứng bằng sách học, phép tính, quan sát hoặc người có chuyên môn phù hợp. Không xem số lượt chia sẻ hay giọng nói tự tin là bằng chứng.",
        activity(
            "fact_check",
            "Chọn nguồn kiểm tra phù hợp cho từng thông tin.",
            [
                ("7 × 8 bằng bao nhiêu", "Tính hoặc đếm nhóm"),
                ("Nghĩa từ tiếng Anh trong bài", "Từ điển học sinh"),
                ("Chi tiết trong truyện đã đọc", "Đọc lại văn bản"),
                ("Hướng dẫn dùng điện an toàn", "Hỏi người lớn phụ trách"),
            ],
            "Chọn nguồn phù hợp nhiệm vụ; vấn đề an toàn cần người lớn hỗ trợ.",
        ),
        [
            quiz("7 × 8 bằng số nào?", "56", "54", "7 nhóm, mỗi nhóm 8: 8+8+8+8+8+8+8=56."),
            quiz(
                "Thông tin được chia sẻ nhiều có chắc đúng?",
                "Không",
                "Luôn đúng",
                "Số lượt chia sẻ không phải bằng chứng.",
            ),
            quiz(
                "Khi chưa kiểm tra được, nên nói gì?",
                "Em chưa chắc và cần xác minh",
                "Chắc đúng vì công cụ tự tin",
                "Thừa nhận chưa chắc giúp tránh lan truyền sai.",
            ),
        ],
        "Yêu cầu trẻ nêu cách kiểm tra, không chỉ chọn đúng. Với an toàn sức khỏe/điện, hướng dẫn hỏi người lớn, không tự thử nguy hiểm.",
        "Tìm hai cách độc lập xác minh một khẳng định và nêu giới hạn mỗi cách.",
        "Ghi một khẳng định, nguồn kiểm tra và kết luận có điều kiện.",
    ),
]


def records():
    from copy import deepcopy

    from app.academy.curriculum_primary import records_for_grade
    from app.academy.curriculum_projects import LESSONS as projects
    from app.academy.curriculum_subjects import LESSONS as subjects

    all_lessons = LESSONS + subjects + projects
    if [row["number"] for row in all_lessons] != list(range(1, 37)):
        raise ValueError("Giáo trình lớp 4 phải đủ 36 tiết theo thứ tự")
    output = []
    for row in all_lessons:
        number = row["number"]
        cursor = 0
        for position, (unit, title, count) in enumerate(UNITS, 1):
            if cursor < number <= cursor + count:
                value = deepcopy(row)
                value.update(
                    grade=4,
                    code=f"AI4-{number:02}",
                    unit_code=f"AI4-{unit}",
                    unit_title=title,
                    unit_position=position,
                    position=number - cursor,
                )
                output.append(value)
                break
            cursor += count
    for grade in [1, 2, 3, 5]:
        output.extend(records_for_grade(grade, UNITS))
    for row in output:
        row["visual_prefix"] = row["code"] + "-v2"
        if (
            row["grade"] in [1, 2, 3]
            and row["unit_code"].endswith("-data")
            and row["position"] == 3
        ):
            row["visual_prefix"] = row["code"] + "-color-v3"
        row["cards"] = [
            row["visual_prefix"] + f"-item-{i}" for i in range(1, len(row["activity"]["items"]) + 1)
        ]
    return output


def content(row):
    from copy import deepcopy

    from app.academy.schemas import LessonContent

    prefix = row["visual_prefix"]
    unit = row["unit_code"].split("-")[-1]
    questions = deepcopy(row["questions"])
    practice = deepcopy(row["activity"])
    for i, item in enumerate(practice["items"], 1):
        item["asset"] = prefix + f"-item-{i}"
    for i, q in enumerate(questions, 1):
        q["id"] = f"q-{i}"
        if (row["number"] + i) % 2:
            q["options"].reverse()
            q["answer"] = 1
    data = dict(
        objectives=[
            f"Giải thích ý chính: {row['title']}.",
            "Thực hiện hoạt động và nêu căn cứ cho lựa chọn.",
            "Dùng dữ liệu mẫu, kiểm tra kết quả và xin người lớn hỗ trợ khi cần.",
        ],
        prerequisites=[],
        estimated_minutes=10 if row["grade"] <= 2 else 15,
        keywords=[unit, "mô phỏng", "kiểm chứng"],
        age_range=[row["grade"] + 5, row["grade"] + 6],
        competencies=[unit],
        teacher_guide=row["teacher"],
        materials=["Thẻ minh họa trong bài", "Giấy/bút hoặc màn hình cảm ứng"],
        misconceptions="Không đồng nhất dự đoán với sự thật hoặc tự động hóa với AI; không gán cảm xúc thật cho nhân vật máy.",
        safety_notes="Không nhập tên thật, địa chỉ, ảnh mặt, giọng cá nhân hoặc mật khẩu. Sản phẩm riêng tư; nhờ người lớn khi có yêu cầu bất thường.",
        support="Nhờ người lớn đọc từng phần, dùng hai thẻ đầu và chỉ hình trước khi chọn. "
        + row["activity"]["instruction"],
        standard=row["activity"]["instruction"],
        advanced=row["advanced"],
        hero=prefix + "-hero",
        cards=row["cards"],
        steps=[
            dict(
                id="story",
                kind="story",
                title="Câu chuyện mở đầu",
                text=row["scene"],
                media=[prefix + "-hero"],
            ),
            dict(
                id="discover",
                kind="illustrated_explanation",
                title="Em khám phá",
                text=row["concept"],
                media=[prefix + "-hero" if row["number"] == 12 else prefix + "-support-1"],
            ),
            dict(
                id="observe",
                kind="flip_card",
                title="Quan sát và đối chiếu",
                text=row["activity"]["explanation"],
                media=[prefix + "-support-2"],
            ),
            dict(
                id="practice",
                kind="activity",
                title="Em thử làm",
                text=row["activity"]["instruction"],
                activity=practice,
                media=[prefix + "-support-3"],
            ),
            dict(
                id="checkpoint",
                kind="quiz",
                title="Em kiểm tra điều đã hiểu",
                text="Chọn đáp án rồi đọc giải thích. Nếu chưa đúng, em có thể thử lại và xin gợi ý.",
                questions=questions,
            ),
            dict(
                id="apply",
                kind="reflection",
                title="Em vận dụng",
                text=row["application"],
                media=[prefix + "-support-3"],
            ),
            dict(
                id="finish",
                kind="project_task",
                title="Điều em mang theo",
                text="Chỉ một tranh và nói điều em đã hiểu.",
                media=[prefix + "-hero"],
            ),
        ],
    )
    for step in data["steps"]:
        text = step["text"]
        sentence = text.split(". ", 1)[0]
        limit = 18 if row["grade"] <= 2 else 36
        if len(sentence.split()) > limit:
            sentence = " ".join(sentence.split()[:limit]) + "…"
        if len(sentence) < len(text):
            step["details_text"] = text
            step["text"] = sentence + ("." if sentence[-1] not in ".!?…" else "")
    return LessonContent.model_validate(data).model_dump()
