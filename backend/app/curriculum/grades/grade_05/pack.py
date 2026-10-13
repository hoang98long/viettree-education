"""Complete inventory and documented topic map for the grade-five supplement."""

from app.curriculum.grades.grade_05.english import ENGLISH
from app.curriculum.grades.grade_05.math import MATH
from app.curriculum.grades.grade_05.vietnamese import VIETNAMESE

TOPICS = {
    "MATH": {
        "fractions": "Ôn số tự nhiên, phân số và hỗn số",
        "decimals": "Đọc, so sánh và làm tròn số thập phân",
        "operations": "Phép tính thập phân và bài toán nhiều bước",
        "ratio": "Tỉ số, phần trăm, tổng–hiệu–tỉ và bản đồ",
        "measurement": "Diện tích, thể tích và đơn vị thời gian",
        "geometry": "Tam giác, hình thang và hình tròn",
        "solids": "Hình khai triển, diện tích và thể tích khối",
        "motion": "Chuyển động đều: vận tốc, quãng đường, thời gian",
        "statistics": "Biểu đồ quạt tròn và tỉ số quan sát",
    },
    "VIETNAMESE": {
        "reading": "Đọc truyện, thơ, thông tin và suy luận có bằng chứng",
        "vocabulary": "Từ điển, đồng nghĩa, đa nghĩa và sắc thái từ",
        "sentences": "Đại từ, kết từ, câu ghép và liên kết câu",
        "writing": "Tả người/cảnh, ý kiến, kết thúc sáng tạo và báo cáo",
        "spelling": "Tên nước ngoài, gạch nối và dấu gạch ngang",
        "speaking": "Nghe ghi ý chính, nói và phản hồi theo lượt",
    },
    "ENGLISH": {
        "self": "Friends, home, dream jobs and polite interviews",
        "school": "Routines, frequency and school activities",
        "health": "Health words, should and asking adults for help",
        "travel": "Transport, directions and travel plans",
        "nature": "Seasons, weather and caring for the environment",
        "stories": "Past events, future plans and short messages",
        "food": "Food, quantities and polite shopping dialogues",
    },
}

FOCUS = {
    "MATH": "Tính có đơn vị và giải thích; thêm thực hành đo/vẽ, gấp mô hình và thu thập dữ liệu tại lớp.",
    "VIETNAMESE": "Truyện/miêu tả/thơ/thông tin có ngữ liệu tự viết; bài viết mở và nghe/nói cần người hướng dẫn nhận xét.",
    "ENGLISH": "Ngữ liệu đọc 60–80 từ, quá khứ/tương lai và giao tiếp quen; luyện viết 30–40 từ, nghe/nói cùng người hướng dẫn, chưa có audio/chấm phát âm.",
}
TOPIC_MAP = {
    subject: {code: (title, FOCUS[subject]) for code, title in topics.items()}
    for subject, topics in TOPICS.items()
}
SOURCES = {
    "MATH": "https://fileth.hcm.shieldix.app/data/hcmedu/thbausen/2020_3/cttoan_193202020.pdf",
    "VIETNAMESE": "https://fileth.hcm.shieldix.app/data/hcmedu/thleductho/attachments/2019_8/2_ctngu_van_18201918.pdf",
    "ENGLISH": "https://fileth.hcm.shieldix.app/data/hcmedu/thlamsonbinhthanh/2020_1/chuong_trinh_mon_tieng_anh_lop_3_den_lop_12_101202010.pdf",
}
ALL = {"MATH": MATH, "VIETNAMESE": VIETNAMESE, "ENGLISH": ENGLISH}
CORE, EXTENSION = {}, {}
for subject, units in ALL.items():
    CORE[subject] = []
    for index in range(0, 8, 2):
        first, second = units[index : index + 2]
        if first["topic"] != second["topic"]:
            raise ValueError("Hai bài nền tảng phải cùng chủ đề")
        CORE[subject].append(
            dict(
                code=first["topic"],
                title=TOPICS[subject][first["topic"]],
                lessons=[first["lesson"], second["lesson"]],
                questions=first["questions"] + second["questions"],
            )
        )
    EXTENSION[subject] = units[8:]

EXPECTED = {
    "MATH": {"topics": 9, "lessons": 25, "questions": 142, "assessments": 21},
    "VIETNAMESE": {"topics": 6, "lessons": 23, "questions": 130, "assessments": 19},
    "ENGLISH": {"topics": 7, "lessons": 20, "questions": 112, "assessments": 16},
}
