"""Supported early-English familiarisation and short upper-primary dialogues."""

from app.curriculum.supplements.applied.builders import cards, unit


def content(grade):
    contexts = {
        1: "Các thẻ đồ dùng: pen = bút mực; book = sách; bag = cặp. Người lớn có thể đọc từ để em nhắc lại.",
        2: "Các thẻ ở nhà: cat = mèo; dog = chó; big = to; small = nhỏ. Em có thể nhờ người lớn đọc cùng.",
        3: "My name is Ben. I am nine. I have a blue bag. There are two books in my bag.",
        4: "On Monday, Anna has English and Maths. She likes English. After school, she plays badminton with Mai. They play in the school yard.",
        5: "It is Saturday. Tom and his sister are going to the library by bus. They want to borrow books about animals. They will meet their mother at the library at ten. Tom has a bottle of water in his bag.",
    }
    vip_contexts = {
        1: "Thẻ của em: red = đỏ; blue = xanh dương; pen = bút mực; book = sách. Người lớn có thể đọc từng thẻ cùng em.",
        2: "Thẻ của em: red = đỏ; blue = xanh dương; ball = bóng; car = ô tô. Em ghép hai thẻ để gọi tên đồ chơi.",
        3: "This is Mia's room. The red ball is under the chair. The blue bag is on the chair. There are three books on the desk. Mia likes reading.",
        4: "It is rainy today. Lucy and Nam cannot play football outside. They can draw in the classroom. Lucy can draw a cat. Nam can draw a bird. They will play football tomorrow if it is sunny.",
        5: "On Sunday, Amy's class visited a park with their teacher. They collected paper near the lake. Amy found a small bird, but she did not touch it. She asked her teacher for help. The teacher called a wildlife rescue centre. Next week, the class will make posters about keeping the park clean.",
    }
    rows = {
        1: [
            ("Thẻ nào có nghĩa là sách?", "book", ["pen", "bag"], "Book là sách."),
            ("Pen là đồ vật nào?", "Bút mực", ["Cặp", "Sách"], "Pen là bút mực."),
            (
                "Bag có nghĩa là gì?",
                "Cặp",
                ["Sách", "Bút mực"],
                "Bag là cặp hoặc túi; trong bài này là cặp.",
            ),
            (
                "Em muốn chỉ chiếc cặp. Em chọn thẻ nào?",
                "bag",
                ["book", "pen"],
                "Thẻ bag dùng để gọi tên chiếc cặp.",
            ),
        ],
        2: [
            ("Cat là con gì?", "Mèo", ["Chó", "Chim"], "Cat có nghĩa là mèo."),
            ("Thẻ nào có nghĩa là chó?", "dog", ["cat", "big"], "Dog là chó."),
            ("Big có nghĩa là gì?", "To", ["Nhỏ", "Đỏ"], "Big là to, lớn."),
            ("Thẻ nào có nghĩa là nhỏ?", "small", ["big", "cat"], "Small là nhỏ."),
        ],
        3: [
            ("What is his name?", "Ben", ["Tom", "Nam"], "Câu đầu: My name is Ben."),
            ("How old is Ben?", "Nine", ["Two", "Ten"], "I am nine nghĩa là Ben chín tuổi."),
            (
                "What colour is his bag?",
                "Blue",
                ["Red", "Green"],
                "Ben có a blue bag, chiếc cặp màu xanh dương.",
            ),
            (
                "How many books are in the bag?",
                "Two",
                ["One", "Three"],
                "There are two books cho biết có hai cuốn sách.",
            ),
        ],
        4: [
            (
                "When does Anna have English?",
                "On Monday",
                ["On Sunday", "On Friday"],
                "Câu đầu nêu thời gian là On Monday.",
            ),
            (
                "What subject does Anna like?",
                "English",
                ["Art", "Music"],
                "She likes English cho biết môn Anna thích.",
            ),
            (
                "Who plays badminton with Anna?",
                "Mai",
                ["Tom", "Ben"],
                "Anna chơi cầu lông with Mai.",
            ),
            (
                "Where do they play?",
                "In the school yard",
                ["In the kitchen", "At the beach"],
                "Câu cuối nêu địa điểm in the school yard.",
            ),
        ],
        5: [
            (
                "Where are Tom and his sister going?",
                "To the library",
                ["To the zoo", "To the market"],
                "Câu thứ hai nói họ đang đi đến thư viện.",
            ),
            (
                "How are they travelling?",
                "By bus",
                ["By bike", "On foot"],
                "By bus cho biết phương tiện là xe buýt.",
            ),
            (
                "What books do they want to borrow?",
                "Books about animals",
                ["Books about cars", "Books about food"],
                "Họ muốn mượn sách về động vật.",
            ),
            (
                "When will they meet their mother?",
                "At ten",
                ["At nine", "At twelve"],
                "Bài đọc nói gặp mẹ ở thư viện lúc mười giờ.",
            ),
        ],
    }
    vip_rows = {
        1: [
            ("Red là màu gì?", "Đỏ", ["Xanh dương", "Vàng"], "Red có nghĩa là đỏ."),
            ("Thẻ nào là màu xanh dương?", "blue", ["red", "book"], "Blue là xanh dương."),
            (
                "A red pen là gì?",
                "Một bút mực đỏ",
                ["Một sách đỏ", "Một bút mực xanh dương"],
                "Red là đỏ, pen là bút mực.",
            ),
            (
                "A blue book là gì?",
                "Một cuốn sách xanh dương",
                ["Một bút mực xanh dương", "Một cuốn sách đỏ"],
                "Blue là xanh dương, book là sách.",
            ),
            (
                "Em chọn bút mực, không chọn sách. Thẻ nào đúng?",
                "pen",
                ["book", "blue"],
                "Pen chỉ bút mực; book chỉ sách; blue chỉ màu.",
            ),
            (
                "Muốn nói sách đỏ, em ghép thẻ nào?",
                "red + book",
                ["blue + pen", "red + pen"],
                "Red chỉ màu đỏ; book chỉ sách.",
            ),
        ],
        2: [
            (
                "A red ball là gì?",
                "Một quả bóng đỏ",
                ["Một ô tô đỏ", "Một quả bóng xanh dương"],
                "Red là đỏ, ball là bóng.",
            ),
            (
                "A blue car là gì?",
                "Một ô tô xanh dương",
                ["Một ô tô đỏ", "Một quả bóng xanh dương"],
                "Blue là xanh dương, car là ô tô.",
            ),
            (
                "Muốn gọi quả bóng xanh dương, em chọn gì?",
                "blue ball",
                ["red car", "blue car"],
                "Chọn blue cho màu và ball cho đồ vật.",
            ),
            ("Thẻ nào gọi tên ô tô?", "car", ["ball", "red"], "Car là ô tô."),
            (
                "Trong red ball, từ nào chỉ màu?",
                "red",
                ["ball", "car"],
                "Red chỉ màu đỏ, ball chỉ đồ vật.",
            ),
            (
                "Đổi red car thành blue car thì điều gì thay đổi?",
                "Màu của ô tô",
                ["Ô tô thành bóng", "Không còn đồ chơi"],
                "Car vẫn là ô tô; chỉ đổi red sang blue.",
            ),
        ],
        3: [
            (
                "Where is the red ball?",
                "Under the chair",
                ["On the desk", "In the bag"],
                "The red ball is under the chair: bóng ở dưới ghế.",
            ),
            (
                "What is on the chair?",
                "The blue bag",
                ["The red ball", "Three books"],
                "The blue bag is on the chair.",
            ),
            (
                "How many books are on the desk?",
                "Three",
                ["Two", "Four"],
                "Bài đọc ghi three books on the desk.",
            ),
            (
                "What does Mia like?",
                "Reading",
                ["Swimming", "Singing"],
                "Mia likes reading nghĩa là Mia thích đọc sách.",
            ),
            (
                "Choose the true sentence.",
                "The ball is under the chair.",
                ["The ball is on the desk.", "The bag is under the chair."],
                "Chỉ câu bóng ở dưới ghế khớp với bài đọc.",
            ),
            (
                "Mia wants a book. Where should she look?",
                "On the desk",
                ["Under the chair", "In the red ball"],
                "Sách ở trên bàn nên tìm on the desk.",
            ),
        ],
        4: [
            (
                "What is the weather like today?",
                "Rainy",
                ["Sunny", "Snowy"],
                "Câu đầu nói It is rainy today.",
            ),
            (
                "Why can't they play football outside today?",
                "It is rainy.",
                ["It is sunny.", "They have no classroom."],
                "Trời mưa nên hai bạn không chơi bóng bên ngoài.",
            ),
            (
                "What can they do in the classroom?",
                "Draw",
                ["Swim", "Play football outside"],
                "They can draw in the classroom.",
            ),
            (
                "Who can draw a cat?",
                "Lucy",
                ["Nam", "Their teacher"],
                "Bài đọc nêu Lucy can draw a cat.",
            ),
            ("What can Nam draw?", "A bird", ["A cat", "A fish"], "Nam can draw a bird."),
            (
                "They will play football tomorrow if it is ...",
                "sunny",
                ["rainy", "snowy"],
                "Câu cuối đặt điều kiện if it is sunny, không khẳng định ngày mai chắc chắn nắng.",
            ),
        ],
        5: [
            (
                "When did Amy's class visit the park?",
                "On Sunday",
                ["On Monday", "Next week"],
                "Câu đầu ghi On Sunday và dùng quá khứ visited.",
            ),
            (
                "What did they collect near the lake?",
                "Paper",
                ["Birds", "Flowers"],
                "They collected paper near the lake.",
            ),
            (
                "What did Amy do after finding the bird?",
                "She asked her teacher for help.",
                ["She took it home.", "She touched it."],
                "Amy không chạm vào chim và nhờ giáo viên giúp.",
            ),
            (
                "Who called the wildlife rescue centre?",
                "The teacher",
                ["Amy's mother", "The bus driver"],
                "Câu The teacher called... xác định rõ người gọi.",
            ),
            (
                "What will the class do next week?",
                "Make posters",
                ["Sell birds", "Build a lake"],
                "Kế hoạch tuần tới là làm áp phích giữ công viên sạch.",
            ),
            (
                "Which sentence describes a future plan?",
                "The class will make posters.",
                ["Amy found a bird.", "They collected paper."],
                "Will make diễn tả kế hoạch tương lai; found và collected kể việc đã xảy ra.",
            ),
        ],
    }
    titles = {
        1: ("Thẻ đồ dùng của em", "Ghép màu với đồ vật"),
        2: ("Thẻ con vật và kích thước", "Đồ chơi đổi màu"),
        3: ("Meet Ben", "Find it in Mia's room"),
        4: ("Anna's school day", "A rainy-day plan"),
        5: ("A trip to the library", "Helping at the park"),
    }
    topic = "stories" if grade == 5 else "school"
    free_pictures = {
        1: ("pen", "book", "bag"),
        2: ("cat", "dog"),
        3: ("bag", "book"),
        4: ("school", "book"),
        5: ("bus", "book", "water"),
    }
    vip_pictures = {
        1: ("red", "blue", "pen", "book"),
        2: ("red", "blue", "ball", "car"),
        3: ("ball", "chair", "desk", "book"),
        4: ("rain", "cat", "bird"),
        5: ("bird", "school"),
    }
    return [
        unit(
            grade,
            topic,
            "english-everyday",
            titles[grade][0],
            contexts[grade],
            "Nhìn thẻ, đọc một từ hoặc một câu rồi chỉ vào ý đúng.",
            "Đọc theo từng cụm ngắn. Chưa hiểu thì xem lại thẻ.",
            [
                "Tìm từ quen thuộc trước.",
                "Ghép từ tiếng Anh với nghĩa tiếng Việt trong thẻ."
                if grade <= 2
                else "Câu hỏi Who hỏi ai, Where hỏi ở đâu, When hỏi khi nào.",
                "Đối chiếu câu trả lời với thẻ hoặc câu trong bài.",
            ],
            cards(*free_pictures[grade]),
            rows[grade],
            context=contexts[grade],
        ),
        unit(
            grade,
            topic,
            "english-detective",
            titles[grade][1],
            vip_contexts[grade],
            "Chú ý từ chỉ màu, vị trí hoặc thời gian. Mỗi từ giúp em chọn đúng ý.",
            "Dựa vào thẻ và bài đọc, không cần đoán thông tin bên ngoài.",
            [
                "Tìm đồ vật hoặc nhân vật được hỏi.",
                "Đọc từ bên cạnh: màu, vị trí hoặc thời gian.",
                "Thử bỏ các lựa chọn không đúng với bài.",
            ],
            cards(*vip_pictures[grade]),
            vip_rows[grade],
            vip=True,
            context=vip_contexts[grade],
        ),
    ]
