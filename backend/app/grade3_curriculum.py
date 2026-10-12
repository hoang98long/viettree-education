"""68 lessons / 384 questions / 56 assessments, matching grade four by subject and plan.

The first four topics per subject each pair two foundation lessons with eight questions.
The remaining lessons each have their own six/eight-question assessment.
"""

from app.grade3_english import ENGLISH
from app.grade3_math import MATH
from app.grade3_vietnamese import VIETNAMESE

TOPICS = {
    "MATH": {
        "numbers": "Số trong phạm vi 100 000 và chữ số La Mã",
        "operations": "Phép tính, biểu thức và chia có dư",
        "parts": "Nhận biết một phần của hình và nhóm đồ vật",
        "measurement": "Độ dài, khối lượng, dung tích, thời gian và tiền",
        "geometry": "Hình học, chu vi và diện tích",
        "statistics": "Đọc bảng số liệu và kiểm đếm",
        "wordproblems": "Giải toán hai bước và lập luận",
        "chance": "Có thể, chắc chắn và không thể",
    },
    "VIETNAMESE": {
        "reading": "Đọc truyện, thơ và văn bản hướng dẫn",
        "vocabulary": "Vốn từ, ngữ cảnh và hình ảnh so sánh",
        "sentences": "Câu, dấu câu và lời nhân vật",
        "spelling": "Chính tả và viết hoa",
        "writing": "Viết đoạn, lời nhắn và thư ngắn",
        "speaking": "Nghe, kể và trao đổi ý kiến",
    },
    "ENGLISH": {
        "self": "Chào hỏi, tên, tuổi và bạn bè",
        "school": "Đồ dùng và giao tiếp trong lớp",
        "family": "Người thân và giới thiệu gia đình",
        "home": "Phòng và vị trí đồ vật",
        "toys": "Đồ chơi, màu sắc và số lượng",
        "pets": "Con vật nuôi quanh em",
        "hobbies": "Sở thích, khả năng và hoạt động",
    },
}

ALL = {"MATH": MATH, "VIETNAMESE": VIETNAMESE, "ENGLISH": ENGLISH}
FOCUS = {
    "MATH": {
        "numbers": "Đọc, viết, so sánh, làm tròn và La Mã đến XX; không học lớp triệu.",
        "operations": "Bảng nhân/chia, tính đặt cột, biểu thức và kiểm tra số dư.",
        "parts": "Một phần của hình hoặc nhóm chia đều; không yêu cầu bốn phép tính phân số.",
        "measurement": "mm, g, ml, giờ, lịch và tiền; cần thêm hoạt động đo vật thật.",
        "geometry": "Chu vi/diện tích; cần thêm góc vuông, đường tròn, hình khối và thực hành vẽ.",
        "statistics": "Đọc bảng và kiểm đếm; cần thêm thu thập số liệu ở lớp.",
        "wordproblems": "Hai bước, số hộp tối thiểu và đếm khoảng; kiểm tra dữ kiện/điều kiện.",
        "chance": "Nhận biết có thể, chắc chắn, không thể; cần tăng câu phân loại và thực nghiệm.",
    },
    "VIETNAMESE": {
        "reading": "Truyện/thơ/văn bản hướng dẫn, trình tự và bằng chứng; cần tăng độ dài/số văn bản.",
        "vocabulary": "Từ theo chủ điểm, nghĩa trong câu và nét giống nhau trong so sánh.",
        "sentences": "Câu, hỏi/cảm, lời nhân vật; cần thêm câu khiến, ngoặc kép và dấu hai chấm liệt kê.",
        "spelling": "Viết hoa tên riêng, chính tả theo ngữ cảnh; cần nghe–viết có người hướng dẫn.",
        "writing": "Đoạn tả/kể, lời nhắn/thư; cần luyện văn mở, giới thiệu bản thân và tờ khai.",
        "speaking": "Kể theo trình tự và trao đổi có lí do; thực hành nghe/nói cần người hướng dẫn.",
    },
    "ENGLISH": {
        "self": "Tên, tuổi, chào hỏi và thẻ bạn bè; cần luyện hỏi đáp trực tiếp.",
        "school": "Đồ dùng, chỉ dẫn, xin phép/nhờ giúp; cần âm thanh để luyện nghe.",
        "family": "Người thân, he/she và thông tin gia đình; không yêu cầu dữ liệu riêng thật.",
        "home": "Phòng, in/on/under, đọc vị trí và số lượng; cần luyện mô tả bằng lời.",
        "toys": "Đồ chơi, màu, there is/are và loại trừ theo điều kiện.",
        "pets": "Tên, màu, vị trí và can/cannot của vật nuôi; cần nghe/nói từ vựng.",
        "hobbies": "Sở thích, khả năng và việc đang làm; cần phát âm và tương tác nói.",
    },
}
CORE, EXTENSION = {}, {}
for subject, units in ALL.items():
    CORE[subject] = []
    for index in range(0, 8, 2):
        first, second = units[index : index + 2]
        assert first["topic"] == second["topic"]
        CORE[subject].append(
            {
                "code": first["topic"],
                "title": TOPICS[subject][first["topic"]],
                "lessons": [first["lesson"], second["lesson"]],
                "questions": first["questions"] + second["questions"],
            }
        )
    EXTENSION[subject] = [dict(item, sort_order=30 + i) for i, item in enumerate(units[8:])]

# Counts express this pack's inventory, not completion of the entire national programme.
EXPECTED = {
    "MATH": {"topics": 8, "lessons": 25, "questions": 142, "assessments": 21},
    "VIETNAMESE": {"topics": 6, "lessons": 23, "questions": 130, "assessments": 19},
    "ENGLISH": {"topics": 7, "lessons": 20, "questions": 112, "assessments": 16},
}
