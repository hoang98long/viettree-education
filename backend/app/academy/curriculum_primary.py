"""Original, age-specific visual courses for grades 1, 2, 3 and 5.

Each topic has four distinct tasks. No provider, camera, typing or training model
is required: children reason about small, explicitly labelled examples.
"""

TITLES = {
    1: {
        "around": [
            "Bạn nhỏ và máy",
            "Mắt nhìn, tai nghe",
            "Máy giúp một việc",
            "Máy cũng có thể nhầm",
        ],
        "data": [
            "Xếp thẻ cùng nhóm",
            "Tìm thẻ khác nhóm",
            "Cùng màu, khác nhóm",
            "Thêm hình mẫu cho máy",
        ],
        "prompt": [
            "Nói một việc rõ ràng",
            "Nói rõ đồ vật",
            "Chọn lời nhắc dễ hiểu",
            "Hỏi lại khi chưa rõ",
        ],
        "math": [
            "Đếm táo cùng robot",
            "Ghép hai nhóm bằng nhau",
            "Chọn phép cộng đúng",
            "Tìm chỗ đếm nhầm",
        ],
        "vietnamese": [
            "Ghép từ với tranh",
            "Kể chuyện hai tranh",
            "Tìm nhân vật trong tranh",
            "Nói lại bằng lời của em",
        ],
        "english": ["Hello, robot!", "Cat or dog?", "Red and blue", "One, two, three"],
        "creative": [
            "Vẽ robot trên giấy",
            "Chọn màu cho tấm thiệp",
            "Kể chuyện hai khung",
            "Đổi một chi tiết",
        ],
        "safety": [
            "Giữ riêng mật khẩu",
            "Hỏi người lớn đáng tin",
            "Tranh có thể không thật",
            "Cho đôi mắt nghỉ",
        ],
        "project": [
            "Chọn việc cho robot giấy",
            "Chọn thẻ hình mẫu",
            "Thử một thẻ mới",
            "Kể với cô điều đã học",
        ],
    },
    2: {
        "around": [
            "Máy làm theo lệnh",
            "Máy nhận biết hình",
            "Dự đoán chưa phải chắc chắn",
            "Người chọn, máy hỗ trợ",
        ],
        "data": [
            "Sắp xếp bộ sưu tập",
            "Tìm nhãn bị đặt nhầm",
            "Cần có nhiều loại mẫu",
            "Thử với tranh chưa xem",
        ],
        "prompt": [
            "Một yêu cầu, một việc",
            "Thêm chi tiết cần thiết",
            "Chọn cách trình bày",
            "Sửa lời nhắc mơ hồ",
        ],
        "math": [
            "Đếm theo nhóm hai",
            "Kiểm tra phép cộng",
            "Tìm quy luật đơn giản",
            "Đếm lại bằng tranh",
        ],
        "vietnamese": [
            "Tên đồ vật và tranh",
            "Đầu, giữa, cuối câu chuyện",
            "Chọn câu đúng với tranh",
            "Lời kể của chính em",
        ],
        "english": ["Hello and goodbye", "Fruit picture cards", "School things", "Count and check"],
        "creative": [
            "Thiệp cảm ơn bằng hình",
            "Ba tranh kể chuyện",
            "Poster có lời nhắc ngắn",
            "Thử rồi sửa sản phẩm",
        ],
        "safety": [
            "Thông tin nào giữ riêng?",
            "Dừng khi gặp yêu cầu lạ",
            "Kiểm tra hình kể chuyện",
            "Lịch học và nghỉ mắt",
        ],
        "project": [
            "Chọn vấn đề gần gũi",
            "Chuẩn bị thẻ có nhãn",
            "Thử với thẻ khác",
            "Kể cách em kiểm tra",
        ],
    },
    3: {
        "around": [
            "Lệnh cố định và học từ mẫu",
            "AI nhận thông tin gì?",
            "Dự đoán và bằng chứng",
            "Con người chịu trách nhiệm",
        ],
        "data": [
            "Nhãn của bộ dữ liệu",
            "Sửa mẫu gắn nhãn sai",
            "Nhìn đủ các nhóm",
            "Tách mẫu học và mẫu thử",
        ],
        "prompt": [
            "Nêu nhiệm vụ rõ ràng",
            "Chỉ đưa dữ liệu cần dùng",
            "Nói dạng kết quả mong muốn",
            "Cải thiện lời nhắc",
        ],
        "math": [
            "Kiểm tra phép nhân",
            "Tìm phép chia bị nhầm",
            "Đọc bảng số mẫu",
            "Kiểm chứng cách giải",
        ],
        "vietnamese": [
            "Từ khóa trong tranh",
            "Sắp ý đầu, giữa, cuối",
            "Sự thật và điều tưởng tượng",
            "Giữ lời kể của mình",
        ],
        "english": [
            "Greetings in pictures",
            "Animals and their names",
            "Singular and plural",
            "Check a short sentence",
        ],
        "creative": [
            "Robot giúp việc gì?",
            "Poster một thông điệp",
            "Truyện có ba sự kiện",
            "So sánh trước và sau khi sửa",
        ],
        "safety": [
            "Dữ liệu mẫu và dữ liệu riêng",
            "Ảnh chưa đủ làm bằng chứng",
            "Xin phép và ghi nguồn",
            "Cân bằng học và nghỉ",
        ],
        "project": [
            "Chọn nhiệm vụ có thể kiểm tra",
            "Chọn bộ mẫu đủ nhóm",
            "Ghi điều đúng và sai",
            "Trình bày giới hạn sản phẩm",
        ],
    },
    5: {
        "around": [
            "Quy tắc và dự đoán từ mẫu",
            "Đầu vào và đầu ra",
            "Khi nào cần bằng chứng?",
            "Quyết định thuộc về con người",
        ],
        "data": [
            "Nhãn quyết định điều máy học",
            "Dữ liệu sai, dự đoán sai",
            "Đủ nhóm để kiểm tra công bằng",
            "Mẫu thử không trùng mẫu học",
        ],
        "prompt": [
            "Nhiệm vụ và tiêu chí rõ",
            "Dữ liệu liên quan, không riêng tư",
            "Định dạng giúp kiểm tra",
            "Sửa yêu cầu sau khi đối chiếu",
        ],
        "math": [
            "Kiểm tra phép tính thập phân",
            "Kiểm chứng phân số",
            "Đọc tỉ lệ từ dữ liệu mẫu",
            "Phát hiện lập luận sai",
        ],
        "vietnamese": [
            "Ý chính và chi tiết minh họa",
            "Bố cục cho câu chuyện",
            "Phân biệt thông tin và hư cấu",
            "Chỉnh văn, giữ ý của em",
        ],
        "english": [
            "Give a clear instruction",
            "Check picture vocabulary",
            "Check noun agreement",
            "Verify a short description",
        ],
        "creative": [
            "Thiết kế cho người sử dụng",
            "Poster với tiêu chí kiểm tra",
            "Kịch bản truyện ngắn",
            "Cải tiến dựa vào phản hồi",
        ],
        "safety": [
            "Tối thiểu thông tin chia sẻ",
            "Kiểm chứng hình ảnh và khẳng định",
            "Tôn trọng tác giả và nguồn",
            "Chọn lúc tự làm thay vì dùng AI",
        ],
        "project": [
            "Nêu vấn đề và tiêu chí",
            "Thiết kế bộ mẫu",
            "Thử, ghi lỗi, cải tiến",
            "Báo cáo cách làm và giới hạn",
        ],
    },
}

