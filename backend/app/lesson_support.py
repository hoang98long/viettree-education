"""Original teaching suggestions and diagrams, independent of learning statistics."""

from copy import deepcopy

SUPPORT = {
    "wordtypes": (
        "Phân biệt danh từ, động từ và tính từ trong câu.",
        [
            "Đọc cả câu để hiểu từ đang nói về điều gì.",
            "Tìm từ chỉ người/vật, hoạt động và đặc điểm.",
            "Thử đặt câu khác để kiểm tra cách dùng từ.",
        ],
        "Em tìm được ba từ chỉ hoạt động trong ngày của mình không?",
        "reading",
    ),
    "weather": (
        "Đọc và nói về thời tiết bằng câu tiếng Anh ngắn.",
        [
            "Tìm từ chỉ thời tiết như sunny, rainy hoặc windy.",
            "Đọc câu hỏi để biết đang hỏi thời tiết hay hoạt động.",
            "Dùng mẫu câu trong ví dụ để nói về hôm nay.",
        ],
        "Em có thể nói một câu tiếng Anh về thời tiết hôm nay không?",
        "reading",
    ),
    "numbers": (
        "Đọc số theo từng lớp và nêu giá trị một chữ số.",
        [
            "Tách số thành nhóm ba chữ số từ phải sang trái.",
            "Đọc tên hàng trước khi tính giá trị chữ số.",
            "Viết số thành tổng các hàng rồi kiểm tra lại.",
        ],
        "Em giải thích được vì sao cùng chữ số nhưng giá trị khác nhau không?",
        "reading",
    ),
    "operations": (
        "Lập thứ tự giải và kiểm tra kết quả phép tính.",
        [
            "Gạch chân dữ kiện và điều đề hỏi.",
            "Viết mỗi bước tính kèm đơn vị; thực hiện ngoặc trước.",
            "Ước lượng hoặc dùng phép tính ngược để kiểm tra.",
        ],
        "Nếu bỏ một dữ kiện, em còn giải được không? Vì sao?",
        "reading",
    ),
    "fractions": (
        "Giải thích phân số bằng các phần bằng nhau.",
        [
            "Chọn cùng một đơn vị, chẳng hạn một chiếc bánh.",
            "Đếm tổng số phần bằng nhau trước, phần được chọn sau.",
            "Với phép cộng hoặc trừ, đưa các phân số về cùng mẫu số.",
        ],
        "Phần tô màu và phần chưa tô ghép lại có bằng một đơn vị không?",
        "fraction",
    ),
    "measurement": (
        "Phân biệt đo quanh hình và đo phần nằm trong hình.",
        [
            "Xác định đề hỏi độ dài quanh hình hay diện tích.",
            "Đổi về cùng đơn vị rồi vẽ hình, ghi các cạnh.",
            "Chu vi dùng đơn vị độ dài; diện tích dùng đơn vị vuông.",
        ],
        "Hai hình có cùng diện tích thì có luôn cùng chu vi không?",
        "garden",
    ),
    "reading": (
        "Tìm bằng chứng trong đoạn văn trước khi kết luận.",
        [
            "Đọc câu hỏi và tìm từ khóa trong đoạn.",
            "Chỉ ra câu hoặc hành động làm bằng chứng.",
            "Phân biệt thông tin nêu trực tiếp và điều em suy ra.",
        ],
        "Câu nào trong đoạn giúp em kiểm tra ý kiến của mình?",
        "reading",
    ),
    "vocabulary": (
        "Hiểu từ trong ngữ cảnh và dùng từ phù hợp.",
        [
            "Đọc cả câu thay vì đoán từ đứng riêng.",
            "Thử thay bằng một từ quen thuộc để kiểm tra nghĩa.",
            "Đặt câu mới và đọc lại xem ý đã rõ chưa.",
        ],
        "Từ em chọn có thay đổi nghĩa khi đặt trong câu khác không?",
        "reading",
    ),
    "sentences": (
        "Viết câu rõ người, việc và mối liên hệ giữa các ý.",
        [
            "Tìm bộ phận chỉ người hoặc vật và bộ phận nói về họ.",
            "Chọn từ nối phù hợp: nguyên nhân, đối lập hay trình tự.",
            "Đọc lại, kiểm tra dấu câu và bỏ từ bị lặp.",
        ],
        "Em có thể sửa câu dài thành hai câu rõ hơn không?",
        "reading",
    ),
    "writing": (
        "Lập dàn ý và chọn chi tiết cụ thể khi viết.",
        [
            "Chọn người đọc và điều em muốn kể.",
            "Ghi ba ý chính trước khi viết thành đoạn.",
            "Thêm chi tiết nhìn thấy, nghe thấy; đọc lại và sửa.",
        ],
        "Chi tiết nào khiến người đọc hình dung rõ nhất?",
        "reading",
    ),
    "school": (
        "Đọc và nói về đồ dùng, hoạt động ở trường.",
        [
            "Tìm từ chỉ đồ vật, người hoặc nơi trong câu.",
            "Quan sát động từ và từ chỉ thời gian.",
            "Đọc cả câu rồi dùng mẫu đó để nói về lớp mình.",
        ],
        "Em có thể nói một câu tiếng Anh về đồ dùng học tập của mình không?",
        "clock",
    ),
    "routines": (
        "Kể hoạt động thường ngày theo thứ tự.",
        [
            "Tìm người thực hiện hoạt động trong câu.",
            "Tìm các từ first, then, before, after hoặc giờ cụ thể.",
            "Kể lại theo trình tự rồi đối chiếu đoạn gốc.",
        ],
        "Nếu đổi thứ tự hai hoạt động, câu chuyện có còn hợp lý không?",
        "clock",
    ),
    "family": (
        "Dùng thông tin trong đoạn để nói về gia đình.",
        [
            "Tìm tên hoặc từ chỉ thành viên gia đình.",
            "Ghép từng người với thông tin được nêu.",
            "Trả lời bằng câu ngắn; không thêm điều đoạn chưa nói.",
        ],
        "Em có thể nói một câu về một người thân mà không nêu thông tin riêng tư không?",
        "reading",
    ),
    "places": (
        "Đọc vị trí và đường đi theo các mốc.",
        [
            "Tìm nơi bắt đầu và nơi cần đến.",
            "Chú ý từ near, next to, opposite và hướng rẽ.",
            "Đi lại từng bước trên sơ đồ tưởng tượng để kiểm tra.",
        ],
        "Em sẽ dùng mốc nào để giải thích đường đi dễ hiểu hơn?",
        "reading",
    ),
}


