"""Editorial corrections: the activity must teach the skill named in its title."""

SCENES = {
    "around": "Cùng xem máy nhận thông tin gì và bạn nhỏ kiểm tra điều gì.",
    "data": "Trên bàn có các thẻ mẫu. Em xem từng thẻ rồi chọn nhóm phù hợp.",
    "prompt": "Robot cần một lời nhắc rõ. Em chọn lời nhắc nói đủ việc cần làm.",
    "math": "Robot đưa ra một gợi ý. Em tự đếm hoặc tính để kiểm tra.",
    "vietnamese": "Cùng đọc tên thẻ và xem tranh. Em tìm chi tiết giúp mình lựa chọn.",
    "english": "Cùng xem tranh và đọc từ tiếng Anh. Em đối chiếu từ với tranh.",
    "creative": "Em chuẩn bị một sản phẩm nhỏ. Cùng xem ý nào giúp sản phẩm dễ hiểu.",
    "safety": "Robot gặp một yêu cầu mới. Em chọn cách giữ an toàn cho mình.",
    "project": "Em làm thử với thẻ mẫu. Cùng chọn việc cần làm và cách kiểm tra.",
}

YOUNG_GOALS = {
    "around": "Nói máy giúp mình việc gì.",
    "data": "Xếp thẻ vào nhóm phù hợp.",
    "prompt": "Chọn lời nhắc nói rõ một việc.",
    "math": "Tự đếm hoặc tính để kiểm tra.",
    "vietnamese": "Tìm chi tiết trong tranh và lời kể.",
    "english": "Ghép từ tiếng Anh với tranh.",
    "creative": "Chọn một cách làm sản phẩm dễ hiểu.",
    "safety": "Chọn cách giữ thông tin riêng.",
    "project": "Làm thử và nói điều cần sửa.",
}


