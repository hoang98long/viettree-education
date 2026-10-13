"""Familiarisation, not grammar exams: Vietnamese directions, model words and adult-led speech."""

from app.curriculum.grades.early_primary.builders import FREE_LESSONS, build, cards


def curriculum(grade):
    items = []

    def needed():
        index = len(items)
        return (
            4
            if index < 8
            else (8 if FREE_LESSONS["ENGLISH"] <= index < FREE_LESSONS["ENGLISH"] + 4 else 6)
        )

    def add(topic, code, title, teaching, example, hints, rows, labels=None, thinking=False):
        items.append(
            build(
                grade,
                "ENGLISH",
                len(items),
                topic,
                code,
                title,
                teaching,
                example,
                "Nhờ người lớn đọc mẫu từ tiếng Anh; em có thể chỉ vào hình hoặc nhắc lại nếu sẵn sàng. Chưa chấm phát âm.",
                hints,
                rows,
                illustration=cards(labels, "Thẻ từ minh họa; đọc chậm cùng người hướng dẫn.")
                if labels
                else None,
                thinking=thinking,
            )
        )

    def word_unit(topic, code, title, vocabulary, *, thinking=False):
        count = needed()
        assert len(vocabulary) >= (count + 1) // 2
        rows = []
        for position in range(count):
            index = position % len(vocabulary)
            word, meaning, symbol = vocabulary[index]
            if position < len(vocabulary):
                prompt, answer = f"Từ {word} chỉ gì?", meaning
                wrong = [vocabulary[(index + i) % len(vocabulary)][1] for i in [1, 2]]
            else:
                prompt, answer = f"Chọn từ chỉ {meaning.lower()}.", word
                wrong = [vocabulary[(index + i) % len(vocabulary)][0] for i in [1, 2]]
            rows.append((prompt, answer, wrong, f"{word} nghĩa là {meaning.lower()}."))
        add(
            topic,
            code,
            title,
            "Nhìn thẻ và từ. Người lớn đọc mẫu, em chỉ vào hoặc nhắc lại từng từ. Không cần viết câu dài.",
            "; ".join(f"{w}: {m.lower()}" for w, m, _ in vocabulary) + ".",
            "Nhìn thẻ có từ được hỏi.|Đối chiếu một từ với một nghĩa trong ví dụ.|Chỉ hoặc đọc lại từ với người thân.",
            rows,
            [f"{s} {w}".strip() for w, _, s in vocabulary],
            thinking,
        )

    def sheet(topic, code, title, example, text, labels=None, thinking=False):
        rows = []
        for line in text.strip().splitlines():
            p, a, w, v, why = line.split("|")
            rows.append((p, a, [w, v], why))
        add(
            topic,
            code,
            title,
            "Đọc mẫu cùng người lớn rồi thực hành một câu ngắn. Có thể chỉ vào từ để trả lời.",
            example,
            "Xem tình huống được hỏi.|Đọc từ hoặc câu mẫu phù hợp.|Thử nói cùng người hướng dẫn, không cần nói nhanh.",
            rows,
            labels,
            thinking,
        )

    if grade == 1:
        sheet(
            "self",
            "hello",
            "Hello và Goodbye",
            "Hello: xin chào. Goodbye: tạm biệt. Please: làm ơn. Thank you: cảm ơn.",
            """Gặp bạn, chọn lời nào?|Hello|Goodbye|Thank you|Hello là lời chào.
Ra về, chọn lời nào?|Goodbye|Hello|Please|Goodbye là tạm biệt.
Được giúp, chọn lời nào?|Thank you|Goodbye|Hello|Thank you là cảm ơn.
Từ nào làm lời nhờ lịch sự hơn?|Please|Goodbye|Hello|Please nghĩa là làm ơn.""",
            ["Hello", "Goodbye"],
        )
        sheet(
            "self",
            "name",
            "Nói tên theo câu mẫu",
            "Hello! I am Ben. Hello! I am Ann. I am dùng khi tự giới thiệu tên.",
            """Bạn trong câu I am Ben tên gì?|Ben|Ann|Hello|Câu này giới thiệu Ben.
Bạn trong câu I am Ann tên gì?|Ann|Ben|Hello|Câu này giới thiệu Ann.
Ben tự giới thiệu thế nào?|I am Ben.|I am Ann.|Goodbye Ann.|Ben dùng I am Ben.
Ann tự giới thiệu thế nào?|I am Ann.|I am Ben.|Goodbye Ben.|Ann dùng I am Ann.""",
            ["Ben", "Ann"],
        )
        word_unit(
            "school",
            "supplies",
            "Book, pen, bag và ruler",
            [
                ("book", "Quyển sách", "📖"),
                ("pen", "Bút", "🖊"),
                ("bag", "Cặp", "🎒"),
                ("ruler", "Thước", "📏"),
            ],
        )
        word_unit(
            "school",
            "actions",
            "Làm theo chỉ dẫn ngắn",
            [
                ("Stand up", "Đứng lên", ""),
                ("Sit down", "Ngồi xuống", ""),
                ("Open", "Mở", ""),
                ("Close", "Đóng", ""),
            ],
        )
        word_unit(
            "colours",
            "bright",
            "Màu red, blue, yellow và green",
            [
                ("red", "Đỏ", "🔴"),
                ("blue", "Xanh dương", "🔵"),
                ("yellow", "Vàng", "🟡"),
                ("green", "Xanh lá", "🟢"),
            ],
        )
        word_unit(
            "colours",
            "other",
            "Màu black, white, pink và brown",
            [
                ("black", "Đen", "⚫"),
                ("white", "Trắng", "⚪"),
                ("pink", "Hồng", ""),
                ("brown", "Nâu", ""),
            ],
        )
        word_unit(
            "numbers",
            "one-five",
            "Số one, two, three, four, five",
            [
                ("one", "Một", "1"),
                ("two", "Hai", "2"),
                ("three", "Ba", "3"),
                ("four", "Bốn", "4"),
                ("five", "Năm", "5"),
            ],
        )
        word_unit(
            "numbers",
            "six-ten",
            "Số six, seven, eight, nine, ten",
            [
                ("six", "Sáu", "6"),
                ("seven", "Bảy", "7"),
                ("eight", "Tám", "8"),
                ("nine", "Chín", "9"),
                ("ten", "Mười", "10"),
            ],
        )
        word_unit(
            "pets",
            "animals",
            "Mèo, chó và chim",
            [("cat", "Mèo", "🐱"), ("dog", "Chó", "🐶"), ("bird", "Chim", "🐦")],
        )
        word_unit(
            "pets",
            "small-animals",
            "Cá, thỏ và vịt",
            [("fish", "Cá", "🐟"), ("rabbit", "Thỏ", "🐰"), ("duck", "Vịt", "🦆")],
        )
        word_unit(
            "toys",
            "toys",
            "Ball, doll và car",
            [("ball", "Quả bóng", "⚽"), ("doll", "Búp bê", ""), ("car", "Ô tô", "🚗")],
        )
        word_unit(
            "home",
            "family",
            "Gọi người thân bằng từ quen",
            [("mum", "Mẹ", ""), ("dad", "Bố", ""), ("baby", "Em bé", "")],
        )
        word_unit(
            "home",
            "fruit",
            "Apple, banana và orange",
            [("apple", "Táo", "🍎"), ("banana", "Chuối", "🍌"), ("orange", "Cam", "🍊")],
        )
        sheet(
            "pets",
            "first-letter",
            "Tư duy: chữ đầu trong tên con vật",
            "cat bắt đầu bằng c; dog bằng d; bird bằng b; fish bằng f. Nhờ người lớn đọc mẫu; đây là nhìn chữ, chưa kiểm tra âm nghe.",
            """Chữ đầu của cat là gì?|c|d|b|Cat bắt đầu bằng c.
Chữ đầu của dog là gì?|d|c|f|Dog bắt đầu bằng d.
Chữ đầu của bird là gì?|b|c|d|Bird bắt đầu bằng b.
Chữ đầu của fish là gì?|f|b|c|Fish bắt đầu bằng f.
Từ nào bắt đầu bằng c?|cat|dog|fish|Cat bắt đầu bằng c.
Từ nào bắt đầu bằng d?|dog|cat|bird|Dog bắt đầu bằng d.
Từ nào bắt đầu bằng b?|bird|cat|fish|Bird bắt đầu bằng b.
Từ nào bắt đầu bằng f?|fish|dog|cat|Fish bắt đầu bằng f.""",
            ["cat", "dog", "bird", "fish"],
            True,
        )
        word_unit(
            "school",
            "school-match",
            "Tư duy: ghép từ với vật ở lớp",
            [
                ("book", "Quyển sách", "📖"),
                ("pen", "Bút", "🖊"),
                ("bag", "Cặp", "🎒"),
                ("ruler", "Thước", "📏"),
            ],
            thinking=True,
        )
        sheet(
            "colours",
            "colour-toy",
            "Tư duy: đọc màu của đồ chơi",
            "red ball: bóng đỏ; blue car: ô tô xanh dương; yellow doll: búp bê vàng; green ball: bóng xanh lá.",
            """Red ball là đồ gì?|Bóng|Ô tô|Búp bê|Ball nghĩa là bóng.
Red ball màu gì?|Đỏ|Vàng|Xanh lá|Red nghĩa là đỏ.
Blue car là đồ gì?|Ô tô|Bóng|Búp bê|Car nghĩa là ô tô.
Blue car màu gì?|Xanh dương|Đỏ|Vàng|Blue nghĩa là xanh dương.
Yellow doll là đồ gì?|Búp bê|Bóng|Ô tô|Doll nghĩa là búp bê.
Yellow doll màu gì?|Vàng|Đỏ|Xanh lá|Yellow nghĩa là vàng.
Green ball màu gì?|Xanh lá|Đỏ|Vàng|Green nghĩa là xanh lá.
Bóng đỏ tương ứng cụm nào?|red ball|blue car|yellow doll|Red ball là bóng đỏ.""",
            ["red ball", "blue car", "yellow doll"],
            True,
        )
        sheet(
            "numbers",
            "count-words",
            "Tư duy: đếm và chọn từ chỉ số",
            "one = 1; two = 2; three = 3; four = 4; five = 5. Mỗi chấm dưới đây là một vật.",
            """● ● tương ứng từ nào?|two|one|three|Có 2 chấm: two.
● ● ● tương ứng từ nào?|three|two|one|Có 3 chấm: three.
● tương ứng từ nào?|one|two|three|Có 1 chấm: one.
● ● ● ● tương ứng từ nào?|four|three|five|Có 4 chấm: four.
● ● ● ● ● tương ứng từ nào?|five|four|three|Có 5 chấm: five.
Từ two chỉ số nào?|2|1|3|Two là 2.
Từ four chỉ số nào?|4|3|5|Four là 4.
Từ five chỉ số nào?|5|4|3|Five là 5.""",
            ["one", "two", "three", "four", "five"],
            True,
        )
        word_unit(
            "home",
            "body",
            "Tư duy: chỉ vào bộ phận cơ thể",
            [("hand", "Bàn tay", "✋"), ("eye", "Mắt", "👁"), ("ear", "Tai", "👂")],
            thinking=True,
        )
        sheet(
            "toys",
            "pattern",
            "Tư duy: nhận ra mẫu từ lặp",
            "Mẫu cat, dog lặp: cat – dog – cat – dog. Đọc chậm từng cặp cùng người lớn.",
            """cat – dog – cat – □. Điền từ nào?|dog|cat|ball|Sau cat là dog.
dog – cat – dog – □. Điền từ nào?|cat|dog|ball|Sau dog là cat.
ball – car – ball – □. Điền từ nào?|car|ball|cat|Sau ball là car.
car – ball – car – □. Điền từ nào?|ball|car|dog|Sau car là ball.
cat – dog – cat – dog – □. Điền từ nào?|cat|dog|ball|Bắt đầu lại cặp bằng cat.
ball – car – ball – car – □. Điền từ nào?|ball|car|cat|Bắt đầu lại cặp bằng ball.""",
            ["cat", "dog", "cat", "dog"],
            True,
        )
        sheet(
            "self",
            "polite",
            "Tư duy: chọn lời nói đúng lúc",
            "Hello khi gặp. Goodbye khi ra về. Thank you khi được giúp. Please để nhờ lịch sự.",
            """Gặp bạn, em nói gì?|Hello|Goodbye|Thank you|Hello dùng chào.
Ra về, em nói gì?|Goodbye|Hello|Please|Goodbye dùng tạm biệt.
Bạn đưa bút giúp, nói gì?|Thank you|Goodbye|Hello|Thank you dùng cảm ơn.
Lời nhờ có thể thêm từ nào?|Please|Goodbye|Hello|Please giúp nhờ lịch sự.
Thank you nghĩa là gì?|Cảm ơn|Tạm biệt|Mở|Thank you là cảm ơn.
Goodbye nghĩa là gì?|Tạm biệt|Xin chào|Đứng lên|Goodbye là tạm biệt.""",
            thinking=True,
        )
    else:
        sheet(
            "self",
            "introduce",
            "Chào và giới thiệu tên",
            "Hello! I am Ben. Hi! I am Ann. Goodbye! Tên và câu chỉ là mẫu.",
            """Ben tự giới thiệu thế nào?|I am Ben.|I am Ann.|Goodbye Ann.|Ben dùng I am Ben.
Ann tự giới thiệu thế nào?|I am Ann.|I am Ben.|Goodbye Ben.|Ann dùng I am Ann.
Từ chào khi gặp là gì?|Hello|Goodbye|Close|Hello là lời chào.
Từ tạm biệt là gì?|Goodbye|Hello|Open|Goodbye là tạm biệt.""",
            ["Hello", "Ben", "Ann"],
        )
        word_unit(
            "self",
            "feelings",
            "Happy, sad, hot và cold",
            [
                ("happy", "Vui", "😊"),
                ("sad", "Buồn", "😢"),
                ("hot", "Nóng", ""),
                ("cold", "Lạnh", ""),
            ],
        )
        word_unit(
            "school",
            "actions",
            "Hành động trong lớp",
            [
                ("read", "Đọc", "📖"),
                ("write", "Viết", "🖊"),
                ("draw", "Vẽ", ""),
                ("listen", "Lắng nghe", "👂"),
            ],
        )
        word_unit(
            "school",
            "instructions",
            "Chỉ dẫn ngắn trong lớp",
            [
                ("Stand up", "Đứng lên", ""),
                ("Sit down", "Ngồi xuống", ""),
                ("Open the book", "Mở sách", ""),
                ("Close the book", "Đóng sách", ""),
            ],
        )
        word_unit(
            "numbers",
            "eleven-fifteen",
            "Số eleven đến fifteen",
            [
                ("eleven", "Mười một", "11"),
                ("twelve", "Mười hai", "12"),
                ("thirteen", "Mười ba", "13"),
                ("fourteen", "Mười bốn", "14"),
                ("fifteen", "Mười lăm", "15"),
            ],
        )
        word_unit(
            "numbers",
            "sixteen-twenty",
            "Số sixteen đến twenty",
            [
                ("sixteen", "Mười sáu", "16"),
                ("seventeen", "Mười bảy", "17"),
                ("eighteen", "Mười tám", "18"),
                ("nineteen", "Mười chín", "19"),
                ("twenty", "Hai mươi", "20"),
            ],
        )
        word_unit(
            "home",
            "family",
            "Người thân trong gia đình",
            [
                ("mother", "Mẹ", ""),
                ("father", "Bố", ""),
                ("sister", "Chị hoặc em gái", ""),
                ("brother", "Anh hoặc em trai", ""),
            ],
        )
        word_unit(
            "home",
            "rooms",
            "Phòng và đồ vật trong nhà",
            [
                ("bedroom", "Phòng ngủ", ""),
                ("kitchen", "Nhà bếp", ""),
                ("bed", "Giường", ""),
                ("chair", "Ghế", ""),
            ],
        )
        word_unit(
            "colours",
            "colour-words",
            "Ôn màu của đồ vật",
            [("red", "Đỏ", "🔴"), ("blue", "Xanh dương", "🔵"), ("green", "Xanh lá", "🟢")],
        )
        word_unit(
            "pets",
            "animals",
            "Các con vật quen thuộc",
            [("cat", "Mèo", "🐱"), ("dog", "Chó", "🐶"), ("fish", "Cá", "🐟")],
        )
        word_unit(
            "toys",
            "shapes",
            "Hình circle, square và triangle",
            [
                ("circle", "Hình tròn", "○"),
                ("square", "Hình vuông", "□"),
                ("triangle", "Hình tam giác", "△"),
            ],
        )
        word_unit(
            "self",
            "days",
            "Một số ngày trong tuần",
            [("Monday", "Thứ hai", ""), ("Tuesday", "Thứ ba", ""), ("Sunday", "Chủ nhật", "")],
        )
        word_unit(
            "home",
            "food",
            "Thức ăn và đồ uống quen",
            [("rice", "Cơm", ""), ("milk", "Sữa", "🥛"), ("water", "Nước", "")],
        )
        sheet(
            "self",
            "friend-card",
            "Tư duy: đọc thẻ bạn ngắn",
            "Ben: happy, red bag. Ann: sad, blue bag. Happy = vui; sad = buồn; red = đỏ; blue = xanh dương; bag = cặp.",
            """Ben có cảm xúc gì?|Vui|Buồn|Lạnh|Ben có từ happy.
Ann có cảm xúc gì?|Buồn|Vui|Nóng|Ann có từ sad.
Cặp Ben màu gì?|Đỏ|Xanh dương|Vàng|Ben có red bag.
Cặp Ann màu gì?|Xanh dương|Đỏ|Vàng|Ann có blue bag.
Ai có red bag?|Ben|Ann|Không bạn nào|Thẻ Ben ghi red bag.
Ai có blue bag?|Ann|Ben|Không bạn nào|Thẻ Ann ghi blue bag.
Happy nghĩa là gì?|Vui|Buồn|Cặp|Happy là vui.
Sad nghĩa là gì?|Buồn|Vui|Đỏ|Sad là buồn.""",
            ["Ben", "Ann", "happy", "sad"],
            True,
        )
        sheet(
            "school",
            "label-check",
            "Tư duy: đọc nhãn đồ dùng",
            "red pen: bút đỏ. blue book: sách xanh dương. green bag: cặp xanh lá. yellow ruler: thước vàng.",
            """Red pen là đồ gì?|Bút|Sách|Cặp|Pen là bút.
Red pen màu gì?|Đỏ|Vàng|Xanh lá|Red là đỏ.
Blue book là đồ gì?|Sách|Bút|Thước|Book là sách.
Blue book màu gì?|Xanh dương|Đỏ|Vàng|Blue là xanh dương.
Green bag là đồ gì?|Cặp|Bút|Sách|Bag là cặp.
Green bag màu gì?|Xanh lá|Đỏ|Vàng|Green là xanh lá.
Yellow ruler là đồ gì?|Thước|Cặp|Bút|Ruler là thước.
Yellow ruler màu gì?|Vàng|Đỏ|Xanh lá|Yellow là vàng.""",
            ["red pen", "blue book", "green bag"],
            True,
        )
        sheet(
            "pets",
            "size",
            "Tư duy: nhìn từ big và small",
            "big cat: mèo to. small dog: chó nhỏ. big fish: cá to. small bird: chim nhỏ. Big = to, small = nhỏ.",
            """Big cat là con gì?|Mèo|Chó|Cá|Cat là mèo.
Big cat có cỡ thế nào?|To|Nhỏ|Không nói|Big là to.
Small dog là con gì?|Chó|Mèo|Chim|Dog là chó.
Small dog có cỡ thế nào?|Nhỏ|To|Không nói|Small là nhỏ.
Big fish là con gì?|Cá|Chó|Chim|Fish là cá.
Big fish có cỡ thế nào?|To|Nhỏ|Không nói|Big là to.
Small bird là con gì?|Chim|Mèo|Cá|Bird là chim.
Small bird có cỡ thế nào?|Nhỏ|To|Không nói|Small là nhỏ.""",
            ["big cat", "small dog", "big fish"],
            True,
        )
        sheet(
            "toys",
            "toy-cards",
            "Tư duy: số lượng và màu đồ chơi",
            "Ben: two red balls. Ann: three blue cars. Two = hai, three = ba; red = đỏ, blue = xanh dương; balls = các bóng, cars = các ô tô. Chỉ đọc theo mẫu, chưa học quy tắc ngữ pháp.",
            """Ben có mấy bóng?|Hai|Ba|Bốn|Two là hai.
Bóng Ben màu gì?|Đỏ|Xanh dương|Vàng|Red là đỏ.
Ann có mấy ô tô?|Ba|Hai|Bốn|Three là ba.
Ô tô Ann màu gì?|Xanh dương|Đỏ|Vàng|Blue là xanh dương.
Ai có bóng đỏ?|Ben|Ann|Không bạn nào|Thẻ Ben nói red balls.
Ai có ô tô xanh?|Ann|Ben|Không bạn nào|Thẻ Ann nói blue cars.
Từ balls chỉ gì?|Các bóng|Các sách|Các bút|Balls là các bóng.
Từ cars chỉ gì?|Các ô tô|Các cặp|Các thước|Cars là các ô tô.""",
            ["two red balls", "three blue cars"],
            True,
        )
        word_unit(
            "home",
            "clothes",
            "Tư duy: tên quần áo",
            [("shirt", "Áo", "👕"), ("hat", "Mũ", "🧢"), ("shoes", "Giày", "👟")],
            thinking=True,
        )
        word_unit(
            "colours",
            "weather",
            "Tư duy: từ chỉ thời tiết quen",
            [("sunny", "Có nắng", "☀"), ("rainy", "Có mưa", "🌧"), ("windy", "Có gió", "")],
            thinking=True,
        )
        sheet(
            "self",
            "last-letter",
            "Tư duy: chữ cuối trong từ quen",
            "cat kết thúc bằng t; dog bằng g; pen bằng n. Nhờ người lớn đọc mẫu; bài này nhận biết chữ viết, chưa chấm phát âm.",
            """Chữ cuối của cat là gì?|t|c|a|Cat kết thúc bằng t.
Chữ cuối của dog là gì?|g|d|o|Dog kết thúc bằng g.
Chữ cuối của pen là gì?|n|p|e|Pen kết thúc bằng n.
Từ nào kết thúc bằng t?|cat|dog|pen|Cat kết thúc bằng t.
Từ nào kết thúc bằng g?|dog|cat|pen|Dog kết thúc bằng g.
Từ nào kết thúc bằng n?|pen|dog|cat|Pen kết thúc bằng n.""",
            ["cat", "dog", "pen"],
            True,
        )
    assert len(items) == 20
    return items
