"""Original grade-four foundation pack; stable codes preserved."""

from app.curriculum.builders import blank, choice, lesson, multiple, ordering

MATH = [
    dict(
        code="numbers",
        title="Số tự nhiên và giá trị chữ số",
        lessons=[
            lesson(
                "Hàng, lớp và cách đọc số",
                "Từ phải sang trái: đơn vị, chục, trăm, nghìn, chục nghìn, trăm nghìn. Cứ ba hàng tạo một lớp. Giá trị của chữ số phụ thuộc vào hàng mà nó đứng.",
                "Trong 325 418, chữ số 2 ở hàng chục nghìn nên có giá trị 20 000. Ta đọc: ba trăm hai mươi lăm nghìn bốn trăm mười tám.",
                "Tách số theo lớp trước khi đọc. Viết số bằng tổng giá trị các hàng giúp em kiểm tra lại.",
            ),
            lesson(
                "So sánh và làm tròn số",
                "Số có nhiều chữ số hơn thì lớn hơn. Nếu số chữ số bằng nhau, so sánh từ trái sang phải. Khi làm tròn, nhìn chữ số ngay bên phải hàng cần làm tròn: dưới 5 giữ nguyên, từ 5 trở lên tăng một.",
                "47 628 làm tròn đến hàng nghìn là 48 000 vì chữ số hàng trăm là 6. 47 328 làm tròn là 47 000.",
                "Sau khi làm tròn, các chữ số bên phải hàng được làm tròn trở thành 0.",
            ),
        ],
        questions=[
            choice(
                "Chữ số 7 trong 274 315 có giá trị bao nhiêu?",
                ["7 000", "70 000", "700", "700 000"],
                1,
                "Chữ số 7 ở hàng chục nghìn nên có giá trị 70 000.",
            ),
            choice(
                "Số nào lớn nhất?",
                ["89 999", "90 001", "90 010", "90 000"],
                2,
                "Các số 90 nghìn lớn hơn 89 999; so sánh tiếp, 90 010 lớn nhất.",
            ),
            blank(
                "Viết số gồm 4 chục nghìn, 2 nghìn và 5 đơn vị (không dùng dấu tách hàng).",
                ["42005"],
                "40 000 + 2 000 + 5 = 42 005.",
            ),
            choice(
                "Làm tròn 36 749 đến hàng nghìn.",
                ["36 000", "37 000", "36 700", "40 000"],
                1,
                "Chữ số hàng trăm là 7 nên tăng hàng nghìn từ 6 lên 7.",
            ),
            multiple(
                "Chọn tất cả số nhỏ hơn 50 000.",
                ["49 999", "50 001", "40 500", "50 000"],
                [0, 2],
                "49 999 và 40 500 nhỏ hơn 50 000; 50 000 bằng mốc, không nhỏ hơn.",
            ),
            ordering(
                "Sắp xếp các số theo thứ tự tăng dần.",
                ["21 030", "20 999", "21 003", "21 300"],
                [1, 2, 0, 3],
                "20 999 < 21 003 < 21 030 < 21 300.",
            ),
            blank(
                "Số liền sau của 99 999 là bao nhiêu? Viết liền các chữ số.",
                ["100000"],
                "Thêm 1 vào 99 999 được 100 000.",
            ),
            choice(
                "Cách viết nào bằng 608 042?",
                [
                    "600 000 + 8 000 + 40 + 2",
                    "60 000 + 8 000 + 42",
                    "600 000 + 800 + 42",
                    "600 000 + 8 000 + 400 + 2",
                ],
                0,
                "Chữ số 8 ở hàng nghìn, 4 ở hàng chục và 2 ở hàng đơn vị.",
            ),
        ],
    ),
    dict(
        code="operations",
        title="Phép tính và bài toán nhiều bước",
        lessons=[
            lesson(
                "Cộng, trừ, nhân, chia",
                "Khi cộng và trừ, đặt các hàng thẳng cột. Nhân với số có một chữ số từ phải sang trái. Phép chia giúp chia đều hoặc tìm số nhóm. Kiểm tra phép chia bằng phép nhân.",
                "125 × 4 = 500. Kiểm tra 500 : 4 = 125. Với 4 508 + 2 315, cộng theo hàng được 6 823.",
                "Trong biểu thức không có ngoặc, nhân chia trước, cộng trừ sau; các phép cùng mức thực hiện từ trái sang phải.",
            ),
            lesson(
                "Giải toán qua từng bước",
                "Đọc đề, ghi dữ kiện và câu hỏi. Tìm đại lượng trung gian trước khi trả lời. Viết đơn vị sau mỗi kết quả và đối chiếu với tình huống.",
                "Có 6 hộp bút, mỗi hộp 8 chiếc. Cho bạn 15 chiếc: ban đầu 6 × 8 = 48 chiếc; còn lại 48 − 15 = 33 chiếc.",
                "Một bài toán có thể cần nhiều phép tính. Hãy giải thích mỗi phép tính đang tìm điều gì.",
            ),
        ],
        questions=[
            choice(
                "4 508 + 2 315 bằng bao nhiêu?",
                ["6 823", "6 813", "6 723", "7 823"],
                0,
                "Cộng từng hàng: 8 + 5 = 13, nhớ 1; kết quả là 6 823.",
            ),
            blank("Tính 8 000 − 2 475. Viết liền các chữ số.", ["5525"], "8 000 − 2 475 = 5 525."),
            choice(
                "125 × 8 bằng bao nhiêu?", ["900", "1 000", "1 100", "800"], 1, "125 × 8 = 1 000."
            ),
            choice(
                "84 : 7 + 6 bằng bao nhiêu?",
                ["6", "18", "13", "90"],
                1,
                "Thực hiện chia trước: 84 : 7 = 12; 12 + 6 = 18.",
            ),
            multiple(
                "Chọn các phép tính có kết quả bằng 24.",
                ["6 × 4", "96 : 4", "12 + 10", "30 − 6"],
                [0, 1, 3],
                "6 × 4 = 24, 96 : 4 = 24 và 30 − 6 = 24; 12 + 10 = 22.",
            ),
            ordering(
                "Sắp xếp các bước giải: 5 hộp, mỗi hộp 12 viên bi; tặng 18 viên, hỏi còn bao nhiêu?",
                [
                    "Kết luận còn 42 viên bi",
                    "Tính số bi ban đầu: 5 × 12",
                    "Tính số bi còn lại: 60 − 18",
                ],
                [1, 2, 0],
                "Tìm 60 viên ban đầu, trừ 18 viên đã tặng, rồi kết luận còn 42 viên.",
            ),
            blank(
                "Chia đều 156 quyển vở vào 6 thùng. Mỗi thùng có bao nhiêu quyển?",
                ["26"],
                "156 : 6 = 26 quyển vở.",
            ),
            choice(
                "Một xe chở 45 kg gạo mỗi chuyến. Ba chuyến chở được bao nhiêu?",
                ["90 kg", "135 kg", "150 kg", "48 kg"],
                1,
                "45 × 3 = 135 kg.",
            ),
        ],
    ),
    dict(
        code="fractions",
        title="Khám phá phân số",
        lessons=[
            lesson(
                "Tử số và mẫu số",
                "Chia một hình thành các phần bằng nhau. Mẫu số cho biết tổng số phần bằng nhau; tử số cho biết số phần được chọn. Mẫu số phải khác 0.",
                "Một chiếc bánh chia 8 phần bằng nhau, lấy 3 phần: phân số là 3/8. Tử số 3, mẫu số 8.",
                "Phân số mô tả các phần bằng nhau của một đơn vị, không phải các phần có kích thước tùy ý.",
            ),
            lesson(
                "So sánh và cộng phân số cùng mẫu",
                "Hai phân số cùng mẫu: tử số lớn hơn thì phân số lớn hơn. Cộng cùng mẫu bằng cách cộng tử số, giữ mẫu số. Các phân số bằng nhau có thể viết bằng những số khác nhau.",
                "2/7 + 3/7 = 5/7. So sánh 4/9 và 7/9: vì 4 < 7 nên 4/9 < 7/9. Một nửa chiếc bánh có thể viết 1/2 hoặc 2/4.",
                "Không cộng mẫu số khi cộng các phân số cùng mẫu. Đọc kết quả theo số phần được chọn.",
            ),
        ],
        questions=[
            choice(
                "Trong phân số 3/8, mẫu số là số nào?",
                ["3", "8", "11", "5"],
                1,
                "Mẫu số nằm dưới gạch phân số, cho biết 8 phần bằng nhau.",
            ),
            choice(
                "Bánh chia 6 phần bằng nhau, ăn 2 phần. Phân số biểu thị phần đã ăn là gì?",
                ["6/2", "2/6", "4/6", "2/4"],
                1,
                "Lấy 2 phần trong 6 phần nên viết 2/6.",
            ),
            blank(
                "Điền tử số còn thiếu: 2/9 + 4/9 = .../9.",
                ["6"],
                "Cộng tử số: 2 + 4 = 6; mẫu số vẫn là 9.",
            ),
            choice(
                "Phân số nào lớn hơn 3/7?",
                ["2/7", "1/7", "5/7", "3/7"],
                2,
                "Cùng mẫu 7, tử số 5 lớn hơn 3 nên 5/7 > 3/7.",
            ),
            multiple(
                "Chọn các phân số bằng 1/2.",
                ["2/4", "3/6", "1/3", "4/8"],
                [0, 1, 3],
                "2/4, 3/6 và 4/8 đều biểu thị một nửa.",
            ),
            ordering(
                "Sắp xếp các phân số từ bé đến lớn.",
                ["5/8", "1/8", "7/8", "3/8"],
                [1, 3, 0, 2],
                "Cùng mẫu 8, sắp xếp tử số: 1 < 3 < 5 < 7.",
            ),
            blank(
                "Điền tử số: 7/10 − 3/10 = .../10.", ["4"], "Trừ tử số: 7 − 3 = 4, giữ mẫu số 10."
            ),
            choice(
                "Phân số nào bằng 1?",
                ["4/5", "5/4", "6/6", "0/6"],
                2,
                "Tử số và mẫu số bằng nhau, khác 0: 6/6 = 1.",
            ),
        ],
    ),
    dict(
        code="measurement",
        title="Đo lường và hình học",
        lessons=[
            lesson(
                "Đổi đơn vị trong đời sống",
                "1 km = 1 000 m; 1 m = 100 cm; 1 kg = 1 000 g; 1 giờ = 60 phút. Chuyển từ đơn vị lớn sang đơn vị nhỏ bằng phép nhân với hệ số tương ứng.",
                "2 kg 300 g = 2 000 g + 300 g = 2 300 g. Một buổi học từ 8 giờ đến 9 giờ 30 phút kéo dài 90 phút.",
                "Luôn viết đơn vị. Khi cộng trừ số đo, hãy đổi về cùng đơn vị trước.",
            ),
            lesson(
                "Chu vi, diện tích và các đường thẳng",
                "Chu vi là độ dài đường bao quanh hình. Diện tích đo phần mặt phẳng bên trong. Hình chữ nhật có chu vi (dài + rộng) × 2 và diện tích dài × rộng. Hai đường vuông góc tạo góc vuông; hai đường song song trong mặt phẳng không gặp nhau.",
                "Hình chữ nhật dài 8 cm, rộng 3 cm: chu vi (8 + 3) × 2 = 22 cm; diện tích 8 × 3 = 24 cm².",
                "Chu vi dùng cm, m; diện tích dùng cm², m². Phân biệt hai đại lượng trước khi chọn công thức.",
            ),
        ],
        questions=[
            blank(
                "3 kg bằng bao nhiêu gam? Chỉ viết số.",
                ["3000"],
                "1 kg = 1 000 g nên 3 kg = 3 000 g.",
            ),
            choice(
                "2 giờ 15 phút bằng bao nhiêu phút?",
                ["120", "125", "135", "215"],
                2,
                "2 × 60 + 15 = 135 phút.",
            ),
            choice(
                "Hình chữ nhật dài 9 cm, rộng 4 cm có chu vi bao nhiêu?",
                ["13 cm", "26 cm", "36 cm", "18 cm"],
                1,
                "Chu vi = (9 + 4) × 2 = 26 cm.",
            ),
            choice(
                "Hình vuông cạnh 5 cm có diện tích bao nhiêu?",
                ["10 cm²", "20 cm²", "25 cm²", "5 cm²"],
                2,
                "Diện tích = 5 × 5 = 25 cm².",
            ),
            multiple(
                "Chọn các cách đổi đơn vị đúng.",
                ["1 km = 1 000 m", "1 m = 10 cm", "1 giờ = 60 phút", "1 kg = 100 g"],
                [0, 2],
                "1 km = 1 000 m và 1 giờ = 60 phút; 1 m = 100 cm, 1 kg = 1 000 g.",
            ),
            ordering(
                "Sắp xếp các độ dài từ ngắn đến dài.",
                ["2 m", "50 cm", "150 cm", "3 m"],
                [1, 2, 0, 3],
                "Đổi sang cm: 50 < 150 < 200 < 300.",
            ),
            blank(
                "Hình chữ nhật dài 7 m, rộng 3 m có diện tích bao nhiêu m²?",
                ["21"],
                "7 × 3 = 21 m².",
            ),
            choice(
                "Hai đường thẳng tạo thành góc vuông được gọi là gì?",
                ["Song song", "Vuông góc", "Trùng nhau", "Đường cong"],
                1,
                "Hai đường vuông góc cắt nhau tạo góc vuông.",
            ),
        ],
    ),
]


