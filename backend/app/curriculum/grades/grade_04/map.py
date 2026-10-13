"""Editorial topic map. Counts indicate resources, never programme completion."""

SOURCES = {
    "MATH": "https://thbausen.hcm.edu.vn/chuong-trinh-chinh-thuc/chuong-trinh-giao-duc-pho-thong-2018-mon-toan/ctmb/85329/442867",
    "VIETNAMESE": "https://thlequydongovap.hcm.edu.vn/chuong-trinh-giao-duc-pho-thong-2018/chuong-trinh-mon-ngu-van-2018/ctmb/128814/1220407",
    "ENGLISH": "https://thptnguyenvancu.hcm.edu.vn/chuong-trinh-gdpt-2018/chuong-trinh-gdpt-2018-mon-tieng-anh/ctmb/91079/457480",
}

TOPIC_MAP = {
    "MATH": {
        "numbers": ("Số đến lớp triệu", "Đọc, viết, so sánh, làm tròn; chẵn, lẻ."),
        "operations": (
            "Phép tính và biểu thức",
            "Bốn phép tính, tính nhẩm; cần bổ sung biểu thức chứa chữ.",
        ),
        "fractions": ("Phân số", "Rút gọn, so sánh, bốn phép tính và phân số của một số."),
        "measurement": ("Đo lường", "Đơn vị diện tích, khối lượng, thời gian và vận dụng thực tế."),
        "geometry": (
            "Hình học",
            "Góc, vuông góc, song song; cần bổ sung hình bình hành, hình thoi và thực hành vẽ.",
        ),
        "statistics": (
            "Thống kê",
            "Đọc bảng, biểu đồ cột, trung bình cộng; cần thêm hoạt động thu thập số liệu.",
        ),
        "chance": (
            "Xác suất đơn giản",
            "Kiểm đếm kết quả thực nghiệm; không yêu cầu công thức xác suất.",
        ),
        "wordproblems": (
            "Giải quyết vấn đề",
            "Tổng–hiệu, giải theo bước, lập luận và kiểm tra dữ kiện.",
        ),
    },
    "VIETNAMESE": {
        "reading": ("Đọc hiểu", "Tìm thông tin, bằng chứng, trình tự; cần thêm thơ và kịch."),
        "wordtypes": ("Từ loại", "Danh từ, động từ, tính từ trong ngữ cảnh."),
        "sentences": (
            "Câu và dấu câu",
            "Thành phần câu, trạng ngữ, dẫn lời; cần thêm dấu ngoặc đơn và ngoặc kép chỉ tên tác phẩm.",
        ),
        "vocabulary": (
            "Vốn từ",
            "Từ theo chủ điểm và nghĩa trong ngữ cảnh; cần thêm thực hành tra từ điển.",
        ),
        "writing": (
            "Viết",
            "Tả cây/con vật, thuật việc và sửa bài; cần bổ sung thư, đơn, báo cáo theo mẫu.",
        ),
        "speaking": (
            "Nói và nghe",
            "Thảo luận, lí lẽ, ghi ý; cần thực hành có người hướng dẫn và nhận xét.",
        ),
    },
    "ENGLISH": {
        "family": (
            "Gia đình",
            "Đọc và hỏi đáp về người thân; cần mở rộng nghề nghiệp và ngoại hình.",
        ),
        "school": ("Trường học", "Môn học và hoạt động học tập, ngoại khóa."),
        "routines": ("Hoạt động hằng ngày", "Thời gian, lịch và kết hợp thông tin."),
        "weather": ("Thế giới quanh em", "Thời tiết và hoạt động phù hợp."),
        "abilities": ("Những việc có thể làm", "Can / can't và hỏi đáp đơn giản."),
        "places": ("Chỉ đường", "Chỉ dẫn ngắn, biển chỉ dẫn và vị trí."),
        "food": (
            "Sở thích và lời mời",
            "Like / would; bối cảnh bữa ăn là ngữ liệu bổ trợ về sở thích.",
        ),
        "animals": ("Động vật", "Cần biên soạn bài đọc và hoạt động giao tiếp về động vật."),
        "past": ("Quá khứ đơn", "Cần bài nền tảng có ngữ cảnh và câu trả lời đơn giản."),
        "listening": (
            "Nghe và phát âm",
            "Cần âm thanh được rà soát và hoạt động nghe/nói; bài đọc chưa thay thế kỹ năng này.",
        ),
    },
}
