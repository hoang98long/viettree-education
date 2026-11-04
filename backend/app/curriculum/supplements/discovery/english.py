"""Picture-led guided English in grades 1–2; short communication tasks thereafter."""

from app.curriculum.supplements.discovery import cards, pick, unit

LESSONS = {
    1: [
        (
            "pets",
            "Mèo và chó: cat, dog",
            "cat = mèo; dog = chó. This is a cat. = Đây là một con mèo.",
            ["Cat", "Dog"],
            "This is a cat.",
            [
                ("Từ nào chỉ con mèo?", "cat", ["dog"], "cat nghĩa là mèo."),
                ("Từ nào chỉ con chó?", "dog", ["cat"], "dog nghĩa là chó."),
                (
                    "Câu mẫu 'This is a cat.' nói về con gì?",
                    "Mèo",
                    ["Chó"],
                    "Từ cat cho biết đó là mèo.",
                ),
                (
                    "Chọn câu giới thiệu con mèo theo mẫu.",
                    "This is a cat.",
                    ["This is a dog."],
                    "Thay đúng tên con vật, không đổi nghĩa cat thành dog.",
                ),
            ],
        ),
        (
            "pets",
            "Hỏi lại: có phải mèo không?",
            "Is it a cat? = Có phải mèo không? Yes. = Đúng. No. = Không.",
            ["Cat", "Dog"],
            "This is a cat. Is it a cat? Yes.",
            [
                ("Câu 'Is it a cat?' hỏi về con gì?", "Mèo", ["Chó"], "cat nghĩa là mèo."),
                (
                    "Thẻ ghi là mèo. Hỏi 'Is it a cat?', chọn lời đáp nào?",
                    "Yes.",
                    ["No."],
                    "Đúng là mèo nên đáp Yes.",
                ),
                (
                    "Thẻ khác ghi là chó. Hỏi 'Is it a cat?', chọn lời đáp nào?",
                    "No.",
                    ["Yes."],
                    "Chó không phải mèo, nên đáp No.",
                ),
                (
                    "Từ 'No' trong bài nghĩa là gì?",
                    "Không",
                    ["Đúng"],
                    "No là lời đáp phủ định trong tình huống mẫu.",
                ),
            ],
        ),
    ],
    2: [
        (
            "school",
            "Thước và tẩy của em",
            "ruler = thước kẻ; eraser = tẩy; I have = Tôi có.",
            ["Ruler", "Eraser"],
            "I have a ruler and an eraser.",
            [
                ("Từ nào nghĩa là thước kẻ?", "ruler", ["eraser", "cat"], "ruler chỉ thước kẻ."),
                ("Từ nào nghĩa là tẩy?", "eraser", ["ruler", "dog"], "eraser là tẩy."),
                (
                    "Bạn trong câu mẫu có những gì?",
                    "Thước và tẩy",
                    ["Mèo và chó", "Sách và cặp"],
                    "Câu nêu a ruler and an eraser.",
                ),
                (
                    "'I have' trong bài có nghĩa là gì?",
                    "Tôi có",
                    ["Tạm biệt", "Trời mưa"],
                    "I have dùng để nói mình có đồ vật.",
                ),
            ],
        ),
        (
            "numbers",
            "Hai chiếc bút xanh",
            "two = hai; blue = xanh dương; pens = những chiếc bút; one = một.",
            ["Blue", "Pen"],
            "I have two blue pens.",
            [
                ("Trong câu mẫu, bạn có mấy chiếc bút?", "Hai", ["Một", "Ba"], "two nghĩa là hai."),
                (
                    "Những chiếc bút trong câu mẫu có màu gì?",
                    "Xanh dương",
                    ["Đỏ", "Vàng"],
                    "blue nghĩa là xanh dương.",
                ),
                (
                    "Cụm nào nói hai chiếc bút?",
                    "two pens",
                    ["one pen", "one cat"],
                    "two chỉ số lượng hai, pens chỉ các chiếc bút.",
                ),
                (
                    "Cần đổi cụm nào để nói một chiếc bút theo mẫu 'one pen'?",
                    "two pens thành one pen",
                    ["blue thành cat", "I thành dog"],
                    "Cần đổi cả số lượng và dạng danh từ theo mẫu đã cho.",
                ),
            ],
        ),
    ],
    3: [
        (
            "pets",
            "My pets can move",
            "dog = chó; bird = chim; can = có thể; run = chạy; fly = bay.",
            ["Dog", "Bird"],
            "My dog can run. My bird can fly.",
            [
                (
                    "Theo đoạn mẫu, con chó có thể làm gì?",
                    "Run",
                    ["Fly", "Read"],
                    "Câu đầu: My dog can run.",
                ),
                (
                    "Theo đoạn mẫu, con chim có thể làm gì?",
                    "Fly",
                    ["Write", "Read"],
                    "Câu sau: My bird can fly.",
                ),
                (
                    "'can' trong bài dùng để nói điều gì?",
                    "Khả năng",
                    ["Màu áo", "Số tuổi"],
                    "can đứng trước việc có thể làm.",
                ),
                (
                    "Câu nào khớp với đoạn mẫu?",
                    "My bird can fly.",
                    ["My dog can fly.", "My bird can read."],
                    "Chọn điều được câu mẫu nêu rõ, không tự thêm khả năng.",
                ),
            ],
        ),
        (
            "home",
            "Where is the rabbit?",
            "rabbit = thỏ; box = hộp; cat = mèo; desk = bàn; in = trong; under = dưới.",
            ["Rabbit", "Desk"],
            "The rabbit is in the box. The cat is under the desk.",
            [
                (
                    "Theo đoạn, con thỏ ở đâu?",
                    "In the box",
                    ["Under the desk", "On the bus"],
                    "Câu đầu ghi thỏ ở trong hộp.",
                ),
                (
                    "Theo đoạn, con mèo ở đâu?",
                    "Under the desk",
                    ["In the box", "In the tree"],
                    "Câu sau ghi mèo ở dưới bàn.",
                ),
                ("Từ nào có nghĩa là dưới?", "under", ["in", "rabbit"], "under chỉ vị trí ở dưới."),
                (
                    "Bạn nói thỏ ở dưới bàn. Câu đó có khớp đoạn không?",
                    "Không, thỏ ở trong hộp",
                    ["Có, đúng hoàn toàn", "Không thể đọc được vị trí"],
                    "Đoạn đã phân biệt chỗ của thỏ và mèo.",
                ),
            ],
        ),
    ],
    4: [
        (
            "weather",
            "The weather card",
            "rainy = có mưa; sunny = có nắng; today = hôm nay; tomorrow = ngày mai.",
            ["Rainy", "Sunny"],
            "It is rainy today. We read books at home.",
            [
                (
                    "Thời tiết hôm nay trong đoạn thế nào?",
                    "Rainy",
                    ["Sunny", "Snowy"],
                    "Câu đầu ghi rainy today.",
                ),
                (
                    "Các bạn làm gì trong đoạn?",
                    "Read books",
                    ["Swim in the sea", "Fly to the moon"],
                    "Câu sau nói các bạn đọc sách.",
                ),
                (
                    "Các bạn đọc sách ở đâu?",
                    "At home",
                    ["At the zoo", "At the airport"],
                    "at home nghĩa là ở nhà.",
                ),
                (
                    "Đoạn có cho biết thời tiết ngày mai không?",
                    "Chưa cho biết",
                    ["Có, chắc chắn có nắng", "Có, chắc chắn có tuyết"],
                    "today nói hôm nay; đoạn không nêu tomorrow.",
                ),
            ],
        ),
        (
            "routines",
            "Two days, two activities",
            "Monday = thứ Hai; Tuesday = thứ Ba; play football = chơi bóng đá; read books = đọc sách.",
            ["Ball", "Book"],
            "I play football on Monday. I read books on Tuesday.",
            [
                (
                    "Bạn làm gì vào thứ Hai theo đoạn?",
                    "Play football",
                    ["Read books", "Go fishing"],
                    "Câu đầu ghép football với Monday.",
                ),
                (
                    "Bạn đọc sách vào ngày nào?",
                    "Tuesday",
                    ["Monday", "Sunday"],
                    "Câu sau ghép read books với Tuesday.",
                ),
                (
                    "Câu nào khớp lịch trong đoạn?",
                    "I read books on Tuesday.",
                    ["I read books on Monday.", "I play football on Tuesday."],
                    "Đối chiếu cả hoạt động và ngày, không chỉ một từ.",
                ),
                (
                    "'on Monday' trong bài có nghĩa là gì?",
                    "Vào thứ Hai",
                    ["Ở sân bóng", "Trong quyển sách"],
                    "on đi cùng tên ngày trong mẫu này.",
                ),
            ],
        ),
    ],
    5: [
        (
            "health",
            "Water after a walk",
            "thirsty = khát; would like = muốn; water = nước; rests = nghỉ; shade = bóng mát.",
            ["Water", "Cây"],
            "Linh is thirsty after a walk. She would like some water. She rests in the shade.",
            [
                (
                    "Linh cảm thấy thế nào sau khi đi bộ?",
                    "Thirsty",
                    ["Sleepy", "Angry"],
                    "Câu đầu nêu Linh is thirsty.",
                ),
                (
                    "Linh muốn gì theo đoạn?",
                    "Some water",
                    ["A new bicycle", "A storybook"],
                    "Câu thứ hai: She would like some water.",
                ),
                (
                    "Linh nghỉ ở đâu?",
                    "In the shade",
                    ["In the river", "On the roof"],
                    "Câu cuối nêu chỗ nghỉ của Linh.",
                ),
                (
                    "'would like' trong câu mẫu có nghĩa nào?",
                    "Muốn",
                    ["Đã đánh rơi", "Không bao giờ"],
                    "Mẫu would like diễn đạt điều muốn có.",
                ),
            ],
        ),
        (
            "travel",
            "Read the trip plan",
            "leave = rời đi; arrive = đến; at = lúc; before = trước; after = sau; museum = bảo tàng; lunch = bữa trưa; one hour = một giờ. Các giờ là dữ liệu giả trong bài.",
            ["Bus", "Clock"],
            "We leave school at 8:00. We arrive at the museum at 9:00. We have lunch at 11:30.",
            [
                (
                    "Theo lịch mẫu, các bạn rời trường lúc nào?",
                    "8:00",
                    ["9:00", "11:30"],
                    "leave school at 8:00 cho biết giờ rời trường.",
                ),
                (
                    "Theo lịch mẫu, các bạn đến bảo tàng lúc nào?",
                    "9:00",
                    ["8:00", "11:30"],
                    "arrive at the museum at 9:00 cho biết giờ đến.",
                ),
                (
                    "Đến bảo tàng lúc 9:00, ăn trưa 11:30. Câu nào đúng với lịch?",
                    "We arrive before lunch.",
                    ["We have lunch before we arrive.", "We leave school at lunch."],
                    "9:00 trước 11:30, nên đến trước bữa trưa.",
                ),
                (
                    "Theo lịch mẫu, từ rời trường đến bảo tàng mất bao lâu?",
                    "One hour",
                    ["Two hours", "Thirty minutes"],
                    "Từ 8:00 đến 9:00 là một giờ, one hour.",
                ),
            ],
        ),
    ],
}


def content(grade):
    result = []
    for index, (topic, title, vocabulary, pictures, passage, rows) in enumerate(LESSONS[grade]):
        result.append(
            unit(
                grade,
                topic,
                f"english-{index + 1}",
                title,
                "Hiểu câu mẫu và chọn lời đáp đúng tình huống.",
                vocabulary,
                passage,
                "Đọc từ mẫu rồi đối chiếu cả câu; có thể nhờ người lớn đọc cùng.",
                [
                    "Tìm từ khóa trong câu hỏi.",
                    vocabulary,
                    "Đọc lại câu mẫu chứa người, vật hoặc thời điểm được hỏi.",
                ],
                cards(*pictures),
                [pick(*q) for q in rows],
                vip=bool(index),
                context=passage,
            )
        )
    return result
