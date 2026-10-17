"""Original, unplugged investigations: one open activity and one VIP challenge per grade."""

from app.academy.curriculum import activity, lesson, quiz


def investigation(grade, number, title, scene, concept, pairs, questions, hints, application):
    row = lesson(
        number,
        title,
        scene,
        concept,
        activity(
            "fact_check" if number == 37 else "train",
            "Đọc từng thẻ rồi chọn cách kiểm tra phù hợp.",
            pairs,
            concept,
            hints=hints,
        ),
        [quiz(*question) for question in questions],
        "Dùng thẻ mẫu, không dùng dữ liệu cá nhân. Đọc cùng trẻ lớp 1–2. "
        "Cho trẻ chỉ căn cứ trước khi chọn; cho phép đếm, vẽ hoặc nói thay cho viết. "
        "Đây là tình huống biên soạn sẵn, không phải kết quả từ mô hình thật.",
        "Tự tạo một thẻ có lỗi và nói cách kiểm tra. Không dùng tên hay ảnh của bạn.",
        application,
    )
    row.update(
        grade=grade,
        code=f"AI{grade}-{number}",
        unit_code=f"AI{grade}-verify",
        unit_title="Thử nghiệm và kiểm chứng",
        unit_position=10,
        position=number - 36,
        objectives=[
            "Tìm căn cứ trong thẻ mẫu.",
            "Chọn cách kiểm tra kết quả.",
            "Nói khi em chưa chắc.",
        ],
    )
    return row