PASSAGE = "Sáng chủ nhật, Mai cùng ông trồng một cây bưởi ở góc vườn. Ông đào hố, Mai nhẹ nhàng đặt cây xuống rồi vun đất. Sau khi tưới nước, Mai buộc một chiếc nơ xanh lên cọc cạnh cây. Em mong mùa sau cả nhà sẽ được thưởng thức những quả bưởi ngọt."


VIETNAMESE = [
    dict(
        code="reading",
        title="Đọc hiểu và tìm thông tin",
        lessons=[
            lesson(
                "Đọc để tìm chi tiết",
                "Đọc toàn đoạn để biết sự việc chính. Đọc lại câu có thông tin về ai, ở đâu, khi nào và làm gì. Khi trả lời, dựa vào chi tiết trong đoạn, không tự thêm điều chưa được nói đến.",
                PASSAGE,
                "Muốn trả lời chính xác, hãy tìm câu văn làm căn cứ. Đoạn văn này do VietTree tự sáng tác.",
            ),
            lesson(
                "Hiểu ý chính và trình tự",
                "Ý chính là điều cả đoạn muốn nói. Trình tự cho biết sự việc nào xảy ra trước, sau. Có thể dựa vào từ chỉ thời gian và hành động.",
                "Trong đoạn về Mai: ông đào hố → Mai đặt cây, vun đất → tưới nước → buộc nơ. Ý chính là Mai cùng ông trồng và chăm sóc cây bưởi.",
                "Phân biệt chi tiết nhỏ với ý chính. Một dự đoán phải hợp lý nhưng không được coi là dữ kiện đã nêu.",
            ),
        ],
        questions=[
            choice(
                PASSAGE + "\nMai trồng cây cùng ai?",
                ["Mẹ", "Ông", "Bạn", "Cô giáo"],
                1,
                "Câu đầu cho biết Mai cùng ông trồng cây.",
            ),
            choice(
                PASSAGE + "\nHai ông cháu trồng cây gì?",
                ["Cây bưởi", "Cây cam", "Cây xoài", "Cây đào"],
                0,
                "Đoạn văn nói rõ đó là một cây bưởi.",
            ),
            blank(
                PASSAGE + "\nChiếc nơ có màu gì? Điền một từ.",
                ["xanh"],
                "Mai buộc một chiếc nơ xanh lên cọc cạnh cây.",
            ),
            choice(
                PASSAGE + "\nSự việc diễn ra khi nào?",
                ["Tối thứ sáu", "Sáng chủ nhật", "Trưa thứ hai", "Chiều thứ bảy"],
                1,
                "Từ ngữ mở đầu là 'Sáng chủ nhật'.",
            ),
            multiple(
                PASSAGE + "\nChọn các việc Mai đã làm theo đoạn văn.",
                ["Đặt cây xuống hố", "Vun đất", "Hái quả bưởi", "Buộc nơ lên cọc"],
                [0, 1, 3],
                "Mai đặt cây, vun đất, buộc nơ. Em mới mong được ăn quả vào mùa sau.",
            ),
            ordering(
                "Sắp xếp sự việc theo đoạn văn về Mai.",
                ["Mai buộc nơ", "Ông đào hố", "Mai đặt cây và vun đất", "Tưới nước"],
                [1, 2, 3, 0],
                "Đào hố trước, đặt cây và vun đất, tưới nước rồi buộc nơ.",
            ),
            blank(
                PASSAGE + "\nMai mong cả nhà được thưởng thức những quả bưởi có vị gì?",
                ["ngọt"],
                "Câu cuối nhắc đến những quả bưởi ngọt.",
            ),
            choice(
                PASSAGE + "\nÝ chính của đoạn văn là gì?",
                ["Mai đi mua nơ", "Mai cùng ông trồng cây bưởi", "Mai hái bưởi bán", "Ông xây nhà"],
                1,
                "Toàn đoạn kể hoạt động trồng cây và mong đợi của Mai.",
            ),
        ],
    ),
    dict(
        code="wordtypes",
        title="Danh từ, động từ, tính từ",
        lessons=[
            lesson(
                "Nhận biết danh từ và động từ",
                "Danh từ gọi tên người, vật, hiện tượng hoặc khái niệm. Động từ chỉ hoạt động, trạng thái. Xét nghĩa của từ trong câu để nhận biết.",
                "Trong câu 'Bạn Lan đọc sách', 'Lan', 'sách' là danh từ; 'đọc' là động từ chỉ hoạt động.",
                "Có thể hỏi 'ai/cái gì?' để tìm danh từ; 'làm gì?' để tìm động từ trong ví dụ đơn giản.",
            ),
            lesson(
                "Tính từ làm câu văn rõ hơn",
                "Tính từ chỉ đặc điểm, tính chất như xanh, cao, chăm chỉ. Khi miêu tả, chọn tính từ phù hợp để người đọc hình dung rõ.",
                "Trong câu 'Bông hoa đỏ nở trong vườn', 'đỏ' chỉ màu sắc của hoa. 'Nở' chỉ hoạt động nên là động từ.",
                "Nhận biết từ loại theo nghĩa trong câu. Không chỉ dựa vào vị trí đứng của từ.",
            ),
        ],
        questions=[
            choice(
                "Từ nào là danh từ chỉ đồ vật?",
                ["Chạy", "Đẹp", "Bàn", "Nhanh"],
                2,
                "'Bàn' gọi tên một đồ vật.",
            ),
            choice(
                "Trong câu 'Nam đọc sách', từ nào là động từ?",
                ["Nam", "Đọc", "Sách", "Cả câu"],
                1,
                "'Đọc' chỉ hoạt động của Nam.",
            ),
            blank(
                "Điền tính từ chỉ màu sắc trong câu: 'Lá cây xanh đung đưa trong gió'.",
                ["xanh"],
                "'Xanh' chỉ màu sắc của lá.",
            ),
            choice(
                "Từ 'chăm chỉ' trong 'Hoa rất chăm chỉ' thuộc từ loại nào?",
                ["Danh từ", "Động từ", "Tính từ", "Dấu câu"],
                2,
                "'Chăm chỉ' chỉ đặc điểm của Hoa.",
            ),
            multiple(
                "Chọn các động từ chỉ hoạt động.",
                ["Nhảy", "Bút", "Viết", "Đỏ"],
                [0, 2],
                "'Nhảy' và 'viết' chỉ hoạt động; 'bút' là danh từ, 'đỏ' là tính từ.",
            ),
            ordering(
                "Sắp xếp thành câu phù hợp: Hoa đọc một quyển sách.",
                ["một quyển sách.", "đọc", "Hoa"],
                [2, 1, 0],
                "Chủ thể Hoa đứng trước hoạt động đọc, rồi đến đối tượng một quyển sách.",
            ),
            blank(
                "Tìm danh từ chỉ con vật trong câu 'Chú mèo đang ngủ'. Viết một từ.",
                ["mèo"],
                "'Mèo' là danh từ gọi tên con vật.",
            ),
            choice(
                "Câu nào dùng tính từ để miêu tả bầu trời?",
                ["Em đọc sách.", "Bầu trời trong xanh.", "Bố tưới cây.", "Mẹ nấu cơm."],
                1,
                "'Trong xanh' miêu tả đặc điểm của bầu trời.",
            ),
        ],
    ),
    dict(
        code="sentences",
        title="Câu và dấu câu",
        lessons=[
            lesson(
                "Câu kể, câu hỏi và lời đề nghị",
                "Câu kể dùng để kể hoặc giới thiệu; thường kết thúc bằng dấu chấm. Câu hỏi để hỏi điều chưa biết, kết thúc bằng dấu hỏi. Lời đề nghị nên lịch sự, rõ ràng.",
                "Câu kể: 'Em học lớp bốn.' Câu hỏi: 'Bạn học lớp mấy?' Đề nghị: 'Bạn giúp mình nhặt bút nhé.'",
                "Đọc cả câu để hiểu mục đích nói, rồi chọn dấu câu phù hợp.",
            ),
            lesson(
                "Dùng dấu câu khi viết",
                "Dấu phẩy ngăn cách các thành phần trong chuỗi liệt kê. Dấu hai chấm có thể báo hiệu lời nói trực tiếp. Đầu câu viết hoa; cuối câu cần dấu phù hợp.",
                "Em mang bút, thước và vở. Mẹ nói: 'Con hãy tưới cây nhé.' Dấu phẩy làm danh sách dễ đọc; dấu hai chấm giới thiệu lời mẹ.",
                "Sau khi viết, đọc lại để kiểm tra chữ đầu câu và dấu kết thúc.",
            ),
        ],
        questions=[
            choice(
                "Dấu nào phù hợp cuối câu 'Bạn tên là gì...' ?",
                ["Dấu chấm", "Dấu hỏi", "Dấu phẩy", "Dấu hai chấm"],
                1,
                "Đây là câu hỏi nên kết thúc bằng dấu hỏi.",
            ),
            choice(
                "Câu nào là câu kể?",
                ["Bạn ở đâu?", "Em thích đọc sách.", "Ai đến vậy?", "Mấy giờ rồi?"],
                1,
                "'Em thích đọc sách.' kể một sở thích.",
            ),
            blank(
                "Điền tên dấu câu dùng cuối câu hỏi (không cần từ 'dấu').",
                ["hỏi", "chấm hỏi"],
                "Câu hỏi kết thúc bằng dấu hỏi, còn gọi là dấu chấm hỏi.",
            ),
            choice(
                "Cách viết nào đúng?",
                ["em đi học.", "Em đi học.", "Em đi học,", "em đi học?"],
                1,
                "Đầu câu viết hoa, câu kể kết thúc bằng dấu chấm.",
            ),
            multiple(
                "Chọn các câu hỏi.",
                ["Bạn có khỏe không?", "Em đến trường.", "Ai đang gõ cửa?", "Trời hôm nay đẹp."],
                [0, 2],
                "Hai câu có mục đích hỏi là 'Bạn có khỏe không?' và 'Ai đang gõ cửa?'.",
            ),
            ordering(
                "Sắp xếp thành câu kể hoàn chỉnh.",
                ["mỗi sáng.", "tưới cây", "Lan"],
                [2, 1, 0],
                "Lan tưới cây mỗi sáng.",
            ),
            blank(
                "Điền dấu còn thiếu: 'Em mang bút... thước và vở.' Chỉ viết ký hiệu dấu câu.",
                [","],
                "Dấu phẩy tách các đồ vật trong phép liệt kê.",
            ),
            choice(
                "Lời nhờ nào lịch sự, rõ ràng?",
                ["Đưa bút!", "Bạn cho mình mượn bút một lát nhé.", "Bút đâu?", "Lấy ngay!"],
                1,
                "Câu nhờ có từ 'bạn', 'mình' và 'nhé', nêu rõ điều cần giúp.",
            ),
        ],
    ),
    dict(
        code="vocabulary",
        title="Từ ngữ và luyện viết câu",
        lessons=[
            lesson(
                "Chọn từ phù hợp với ngữ cảnh",
                "Nghĩa của từ cần phù hợp với sự vật và tình huống. Từ đồng nghĩa có nghĩa gần nhau; từ trái nghĩa có nghĩa đối lập. Không phải lúc nào cũng thay thế từ đồng nghĩa được.",
                "'Vui vẻ' gần nghĩa với 'phấn khởi' trong nhiều tình huống. 'Cao' trái nghĩa với 'thấp'. Ta nói 'dòng suối trong veo', không nói 'dòng suối chăm chỉ'.",
                "Đọc câu sau khi điền từ để kiểm tra ý nghĩa.",
            ),
            lesson(
                "Viết câu và đoạn ngắn",
                "Một đoạn ngắn có thể có câu giới thiệu, câu nêu chi tiết và câu kết. Khi kể việc chăm cây, hãy nêu việc em làm và cảm nghĩ. Viết câu rõ ý, dùng dấu câu phù hợp.",
                "Em có một chậu hoa nhỏ. Mỗi sáng, em tưới nước vừa đủ và nhặt lá khô. Em rất vui khi thấy hoa nở. Hãy tự viết ba câu về một việc tốt của em vào vở.",
                "Bài viết sáng tạo cần người đọc nhận xét. VietTree chỉ tự chấm các câu khách quan; không tự phán đúng/sai đoạn văn của em.",
            ),
        ],
        questions=[
            choice(
                "Từ nào gần nghĩa với 'vui vẻ'?",
                ["Buồn bã", "Phấn khởi", "Mệt mỏi", "Lo lắng"],
                1,
                "'Phấn khởi' diễn tả tâm trạng vui và hào hứng.",
            ),
            choice(
                "Từ nào trái nghĩa với 'cao'?",
                ["Lớn", "Rộng", "Thấp", "Dài"],
                2,
                "'Cao' và 'thấp' biểu thị hai đặc điểm đối lập.",
            ),
            blank(
                "Điền từ trái nghĩa với 'nóng' khi nói về nhiệt độ.",
                ["lạnh"],
                "'Nóng' và 'lạnh' trái nghĩa về nhiệt độ.",
            ),
            choice(
                "Chọn từ phù hợp: 'Dòng suối ... chảy qua khe đá'.",
                ["Trong veo", "Chăm chỉ", "Dũng cảm", "Lễ phép"],
                0,
                "'Trong veo' miêu tả nước suối trong, nhìn rõ.",
            ),
            multiple(
                "Chọn các từ thể hiện phẩm chất tốt của con người.",
                ["Trung thực", "Nhân hậu", "Ích kỷ", "Chăm chỉ"],
                [0, 1, 3],
                "Trung thực, nhân hậu, chăm chỉ là những phẩm chất tốt.",
            ),
            ordering(
                "Sắp xếp ba câu thành đoạn có trình tự hợp lý.",
                [
                    "Em rất vui khi hoa nở.",
                    "Em có một chậu hoa nhỏ.",
                    "Mỗi sáng, em tưới nước cho hoa.",
                ],
                [1, 2, 0],
                "Giới thiệu chậu hoa → kể việc chăm sóc → nêu cảm xúc.",
            ),
            blank(
                "Điền từ còn thiếu: 'Uống nước nhớ ...'.",
                ["nguồn"],
                "'Uống nước nhớ nguồn' nhắc ta biết ơn người đã giúp mình.",
            ),
            choice(
                "Câu nào nêu cảm xúc?",
                [
                    "Chậu hoa ở ban công.",
                    "Em tưới cây mỗi sáng.",
                    "Em rất vui khi cây lớn lên.",
                    "Cây có năm chiếc lá.",
                ],
                2,
                "'Rất vui' diễn tả cảm xúc của người viết.",
            ),
        ],
    ),
]