# Keep the three previously shipped lesson identities and their unit positions.
LEGACY_UNITS = {
    1: ["around", "data", "safety"],
    2: ["data", "data", "safety"],
    3: ["prompt", "data", "project"],
    5: ["data", "project", "project"],
}


def tasks(grade, unit, variant):
    young = grade <= 2
    correct, retry = ("Đúng", "Thử lại") if young else ("Có căn cứ", "Cần kiểm tra")
    if unit == "around":
        cases = [
            (
                "Máy làm theo việc đã thiết kế.",
                [("Quạt bật bằng công tắc", "Theo lệnh"), ("Máy học nhận hình mèo", "Từ mẫu")],
            ),
            (
                "Máy cần nhận thông tin trước khi làm việc.",
                [("Hình con mèo", "Nhìn hình"), ("Âm thanh tiếng nói", "Nghe tiếng")],
            ),
            (
                "Máy đoán có thể sai. Em kiểm tra bằng tranh.",
                [("Máy gọi mèo, tranh là mèo", correct), ("Máy gọi mèo, tranh là chó", retry)],
            ),
            (
                "Người lớn quyết định việc quan trọng.",
                [("Chọn cách chăm người bệnh", "Người lớn"), ("Gợi ý tên con vật", "Máy hỗ trợ")],
            ),
        ]
        if grade == 1:
            cases[0] = (
                "Con người cảm nhận. Máy làm việc được thiết kế.",
                [("Bạn nhỏ chăm bạn", "Con người"), ("Quạt bật bằng công tắc", "Máy")],
            )
    elif unit == "data":
        cases = [
            (
                "Máy học từ các mẫu có nhãn.",
                [("Mèo", "Con vật"), ("Cam", "Trái cây"), ("Chó", "Con vật")],
            ),
            (
                "Kiểm tra nhãn trước khi dùng mẫu.",
                [
                    ("Tranh mèo, nhãn mèo", correct),
                    ("Tranh chó, nhãn mèo", retry),
                    ("Tranh cam, nhãn cam", correct),
                ],
            ),
            (
                "Cần xem đủ nhóm, không chỉ nhìn màu.",
                [("Táo đỏ", "Trái cây"), ("Cặp đỏ", "Đồ dùng"), ("Bút chì đỏ", "Đồ dùng")],
            ),
            (
                "Dùng thẻ mới để thử điều đã học.",
                [
                    ("Thẻ mèo đã xem", "Mẫu học"),
                    ("Thẻ chó chưa xem", "Mẫu thử"),
                    ("Thẻ cam chưa xem", "Mẫu thử"),
                ],
            ),
        ]
    elif unit == "prompt":
        cases = [
            (
                "Nói rõ việc em muốn làm.",
                [("Đếm ba quả táo", "Rõ ràng"), ("Làm cái này", "Chưa rõ")],
            ),
            (
                "Đưa thông tin cần cho nhiệm vụ.",
                [("Thẻ mẫu: mèo và chó", "Cần dùng"), ("Mật khẩu của em", "Giữ riêng")],
            ),
            (
                "Nói cách em muốn nhận kết quả.",
                [("Cho hai tên con vật", "Rõ ràng"), ("Cho thật nhiều thứ", "Chưa rõ")],
            ),
            (
                "Chưa rõ thì hỏi lại, không đoán thông tin thiếu.",
                [("Em muốn hình mèo hay chó?", "Hỏi lại"), ("Tự bịa tên bạn", "Không nên")],
            ),
        ]
    elif unit == "math":
        a, b = {1: (2, 3), 2: (8, 6), 3: (12, 3), 5: (25, 10)}[grade]
        if grade == 5:
            equations = [
                [("2,5 + 1,2 = 3,7", correct), ("2,5 + 1,2 = 2,7", retry)],
                [("1/2 + 1/4 = 3/4", correct), ("1/2 + 1/4 = 2/6", retry)],
                [("25 trong 100 là 25%", correct), ("25 trong 100 là 50%", retry)],
                [("3 × 1,5 = 4,5", correct), ("3 × 1,5 = 3,5", retry)],
            ]
        elif grade == 3:
            equations = [
                [(f"{a} × {b} = {a * b}", correct), (f"{a} × {b} = {a * b + 1}", retry)],
                [("24 : 3 = 8", correct), ("24 : 3 = 6", retry)],
                [("Ba nhóm bốn là 12", correct), ("Ba nhóm bốn là 7", retry)],
                [("Kiểm tra bằng phép tính ngược", correct), ("Tin kết quả không kiểm tra", retry)],
            ]
        else:
            equations = [
                [
                    (f"{a} quả và {b} quả là {a + b}", correct),
                    (f"{a} quả và {b} quả là {a + b + 1}", retry),
                ],
                [("Hai nhóm, mỗi nhóm hai: 4", correct), ("Hai nhóm, mỗi nhóm hai: 3", retry)],
                [(f"{a} + {b} = {a + b}", correct), (f"{a} + {b} = {a + b - 1}", retry)],
                [("Đếm mỗi quả một lần", correct), ("Đếm một quả hai lần", retry)],
            ]
        cases = [("Tự đếm hoặc tính để kiểm tra lời máy gợi ý.", pairs) for pairs in equations]
    elif unit == "vietnamese":
        cases = [
            (
                "Dùng tranh và chi tiết để hiểu từ.",
                [("Mèo", "Con vật"), ("Sách", "Đồ dùng"), ("Cam", "Trái cây")],
            ),
            (
                "Kể theo thứ tự để người nghe hiểu.",
                [("Nhặt hạt", "Đầu"), ("Gieo hạt", "Giữa"), ("Cây mọc", "Cuối")],
            ),
            (
                "Truyện tưởng tượng khác thông tin có thể kiểm tra.",
                [("Mèo là con vật", "Có thật"), ("Mèo đi học trên mây", "Tưởng tượng")],
            ),
            (
                "Gợi ý giúp tìm ý. Em tự kể bằng lời của mình.",
                [("Tự nói điều em thấy", "Lời của em"), ("Chép mà không hiểu", "Cần thử lại")],
            ),
        ]
    elif unit == "english":
        cases = [
            (
                "Chọn lời chào phù hợp với tình huống.",
                [
                    ("Gặp bạn: Hello", correct),
                    ("Tạm biệt: Goodbye", correct),
                    ("Gặp bạn: Goodbye", retry),
                ],
            ),
            (
                "Nhìn tranh rồi kiểm tra tên tiếng Anh.",
                [("Mèo: cat", correct), ("Chó: dog", correct), ("Cam: cat", retry)],
            ),
            (
                "Kiểm tra số lượng và từ đi kèm."
                if grade >= 3
                else "Nhìn tranh để kiểm tra màu hoặc đồ vật.",
                [("One cat", correct), ("Two cats", correct), ("Two cat", retry)]
                if grade >= 3
                else [("Táo đỏ: red", correct), ("Sách: book", correct), ("Bút chì: cat", retry)],
            ),
            (
                "Kiểm tra từng từ, không tin mọi gợi ý.",
                [("Three là ba", correct), ("Two là hai", correct), ("One là ba", retry)],
            ),
        ]
    elif unit == "creative":
        cases = [
            (
                "Robot trên giấy là nhân vật do em tạo.",
                [("Vẽ robot trên giấy", "Sáng tạo"), ("Nói robot có cảm xúc thật", "Cần sửa")],
            ),
            (
                "Tấm thiệp nên có một thông điệp rõ.",
                [("Thiệp: Cảm ơn cô", "Rõ ràng"), ("Chữ chồng lên nhau", "Cần sửa")],
            ),
            (
                "Các khung truyện cần nối tiếp nhau.",
                [("Gieo hạt rồi tưới cây", "Nối tiếp"), ("Cây lớn trước khi gieo", "Cần sửa")],
            ),
            (
                "Thử xem người khác có hiểu sản phẩm không.",
                [("Sửa chữ khó đọc", "Cải thiện"), ("Bỏ qua góp ý", "Cần thử lại")],
            ),
        ]
    elif unit == "safety":
        cases = [
            (
                "Giữ riêng thông tin của em.",
                [
                    ("Mật khẩu", "Giữ riêng"),
                    ("Thẻ mèo mẫu", "Dùng để học"),
                    ("Địa chỉ nhà", "Giữ riêng"),
                ],
            ),
            (
                "Không chắc thì dừng và hỏi người lớn.",
                [("Trò chơi hỏi mật khẩu", "Dừng, hỏi cô"), ("Trò ghép hình mẫu", "Có thể học")],
            ),
            (
                "Hình đẹp chưa chứng minh chuyện có thật.",
                [
                    ("Ảnh mèo bay trên mây", "Cần kiểm tra"),
                    ("Đối chiếu với sách và cô", "Có căn cứ"),
                ],
            ),
            (
                "Em cần tự nghĩ và nghỉ mắt đúng lúc.",
                [("Học rồi nghỉ mắt", "Nên làm"), ("Nhờ máy làm hết bài", "Không nên")],
            ),
        ]
    else:
        cases = [
            (
                "Chọn một việc nhỏ có thể kiểm tra.",
                [("Xếp thẻ mèo và cam", "Làm được"), ("Máy biết mọi điều", "Quá rộng")],
            ),
            (
                "Chuẩn bị mẫu rõ ràng, đủ nhóm.",
                [("Có mèo và cam", "Đủ nhóm"), ("Chỉ có mèo", "Thiếu nhóm")],
            ),
            (
                "Thử với hình khác rồi ghi điều cần sửa.",
                [("Thử thẻ chó mới", "Mẫu mới"), ("Thử đúng thẻ đã xem", "Mẫu cũ")],
            ),
            (
                "Nói cách làm và điều sản phẩm chưa làm được.",
                [("Kể cách kiểm tra", "Có căn cứ"), ("Nói máy luôn đúng", "Cần sửa")],
            ),
        ]
    if grade == 5 and unit == "data":
        cases = [
            (
                "Nhãn sai khiến máy học điều sai. Kiểm tra nhãn trước khi dùng mẫu.",
                [
                    ("Ảnh mèo, nhãn mèo", "Nhãn phù hợp"),
                    ("Ảnh chó, nhãn mèo", "Cần sửa nhãn"),
                    ("Ảnh chó, nhãn chó", "Nhãn phù hợp"),
                ],
            ),
            (
                "Mẫu cần có nhiều tình huống. Màu nền không quyết định con vật.",
                [
                    ("Mèo có nền sáng và tối", "Nhiều tình huống"),
                    ("Mèo chỉ có nền sáng", "Cần thêm mẫu"),
                    ("Chó có nhiều tư thế", "Nhiều tình huống"),
                ],
            ),
            (
                "Thử riêng từng nhóm để phát hiện nhóm bị bỏ sót.",
                [
                    ("Có nhiều mẫu mèo và chó", "Đủ hai nhóm"),
                    ("Chỉ có mẫu mèo", "Thiếu nhóm chó"),
                    ("Kiểm tra cả mèo và chó", "Đủ hai nhóm"),
                ],
            ),
            (
                "Giữ mẫu thử khác mẫu học để kiểm tra khả năng áp dụng.",
                [
                    ("Học A1, thử A2 chưa xem", "Mẫu thử mới"),
                    ("Học A1, thử lại A1", "Trùng mẫu học"),
                    ("Học B1, thử B2 chưa xem", "Mẫu thử mới"),
                ],
            ),
        ]
    if grade == 5 and unit == "prompt":
        cases = [
            (
                "Nêu nhiệm vụ và tiêu chí để biết kết quả có phù hợp không.",
                [
                    ("Giải thích một cách, hỏi một câu tự kiểm tra", "Có tiêu chí"),
                    ("Hãy làm mọi thứ", "Thiếu tiêu chí"),
                ],
            ),
            (
                "Chỉ đưa dữ liệu liên quan. Thông tin riêng không giúp giải bài mẫu.",
                [
                    ("Bảng số liệu giả của bài", "Liên quan"),
                    ("Địa chỉ nhà của bạn", "Không chia sẻ"),
                ],
            ),
            (
                "Dạng trình bày rõ giúp em tự đối chiếu từng phần.",
                [
                    ("Bảng hai cột: dữ liệu và cách kiểm tra", "Dễ đối chiếu"),
                    ("Đoạn rất dài không chia ý", "Khó đối chiếu"),
                ],
            ),
            (
                "Chỉ rõ chi tiết chưa phù hợp rồi sửa yêu cầu.",
                [
                    ("Đổi ví dụ thành ba quả táo", "Sửa cụ thể"),
                    ("Nói sai rồi bỏ qua", "Chưa cải thiện"),
                ],
            ),
        ]
    if grade == 5 and unit == "english" and variant == 0:
        cases[0] = (
            "Nêu rõ việc cần làm bằng câu tiếng Anh ngắn.",
            [
                ("Write two animal names", "Clear"),
                ("Do it", "Unclear"),
                ("Name the fruit in this picture", "Clear"),
            ],
        )
    if grade == 5 and unit == "project" and variant == 2:
        cases[2] = (
            "Ghi kết quả trên mẫu mới. Chưa đạt thì sửa rồi thử lại.",
            [
                ("Đúng 4 trong 5: 80%", "Tính đúng"),
                ("Đúng 4 trong 5: 100%", "Cần sửa"),
                ("Một lần đúng nên luôn đúng", "Cần sửa"),
            ],
        )
    concept, pairs = cases[variant]
    if grade == 1 and len(pairs) > 2:
        pairs = [pairs[0], next(pair for pair in pairs if pair[1] != pairs[0][1])]
    return concept, pairs