def records():
    return [
        investigation(
            1,
            37,
            "Đếm lại cùng robot",
            "Robot nói 2 + 3 = 6. Em lấy hai que và ba que để thử.",
            "Gộp 2 que với 3 que được 5 que. Robot trong truyện đã nói sai.",
            [("2 + 3 = 6", "Đếm lại"), ("2 + 3 = 5", "Khớp với que tính")],
            [
                (
                    "Gộp 2 que với 3 que được mấy que?",
                    "5 que",
                    "6 que",
                    "Đếm lần lượt: 1, 2, 3, 4, 5.",
                ),
                (
                    "Robot nói gì cũng đúng phải không?",
                    "Không",
                    "Có",
                    "Kết quả của công cụ vẫn cần kiểm tra.",
                ),
                (
                    "Em dùng gì để kiểm tra phép cộng?",
                    "Que tính",
                    "Màu vỏ robot",
                    "Que tính giúp em đếm lại số lượng.",
                ),
            ],
            [
                "Lấy hai nhóm que.",
                "Đếm cả hai nhóm từ 1.",
                "Đối chiếu số que với kết quả trên thẻ.",
            ],
            "Vẽ hai chấm và ba chấm. Đếm rồi nói kết quả.",
        ),
        investigation(
            1,
            38,
            "Hai màu của quả táo",
            "Bộ thẻ có táo đỏ và táo xanh. Cả hai đều là táo.",
            "Màu khác nhau vẫn có thể cùng loại. Chỉ nhìn màu chưa đủ để gọi tên quả.",
            [("Quả táo xanh", "Táo"), ("Chiếc bút đỏ", "Không phải táo")],
            [
                (
                    "Quả táo xanh có thuộc nhóm táo không?",
                    "Có",
                    "Không",
                    "Táo có thể có nhiều màu.",
                ),
                (
                    "Chiếc bút đỏ có phải quả táo không?",
                    "Không",
                    "Có",
                    "Cùng màu đỏ nhưng bút và táo khác loại.",
                ),
                (
                    "Bộ thẻ nào có hai màu táo?",
                    "Táo đỏ và táo xanh",
                    "Chỉ táo đỏ",
                    "Hai màu giúp bộ ví dụ đa dạng hơn.",
                ),
            ],
            [
                "Nhìn cả vật, không chỉ màu.",
                "So hình quả táo và chiếc bút.",
                "Thử thêm thẻ táo xanh vào nhóm táo.",
            ],
            "Vẽ hai quả táo khác màu và gọi tên nhóm của chúng.",
        ),
        investigation(
            2,
            37,
            "Đọc lại lời chỉ dẫn",
            "Thẻ mẫu ghi: đặt bút cạnh sách. Robot lại nói: đặt bút trong cặp.",
            "Đọc lại thẻ gốc để biết yêu cầu. Lời gợi ý của robot có thể khác thẻ gốc.",
            [("Bút cạnh sách", "Đúng thẻ gốc"), ("Bút trong cặp", "Cần sửa")],
            [
                (
                    "Theo thẻ gốc, bút đặt ở đâu?",
                    "Cạnh sách",
                    "Trong cặp",
                    "Thẻ gốc ghi rõ: đặt bút cạnh sách.",
                ),
                (
                    "Lời robot khác thẻ gốc, em làm gì?",
                    "Đọc lại thẻ gốc",
                    "Làm theo robot ngay",
                    "Đọc lại giúp tìm chỗ khác nhau.",
                ),
                (
                    "Không hiểu từ 'cạnh', em nên làm gì?",
                    "Nhờ người lớn chỉ bằng vật mẫu",
                    "Đoán rồi bỏ qua",
                    "Có thể nhờ chỉ vị trí bằng bút và sách.",
                ),
            ],
            [
                "Tìm đồ vật trên thẻ gốc.",
                "Tìm từ chỉ vị trí.",
                "Dùng bút và sách đặt thử rồi đối chiếu.",
            ],
            "Đặt bút cạnh sách. Nói một câu tả vị trí của bút.",
        ),
        investigation(
            2,
            38,
            "Nhãn nào cần sửa?",
            "Bộ thẻ mẫu có hình mèo, chó và cam. Một thẻ bị dán nhầm tên.",
            "Nhãn là tên nhóm gắn cho mẫu. Cần sửa nhãn sai trước khi dùng bộ mẫu.",
            [
                ("Hình mèo, nhãn con vật", "Giữ nhãn"),
                ("Hình cam, nhãn con vật", "Sửa nhãn"),
                ("Hình chó, nhãn con vật", "Giữ nhãn"),
            ],
            [
                ("Thẻ cam nên có nhãn nào?", "Trái cây", "Con vật", "Cam thuộc nhóm trái cây."),
                (
                    "Thẻ mèo, nhãn con vật có cần sửa không?",
                    "Không cần",
                    "Cần sửa",
                    "Nhãn con vật phù hợp với hình mèo.",
                ),
                (
                    "Thấy nhãn sai trong bộ mẫu, em làm gì?",
                    "Sửa và kiểm tra lại",
                    "Thêm nhiều bản sao nhãn sai",
                    "Lặp lại nhãn sai không làm mẫu chính xác hơn.",
                ),
            ],
            [
                "Nhìn hình rồi đọc nhãn.",
                "Cam là trái cây, mèo và chó là con vật.",
                "Sửa nhãn không khớp hình trước khi dùng bộ mẫu.",
            ],
            "Vẽ ba đồ vật và nhờ người lớn cùng kiểm tra nhãn.",
        ),
        investigation(
            3,
            37,
            "Thử bằng thẻ chưa gặp",
            "Máy mẫu đã xem thẻ mèo A và chó B. Ta cất thẻ mèo C để thử sau.",
            "Thẻ dùng để học và thẻ dùng để thử cần tách riêng. Làm đúng thẻ đã xem chưa chứng tỏ làm đúng thẻ mới.",
            [
                ("Mèo A: đã dùng để học", "Bộ học"),
                ("Chó B: đã dùng để học", "Bộ học"),
                ("Mèo C: để riêng, chưa cho xem", "Bộ thử"),
                ("Chó D: để riêng, chưa cho xem", "Bộ thử"),
            ],
            [
                (
                    "Nên thử bằng thẻ nào để xem khả năng với mẫu mới?",
                    "Mèo C để riêng",
                    "Mèo A đã học",
                    "Mèo C chưa được dùng để học.",
                ),
                (
                    "Đúng mọi thẻ đã học có chắc đúng mọi thẻ mới?",
                    "Chưa chắc",
                    "Chắc chắn",
                    "Công cụ có thể nhớ mẫu nhưng nhầm với mẫu khác.",
                ),
                (
                    "Sau khi dùng mèo C để sửa bộ học, cần làm gì?",
                    "Chuẩn bị thẻ thử mới",
                    "Vẫn gọi C là thẻ chưa từng học",
                    "Khi đã dùng để sửa bộ học, C không còn là mẫu thử chưa gặp.",
                ),
            ],
            [
                "Tìm thẻ ghi 'đã dùng để học'.",
                "Để riêng thẻ chưa cho máy mẫu xem.",
                "Nếu đưa thẻ thử vào bộ học, hãy chọn thẻ mới để thử tiếp.",
            ],
            "Vẽ bốn thẻ, chia bộ học và bộ thử trước khi chơi phân loại.",
        ),
        investigation(
            3,
            38,
            "Không đoán quả chỉ từ màu",
            "Bộ học có toàn táo đỏ và cam màu cam. Thử thêm táo xanh và bút đỏ.",
            "Công cụ có thể dựa nhầm vào màu. Thêm mẫu khác màu và khác loại rồi thử lại; thêm mẫu không bảo đảm luôn đúng.",
            [
                ("Táo xanh chưa có trong bộ học", "Thêm mẫu đa dạng"),
                ("Bút đỏ bị gọi là táo", "Kiểm tra đặc điểm"),
                ("Bản sao y hệt táo đỏ đã có", "Chưa thêm dạng mới"),
                ("Cam trên nền khác", "Thêm mẫu đa dạng"),
            ],
            [
                (
                    "Bút đỏ bị gọi là táo gợi ý lỗi gì?",
                    "Có thể dựa nhầm vào màu",
                    "Mọi vật đỏ đều là táo",
                    "Cần kiểm tra thêm trước khi kết luận nguyên nhân.",
                ),
                (
                    "Mẫu nào giúp có thêm dạng táo?",
                    "Táo xanh",
                    "Bản sao thẻ táo đỏ",
                    "Táo xanh bổ sung màu chưa có.",
                ),
                (
                    "Sau khi thêm mẫu, có cần thử lại không?",
                    "Có, bằng thẻ để riêng",
                    "Không, chắc chắn luôn đúng",
                    "Mẫu đa dạng hữu ích nhưng vẫn cần kiểm tra kết quả.",
                ),
            ],
            [
                "Đọc loại vật và màu của mỗi thẻ.",
                "Tìm dạng mẫu bộ học chưa có.",
                "Thử cả táo xanh lẫn vật đỏ không phải táo.",
            ],
            "Nói một cách làm bộ thẻ đa dạng hơn mà không dùng ảnh người.",
        ),
        investigation(
            4,
            37,
            "Hai cách kiểm tra phép tính",
            "Robot viết 6 × 7 = 40. Em tính bằng bảng nhân và phép cộng các nhóm.",
            "6 × 7 = 42. Có thể cộng sáu số 7 để kiểm tra; lời giải dài hay giọng tự tin không thay thế phép tính.",
            [
                ("6 × 7 = 40", "Cần sửa"),
                ("7 + 7 + 7 + 7 + 7 + 7 = 42", "Có căn cứ tính"),
                ("Đúng vì robot nói rất tự tin", "Chưa có căn cứ"),
                ("6 × 7 = 42", "Có căn cứ tính"),
            ],
            [
                ("Kết quả đúng của 6 × 7 là bao nhiêu?", "42", "40", "7 + 7 + 7 + 7 + 7 + 7 = 42."),
                (
                    "Cách nào kiểm tra độc lập với lời robot?",
                    "Tự tính và đối chiếu bảng nhân",
                    "Hỏi robot lặp lại y nguyên",
                    "Tự tính tạo căn cứ thay vì lặp lại một khẳng định.",
                ),
                (
                    "Nếu chưa kiểm tra xong, em nên nói gì?",
                    "Em cần kiểm tra thêm",
                    "Chắc chắn đúng",
                    "Nêu điều chưa chắc giúp tránh lan truyền kết quả sai.",
                ),
            ],
            [
                "Tách phép nhân thành các nhóm bằng nhau.",
                "Cộng sáu số 7 hoặc xem bảng nhân.",
                "So kết quả tính lại với 40 trên thẻ robot.",
            ],
            "Chọn một phép nhân đã học và kiểm tra bằng hai cách.",
        ),
        investigation(
            4,
            38,
            "Bộ mẫu đồ dùng công bằng hơn",
            "Máy mẫu nhận đúng bút xanh nhưng nhầm bút đỏ. Bộ học chỉ có bút xanh trên nền trắng.",
            "Thử thay đổi màu bút, góc nhìn và nền. So số đúng ở từng nhóm, không chỉ nhìn tổng số; không dùng kết quả này xếp loại con người.",
            [
                ("Thêm bút đỏ trên nền trắng", "Bổ sung mẫu"),
                ("Thêm bút xanh trên nền khác", "Bổ sung mẫu"),
                ("Chỉ thử bút xanh giống bộ học", "Kiểm tra chưa đủ"),
                ("So kết quả bút đỏ và bút xanh", "Kiểm tra theo nhóm"),
            ],
            [
                (
                    "Mẫu nào bổ sung màu đang thiếu?",
                    "Bút đỏ",
                    "Bản sao bút xanh",
                    "Bộ học chưa có bút đỏ.",
                ),
                (
                    "Đúng nhiều bút xanh có bảo đảm đúng bút đỏ?",
                    "Không bảo đảm",
                    "Luôn bảo đảm",
                    "Các nhóm mẫu có thể cho kết quả khác nhau.",
                ),
                (
                    "Sau khi sửa bộ mẫu, nên làm gì?",
                    "Thử từng nhóm bằng thẻ mới",
                    "Bỏ thử nhóm từng bị nhầm",
                    "Cần kiểm tra cả nhóm trước đây gặp lỗi.",
                ),
            ],
            [
                "Tìm màu hoặc nền còn thiếu.",
                "Ghi riêng số đúng của mỗi nhóm bút.",
                "Bổ sung mẫu rồi thử lại bằng thẻ chưa dùng để học.",
            ],
            "Lập kế hoạch thử bút hai màu và hai nền bằng tranh tự vẽ.",
        ),
        investigation(
            5,
            37,
            "Bốn trên năm chưa phải tất cả",
            "Trong lần thử bằng năm thẻ mới, máy mẫu đúng bốn thẻ và sai một thẻ.",
            "4 trên 5 là 80% trong lần thử này. Không suy ra đúng 80% với mọi dữ liệu; cần ghi rõ bộ thử và xem cả lỗi.",
            [
                ("4 thẻ đúng trên 5 thẻ thử", "Đúng 80% lần thử này"),
                ("Đúng 80% với mọi tình huống", "Kết luận quá rộng"),
                ("Ghi lại thẻ bị nhầm", "Cần kiểm tra lỗi"),
                ("Thử thêm thẻ mới để riêng", "Thu thập thêm căn cứ"),
            ],
            [
                (
                    "4 thẻ đúng trên 5 thẻ là bao nhiêu phần trăm?",
                    "80%",
                    "40%",
                    "4 : 5 × 100% = 80%.",
                ),
                (
                    "Kết luận nào đúng với dữ kiện?",
                    "Đúng 4/5 thẻ của lần thử này",
                    "Luôn đúng 80% ở mọi nơi",
                    "Kết quả chỉ mô tả bộ thử đã dùng.",
                ),
                (
                    "Một thẻ bị sai có nên bỏ khỏi báo cáo?",
                    "Không, cần ghi và tìm hiểu lỗi",
                    "Có, để điểm đẹp hơn",
                    "Báo cáo đủ lỗi giúp đánh giá trung thực.",
                ),
            ],
            [
                "Xác định số đúng và tổng số thẻ.",
                "Tính 4 : 5 rồi đổi sang phần trăm.",
                "Gắn kết quả với bộ thử cụ thể, không với mọi trường hợp.",
            ],
            "Viết một câu báo cáo gồm số đúng, tổng số thẻ và giới hạn kết luận.",
        ),
        investigation(
            5,
            38,
            "Điểm tổng có che một nhóm lỗi?",
            "Bộ thử có 8 bút xanh: đúng 8; 2 bút đỏ: đúng 0. Tổng đúng 8/10.",
            "Tổng đúng 80% nhưng bút đỏ đúng 0/2. Nhóm nhỏ cần thêm mẫu thử phù hợp; chưa đủ căn cứ kết luận với mọi bút đỏ.",
            [
                ("Bút xanh: đúng 8/8", "Kết quả nhóm xanh"),
                ("Bút đỏ: đúng 0/2", "Kết quả nhóm đỏ"),
                ("Chỉ công bố tổng 8/10", "Thiếu thông tin nhóm"),
                ("Thử thêm bút đỏ mới", "Bổ sung kiểm tra"),
            ],
            [
                (
                    "Tỉ lệ đúng chung của lần thử là bao nhiêu?",
                    "80%",
                    "100%",
                    "(8 + 0) : (8 + 2) = 0,8 = 80%.",
                ),
                (
                    "Kết quả với bút đỏ trong lần thử là gì?",
                    "Đúng 0 trong 2 thẻ",
                    "Đúng 80%",
                    "Tổng 80% không phải tỉ lệ đúng của từng nhóm.",
                ),
                (
                    "Có thể kết luận máy sai với mọi bút đỏ không?",
                    "Chưa, mới thử hai thẻ đỏ",
                    "Có, hai thẻ đại diện mọi bút",
                    "Mẫu thử nhỏ chưa đủ cho kết luận với mọi trường hợp.",
                ),
            ],
            [
                "Ghi riêng số đúng và số thử của từng màu.",
                "So 8/8 với 0/2 trước khi nhìn tổng.",
                "Báo cáo cả hai nhóm và bổ sung thẻ thử mới cho nhóm đỏ.",
            ],
            "Vẽ bảng hai nhóm và nêu điều điểm tổng chưa cho biết.",
        ),
    ]
