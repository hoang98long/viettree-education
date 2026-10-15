"""Picture-supported familiarisation and four-question reading missions."""

from app.curriculum.supplements.explorers.builders import cards, pick, unit


def content(grade):
    stories = {
        1: "Thẻ con vật: cat = mèo; dog = chó; bird = chim. Em có thể nhờ người lớn đọc từng từ rồi nhắc lại.",
        2: "Thẻ bữa sáng: milk = sữa; bread = bánh mì; egg = trứng; water = nước uống. Em có thể nhờ người lớn đọc cùng.",
        3: "Ben can swim. He cannot ride a bike. Mia can ride a bike. She likes reading books. They like playing in the park.",
        4: "On Tuesday, Rose has English at school. After school, she plays the guitar at four. Her brother plays football at five. They have dinner at six.",
        5: "From the school gate, go straight to the bakery. Turn right at the bakery. The library is next to the park. Meet your teacher at the library at nine. Do not turn left at the bakery.",
    }
    rows = {
        1: [
            ("Cat là con gì?", "Mèo", ["Chó", "Chim"], "Thẻ cat có nghĩa là mèo."),
            ("Thẻ nào có nghĩa là chim?", "bird", ["dog", "cat"], "Bird có nghĩa là chim."),
            ("Dog có nghĩa là gì?", "Chó", ["Mèo", "Chim"], "Dog có nghĩa là chó."),
            (
                "Muốn chỉ con mèo, em chọn thẻ nào?",
                "cat",
                ["bird", "dog"],
                "Chọn cat để gọi tên con mèo.",
            ),
        ],
        2: [
            ("Milk có nghĩa là gì?", "Sữa", ["Trứng", "Bánh mì"], "Milk là sữa."),
            ("Thẻ nào chỉ bánh mì?", "bread", ["egg", "water"], "Bread là bánh mì."),
            ("Egg có nghĩa là gì?", "Trứng", ["Sữa", "Nước uống"], "Egg là trứng."),
            (
                "Em muốn chỉ nước uống. Thẻ nào đúng?",
                "water",
                ["milk", "bread"],
                "Water là nước uống trong các thẻ của bài.",
            ),
        ],
        3: [
            ("What can Ben do?", "Swim", ["Ride a bike", "Fly"], "Ben can swim: Ben có thể bơi."),
            (
                "Can Ben ride a bike?",
                "No, he cannot.",
                ["Yes, he can.", "Yes, she can."],
                "He cannot ride a bike cho biết Ben chưa đi xe đạp được.",
            ),
            (
                "Who can ride a bike?",
                "Mia",
                ["Ben", "Ben's father"],
                "Mia can ride a bike xác định Mia là người có thể đi xe đạp.",
            ),
            (
                "What does Mia like?",
                "Reading books",
                ["Flying a plane", "Cooking rice"],
                "She likes reading books nói về sở thích của Mia.",
            ),
        ],
        4: [
            (
                "When does Rose have English?",
                "On Tuesday",
                ["On Monday", "On Sunday"],
                "Câu đầu nêu On Tuesday.",
            ),
            (
                "What does Rose do at four?",
                "Plays the guitar",
                ["Has dinner", "Plays football"],
                "She plays the guitar at four: Rose chơi đàn lúc bốn giờ.",
            ),
            (
                "Who plays football at five?",
                "Her brother",
                ["Rose", "Her teacher"],
                "Her brother plays football at five xác định người anh hoặc em trai của Rose.",
            ),
            (
                "Which activity happens last in the text?",
                "Having dinner",
                ["Playing the guitar", "Playing football"],
                "Chơi đàn lúc 4, bóng đá lúc 5, ăn tối lúc 6 nên ăn tối là việc sau cùng được nêu.",
            ),
        ],
        5: [
            (
                "Where do you turn right?",
                "At the bakery",
                ["At the school gate", "At the lake"],
                "Chỉ dẫn nói Turn right at the bakery.",
            ),
            (
                "What is the library next to?",
                "The park",
                ["The airport", "The station"],
                "The library is next to the park: thư viện cạnh công viên.",
            ),
            (
                "Where will you meet the teacher?",
                "At the library",
                ["At the bakery", "At home"],
                "Điểm hẹn được ghi rõ là at the library.",
            ),
            (
                "Which instruction is correct at the bakery?",
                "Turn right.",
                ["Turn left.", "Go back to the gate."],
                "Turn right là chỉ dẫn đúng; đoạn còn nhắc không rẽ trái ở tiệm bánh.",
            ),
        ],
    }
    titles = {
        1: "Hello, little animals!",
        2: "My breakfast cards",
        3: "What can our friends do?",
        4: "Rose's Tuesday timetable",
        5: "Follow the library directions",
    }
    topics = {1: "pets", 2: "home", 3: "hobbies", 4: "routines", 5: "travel"}
    pictures = {
        1: ("cat", "dog", "bird"),
        2: ("milk", "bread", "egg", "water"),
        3: ("bicycle", "book"),
        4: ("clock", "ball"),
        5: ("school", "book"),
    }
    return unit(
        grade,
        topics[grade],
        "english-mission",
        titles[grade],
        "Ghép từ với tranh."
        if grade <= 2
        else "Dùng thông tin trong đoạn để trả lời bốn câu ngắn.",
        stories[grade],
        "Nhìn tranh, đọc cùng người lớn và chọn từ đúng."
        if grade <= 2
        else "At four = lúc bốn giờ; next to = bên cạnh. Tìm câu có thông tin được hỏi.",
        "Chỉ chọn điều thẻ hoặc bài đọc đã cho biết.",
        [
            "Tìm một từ em đã biết.",
            "Đọc câu có nhân vật hoặc đồ vật được hỏi.",
            "So lựa chọn với thẻ hoặc câu trong đoạn, rồi thử đọc lại.",
        ],
        cards(*pictures[grade]),
        [pick(*row) for row in rows[grade]],
        vip=grade >= 3,
        context=stories[grade],
    )