def records_for_grade(grade, units):
    from app.academy.curriculum import activity, lesson, quiz

    unit_titles = {code: title for code, title, _ in units}
    ordered_units = list(dict.fromkeys(LEGACY_UNITS[grade] + list(unit_titles)))
    pending = {unit: 0 for unit in unit_titles}
    plans = list(LEGACY_UNITS[grade])
    for unit in plans:
        pending[unit] += 1
    for unit in ordered_units:
        plans.extend([unit] * (4 - pending[unit]))
    pending = {unit: 0 for unit in unit_titles}
    result = []
    for number, unit in enumerate(plans, 1):
        variant = pending[unit]
        pending[unit] += 1
        title = TITLES[grade][unit][variant]
        concept, pairs = tasks(grade, unit, variant)
        choices = list(dict.fromkeys(answer for _, answer in pairs))
        questions = [
            quiz(
                f"Thẻ ‘{text}’: em chọn gì?",
                answer,
                next(choice for choice in choices if choice != answer),
                f"Em đối chiếu với tranh hoặc quy tắc: {answer}.",
            )
            for text, answer in (pairs[0], pairs[-1])
        ]
        questions.append(
            quiz(
                "Máy đoán khác điều em kiểm tra. Em làm gì?",
                "Kiểm tra lại, nhờ cô giúp",
                "Tin máy ngay",
                "Máy có thể nhầm. Dùng tranh, phép tính hoặc người lớn để kiểm tra.",
            )
        )
        row = lesson(
            number,
            title,
            "Cùng xem tranh. Em chỉ một điều mình nhận ra.",
            concept,
            activity(
                "classify",
                "Chạm một thẻ rồi chọn nhóm phù hợp.",
                pairs,
                concept,
                [
                    "Nhìn kỹ hình và đọc tên thẻ.",
                    "So sánh thẻ với hai nhóm trong bài.",
                    "Đối chiếu lại với ví dụ, rồi tự chọn.",
                ],
            ),
            questions,
            f"Lớp {grade}: {concept} Cho trẻ chỉ tranh, giải thích bằng lời; không bắt gõ. "
            "Đây là hoạt động mô phỏng quy tắc/dữ liệu, không gọi hoặc huấn luyện mô hình AI thật. "
            "Nếu trẻ chưa đọc được, người lớn đọc nhãn và làm mẫu một thẻ; kiểm tra trẻ hiểu thay vì chỉ nhớ đáp án.",
            "Vẽ thêm một thẻ khác và giải thích em sẽ kiểm tra thế nào.",
            "Chỉ một tranh. Nói điều em đã hiểu với cô hoặc người thân.",
        )
        row.update(
            grade=grade,
            code=f"AI{grade}-{number:02}",
            unit_code=f"AI{grade}-{unit}",
            unit_title=unit_titles[unit],
            unit_position=ordered_units.index(unit) + 1,
            position=variant + 1,
        )
        result.append(row)
    return result
