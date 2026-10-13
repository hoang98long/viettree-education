"""Two original packs matching grades 3/4 in quantity, not in difficulty."""

from app.curriculum.grades.early_primary.builders import assemble
from app.curriculum.grades.early_primary.english import curriculum as english
from app.curriculum.grades.early_primary.math import curriculum as math
from app.curriculum.grades.early_primary.vietnamese import curriculum as vietnamese

TOPICS = {
    1: {
        "MATH": dict(
            numbers="Số, chục và đơn vị đến 100",
            operations="Cộng, trừ không nhớ đến 100",
            geometry="Nhận biết hình phẳng và khối",
            measurement="So và đo độ dài bằng cm",
            time="Giờ đúng và các ngày trong tuần",
            wordproblems="Thêm, bớt bằng một phép tính",
            sorting="Phân nhóm theo hình dạng",
            patterns="Quan sát mẫu hình lặp",
        ),
        "VIETNAMESE": dict(
            letters="Âm, chữ và ghép tiếng",
            rhymes="Vần và dấu thanh",
            reading="Đọc câu, truyện, thơ và chỉ dẫn ngắn",
            vocabulary="Từ quen thuộc ở nhà và trường",
            writing="Viết đúng tiếng, câu và dấu câu",
            speaking="Chào hỏi, nghe và nói theo lượt",
        ),
        "ENGLISH": dict(
            self="Chào hỏi và tên",
            school="Đồ dùng và chỉ dẫn trong lớp",
            colours="Các màu quen thuộc",
            numbers="Làm quen số đếm 1–10",
            pets="Tên con vật và chữ đầu",
            toys="Đồ chơi và mẫu lặp",
            home="Người thân, quả và bộ phận cơ thể",
        ),
    },
    2: {
        "MATH": dict(
            numbers="Số và các hàng đến 1000",
            operations="Cộng, trừ đến 1000, không quá một lượt nhớ",
            groups="Nhân, chia theo bảng 2 và 5",
            measurement="Độ dài, kg và lít",
            geometry="Đường gấp khúc, tứ giác và khối",
            time="Giờ, 15/30 phút và lịch",
            statistics="Biểu đồ tranh và khả năng xảy ra",
            wordproblems="Bài toán một bước, nhiều hơn/ít hơn",
        ),
        "VIETNAMESE": dict(
            reading="Đọc truyện, thơ, thông báo và bìa sách",
            vocabulary="Từ chỉ sự vật, hoạt động, đặc điểm",
            sentences="Câu và dấu chấm, hỏi, than, phẩy",
            writing="Viết câu, đoạn ngắn và lời nhắn",
            speaking="Nghe, kể và trao đổi theo lượt",
            spelling="Chữ và quy tắc chính tả",
        ),
        "ENGLISH": dict(
            self="Giới thiệu, cảm xúc, ngày và chữ",
            school="Hoạt động, chỉ dẫn và nhãn đồ dùng",
            numbers="Làm quen số đếm 11–20",
            home="Người thân, phòng, thức ăn và quần áo",
            colours="Màu sắc và thời tiết",
            pets="Con vật và cỡ to/nhỏ",
            toys="Hình, đồ chơi và số lượng",
        ),
    },
}
# Grade 2 revisits punctuation in a separate proofreading topic.
PACKS = {}
for grade in (1, 2):
    units = {"MATH": math(grade), "VIETNAMESE": vietnamese(grade), "ENGLISH": english(grade)}
    if grade == 2:
        units["VIETNAMESE"][17]["topic"] = "spelling"
    core, extension = assemble(units, TOPICS[grade])
    PACKS[grade] = {"all": units, "core": core, "extension": extension}

SOURCES = {
    "MATH": "https://fileth.hcm.shieldix.app/data/hcmedu/thleductho/attachments/2019_8/3_cttoan_18201918.pdf",
    "VIETNAMESE": "https://fileth.hcm.shieldix.app/Data/hcmedu/thlequydongovap/2023_8/02ngu-van54202222381_138202312146.pdf",
    "ENGLISH": "https://admintruong.haiphong.shieldix.app/data/haiphong/thcsandong/2023_6/1/21-cttieng-anh-12_16202320.pdf",
}
