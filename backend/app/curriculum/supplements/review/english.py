"""Optional short conversations, with Vietnamese scaffolding."""

from app.curriculum.supplements.review.builders import cards, pick, unit

DATA = {
    1: (
        "school",
        "Hello, little pencil!",
        "Hello = Xin chào. A pencil = một bút chì. A book = một quyển sách.",
        [
            (
                "Chọn lời chào bằng tiếng Anh.",
                "Hello!",
                ["A book", "A pencil"],
                "Hello là lời chào.",
            ),
            (
                "'A pencil' là đồ vật nào?",
                "Một bút chì",
                ["Một quyển sách", "Một con mèo"],
                "Pencil nghĩa là bút chì.",
            ),
            (
                "'A book' là đồ vật nào?",
                "Một quyển sách",
                ["Một bút chì", "Một quả táo"],
                "Book nghĩa là quyển sách.",
            ),
            (
                "Bạn nói 'Hello!'. Em đáp lại lời chào thế nào?",
                "Hello!",
                ["A book", "A pencil"],
                "Có thể đáp Hello để chào bạn.",
            ),
        ],
    ),
    2: (
        "pets",
        "A cat or a dog?",
        "Cat = mèo. Dog = chó. This is a cat = Đây là một con mèo.",
        [
            ("Từ nào có nghĩa là mèo?", "Cat", ["Dog", "Book"], "Cat nghĩa là mèo."),
            ("Từ nào có nghĩa là chó?", "Dog", ["Cat", "Pencil"], "Dog nghĩa là chó."),
            (
                "Chọn câu có nghĩa 'Đây là một con mèo'.",
                "This is a cat.",
                ["This is a dog.", "This is a book."],
                "Cat là mèo; this is là đây là.",
            ),
            (
                "'This is a dog.' giới thiệu con gì?",
                "Một con chó",
                ["Một con mèo", "Một quyển sách"],
                "Dog là chó; this is là đây là.",
            ),
        ],
    ),
    3: (
        "school",
        "May I come in?",
        "May I come in? = Em xin phép vào. Yes, you can. = Em có thể vào. Thank you. = Em cảm ơn.",
        [
            (
                "Em muốn xin phép vào lớp. Chọn câu phù hợp.",
                "May I come in?",
                ["This is my book.", "I like cats."],
                "May I come in dùng để xin phép vào.",
            ),
            (
                "Cô đồng ý cho vào. Cô có thể nói gì?",
                "Yes, you can.",
                ["No, you can't.", "I'm nine."],
                "Yes, you can thể hiện cho phép.",
            ),
            (
                "Sau khi được giúp đỡ, em nói gì?",
                "Thank you.",
                ["I'm nine.", "This is a pen."],
                "Thank you là lời cảm ơn.",
            ),
            (
                "'No, you can't.' cho biết điều gì?",
                "Chưa được phép",
                ["Đã được phép", "Lời cảm ơn"],
                "No, you can't là không được phép.",
            ),
        ],
    ),
    4: (
        "weather",
        "A rainy day",
        "It's rainy. = Trời có mưa. It's sunny. = Trời có nắng. Take an umbrella. = Hãy mang ô.",
        [
            (
                "Câu nào nói trời đang mưa?",
                "It's rainy.",
                ["It's sunny.", "It's hot."],
                "Rainy mô tả thời tiết có mưa.",
            ),
            (
                "'It's sunny.' có nghĩa gì?",
                "Trời có nắng",
                ["Trời có mưa", "Trời có tuyết"],
                "Sunny nghĩa là có nắng.",
            ),
            (
                "Bạn nói 'It's rainy.' Chọn lời nhắc phù hợp.",
                "Take an umbrella.",
                ["This is my cat.", "I can swim."],
                "Mang ô phù hợp tình huống trời mưa.",
            ),
            (
                "Từ 'umbrella' trong lời nhắc nghĩa là gì?",
                "Cái ô",
                ["Quyển sách", "Chiếc bàn"],
                "Umbrella nghĩa là cái ô.",
            ),
        ],
    ),
    5: (
        "travel",
        "Ask the way politely",
        "Excuse me. Where is the library? — Go straight. Then turn left. = Xin hỏi thư viện ở đâu? — Đi thẳng, rồi rẽ trái.",
        [
            (
                "Câu nào hỏi đường đến thư viện?",
                "Where is the library?",
                ["What is your name?", "How old are you?"],
                "Where is hỏi vị trí; library là thư viện.",
            ),
            (
                "'Go straight.' có nghĩa gì?",
                "Đi thẳng",
                ["Rẽ trái", "Rẽ phải"],
                "Go straight là đi thẳng.",
            ),
            (
                "Theo chỉ dẫn, sau khi đi thẳng cần làm gì?",
                "Turn left.",
                ["Turn right.", "Go back."],
                "Từ then chỉ bước tiếp theo: turn left, rẽ trái.",
            ),
            (
                "Cụm nào dùng để mở lời hỏi lịch sự?",
                "Excuse me.",
                ["Turn left.", "Go straight."],
                "Excuse me được dùng để thu hút sự chú ý một cách lịch sự.",
            ),
        ],
    ),
}


def content(grade):
    topic, title, example, rows = DATA[grade]
    return unit(
        grade,
        topic,
        "little-conversation",
        title,
        "Chọn lời đáp phù hợp một tình huống quen thuộc.",
        "Đọc câu tiếng Anh cùng nghĩa tiếng Việt. Chọn lời đáp đúng tình huống.",
        example,
        "Đọc cả câu và tình huống trước khi chọn.",
        [
            "Nhìn từ hoặc tình huống được hỏi.",
            "Tìm câu mẫu có cùng ý.",
            "Đối chiếu với nghĩa tiếng Việt rồi đọc lại lời đáp.",
        ],
        cards("Mèo", "Chó") if grade == 2 else cards("Sách", "Bút chì"),
        [pick(*row) for row in rows],
        vip=True,
        context="Chỉ dẫn: Go straight. Then turn left." if grade == 5 else "",
    )