ENGLISH = [
    dict(
        code="family",
        title="Hello! Gia đình và bạn bè",
        lessons=[
            lesson(
                "Chào hỏi và giới thiệu",
                "Hello/Hi nghĩa là xin chào. 'My name is ...' dùng để giới thiệu tên. Hỏi tên bằng 'What is your name?' và hỏi sức khỏe bằng 'How are you?'.",
                "Hello! My name is Mai. — Xin chào! Mình tên là Mai. How are you? — Bạn có khỏe không? I'm fine, thank you. — Mình khỏe, cảm ơn bạn.",
                "Dùng 'I am' hoặc dạng rút gọn 'I'm' khi nói về bản thân. Viết hoa I.",
            ),
            lesson(
                "Nói về gia đình",
                "Mother là mẹ, father là bố, sister là chị/em gái, brother là anh/em trai. 'This is my ...' dùng để giới thiệu người trong gia đình.",
                "This is my mother. — Đây là mẹ của mình. I have one brother. — Mình có một anh/em trai.",
                "'My' nghĩa là của tôi. Dùng từ chỉ thành viên gia đình đúng với người em giới thiệu.",
            ),
        ],
        questions=[
            choice(
                "Chọn lời chào bằng tiếng Anh.",
                ["Hello", "Table", "Blue", "Seven"],
                0,
                "Hello nghĩa là xin chào.",
            ),
            choice("'Mother' nghĩa là gì?", ["Bố", "Mẹ", "Anh trai", "Bạn"], 1, "Mother là mẹ."),
            blank("Điền: My name ... Nam.", ["is"], "My name is Nam. — Tên mình là Nam."),
            choice(
                "Câu nào dùng để hỏi tên?",
                [
                    "How old are you?",
                    "What is your name?",
                    "What color is it?",
                    "Where is my book?",
                ],
                1,
                "What is your name? nghĩa là Bạn tên là gì?",
            ),
            multiple(
                "Chọn những từ chỉ thành viên gia đình.",
                ["Father", "Sister", "Pencil", "Brother"],
                [0, 1, 3],
                "Father, sister, brother là người trong gia đình; pencil là bút chì.",
            ),
            ordering(
                "Sắp xếp thành câu 'Đây là bố của tôi'.",
                ["my father.", "is", "This"],
                [2, 1, 0],
                "This is my father.",
            ),
            blank(
                "Điền từ còn thiếu: I'm fine, ... you.",
                ["thank"],
                "I'm fine, thank you. — Mình khỏe, cảm ơn bạn.",
            ),
            choice(
                "'Friend' nghĩa là gì?", ["Bạn", "Cửa", "Đồng hồ", "Mẹ"], 0, "Friend là người bạn."
            ),
        ],
    ),
    dict(
        code="school",
        title="My school! Trường học",
        lessons=[
            lesson(
                "Đồ vật trong lớp",
                "Book: sách; pen: bút mực; pencil: bút chì; ruler: thước; desk: bàn học. Hỏi vật bằng 'What is this?' và trả lời 'It is a ...'.",
                "What is this? It is a ruler. — Đây là gì? Đây là một cái thước. This is my book. — Đây là sách của mình.",
                "Dùng 'a' trước danh từ số ít bắt đầu bằng âm phụ âm trong các ví dụ này: a book, a pen.",
            ),
            lesson(
                "Môn học em yêu thích",
                "Maths: Toán; English: Tiếng Anh; Art: Mỹ thuật; Music: Âm nhạc. 'I like ...' để nói thích môn gì. 'My favourite subject is ...' để nói môn yêu thích.",
                "I like English. — Mình thích Tiếng Anh. My favourite subject is Art. — Môn yêu thích của mình là Mỹ thuật.",
                "Đọc câu theo từng cụm và tự thay tên môn để giới thiệu sở thích. Không cần tệp âm thanh để học bài này.",
            ),
        ],
        questions=[
            choice(
                "'Pencil' là đồ vật nào?",
                ["Bút chì", "Thước", "Sách", "Cặp"],
                0,
                "Pencil nghĩa là bút chì.",
            ),
            choice(
                "Môn 'Music' là môn gì?",
                ["Toán", "Âm nhạc", "Tiếng Anh", "Mỹ thuật"],
                1,
                "Music nghĩa là Âm nhạc.",
            ),
            blank("Điền: This ... my book.", ["is"], "This is my book. — Đây là sách của mình."),
            choice(
                "Chọn câu đúng.",
                ["I like English.", "I likes English.", "I liking English.", "I English like."],
                0,
                "Với I, dùng like: I like English.",
            ),
            multiple(
                "Chọn những đồ vật thường dùng để viết hoặc kẻ.",
                ["Pen", "Pencil", "Ruler", "Window"],
                [0, 1, 2],
                "Pen và pencil để viết; ruler để kẻ; window là cửa sổ.",
            ),
            ordering(
                "Sắp xếp thành câu hỏi 'Đây là gì?'.",
                ["this?", "What", "is"],
                [1, 2, 0],
                "What is this?",
            ),
            blank("Viết từ tiếng Anh nghĩa là 'sách' (số ít).", ["book"], "Book nghĩa là sách."),
            choice(
                "'My favourite subject is Art.' nói về điều gì?",
                ["Môn học yêu thích", "Giờ ngủ", "Thời tiết", "Tuổi"],
                0,
                "Favourite subject nghĩa là môn học yêu thích.",
            ),
        ],
    ),
    dict(
        code="routines",
        title="My day! Thói quen và thời gian",
        lessons=[
            lesson(
                "Nói về một ngày của em",
                "Get up: thức dậy; have breakfast: ăn sáng; go to school: đi học; go to bed: đi ngủ. Dùng 'I ...' để kể thói quen và 'at' trước giờ.",
                "I get up at six. — Mình thức dậy lúc sáu giờ. I go to school at seven. — Mình đi học lúc bảy giờ.",
                "Dùng động từ nguyên mẫu với I: I get up, I go to school.",
            ),
            lesson(
                "Các ngày trong tuần và giờ",
                "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday là thứ hai đến chủ nhật. 'What time is it?' hỏi giờ; 'It is seven o'clock.' nghĩa là bảy giờ đúng.",
                "On Monday, I have English. — Vào thứ hai, mình học Tiếng Anh. It is eight o'clock. — Bây giờ là tám giờ đúng.",
                "Viết hoa tên ngày. Dùng on với ngày trong tuần và at với giờ.",
            ),
        ],
        questions=[
            choice(
                "Ngày nào đứng ngay sau Monday?",
                ["Sunday", "Tuesday", "Friday", "Saturday"],
                1,
                "Sau thứ hai (Monday) là thứ ba (Tuesday).",
            ),
            choice(
                "'I get up at six.' nghĩa là gì?",
                [
                    "Mình ngủ lúc sáu giờ",
                    "Mình thức dậy lúc sáu giờ",
                    "Mình ăn trưa lúc sáu giờ",
                    "Mình có sáu quyển sách",
                ],
                1,
                "Get up là thức dậy; at six là lúc sáu giờ.",
            ),
            blank(
                "Điền giới từ: I go to school ... seven o'clock.",
                ["at"],
                "Dùng at trước giờ cụ thể.",
            ),
            choice(
                "Câu nào dùng để hỏi giờ?",
                ["What time is it?", "What is your name?", "How are you?", "What is this?"],
                0,
                "What time is it? nghĩa là Bây giờ là mấy giờ?",
            ),
            multiple(
                "Chọn hai ngày cuối tuần.",
                ["Monday", "Saturday", "Sunday", "Wednesday"],
                [1, 2],
                "Saturday và Sunday là thứ bảy và chủ nhật.",
            ),
            ordering(
                "Sắp xếp các ngày theo thứ tự từ thứ hai đến thứ tư.",
                ["Wednesday", "Monday", "Tuesday"],
                [1, 2, 0],
                "Monday → Tuesday → Wednesday.",
            ),
            blank("Điền: I ... to bed at nine.", ["go"], "Go to bed nghĩa là đi ngủ."),
            choice(
                "'Have breakfast' nghĩa là gì?",
                ["Ăn sáng", "Ăn tối", "Đi học", "Chơi bóng"],
                0,
                "Have breakfast nghĩa là ăn sáng.",
            ),
        ],
    ),
    dict(
        code="weather",
        title="Weather & hobbies! Thời tiết và sở thích",
        lessons=[
            lesson(
                "Miêu tả thời tiết",
                "Sunny: có nắng; rainy: có mưa; windy: có gió; cloudy: nhiều mây. Hỏi 'What's the weather like?' và trả lời 'It's ...'.",
                "What's the weather like? It's sunny. — Thời tiết thế nào? Trời có nắng. It's rainy today. — Hôm nay trời mưa.",
                "It's là dạng rút gọn của It is. Các từ sunny/rainy/windy/cloudy miêu tả thời tiết.",
            ),
            lesson(
                "Nói về sở thích",
                "Reading: đọc sách; swimming: bơi; drawing: vẽ; playing football: chơi bóng đá. Dùng 'I like ...' với hoạt động để giới thiệu sở thích.",
                "I like drawing. — Mình thích vẽ. I like playing football with my friends. — Mình thích chơi bóng đá với bạn bè.",
                "Sau like trong các ví dụ hoạt động này, dùng dạng -ing. Chọn hoạt động đúng với sở thích của em.",
            ),
        ],
        questions=[
            choice(
                "'Sunny' miêu tả thời tiết nào?",
                ["Có nắng", "Có mưa", "Có tuyết", "Có sương"],
                0,
                "Sunny nghĩa là có nắng.",
            ),
            choice(
                "Hoạt động 'swimming' là gì?", ["Đọc", "Bơi", "Vẽ", "Hát"], 1, "Swimming là bơi."
            ),
            blank("Điền: It ... rainy today.", ["is"], "It is rainy today. — Hôm nay trời mưa."),
            choice(
                "Chọn câu đúng để nói 'Mình thích vẽ'.",
                ["I like drawing.", "I drawing like.", "I likes drawing.", "I draw like."],
                0,
                "I like drawing là cấu trúc đúng để nêu sở thích.",
            ),
            multiple(
                "Chọn các từ miêu tả thời tiết.",
                ["Windy", "Cloudy", "Book", "Rainy"],
                [0, 1, 3],
                "Windy, cloudy và rainy chỉ thời tiết; book là sách.",
            ),
            ordering(
                "Sắp xếp thành câu 'Mình thích đọc sách'.",
                ["books.", "I", "like reading"],
                [1, 2, 0],
                "I like reading books.",
            ),
            blank("Viết từ tiếng Anh chỉ thời tiết 'có gió'.", ["windy"], "Windy nghĩa là có gió."),
            choice(
                "'Playing football' nghĩa là gì?",
                ["Chơi bóng đá", "Chơi cờ", "Bơi", "Vẽ"],
                0,
                "Playing football là chơi bóng đá.",
            ),
        ],
    ),
]


CURRICULUM = {"MATH": MATH, "VIETNAMESE": VIETNAMESE, "ENGLISH": ENGLISH}
