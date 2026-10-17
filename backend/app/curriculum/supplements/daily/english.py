from app.curriculum.supplements.daily.builders import cards, pick, unit

DATA = {
    1: (
        "self",
        "Thank you, my friend!",
        "Thank you = Cảm ơn. Sorry = Xin lỗi. Hello = Xin chào.",
        "",
        [
            (
                "Bạn đưa giúp em bút. Em nói lời cảm ơn thế nào?",
                "Thank you!",
                ["Hello!", "Sorry!"],
                "Thank you là lời cảm ơn.",
            ),
            (
                "Em vô tình làm rơi bút của bạn. Chọn lời xin lỗi.",
                "Sorry!",
                ["Hello!", "Thank you!"],
                "Sorry là lời xin lỗi.",
            ),
            (
                "Cụm 'Thank you' nghĩa là gì?",
                "Cảm ơn",
                ["Xin lỗi", "Xin chào"],
                "Thank you nghĩa là cảm ơn.",
            ),
            (
                "Cụm 'Hello' dùng để làm gì?",
                "Chào hỏi",
                ["Xin lỗi", "Cảm ơn"],
                "Hello là lời chào.",
            ),
        ],
    ),
    2: (
        "home",
        "Where is my book?",
        "In = ở trong. On = ở trên. Under = ở dưới. The book is on the table = Sách ở trên bàn.",
        "",
        [
            (
                "'On the table' nghĩa là ở đâu?",
                "Ở trên bàn",
                ["Ở dưới bàn", "Ở trong cặp"],
                "On là ở trên; table là bàn.",
            ),
            ("Chọn từ có nghĩa 'ở dưới'.", "Under", ["In", "On"], "Under nghĩa là ở dưới."),
            ("Chọn từ có nghĩa 'ở trong'.", "In", ["On", "Under"], "In nghĩa là ở trong."),
            (
                "Chọn câu nói sách ở trên bàn.",
                "The book is on the table.",
                ["The book is under the table.", "The book is in the bag."],
                "On the table là ở trên bàn.",
            ),
        ],
    ),
    3: (
        "family",
        "Meet my family",
        "Mother = mẹ. Father = bố. Teacher = giáo viên. Farmer = nông dân.",
        "This is my mother. She is a teacher. This is my father. He is a farmer.",
        [
            (
                "Trong đoạn, mẹ làm nghề gì?",
                "Teacher",
                ["Farmer", "Pupil"],
                "Đoạn giới thiệu mẹ bằng She is a teacher.",
            ),
            (
                "Trong đoạn, bố làm nghề gì?",
                "Farmer",
                ["Teacher", "Pupil"],
                "He is a farmer nói về bố vừa được giới thiệu.",
            ),
            ("Từ 'mother' nghĩa là gì?", "Mẹ", ["Bố", "Anh trai"], "Mother nghĩa là mẹ."),
            (
                "Từ 'He' trong đoạn chỉ ai?",
                "Bố",
                ["Mẹ", "Cô giáo"],
                "He nối với câu giới thiệu my father.",
            ),
        ],
    ),
    4: (
        "routines",
        "My morning",
        "Get up = thức dậy. Have breakfast = ăn sáng. Go to school = đi học.",
        "I get up at six o'clock. I have breakfast at seven o'clock. I go to school at seven thirty.",
        [
            (
                "Theo đoạn, người kể thức dậy lúc nào?",
                "Six o'clock",
                ["Seven o'clock", "Seven thirty"],
                "I get up at six o'clock: thức dậy lúc 6 giờ.",
            ),
            (
                "Cụm 'have breakfast' có nghĩa gì?",
                "Ăn sáng",
                ["Đi học", "Đi ngủ"],
                "Have breakfast nghĩa là ăn sáng.",
            ),
            (
                "Theo đoạn, việc nào đến trước ăn sáng?",
                "Get up",
                ["Go to school", "Go to bed"],
                "Thức dậy lúc 6 giờ, ăn sáng lúc 7 giờ.",
            ),
            (
                "Theo đoạn, người kể đi học lúc nào?",
                "Seven thirty",
                ["Six o'clock", "Seven o'clock"],
                "Go to school at seven thirty là đi học lúc 7 giờ 30.",
            ),
        ],
    ),
    5: (
        "food",
        "A polite meal",
        "I'd like = Tôi muốn. Rice = cơm. Water = nước. Please = làm ơn. Thank you = cảm ơn.",
        "A: What would you like to eat? B: I'd like some rice, please. A: What would you like to drink? B: Some water, please.",
        [
            (
                "Trong hội thoại, B muốn ăn gì?",
                "Rice",
                ["Bread", "Fish"],
                "B nói I'd like some rice, please.",
            ),
            (
                "Trong hội thoại, B muốn uống gì?",
                "Water",
                ["Milk", "Tea"],
                "B trả lời Some water, please.",
            ),
            (
                "Từ nào trong lời đáp giúp nói yêu cầu lịch sự?",
                "Please",
                ["Rice", "Water"],
                "Please được dùng để nói yêu cầu lịch sự.",
            ),
            (
                "Câu nào hỏi người nghe muốn uống gì?",
                "What would you like to drink?",
                ["What would you like to eat?", "What is your name?"],
                "Drink là uống, eat là ăn.",
            ),
        ],
    ),
}


def content(grade):
    topic, title, vocabulary, passage, rows = DATA[grade]
    return unit(
        grade,
        topic,
        "daily-words",
        title,
        "Hiểu từ mẫu và chọn lời nói phù hợp.",
        "Đọc câu tiếng Anh cùng nghĩa tiếng Việt. Người lớn có thể đọc mẫu cho em.",
        vocabulary + ("\n" + passage if passage else ""),
        "Dựa vào câu mẫu, không đoán thêm thông tin.",
        [
            "Tìm từ chỉ người, việc hoặc đồ vật được hỏi.",
            vocabulary,
            "Đọc lại câu chứa từ khóa trong đoạn mẫu."
            if passage
            else "Đọc nghĩa tiếng Việt rồi thử lời đáp.",
        ],
        cards("Bút chì")
        if grade == 1
        else cards("Sách", "Bàn học")
        if grade == 2
        else cards("Mẹ", "Bố")
        if grade == 3
        else cards("Đồng hồ", "Trường học")
        if grade == 4
        else cards("Cơm", "Nước uống"),
        [pick(*row) for row in rows],
        vip=True,
        context=passage,
    )