def enrich(content, topic_code):
    result = deepcopy(content)
    result.setdefault("blocks", [])
    topic = topic_code.rsplit("-", 1)[-1]
    goal, hints, reflection, kind = SUPPORT.get(
        topic,
        (
            "Giải thích lại ý chính bằng lời của em.",
            [
                "Đọc yêu cầu và đánh dấu từ quan trọng.",
                "Thử lại ví dụ từng bước.",
                "Kiểm tra kết quả và giải thích cách làm.",
            ],
            "Em đã hiểu điều gì và muốn hỏi thêm điều gì?",
            "reading",
        ),
    )
    captions = {
        "fraction": "Ví dụ minh họa: 3 trong 8 phần bằng nhau được tô màu, tức là 3/8.",
        "garden": "Ví dụ minh họa: luống rau hình chữ nhật gồm 3 hàng, 4 cột ô vuông, mỗi ô có cạnh 1 m.",
        "reading": "Hành trình đọc: đọc yêu cầu → tìm bằng chứng → giải thích → kiểm tra.",
        "clock": "Đồng hồ minh họa 8 giờ sáng: kim ngắn chỉ giờ, kim dài chỉ phút.",
    }
    result.setdefault("goals", [goal])
    result.setdefault("hints", hints)
    result.setdefault("reflection", [reflection])
    result.setdefault(
        "illustration",
        {
            "kind": kind,
            "caption": captions[kind],
            "numerator": 3,
            "denominator": 8,
            "rows": 3,
            "columns": 4,
            "hour": 8,
            "minute": 0,
        },
    )
    return result
