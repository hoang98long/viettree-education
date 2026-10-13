"""Original Vietnamese texts, language activities and guided writing for grade three."""

from app.curriculum.grades.grade_03.builders import unit

VIETNAMESE = [
    unit(
        "reading",
        "garden-story",
        "Đọc truyện: Chậu cây nhỏ",
        "Đọc câu chuyện rồi tìm nhân vật, việc làm và kết quả. Câu trả lời cần dựa vào chi tiết trong truyện.",
        "Mai gieo ba hạt đậu vào chậu. Mỗi sáng, em tưới một ít nước. Một tuần sau, mầm xanh nhú lên. Mai đặt chậu bên cửa sổ để cây nhận ánh sáng.",
        "Thông tin không có trong truyện thì không tự thêm vào câu trả lời.",
        "Tìm tên nhân vật và từ chỉ hoạt động.|Gạch chân câu nói về điều câu hỏi yêu cầu.|Đọc lại câu trả lời cùng chi tiết làm bằng chứng.",
        """Trong truyện Chậu cây nhỏ, ai gieo hạt đậu?|Mai|Nam|Bà|Câu đầu nêu Mai gieo hạt.
Mai tưới cây vào lúc nào?|Mỗi sáng|Mỗi tối|Chỉ chủ nhật|Truyện viết: mỗi sáng em tưới một ít nước.
Vì sao Mai đặt chậu bên cửa sổ?|Để cây nhận ánh sáng|Để giấu cây|Để cây không lớn|Câu cuối giải thích mục đích nhận ánh sáng.
Sau một tuần, điều gì xuất hiện?|Mầm xanh|Quả đậu|Hoa đỏ|Truyện nêu mầm xanh nhú lên.""",
        illustration={
            "kind": "garden",
            "caption": "Những cây non trong góc vườn nhỏ.",
            "rows": 2,
            "columns": 3,
        },
    ),
    unit(
        "reading",
        "library-story",
        "Đọc truyện: Cuốn sách được sửa",
        "Chú ý diễn biến trước, sau và lời nói của nhân vật. Hành động có thể cho thấy sự cẩn thận và trách nhiệm.",
        "Nam thấy bìa một cuốn truyện bị bong. Em báo cô thủ thư rồi cùng cô dán lại bìa. Khi keo khô, Nam đặt sách lên giá. Cô khen em biết giữ gìn sách chung.",
        "Khi đồ dùng chung hỏng, báo người hướng dẫn để sửa đúng cách.",
        "Tìm việc xảy ra đầu tiên.|Dùng các mốc thấy bìa bong, báo cô, dán bìa, chờ khô.|Kiểm tra nhận xét về nhân vật có phù hợp hành động không.",
        """Nam phát hiện điều gì ở cuốn truyện?|Bìa bị bong|Mất cả cuốn|Có hoa ở bìa|Truyện nêu bìa bị bong.
Nam báo cho ai?|Cô thủ thư|Bác lái xe|Bạn ở nhà|Nam báo cô thủ thư để được giúp.
Khi nào Nam đặt sách lên giá?|Khi keo khô|Trước khi dán|Khi bìa còn ướt|Đặt khi keo khô giúp bìa được dán chắc.
Hành động của Nam cho thấy điều gì?|Biết giữ gìn sách chung|Không thích đọc|Muốn giấu sách|Cô khen Nam giữ gìn sách chung.""",
    ),
    unit(
        "vocabulary",
        "school-words",
        "Từ ngữ về trường học và hoạt động",
        "Các từ có thể gọi tên người, đồ vật, hoạt động hoặc đặc điểm. Dùng từ đúng nghĩa trong tình huống quen thuộc ở trường.",
        "Bạn Lan đọc sách trong thư viện. Lan là tên người, sách là đồ vật, đọc là hoạt động.",
        "Đọc cả câu để biết từ được dùng với nghĩa nào.",
        "Từ đang gọi tên hay nói việc làm?|Thử hỏi ai, cái gì hoặc làm gì với từ đó.|Thay từ vào câu mới để kiểm tra nghĩa.",
        """Từ nào chỉ đồ dùng học tập?|Thước kẻ|Chạy|Vui vẻ|Thước kẻ là một đồ dùng học tập.
Từ nào chỉ hoạt động đọc sách?|Đọc|Sách|Yên tĩnh|Đọc gọi tên hoạt động.
Từ nào chỉ người làm việc ở thư viện?|Thủ thư|Giá sách|Bàn gỗ|Thủ thư là người phụ trách thư viện.
Trong câu 'Sân trường rộng', từ nào chỉ đặc điểm?|Rộng|Sân|Trường|Rộng nêu đặc điểm của sân.""",
    ),
    unit(
        "vocabulary",
        "community-words",
        "Chọn từ ngữ về gia đình và cộng đồng",
        "Dùng từ phù hợp thể hiện sự quan tâm và hợp tác. Một câu lịch sự thường có lời nhờ, cảm ơn hoặc xin lỗi đúng lúc.",
        "Khi nhờ bà chỉ cách gấp áo, em nói: Bà hướng dẫn cháu với ạ. Khi được giúp, em cảm ơn bà.",
        "Chọn từ theo người nghe và tình huống giao tiếp.",
        "Xác định em đang nhờ, cảm ơn hay xin lỗi.|Chọn cách xưng hô phù hợp người nghe.|Đọc câu thành tiếng để kiểm tra sự lịch sự.",
        """Khi được bạn nhặt giúp bút, em nên nói gì?|Cảm ơn bạn|Bạn tránh ra|Không cần bạn|Lời cảm ơn phù hợp khi được giúp.
Từ nào chỉ tình cảm trong gia đình?|Yêu thương|Bút chì|Bơi lội|Yêu thương nói về tình cảm.
Từ nào chỉ hoạt động giúp việc nhà?|Quét nhà|Cái chổi|Sạch sẽ|Quét nhà là hoạt động.
Khi vô ý làm rơi sách của bạn, em nên nói gì?|Xin lỗi bạn|Bạn phải chịu|Tớ đi đây|Xin lỗi và giúp nhặt sách thể hiện trách nhiệm.""",
    ),
    unit(
        "sentences",
        "sentence-patterns",
        "Câu giới thiệu, hoạt động và đặc điểm",
        "Câu có thể giới thiệu ai là gì, kể ai làm gì hoặc nói ai thế nào. Phân biệt bằng nội dung câu thay vì chỉ nhìn một từ.",
        "Mẹ em là bác sĩ: giới thiệu. Mẹ đọc sách: hoạt động. Mẹ rất dịu dàng: đặc điểm.",
        "Câu cần nêu được một ý rõ ràng.",
        "Tìm người hoặc vật được nói đến.|Đọc phần còn lại để xem giới thiệu, hoạt động hay đặc điểm.|Thử đặt câu hỏi tương ứng với nội dung.",
        """Câu nào giới thiệu người?|Anh em là sinh viên.|Anh em chạy bộ.|Anh em vui vẻ.|Câu có 'là sinh viên' giới thiệu anh.
Câu nào kể hoạt động?|Lan vẽ tranh.|Lan là lớp trưởng.|Lan rất hiền.|Vẽ tranh là hoạt động.
Câu nào nói đặc điểm?|Bông hoa thơm.|Bông hoa ở bàn.|Em tưới hoa.|Thơm là đặc điểm của bông hoa.
Trong câu 'Bé đọc truyện', ai thực hiện hoạt động?|Bé|Truyện|Đọc|Bé là người đọc truyện.""",
    ),
    unit(
        "sentences",
        "punctuation",
        "Dấu chấm, hỏi và cảm thán",
        "Dấu chấm kết thúc câu kể. Dấu hỏi kết thúc câu hỏi. Dấu chấm than thường dùng khi bộc lộ cảm xúc hoặc lời gọi, lời yêu cầu mạnh.",
        "Em đi học. Bạn tên là gì? Ôi, bông hoa đẹp quá! Mỗi dấu giúp người đọc hiểu giọng câu.",
        "Chọn dấu theo mục đích của cả câu.",
        "Câu đang kể, hỏi hay bộc lộ cảm xúc?|Đọc thành tiếng để nhận ra giọng câu.|Kiểm tra dấu cuối câu và chữ hoa đầu câu.",
        """Câu 'Bạn sống ở đâu' cần dấu cuối nào?|Dấu hỏi|Dấu phẩy|Dấu hai chấm|Đây là câu hỏi về nơi sống.
Câu 'Em đang viết bài' thường kết thúc bằng dấu nào?|Dấu chấm|Dấu hỏi|Dấu phẩy|Đây là câu kể hoạt động.
Câu 'Ôi, đẹp quá' thể hiện cảm xúc, cần dấu nào?|Dấu chấm than|Dấu phẩy|Dấu hai chấm|Dấu chấm than thể hiện cảm xúc.
Đầu câu mới thường viết thế nào?|Viết hoa chữ cái đầu|Viết thường tất cả|Bỏ chữ đầu|Chữ cái đầu câu cần viết hoa.""",
    ),
    unit(
        "spelling",
        "proper-names",
        "Viết hoa tên riêng và đầu câu",
        "Viết hoa chữ cái đầu mỗi tiếng trong tên người Việt Nam, tên địa lí quen thuộc. Chữ đầu câu cũng viết hoa.",
        "Bạn Trần Ngọc Mai sống ở Hà Nội. Trần, Ngọc, Mai và Hà, Nội đều có chữ cái đầu viết hoa.",
        "Phân biệt tên riêng với từ gọi tên chung.",
        "Tìm tên riêng trong câu.|Tách tên thành từng tiếng và viết hoa chữ cái đầu.|Đọc lại đầu câu, tên người và tên nơi chốn.",
        """Tên người nào viết hoa đúng?|Nguyễn Văn An|nguyễn Văn an|Nguyễn văn an|Mỗi tiếng trong tên người Việt Nam viết hoa chữ đầu.
Tên địa lí nào viết đúng?|Hà Nội|hà nội|Hà nội|Hai tiếng của tên riêng Hà Nội đều viết hoa.
Từ nào trong 'Lan đọc sách' là tên riêng?|Lan|Đọc|Sách|Lan là tên người.
Câu nào viết đầu câu đúng?|Em yêu trường em.|em yêu trường em.|EM yêu trường em.|Chữ E đầu câu viết hoa, các từ chung sau đó viết thường.""",
    ),
    unit(
        "spelling",
        "context-spelling",
        "Chọn chính tả theo nghĩa của câu",
        "Khi phân vân giữa các tiếng gần âm, xem nghĩa và từ đi kèm. Có thể tra từ hoặc hỏi người hướng dẫn; không đoán chỉ dựa vào âm đọc địa phương.",
        "Chân trời là nơi ta nhìn thấy trời và mặt đất như gặp nhau; không viết thành trân trời.",
        "Đọc lại cả cụm từ sau khi chọn tiếng.",
        "Xem câu đang nói về sự vật gì.|Ghép tiếng với từ đi kèm để kiểm tra nghĩa.|Tra từ khi chưa chắc, rồi ghi lại một câu dùng đúng.",
        """Cụm từ nào viết đúng?|Chân trời|Trân trời|Chân chời|Chân trời là cụm từ đúng.
Cụm từ nào gọi nơi chim làm tổ?|Tổ chim|Tỗ chim|Tộ chim|Tổ chim dùng tiếng tổ với dấu hỏi.
Cụm từ nào viết đúng về nụ cười?|Nụ cười|Nụ cườii|Nụ cườiì|Nụ cười là cách viết đúng.
Từ nào điền vào 'Bé ... tay trước khi ăn' đúng nghĩa?|Rửa|Dửa|Giửa|Rửa tay là làm sạch tay bằng nước.""",
    ),
    unit(
        "reading",
        "poem",
        "Đọc thơ: Buổi sáng sân trường",
        "Đọc chậm từng dòng, chú ý hình ảnh và cảm xúc. Có thể ngắt ở cuối dòng nhưng vẫn giữ đúng nghĩa của câu.",
        "Nắng ghé qua ô cửa / Gió lay nhành lá xanh / Tiếng cười vang sân nhỏ / Một ngày mới trong lành. Bốn dòng thơ do VietTree biên soạn nói về buổi sáng vui tươi.",
        "Nêu hình ảnh thật có trong bài thơ để giải thích cảm xúc.",
        "Tìm các từ chỉ cảnh vật và âm thanh.|Đọc lại dòng chứa hình ảnh câu hỏi nhắc đến.|Giải thích cảm xúc bằng chi tiết, không chỉ nói em thích.",
        """Trong bài thơ Buổi sáng sân trường, nắng ghé qua đâu?|Ô cửa|Dòng sông|Mái núi|Dòng đầu viết nắng ghé qua ô cửa.
Điều gì lay nhành lá?|Gió|Mưa|Tuyết|Dòng hai nêu gió lay nhành lá xanh.
Âm thanh nào xuất hiện?|Tiếng cười|Tiếng còi tàu|Tiếng sấm|Dòng ba nêu tiếng cười vang sân nhỏ.
Bài thơ có mấy dòng?|Bốn dòng|Hai dòng|Sáu dòng|Văn bản có bốn dòng thơ.
Cảm xúc phù hợp với bài thơ là gì?|Vui tươi|Sợ hãi|Giận dữ|Nắng, lá xanh và tiếng cười gợi buổi sáng vui tươi.
Hình ảnh nào thực sự có trong bài thơ?|Nhành lá xanh|Ngọn núi trắng|Con thuyền đỏ|Dòng hai có nhành lá xanh.""",
    ),
    unit(
        "reading",
        "instructions",
        "Đọc văn bản hướng dẫn làm hộp bút",
        "Văn bản hướng dẫn có vật liệu và các bước. Thực hiện theo trình tự; dụng cụ sắc cần người lớn hỗ trợ.",
        "Chuẩn bị hộp giấy sạch, giấy màu và hồ dán. Nhờ người lớn cắt phần nắp. Sau đó dán giấy màu bên ngoài, chờ khô rồi đặt bút vào hộp.",
        "Không tự dùng dao, kéo sắc khi chưa có người hướng dẫn.",
        "Tách phần vật liệu và phần bước làm.|Tìm các từ sau đó, rồi để sắp thứ tự.|Kiểm tra bước an toàn có được giữ trong kế hoạch không.",
        """Theo hướng dẫn, hộp giấy cần như thế nào?|Sạch|Ướt|Có thức ăn thừa|Hộp giấy sạch phù hợp để làm hộp bút.
Ai hỗ trợ cắt nắp hộp?|Người lớn|Em tự dùng dao|Không cần ai|Hướng dẫn yêu cầu nhờ người lớn.
Giấy màu được dán ở đâu?|Bên ngoài hộp|Vào ngòi bút|Lên tay|Văn bản nêu dán giấy màu bên ngoài.
Khi nào đặt bút vào hộp?|Khi hồ dán khô|Trước khi dán|Khi giấy còn ướt|Chờ khô trước khi đặt bút.
Vật liệu nào có trong hướng dẫn?|Hồ dán|Sơn xịt|Dây điện|Hồ dán được nêu ở phần chuẩn bị.
ORDER|Sắp xếp ba bước sau khi người lớn đã cắt nắp hộp.|Đặt bút vào hộp~Dán giấy màu~Chờ hồ khô|1~2~0|Dán giấy, chờ khô rồi mới đặt bút.""",
    ),
    unit(
        "vocabulary",
        "comparison",
        "Hình ảnh so sánh trong câu",
        "So sánh giúp hình ảnh sinh động bằng cách tìm nét giống nhau. Các từ như, tựa có thể nối hai sự vật được so sánh.",
        "Mặt trăng tròn như chiếc đĩa. Mặt trăng được so sánh với chiếc đĩa vì cùng gợi dáng tròn.",
        "Nêu cả hai hình ảnh và điểm giống nhau.",
        "Tìm từ như hoặc tựa trong câu.|Xác định hai hình ảnh ở hai bên từ so sánh.|Chỉ ra nét giống nhau phù hợp với câu.",
        """Trong 'Mặt trăng tròn như chiếc đĩa', trăng được so sánh với gì?|Chiếc đĩa|Ngọn núi|Cây bút|Hai hình ảnh là mặt trăng và chiếc đĩa.
Nét giống nhau trong câu so sánh trên là gì?|Dáng tròn|Mùi thơm|Tiếng vang|Từ tròn nêu nét giống nhau.
Từ nào nối hai hình ảnh trong 'Mây trắng như bông'?|Như|Mây|Trắng|Như là từ so sánh trong câu.
Câu nào có hình ảnh so sánh?|Suối trong như gương.|Suối chảy qua rừng.|Em nhìn dòng suối.|Suối được so sánh với gương.
Trong 'Tóc bà trắng như mây', điểm giống nhau là gì?|Màu trắng|Độ cao|Khả năng bay|Tóc và mây được so sánh về màu trắng.
Cách so sánh nào hợp lí về hình dáng?|Lá bàng như chiếc quạt.|Lá bàng như tiếng hát.|Lá bàng như mùi hương.|Lá bàng và chiếc quạt có hình dáng gợi nét giống nhau.""",
    ),
    unit(
        "sentences",
        "dialogue",
        "Dấu hai chấm và gạch ngang trong lời nói",
        "Dấu hai chấm có thể báo trước lời nhân vật. Gạch ngang ở đầu dòng có thể đánh dấu lượt nói trong hội thoại.",
        "Mẹ hỏi:\n– Con đã chuẩn bị sách chưa?\nAn đáp:\n– Con chuẩn bị rồi ạ.",
        "Gạch ngang đầu dòng không phải là dấu gạch nối trong một từ.",
        "Tìm chỗ lời nhân vật bắt đầu.|Quan sát dấu sau từ hỏi, đáp và dấu đầu lượt nói.|Đọc lại hội thoại, xác định ai nói từng câu.",
        """Sau 'Mẹ hỏi' trong ví dụ hội thoại, dấu nào báo trước lời nói?|Dấu hai chấm|Dấu hỏi|Dấu phẩy|Dấu hai chấm báo trước lời nhân vật.
Gạch ngang đầu dòng trong hội thoại dùng để làm gì?|Đánh dấu lời nhân vật|Kết thúc đoạn văn|Viết tên người|Gạch ngang đánh dấu lượt lời.
Trong ví dụ, ai hỏi về việc chuẩn bị sách?|Mẹ|An|Cô giáo|Dòng giới thiệu người hỏi là mẹ.
An trả lời thế nào?|Con chuẩn bị rồi ạ.|Con không có sách.|Mẹ đi đâu?|Đó là lời An đáp trong ví dụ.
Từ 'ạ' trong câu đáp thể hiện điều gì?|Sự lễ phép|Sự giận dữ|Tên đồ vật|An nói ạ để thể hiện lễ phép với mẹ.
Cuối câu 'Con đã chuẩn bị sách chưa' cần dấu nào?|Dấu hỏi|Dấu phẩy|Dấu hai chấm|Đây là câu hỏi của mẹ.""",
    ),
    unit(
        "writing",
        "short-paragraph",
        "Viết đoạn ngắn về một đồ vật",
        "Quan sát một đồ vật quen thuộc. Viết câu giới thiệu, vài đặc điểm rõ và cách em dùng, giữ gìn đồ vật. Có thể viết 4–5 câu theo nhịp của em.",
        "Chiếc cặp của em màu xanh. Cặp có hai ngăn và quai đeo mềm. Em xếp sách vào ngăn lớn. Mỗi tối, em lau cặp và chuẩn bị đồ dùng cho ngày mai.",
        "Đoạn viết cần cùng nói về một đồ vật; không chỉ liệt kê từ rời.",
        "Chọn một đồ vật em thật sự biết.|Lập ba ý: giới thiệu, đặc điểm, cách dùng hoặc giữ gìn.|Đọc lại xem các câu đều nói về đồ vật đó và có dấu cuối câu.",
        """Đoạn mẫu giới thiệu đồ vật nào?|Chiếc cặp|Cây bàng|Bình hoa|Câu đầu giới thiệu chiếc cặp.
Câu nào nêu đặc điểm chiếc cặp trong đoạn mẫu?|Cặp có hai ngăn.|Em đi đá bóng.|Trời hôm nay mưa.|Hai ngăn là đặc điểm của cặp.
Câu nào phù hợp để thêm vào đoạn tả cặp?|Quai cặp giúp em đeo thoải mái.|Con mèo đang ngủ.|Em ăn cơm.|Câu về quai cặp tiếp tục đúng chủ đề.
Câu nào nói cách giữ gìn cặp?|Em lau cặp mỗi tối.|Cặp màu xanh.|Cặp có hai ngăn.|Lau cặp là hoạt động giữ gìn đồ vật.
Trước khi viết tả đồ vật, em nên làm gì?|Quan sát đồ vật|Chép nguyên bài bạn|Viết điều chưa biết|Quan sát giúp có chi tiết thật.
ORDER|Xếp trình tự chuẩn bị và sửa đoạn viết.|Đọc và sửa~Quan sát, lập ý~Viết thành câu|1~2~0|Quan sát lập ý, viết, rồi đọc và sửa.""",
    ),
    unit(
        "writing",
        "message",
        "Viết lời nhắn rõ việc và lịch sự",
        "Lời nhắn ngắn cần người nhận, việc muốn nói và người gửi. Nếu có thời gian hoặc nơi hẹn, viết rõ để người nhận hiểu.",
        "Mẹ ơi, con sang nhà bà cùng bố. Con về lúc 5 giờ chiều. Con chào mẹ. An. Lời nhắn cho biết ai đi, đi đâu, đi cùng ai và lúc về.",
        "Không chia sẻ địa chỉ hoặc số điện thoại riêng vào nơi công khai.",
        "Xác định người sẽ đọc lời nhắn.|Ghi việc chính, thời gian cần thiết và tên người gửi.|Đọc như người nhận để xem còn thiếu thông tin gì.",
        """Lời nhắn trong ví dụ gửi cho ai?|Mẹ|Cô giáo|Bạn Nam|Lời nhắn mở bằng Mẹ ơi.
Ai gửi lời nhắn?|An|Bà|Mẹ|Tên An ở cuối xác định người gửi.
An đi đâu?|Nhà bà|Thư viện|Sân bóng|An viết con sang nhà bà.
An đi cùng ai?|Bố|Bạn|Một mình|Lời nhắn nêu đi cùng bố.
An dự định về lúc nào?|5 giờ chiều|5 giờ sáng|9 giờ tối|Thời gian về được ghi rõ là 5 giờ chiều.
Lời nhắn nên có điều gì?|Việc chính và người gửi|Chỉ hình vẽ|Mọi bí mật gia đình|Việc chính và người gửi giúp người nhận hiểu.""",
    ),
    unit(
        "speaking",
        "listen-retell",
        "Nghe và kể lại việc theo trình tự",
        "Khi nghe người khác kể, tập trung, ghi nhớ người, nơi, việc chính. Kể lại theo thứ tự; nhờ người lớn đọc đoạn mẫu để thực hành nghe thật.",
        "Sáng chủ nhật, Bình nhặt lá ở sân. Sau đó em phân loại lá khô để ủ phân. Cuối cùng em rửa tay. Khi kể lại, giữ đúng ba việc theo thứ tự.",
        "Bài đọc và câu hỏi trên màn hình hỗ trợ chuẩn bị; cần luyện nghe, nói cùng người hướng dẫn.",
        "Nhớ ai làm việc, ở đâu.|Dùng các từ đầu tiên, sau đó, cuối cùng để kể.|So với lời kể gốc; hỏi lại khi chưa nghe rõ.",
        """Trong đoạn mẫu, ai nhặt lá?|Bình|Mai|Cô giáo|Người thực hiện là Bình.
Bình nhặt lá ở đâu?|Sân|Lớp học|Bãi biển|Đoạn mẫu nêu ở sân.
Sau khi nhặt lá, Bình làm gì?|Phân loại lá khô|Đi ngủ ngay|Vẽ tranh|Đoạn mẫu dùng sau đó cho việc phân loại.
Việc cuối cùng là gì?|Rửa tay|Nhặt lá|Chuẩn bị sân|Câu cuối nêu Bình rửa tay.
Khi nghe chưa rõ, nên làm gì?|Nhờ người nói nhắc lại|Tự thêm chuyện|Ngắt lời liên tục|Hỏi lại giúp hiểu đúng nội dung.
ORDER|Sắp ba việc của Bình.|Rửa tay~Nhặt lá~Phân loại lá|1~2~0|Bình nhặt lá, phân loại rồi rửa tay.""",
    ),
    unit(
        "reading",
        "evidence",
        "Suy luận từ chi tiết: Áo mưa của Hòa",
        "Suy luận cần bằng chứng trong đoạn. Phân biệt điều được nói rõ, điều có thể suy ra và điều chưa đủ thông tin.",
        "Hòa nhìn những đám mây xám rồi bỏ áo mưa vào cặp. Trên đường về, mưa bắt đầu rơi. Hòa mặc áo mưa và đi cùng mẹ. Em về nhà với chiếc áo đồng phục khô.",
        "Không biến một phỏng đoán thành sự thật của truyện.",
        "Tìm chi tiết trực tiếp liên quan câu hỏi.|Nối hành động với kết quả; chỉ suy ra điều có bằng chứng.|Thử chỉ ra câu chứng minh, nếu không có thì chưa kết luận.",
        """Hòa mang áo mưa sau khi nhìn thấy gì?|Mây xám|Hoa đỏ|Sân khô|Đoạn đầu nêu những đám mây xám.
Hòa đi về cùng ai?|Mẹ|Bố|Bạn Lan|Truyện viết Hòa đi cùng mẹ.
Vì sao đồng phục của Hòa vẫn khô?|Em mặc áo mưa|Mưa chưa rơi|Em không đi về|Áo mưa che cho đồng phục khi trời mưa.
Nhận xét nào có bằng chứng?|Hòa biết chuẩn bị trước.|Hòa có ba áo mưa.|Hòa ghét mưa.|Em mang áo mưa trước lúc mưa rơi.
Điều nào chưa được truyện cho biết?|Màu áo mưa|Thời điểm mưa rơi|Người đi cùng Hòa|Truyện không nói màu áo mưa.
Hòa mặc áo mưa khi nào?|Khi mưa bắt đầu rơi|Khi ngủ|Khi vào lớp|Trình tự câu chuyện nêu mưa rơi rồi Hòa mặc áo.
MULTI|Chọn các chi tiết có thật trong truyện Áo mưa của Hòa.|Có mây xám~Hòa đi cùng mẹ~Áo mưa màu đỏ~Hòa đi một mình|0~1|Truyện nêu mây xám và đi cùng mẹ, không nêu áo màu đỏ.
Cách nào giúp kiểm tra một suy luận?|Tìm chi tiết làm bằng chứng|Chọn ý nghe hay nhất|Bỏ qua đoạn đọc|Bằng chứng giúp phân biệt suy luận hợp lí và đoán tùy ý.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "reading",
        "logic-books",
        "Đố mẹo đọc hiểu: Ai chọn cuốn nào?",
        "Dùng từng điều kiện để loại trừ. Với ba người và ba sách, mỗi người chọn đúng một cuốn khác nhau; không tự thêm điều kiện.",
        "An, Bình, Chi chọn truyện, thơ và sách cây, mỗi bạn một cuốn. An chọn thơ. Bình không chọn truyện. Vì thơ đã có người chọn, Bình chọn sách cây; Chi chọn truyện.",
        "Mỗi kết luận cần phù hợp đồng thời với tất cả điều kiện.",
        "Lập bảng ba bạn và ba cuốn sách.|Điền điều đã biết trước rồi loại các ô không thể.|Kiểm tra mỗi bạn một cuốn, mỗi cuốn một bạn và mọi điều kiện ban đầu.",
        """Trong ví dụ, An chọn cuốn nào?|Thơ|Truyện|Sách cây|Điều kiện nói rõ An chọn thơ.
Bình không chọn cuốn nào theo điều kiện?|Truyện|Sách cây|Chưa có điều kiện|Điều kiện nêu Bình không chọn truyện.
Bình chọn cuốn nào?|Sách cây|Thơ|Truyện|Thơ thuộc An, Bình không chọn truyện nên còn sách cây.
Chi chọn cuốn nào?|Truyện|Thơ|Sách cây|Hai cuốn còn lại đã được An và Bình chọn.
Có thể cho Bình và An cùng chọn thơ không?|Không, vì mỗi cuốn một bạn|Có, luôn được|Có, không cần điều kiện|Đề quy định ba cuốn khác nhau cho ba bạn.
Để giải bài này, cách nào phù hợp?|Lập bảng và loại trừ|Chọn sách mình thích|Đoán người lớn nhất|Lập bảng giúp theo dõi từng điều kiện.
Điều nào được nói trực tiếp, không cần suy ra?|An chọn thơ|Chi chọn truyện|Bình chọn sách cây|An chọn thơ là điều kiện cho sẵn.
Nếu bỏ điều kiện 'Bình không chọn truyện', biết chắc Bình chọn gì không?|Chưa đủ thông tin|Chắc chắn thơ|Chắc chắn sách cây|Bình có thể chọn truyện hoặc sách cây khi thiếu điều kiện.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "vocabulary",
        "meaning-context",
        "Hiểu từ trong ngữ cảnh và so sánh hợp lí",
        "Một từ có thể xuất hiện ở nhiều ngữ cảnh; đọc cả cụm để hiểu. Khi tạo so sánh, chọn nét giống rõ ràng, tránh ghép hình ảnh không cùng đặc điểm.",
        "Bạn nói nhẹ nhàng: cách nói dịu, không gay gắt. Cặp nhẹ: khối lượng nhỏ. Cùng tiếng nhẹ nhưng ý cụ thể khác nhau.",
        "Giải thích nghĩa theo câu, không tách từ khỏi ngữ cảnh.",
        "Đọc cả câu chứa từ cần hiểu.|Thử diễn đạt lại bằng một cụm từ dễ hiểu.|Kiểm tra nghĩa thay thế vẫn giữ đúng ý của câu.",
        """'Nói nhẹ nhàng' nói về điều gì?|Cách nói dịu dàng|Cân nặng của lời nói|Màu của giọng|Nhẹ nhàng ở đây chỉ cách nói.
'Chiếc cặp nhẹ' nói về điều gì?|Khối lượng cặp nhỏ|Cặp biết nói|Cặp màu nhạt|Nhẹ ở đây là ít nặng.
Câu nào so sánh hợp lí về màu?|Mây trắng như bông.|Mây trắng như tiếng còi.|Mây trắng như vị ngọt.|Mây và bông cùng gợi màu trắng.
Trong 'Bàn tay ấm như nắng', nét so sánh là gì?|Sự ấm áp|Hình tròn|Độ dài|Ấm là điểm được nhấn mạnh.
Từ nào phù hợp 'Bạn ... lắng nghe khi em kể'?|Chăm chú|Cái bàn|Vội vã bỏ đi|Chăm chú diễn tả cách lắng nghe.
Muốn hiểu nghĩa từ khó, nên làm gì trước?|Đọc câu và đoạn quanh từ|Bỏ cả bài|Đếm chữ trong từ|Ngữ cảnh giúp hiểu nghĩa phù hợp.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "sentences",
        "repair-sentences",
        "Sửa câu thiếu ý và chọn dấu câu",
        "Đọc câu để xem đã có ý rõ chưa. Thêm thông tin cần thiết, bỏ phần lặp; dùng dấu phù hợp mục đích kể, hỏi, bộc lộ cảm xúc.",
        "'Bạn Lan ở thư viện đang' còn thiếu hoạt động. Sửa thành 'Bạn Lan đang đọc sách ở thư viện.' Không thêm chi tiết không được yêu cầu vào bài đọc hiểu.",
        "Sửa câu để rõ nghĩa, vẫn giữ ý muốn nói.",
        "Đọc cả câu và hỏi xem còn thiếu điều gì.|Thử thêm hoạt động hoặc sắp lại từ cho rõ ý.|Đọc thành tiếng, kiểm tra chữ hoa và dấu cuối câu.",
        """Câu nào đã diễn đạt rõ hoạt động?|Lan đang đọc sách.|Lan đang.|Đang Lan.|Câu nêu Lan và hoạt động đọc sách đầy đủ.
Câu hỏi nào viết dấu đúng?|Bạn đọc sách gì?|Bạn đọc sách gì,|Bạn đọc sách gì:|Câu hỏi kết thúc bằng dấu hỏi.
Câu nào sửa đúng từ 'Em thích thích vẽ'?|Em thích vẽ.|Em thích thích thích vẽ.|Em vẽ thích thích.|Bỏ từ thích bị lặp giữ được ý câu.
Câu nào có lời gọi và cảm xúc phù hợp?|Ôi, hoa đẹp quá!|Ôi hoa đẹp quá,|ôi hoa đẹp quá?|Chữ đầu hoa và dấu chấm than phù hợp cảm xúc.
Sau 'Cô nói' để báo trước lời nói, dùng dấu nào?|Dấu hai chấm|Dấu phẩy luôn luôn|Dấu hỏi|Dấu hai chấm có thể báo trước lời nói.
Cách sửa bài phù hợp là gì?|Giữ ý chính và làm câu rõ hơn|Thay toàn bộ bằng ý khác|Bỏ hết dấu câu|Sửa câu phải giữ ý định diễn đạt.""",
        vip=True,
    ),
    unit(
        "spelling",
        "edit-notice",
        "Rà soát thông báo ngắn",
        "Thông báo cần người hoặc nhóm được mời, việc, nơi và thời gian rõ. Rà soát chính tả và chữ hoa trước khi gửi.",
        "Thông báo: Lớp 3B đổi sách tại thư viện lúc 15 giờ thứ sáu. Mỗi bạn mang một cuốn truyện sạch, đủ trang. Liên hệ cô Hoa nếu cần hỗ trợ.",
        "Thời gian và địa điểm không được đoán nếu thông báo chưa ghi.",
        "Tìm ai, làm gì, ở đâu, khi nào.|Đọc từng tên riêng và số chỉ thời gian; ghi chỗ còn thiếu.|So lại bản sửa để đảm bảo thông tin chính không thay đổi.",
        """Thông báo mẫu gửi đến nhóm nào?|Lớp 3B|Lớp 5A|Mọi người trong thành phố|Thông báo nêu lớp 3B.
Hoạt động diễn ra ở đâu?|Thư viện|Sân bóng|Nhà bà|Địa điểm là thư viện.
Thời gian được ghi là lúc nào?|15 giờ thứ sáu|15 giờ thứ hai|5 giờ sáng|Thông báo viết 15 giờ thứ sáu.
Mỗi bạn mang gì?|Một truyện sạch, đủ trang|Ba sách rách|Một quả bóng|Yêu cầu mang một cuốn truyện sạch đủ trang.
Tên người hỗ trợ nào viết đúng?|Cô Hoa|cô hoa|Cô hoa|Hoa là tên riêng cần viết hoa.
Nếu thông báo thiếu địa điểm, nên làm gì?|Hỏi người phụ trách|Tự đoán nơi gần nhất|Bỏ thông báo|Cần hỏi để có thông tin chính xác.
MULTI|Chọn hai thông tin cần thiết của một thông báo hẹn gặp.|Thời gian~Địa điểm~Màu tóc người gửi~Món ăn yêu thích|0~1|Thời gian và địa điểm giúp người nhận đến đúng hẹn.
Vì sao phải đọc lại sau khi sửa chính tả?|Để giữ đúng thông tin ban đầu|Để thay giờ tùy ý|Để bỏ tên người nhận|Rà soát giúp sửa chữ mà không làm sai nội dung.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "writing",
        "recount",
        "Viết đoạn kể việc tốt và sửa trình tự",
        "Kể một việc thật với người tham gia, thời điểm, các bước và cảm xúc. Bài mẫu giúp lập ý; em cần viết trải nghiệm của chính mình.",
        "Chiều hôm qua, em thấy bạn đánh rơi sách. Em nhặt sách và đưa lại cho bạn. Bạn mỉm cười cảm ơn. Em vui vì đã giúp bạn một việc nhỏ.",
        "Tránh ghép nhiều việc không liên quan trong một đoạn kể ngắn.",
        "Chọn một việc em có thể kể rõ.|Lập các ý trước, trong và sau việc; thêm cảm xúc có lí do.|Đọc lại thứ tự và bỏ chi tiết không liên quan.",
        """Việc tốt trong đoạn mẫu là gì?|Nhặt và trả sách|Giấu sách|Mua bóng|Người kể giúp nhặt và trả sách cho bạn.
Việc gì xảy ra trước khi em nhặt sách?|Bạn đánh rơi sách|Bạn cảm ơn|Em đi ngủ|Sách phải rơi trước khi được nhặt.
Câu nào nêu cảm xúc có lí do?|Em vui vì đã giúp bạn.|Em ở sân.|Cuốn sách màu xanh.|Câu nói rõ cảm xúc vui và lí do.
ORDER|Xếp các ý kể việc trả sách.|Bạn cảm ơn~Em trả sách~Bạn đánh rơi sách|2~1~0|Sách rơi, được trả, rồi bạn cảm ơn.
Câu nào không liên quan đến đoạn kể trả sách?|Cá vàng bơi trong bể.|Em nhặt sách.|Bạn cảm ơn em.|Câu về cá vàng không liên quan việc đang kể.
Khi viết việc tốt của mình, em nên làm gì?|Kể việc thật bằng lời của mình|Chép tên bạn vào bài mẫu|Thêm điều không xảy ra|Bài viết nên dựa trên trải nghiệm thật.
Kết đoạn có thể nêu điều gì?|Cảm xúc hoặc điều em học được|Danh sách mọi đồ chơi|Một việc hoàn toàn khác|Cảm xúc hoặc bài học gắn với việc kể giúp kết đoạn.
Sau khi viết, nên kiểm tra gì?|Trình tự, ý câu và dấu câu|Chỉ số dòng|Chỉ màu mực|Những kiểm tra này giúp đoạn kể rõ và đúng.""",
        vip=True,
    ),
    unit(
        "writing",
        "letter",
        "Viết thư ngắn cho người thân",
        "Thư ngắn có lời chào, thăm hỏi, điều muốn kể và lời kết, tên người gửi. Xưng hô lễ phép, thể hiện cảm xúc thật.",
        "Bà kính yêu! Dạo này bà có khỏe không ạ? Cháu vừa biết tự chuẩn bị cặp sách. Cháu mong sớm được về thăm bà. Cháu chúc bà khỏe. Cháu của bà, Mai.",
        "Không đăng địa chỉ riêng của người thân trong thư chia sẻ công khai.",
        "Xác định người nhận và cách xưng hô.|Lập ý thăm hỏi, kể một việc, gửi lời chúc.|Đọc lại xem có lời chào, lời kết và tên người gửi.",
        """Thư mẫu gửi cho ai?|Bà|Cô thủ thư|Bạn Bình|Lời đầu là Bà kính yêu.
Người gửi thư là ai?|Mai|Bà|Bố|Thư kết bằng tên Mai.
Câu nào là lời thăm hỏi?|Dạo này bà có khỏe không ạ?|Cháu vừa chuẩn bị cặp.|Cháu của bà, Mai.|Đây là câu hỏi thăm sức khỏe bà.
Mai kể việc gì?|Biết tự chuẩn bị cặp|Đi tàu hôm qua|Trồng cây ở trường|Nội dung thư nêu tự chuẩn bị cặp.
Lời kết nào phù hợp thư cho bà?|Cháu chúc bà khỏe.|Bạn đi ngay đi.|Không cần hồi âm!|Lời chúc thể hiện sự quan tâm và lễ phép.
Khi viết thư, điều nào cần có?|Tên người gửi|Mật khẩu tài khoản|Mọi thông tin riêng|Tên người gửi giúp người nhận biết ai viết.""",
        vip=True,
    ),
    unit(
        "speaking",
        "discussion",
        "Thảo luận và giải thích bằng chứng",
        "Nêu ý kiến ngắn, giải thích bằng lí do. Lắng nghe hết lượt, hỏi rõ điều chưa hiểu; có thể khác ý nhưng vẫn tôn trọng.",
        "Nhóm chọn nơi đặt góc đọc. Lan đề nghị gần cửa sổ vì đủ ánh sáng. Bình nhắc tránh lối đi để an toàn. Nhóm kiểm tra hai điều trước khi quyết định.",
        "Đề xuất tốt cần lí do và chú ý nhu cầu chung.",
        "Xác định vấn đề cả nhóm cần quyết định.|Nêu một phương án với lí do rõ, rồi nghe ý bạn.|Kiểm tra phương án theo các điều kiện đã thống nhất.",
        """Nhóm trong ví dụ thảo luận việc gì?|Nơi đặt góc đọc|Màu áo mưa|Tên con mèo|Vấn đề là chọn nơi đặt góc đọc.
Lan chọn gần cửa sổ vì sao?|Đủ ánh sáng|Không ai đọc|Có nhiều nước|Lan nêu lí do đủ ánh sáng.
Bình nhắc điều gì?|Tránh lối đi để an toàn|Chặn cửa ra vào|Bỏ hết sách|Điều Bình nhắc là an toàn lối đi.
Khi bạn đang nêu ý kiến, em nên làm gì?|Lắng nghe hết lượt|Nói át bạn|Bỏ đi|Nghe hết lượt thể hiện tôn trọng.
Nếu khác ý, cách nói nào phù hợp?|Mình đề xuất cách khác vì...|Bạn luôn sai.|Mình không nghe đâu.|Nêu cách khác với lí do giúp trao đổi rõ và tôn trọng.
Phương án nhóm chọn nên đáp ứng điều gì?|Đủ sáng và tránh lối đi|Chỉ đẹp dù chặn cửa|Chỉ theo ý một bạn|Cần kết hợp hai điều kiện mà nhóm đã nêu.""",
        vip=True,
        thinking=True,
    ),
]