def task(grade, unit, variant, original):
    correct, retry = ("Đúng", "Thử lại") if grade <= 2 else ("Có căn cứ", "Cần kiểm tra")
    revisions = {
        (1, "around", 2): (
            "Máy gợi ý tên con vật. Bạn nhỏ xem tranh để kiểm tra.",
            [("Máy gợi ý tên mèo", "Máy hỗ trợ"), ("Bạn nhỏ kiểm tra tranh", "Con người")],
        ),
        (1, "around", 3): (
            "Máy có thể gọi nhầm tên. Em đối chiếu với tranh.",
            [("Máy gọi mèo, tranh là mèo", correct), ("Máy gọi mèo, tranh là chó", retry)],
        ),
        (1, "vietnamese", 1): (
            "Hai tranh kể hai việc theo thứ tự: nhặt hạt trước, gieo hạt sau.",
            [("Nhặt hạt", "Trước"), ("Gieo hạt", "Sau")],
        ),
        (1, "vietnamese", 2): (
            "Nhân vật là người hoặc con vật trong truyện. Hai thẻ có mèo và thỏ.",
            [("Mèo ngồi đọc sách", "Mèo"), ("Thỏ đang tưới cây", "Thỏ")],
        ),
        (1, "english", 1): (
            "cat là mèo; dog là chó. Nhìn tranh và kiểm tra tên.",
            [("Mèo: cat", correct), ("Chó: cat", retry)],
        ),
        (1, "english", 2): (
            "red là đỏ; blue là xanh dương. Từ cần khớp màu của vật.",
            [("Táo đỏ: red", correct), ("Cặp xanh dương: red", retry)],
        ),
        (2, "math", 0): (
            "Ba nhóm, mỗi nhóm có hai chấm: đếm 2, 4, 6.",
            [("Ba nhóm hai chấm: 6", correct), ("Ba nhóm hai chấm: 5", retry)],
        ),
        (2, "math", 1): (
            "Cộng 8 với 6 được 14. Em có thể tách 6 thành 2 và 4 để tính.",
            [("8 + 6 = 14", correct), ("8 + 6 = 13", retry)],
        ),
        (2, "math", 2): (
            "Dãy bắt đầu từ 2, mỗi bước thêm 2. Em kiểm tra từng bước.",
            [("2, 4, 6, 8; mỗi bước thêm 2", correct), ("2, 4, 6, 9; mỗi bước thêm 2", retry)],
        ),
        (2, "vietnamese", 0): (
            "Gọi đúng tên đồ vật trong tranh trước khi dùng lời gợi ý.",
            [("Quyển sách", "Sách"), ("Chiếc bút chì", "Bút chì"), ("Chiếc cặp", "Cặp")],
        ),
        (2, "vietnamese", 2): (
            "Đọc câu rồi đối chiếu với việc được ghi trong thẻ tranh.",
            [
                ("Tranh: mèo ngồi. Câu: Mèo ngồi.", correct),
                ("Tranh: mèo ngồi. Câu: Mèo bay.", retry),
            ],
        ),
        (2, "english", 1): (
            "apple là táo; orange là cam; banana là chuối. Kiểm tra từ theo tranh.",
            [("Táo: apple", correct), ("Cam: orange", correct), ("Chuối: cat", retry)],
        ),
        (2, "english", 2): (
            "book là sách; pencil là bút chì; bag là cặp. Cùng kiểm tra đồ dùng.",
            [("Sách: book", correct), ("Bút chì: pencil", correct), ("Cặp: cat", retry)],
        ),
        (3, "math", 2): (
            "Bảng mẫu ghi: tổ Một 4 cây, tổ Hai 6 cây, tổ Ba 5 cây. Đối chiếu đúng hàng.",
            [
                ("Bảng: 4, 6, 5 cây. Tổ Hai có 6 cây.", correct),
                ("Bảng: 4, 6, 5 cây. Tổ Ba có 6 cây.", retry),
            ],
        ),
        (3, "english", 1): (
            "cat là mèo; dog là chó; bird là chim. Kiểm tra từng nhãn con vật.",
            [("Mèo: cat", correct), ("Chó: dog", correct), ("Chim: cat", retry)],
        ),
        (3, "english", 3): (
            "Đoạn mẫu: The cat is on the chair. Nghĩa là mèo ở trên ghế.",
            [
                ("Mẫu: cat on chair. The cat is on the chair.", correct),
                ("Mẫu: cat on chair. The cat is under the chair.", retry),
            ],
        ),
        (5, "vietnamese", 0): (
            "Đoạn mẫu: Lớp chăm góc đọc. Các bạn xếp sách, lau bàn và đặt cây nhỏ. Ý chính là việc chăm góc đọc; xếp sách là một chi tiết.",
            [
                ("Lớp chăm góc đọc", "Ý chính"),
                ("Các bạn xếp sách", "Chi tiết"),
                ("Các bạn lau bàn", "Chi tiết"),
            ],
        ),
        (5, "vietnamese", 3): (
            "Bản nháp: Em tưới cây. Cây rất rất xanh. Sửa từ lặp, giữ việc tưới cây và ý tả màu lá.",
            [
                ("Bỏ một từ rất bị lặp", "Giữ ý, sửa cách viết"),
                ("Đổi thành em đi bơi", "Làm đổi ý ban đầu"),
            ],
        ),
        (5, "vietnamese", 1): (
            "Truyện mẫu: Mai thấy sách bị rách. Bạn cùng cô dán lại trang sách. Cuối buổi, sách được đặt ngay ngắn lên kệ. Sắp các ý theo việc xảy ra.",
            [
                ("Mai thấy sách bị rách", "Mở đầu"),
                ("Mai cùng cô dán trang sách", "Diễn biến"),
                ("Sách được đặt lại lên kệ", "Kết thúc"),
            ],
        ),
        (5, "vietnamese", 2): (
            "Đoạn mẫu: Mai mượn sách ở thư viện. Trong truyện tưởng tượng, quyển sách mọc cánh bay lên. Phân biệt việc của Mai với chi tiết hư cấu trong truyện.",
            [
                ("Mai mượn sách theo đoạn mẫu", "Thông tin trong đoạn"),
                ("Sách mọc cánh trong truyện", "Chi tiết hư cấu"),
            ],
        ),
        (5, "math", 3): (
            "Bạn nói nhân với 1,5 luôn làm số nhỏ đi. Thử 3 × 1,5 = 4,5: kết quả lớn hơn 3. Một ví dụ này đủ bác bỏ lời khẳng định luôn nhỏ đi.",
            [("3 × 1,5 = 4,5; 4,5 lớn hơn 3", correct), ("3 × 1,5 phải nhỏ hơn 3", retry)],
        ),
        (5, "english", 3): (
            "Đoạn mẫu: There are two books on the desk. Có hai quyển sách trên bàn.",
            [
                ("Mẫu: two books on desk. There are two books.", correct),
                ("Mẫu: two books on desk. There is one book.", retry),
                ("Mẫu: two books on desk. The books are on the desk.", correct),
            ],
        ),
    }
    if grade in {3, 5}:
        revisions[grade, "safety", 1] = (
            "Một bức ảnh đẹp chưa đủ chứng minh lời kể đúng. Tìm nguồn và đối chiếu thêm trước khi chia sẻ.",
            [
                ("Xem nguồn ảnh và hỏi cô", "Có kiểm tra"),
                ("Chia sẻ chỉ vì ảnh đẹp", "Cần dừng lại"),
            ],
        )
        revisions[grade, "safety", 2] = (
            "Tôn trọng người tạo. Dùng hình được phép, ghi nguồn theo hướng dẫn của cô và nói rõ phần mình tự làm.",
            [
                ("Ảnh được phép dùng và có ghi người vẽ", "Dùng có trách nhiệm"),
                ("Nhận ảnh của bạn là do mình vẽ", "Cần sửa"),
            ],
        )
    if grade == 2:
        revisions[2, "around", 1] = (
            "Trong ví dụ, máy gợi ý tên con vật từ hình. Em xem lại con vật thật sự trong tranh.",
            [("Tranh mèo, máy gọi mèo", correct), ("Tranh chó, máy gọi mèo", retry)],
        )
        revisions[2, "creative", 0] = (
            "Tấm thiệp cảm ơn cần có lời ngắn, rõ và lịch sự.",
            [("Thiệp: Em cảm ơn cô", "Rõ ràng"), ("Thiệp: Chữ đè lên nhau", "Cần sửa")],
        )
        revisions[2, "creative", 1] = (
            "Ba tranh kể theo thứ tự: nhặt hạt, gieo hạt, cây mọc.",
            [("Nhặt hạt", "Đầu"), ("Gieo hạt", "Giữa"), ("Cây mọc", "Cuối")],
        )
        revisions[2, "creative", 2] = (
            "Poster nhắc một việc rõ. Chữ ngắn, dễ đọc giúp người xem hiểu.",
            [
                ("Poster: Cất sách lên kệ", "Dễ hiểu"),
                ("Poster: Chữ quá nhỏ, chồng nhau", "Cần sửa"),
            ],
        )
    if grade == 3:
        revisions[3, "creative", 0] = (
            "Chọn một việc cụ thể cho robot giấy. Nêu cách biết việc đã làm đúng.",
            [
                ("Robot xếp thẻ sách và bút", "Việc cụ thể"),
                ("Robot biết tất cả mọi thứ", "Quá rộng"),
            ],
        )
        revisions[3, "creative", 1] = (
            "Poster nêu một thông điệp rõ. Người xem biết cần làm gì sau khi đọc.",
            [
                ("Poster: Cất sách đúng kệ", "Rõ một việc"),
                ("Poster có nhiều chữ chồng nhau", "Cần sửa"),
            ],
        )
        revisions[3, "creative", 2] = (
            "Truyện gồm ba sự kiện nối tiếp: nhặt hạt, gieo hạt rồi cây mọc.",
            [("Nhặt hạt", "Đầu"), ("Gieo hạt", "Giữa"), ("Cây mọc", "Cuối")],
        )
        revisions[3, "creative", 3] = (
            "So sánh trước và sau khi sửa đúng lỗi đã thấy. Cho bạn thử lại để kiểm tra.",
            [
                ("Trước chữ nhỏ; sau tăng chữ và thử đọc", "Sửa đúng lỗi"),
                ("Trước chữ nhỏ; sau chỉ đổi màu", "Chưa sửa lỗi chữ"),
            ],
        )
    if grade == 5:
        revisions[5, "safety", 3] = (
            "Tự làm phần em đã biết. Khi vướng, nêu chỗ chưa hiểu và xin một gợi ý; em vẫn tự hoàn thành.",
            [
                ("Tự tính rồi xin gợi ý khi cần", "Chủ động học"),
                ("Nhờ máy làm hết để chép", "Cần thay đổi"),
            ],
        )
        revisions[5, "creative", 0] = (
            "Thiết kế cho người dùng cần biết họ gặp khó ở đâu. Bạn dùng điện thoại cần chữ rõ, nút dễ bấm.",
            [
                ("Bạn khó đọc: tăng chữ và thử lại", "Phù hợp người dùng"),
                ("Thêm nhiều nút nhỏ hơn", "Cần sửa"),
            ],
        )
        revisions[5, "creative", 1] = (
            "Poster cần tiêu chí kiểm tra: một việc rõ, chữ dễ đọc và người xem biết nên làm gì.",
            [
                ("Poster: Tắt vòi sau khi dùng, chữ rõ", "Đạt tiêu chí"),
                ("Poster không nêu việc cần làm", "Cần sửa"),
            ],
        )
        revisions[5, "creative", 2] = (
            "Kịch bản mẫu: Mai thấy vòi rỉ nước, báo cô phụ trách, rồi cùng bạn làm biển nhắc. Xếp sự kiện theo quan hệ trước sau.",
            [
                ("Mai thấy vòi rỉ", "Mở đầu"),
                ("Mai báo cô phụ trách", "Diễn biến"),
                ("Các bạn làm biển nhắc", "Kết thúc"),
            ],
        )
        revisions[5, "creative", 3] = (
            "Sau góp ý, sửa một điểm rồi cho bạn thử lại theo cùng tiêu chí. Ghi điều thực sự quan sát được.",
            [
                ("Tăng chữ, nhờ bạn đọc lại", "Có thử sau khi sửa"),
                ("Đổi màu rồi nói chắc đã tốt", "Chưa kiểm tra lại"),
            ],
        )
    return revisions.get((grade, unit, variant), original)


def reviewed_art(row):
    return row["number"] <= 36 and row["unit_code"].split("-")[-1] in {
        "around",
        "data",
        "math",
        "vietnamese",
        "english",
        "creative",
        "safety",
    }
