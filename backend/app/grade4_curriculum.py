"""Original supplementary grade-four material, mapped in docs/grade4-curriculum.md.

Twenty lessons and 120 questions. These are supplements, not a complete textbook.
Published older lessons and question versions are never rewritten by this pack.
"""

from app.curriculum import blank, choice, lesson, multiple, ordering

NEW_TOPICS = {
    "MATH": {
        "geometry": "Góc, đường thẳng vuông góc và song song",
        "statistics": "Bảng số liệu, biểu đồ cột và trung bình cộng",
        "chance": "Thực nghiệm và khả năng xảy ra",
        "wordproblems": "Giải toán có lời văn và lập luận",
    },
    "VIETNAMESE": {"writing": "Viết và chỉnh sửa bài văn", "speaking": "Nói, nghe và thảo luận"},
    "ENGLISH": {
        "abilities": "Những việc em có thể làm",
        "places": "Chỉ đường và biển chỉ dẫn",
        "food": "Sở thích và giao tiếp trong bữa ăn",
    },
}


def unit(
    topic,
    code,
    title,
    teaching,
    example,
    remember,
    goals,
    hints,
    questions,
    *,
    plan="free",
    thinking=False,
    reflection=None,
):
    value = lesson(title, teaching, example, remember)
    value["content"].update(
        category="thinking" if thinking else "core",
        goals=goals,
        hints=hints,
        reflection=reflection or ["Em hãy giải thích một ví dụ bằng lời của mình."],
        illustration=None,
    )
    return dict(
        topic=topic,
        code="g4-" + code,
        title=title,
        lesson=value,
        questions=questions,
        minimum_plan_code=plan,
        learning_level="advanced" if plan == "vip" else "basic",
        sort_order=50,
    )


INFORMATION = (
    "GÓC ĐỔI SÁCH CỦA LỚP 4\n"
    "Chiều thứ sáu, lớp 4 tổ chức góc đổi sách tại thư viện từ 14 giờ đến 15 giờ. "
    "Mỗi bạn được mang tối đa hai cuốn sách còn đủ trang, sạch và phù hợp với học sinh tiểu học. "
    "Sách giáo khoa đang dùng không được đưa vào góc đổi sách.\n"
    "Trước tiên, các bạn ghi tên mình và tên sách vào phiếu. Tiếp theo, nhóm trực thư viện kiểm tra "
    "sách rồi xếp sách lên bàn theo hai nhóm: truyện và sách tìm hiểu. Cuối cùng, mỗi bạn chọn "
    "một cuốn muốn đọc và ghi lại tên sách đã nhận. Nếu chưa tìm được sách phù hợp, bạn có thể "
    "nhờ cô thủ thư gợi ý; không cần chọn vội.\n"
    "Các bạn giữ trật tự, không viết hay vẽ lên sách. Sau một tuần, người đọc trả sách về góc đổi "
    "sách để bạn khác tiếp tục đọc. Lớp mong rằng mỗi cuốn sách sẽ đến với nhiều người bạn mới."
)

LOGIC_STORY = (
    "Sáng thứ hai, Mai, Nam và Hoa cùng chuẩn bị góc đọc sách. Trên bàn có một tập thơ, một "
    "truyện về khu vườn và một cuốn tìm hiểu chim. Mỗi bạn chọn đúng một cuốn, không ai chọn "
    "trùng sách. Mai nói: 'Hôm nay mình muốn đọc thơ.' Nam đã đọc truyện khu vườn hôm qua "
    "nên chọn một cuốn khác. Hoa chờ hai bạn chọn xong rồi nhận cuốn còn lại.\n"
    "Ba bạn ngồi đọc yên lặng. Mai chép một câu thơ mình thích vào sổ, còn Nam vẽ lại chiếc "
    "mỏ chim theo hình trong sách. Hoa đặt một chiếc lá làm dấu trang, rồi đổi sang thẻ giấy "
    "khi cô nhắc lá tươi có thể làm ẩm sách. Cuối giờ, cả nhóm đặt sách lại lên kệ. "
    "Các bạn hẹn nhau tuần sau sẽ kể điều thú vị đã đọc."
)

SCHEDULE = (
    "Our club meets on Saturday. Art starts at nine and ends at ten. Reading starts at ten "
    "and ends at eleven. Football starts at eleven. Ben likes art and reading. He cannot "
    "come before ten. He wants to join one activity from the start."
)

GRADE4 = {
    "MATH": [
        unit(
            "numbers",
            "millions",
            "Đọc số đến lớp triệu; số chẵn và số lẻ",
            "Tách số từ phải sang trái thành các lớp đơn vị, nghìn, triệu, mỗi lớp ba chữ số. "
            "Chữ số có giá trị theo hàng. Số chẵn có chữ số tận cùng 0, 2, 4, 6 hoặc 8; các số còn lại là số lẻ. "
            "Số 0 là số chẵn. Muốn so sánh hai số cùng độ dài, xét chữ số từ trái sang phải.",
            "Số 12 305 418 gồm 12 triệu, 305 nghìn và 418. Chữ số 3 có giá trị 300 000. "
            "Số này chẵn vì tận cùng là 8. Số liền sau là 12 305 419, lớn hơn đúng 1.",
            "Tên lớp khác tên hàng. Khi viết số, giữ các chữ số 0 để đúng vị trí.",
            ["Đọc và phân tích số đến lớp triệu.", "Nhận biết số chẵn, số lẻ và số liền sau."],
            [
                "Tách thành các nhóm ba chữ số.",
                "Xác định hàng của chữ số được hỏi.",
                "Xét chữ số tận cùng khi tìm số chẵn.",
            ],
            [
                blank(
                    "Chữ số 3 trong 12 305 418 có giá trị bao nhiêu? Viết số không có dấu cách.",
                    ["300000", "300 000"],
                    "Chữ số 3 ở hàng trăm nghìn: 300 000.",
                ),
                choice(
                    "Số nào đọc là hai triệu không trăm linh năm nghìn không trăm linh sáu?",
                    ["2 005 006", "2 050 060", "2 500 006", "2 005 060"],
                    0,
                    "Hai triệu, năm nghìn, sáu đơn vị tạo số 2 005 006.",
                ),
                multiple(
                    "Chọn tất cả các số chẵn.",
                    ["0", "12 305 418", "7 000 003", "9 999 999"],
                    [0, 1],
                    "0 và số tận cùng 8 là số chẵn.",
                ),
                choice(
                    "Số lớn nhất là?",
                    ["9 999 999", "10 000 001", "10 000 010", "1 000 100"],
                    2,
                    "Hai số 10 triệu lớn hơn các số còn lại; 10 000 010 > 10 000 001.",
                ),
                blank(
                    "Số liền sau của 999 999 là? Viết số không có dấu cách.",
                    ["1000000", "1 000 000"],
                    "999 999 + 1 = 1 000 000.",
                ),
                choice(
                    "8 400 000 gồm bao nhiêu triệu và bao nhiêu trăm nghìn?",
                    [
                        "8 triệu và 4 trăm nghìn",
                        "84 triệu",
                        "8 triệu và 4 nghìn",
                        "8 nghìn và 4 trăm",
                    ],
                    0,
                    "8 400 000 = 8 000 000 + 400 000.",
                ),
            ],
        ),
        unit(
            "geometry",
            "angles",
            "Góc nhọn, góc vuông, góc tù và đường thẳng",
            "Độ lớn góc đo bằng độ (°). Góc nhọn lớn hơn 0° và nhỏ hơn 90°; góc vuông bằng 90°; "
            "góc tù lớn hơn 90° và nhỏ hơn 180°; góc bẹt bằng 180°. Hai đường thẳng vuông góc tạo góc vuông. "
            "Hai đường thẳng song song trong cùng mặt phẳng không cắt nhau dù kéo dài. "
            "Khi đo bằng thước đo góc, đặt tâm thước vào đỉnh, vạch 0 trùng một cạnh rồi đọc theo đúng thang.",
            "Góc 45° là góc nhọn, 120° là góc tù. Hai cạnh kề của hình chữ nhật vuông góc, hai cạnh đối song song. "
            "Một góc quay nửa vòng là 180°, tức góc bẹt.",
            "Không đoán góc chỉ theo độ dài hai cạnh. Dùng ê ke kiểm tra vuông góc và thước đo góc đọc số độ.",
            ["Phân loại góc theo số đo.", "Nhận biết vuông góc và song song trong hình chữ nhật."],
            [
                "So sánh số đo với 90° và 180°.",
                "Xét cạnh kề hay cạnh đối.",
                "Đọc thang bắt đầu từ cạnh đặt tại vạch 0.",
            ],
            [
                choice("Góc 60° là góc gì?", ["Nhọn", "Vuông", "Tù", "Bẹt"], 0, "0° < 60° < 90°."),
                choice(
                    "Góc 135° là góc gì?", ["Nhọn", "Vuông", "Tù", "Bẹt"], 2, "90° < 135° < 180°."
                ),
                blank(
                    "Góc vuông có số đo bao nhiêu độ? Chỉ điền số.", ["90"], "Góc vuông bằng 90°."
                ),
                choice(
                    "Hai cạnh đối của hình chữ nhật có quan hệ nào?",
                    ["Song song", "Vuông góc", "Luôn cắt nhau", "Trùng nhau"],
                    0,
                    "Hai cạnh đối song song; hai cạnh kề vuông góc.",
                ),
                multiple(
                    "Chọn tất cả các góc tù.",
                    ["91°", "120°", "90°", "180°"],
                    [0, 1],
                    "Góc tù lớn hơn 90° và nhỏ hơn 180°.",
                ),
                ordering(
                    "Xếp ba bước đo góc.",
                    [
                        "Đọc số trên thang bắt đầu từ vạch 0 đã chọn",
                        "Đặt tâm thước tại đỉnh góc",
                        "Đặt vạch 0 trùng một cạnh",
                    ],
                    [1, 2, 0],
                    "Đặt tâm, đặt vạch 0 rồi đọc đúng thang.",
                ),
            ],
        ),
        unit(
            "statistics",
            "data",
            "Đọc bảng số liệu và tính trung bình cộng",
            "Khi đọc bảng, tìm tên hàng, cột và đơn vị. Với biểu đồ cột, đọc nhãn và thang số trước khi so sánh "
            "độ cao các cột. Mỗi khoảng trên thang có thể biểu thị nhiều đơn vị. Trung bình cộng bằng tổng các "
            "số chia cho số lượng các số; không chia cho số lớn nhất.",
            "Ba tổ trồng được lần lượt 12, 16 và 20 cây. Tổng là 48 cây, trung bình mỗi tổ 48 : 3 = 16 cây. "
            "Tổ thứ ba nhiều hơn tổ thứ nhất 8 cây. Nếu biểu đồ dùng mỗi vạch cho 4 cây thì cột 12 cây cao 3 khoảng.",
            "So sánh các số có cùng đơn vị. Trung bình không có nghĩa mỗi tổ thực tế trồng đúng bằng nhau.",
            ["Đọc và so sánh số liệu.", "Tính trung bình cộng và đọc thang biểu đồ."],
            [
                "Ghi tên và đơn vị của từng số.",
                "Cộng tất cả giá trị, đếm số nhóm.",
                "Lấy tổng chia số nhóm, rồi kiểm tra.",
            ],
            [
                blank(
                    "Ba tổ trồng 12, 16, 20 cây. Tổng bao nhiêu cây? Chỉ điền số.",
                    ["48"],
                    "12 + 16 + 20 = 48.",
                ),
                blank(
                    "Trung bình cộng của 12, 16, 20 là? Chỉ điền số.",
                    ["16"],
                    "(12 + 16 + 20) : 3 = 16.",
                ),
                choice(
                    "Tổ 3 trồng 20 cây, tổ 1 trồng 12 cây. Tổ 3 nhiều hơn bao nhiêu?",
                    ["8 cây", "32 cây", "4 cây", "20 cây"],
                    0,
                    "20 − 12 = 8 cây.",
                ),
                choice(
                    "Mỗi khoảng trên trục biểu đồ ứng với 4 cây. Cột cao 5 khoảng biểu thị?",
                    ["5 cây", "9 cây", "20 cây", "4 cây"],
                    2,
                    "5 × 4 = 20 cây.",
                ),
                multiple(
                    "Chọn nhận xét đúng về bảng: A = 12, B = 16, C = 20 cây.",
                    ["C nhiều nhất", "A ít nhất", "B bằng tổng A và C", "Ba tổ bằng nhau"],
                    [0, 1],
                    "20 lớn nhất, 12 nhỏ nhất; 16 không bằng 12 + 20.",
                ),
                choice(
                    "Hai bạn đọc 10 và 14 trang. Trung bình mỗi bạn đọc?",
                    ["24 trang", "12 trang", "4 trang", "14 trang"],
                    1,
                    "(10 + 14) : 2 = 12 trang.",
                ),
            ],
        ),
        unit(
            "chance",
            "experiment",
            "Thực nghiệm: có thể, không thể và chắc chắn",
            "Khi rút ngẫu nhiên một thẻ từ túi, hãy liệt kê những thẻ có trong túi. Việc không xuất hiện trong "
            "một vài lần thử chưa có nghĩa là không thể xảy ra. Ghi số lần xuất hiện của mỗi kết quả sau từng "
            "lần thử; tổng số lần xuất hiện phải bằng tổng số lần thử. Nếu thử lại độc lập, đặt thẻ trở lại túi và trộn đều.",
            "Túi có 3 thẻ đỏ và 2 thẻ xanh, không có thẻ vàng. Rút một thẻ có thể đỏ hoặc xanh, không thể vàng. "
            "Trong 10 lần rút có hoàn lại, ghi nhận đỏ 6 lần và xanh 4 lần. Lần tiếp theo vẫn có thể xanh; "
            "không thể khẳng định kết quả chắc chắn chỉ từ bảng đã ghi.",
            "Phân biệt kết quả thực nghiệm đã quan sát với dự đoán. Bài này không yêu cầu tính xác suất bằng phân số.",
            ["Nhận biết kết quả có thể xảy ra.", "Đếm và kiểm tra bảng kết quả thực nghiệm."],
            [
                "Liệt kê thẻ thật sự có trong túi.",
                "Cộng số lần của các màu.",
                "Một lần thử mới chưa được quyết định bởi kết quả cũ.",
            ],
            [
                choice(
                    "Túi chỉ có thẻ đỏ và xanh. Rút một thẻ: màu nào không thể xuất hiện?",
                    ["Đỏ", "Xanh", "Vàng", "Đỏ hoặc xanh"],
                    2,
                    "Không có thẻ vàng trong túi.",
                ),
                multiple(
                    "Túi có 3 thẻ đỏ, 2 thẻ xanh. Chọn các kết quả có thể khi rút một thẻ.",
                    ["Đỏ", "Xanh", "Vàng", "Tím"],
                    [0, 1],
                    "Chỉ đỏ và xanh có trong túi.",
                ),
                blank(
                    "Rút 10 lần: đỏ 6 lần. Các lần còn lại đều xanh. Xanh mấy lần?",
                    ["4"],
                    "10 − 6 = 4 lần.",
                ),
                choice(
                    "Túi chỉ có 5 thẻ đỏ. Rút một thẻ sẽ?",
                    ["Chắc chắn đỏ", "Có thể xanh", "Không thể đỏ", "Chắc chắn vàng"],
                    0,
                    "Mọi thẻ đều đỏ.",
                ),
                choice(
                    "Túi có đỏ và xanh. Đã rút đỏ 3 lần, mỗi lần đều trả lại và trộn. Lần sau?",
                    [
                        "Chắc chắn đỏ",
                        "Chắc chắn xanh",
                        "Vẫn có thể đỏ hoặc xanh",
                        "Không thể rút nữa",
                    ],
                    2,
                    "Các thẻ xanh vẫn có trong túi.",
                ),
                ordering(
                    "Xếp cách thực hiện một lần thử có hoàn lại.",
                    [
                        "Trả thẻ vào túi và trộn cho lần sau",
                        "Rút ngẫu nhiên một thẻ",
                        "Ghi màu thẻ vào bảng",
                    ],
                    [1, 2, 0],
                    "Rút, ghi rồi trả lại và trộn.",
                ),
            ],
        ),
        unit(
            "wordproblems",
            "sum-difference",
            "Tìm hai số khi biết tổng và hiệu",
            "Vẽ hai đoạn thẳng để biểu diễn số lớn và số bé. Nếu bớt phần hơn ở số lớn, phần còn lại là "
            "hai số bé bằng nhau. Vì vậy số bé = (tổng − hiệu) : 2; số lớn = số bé + hiệu. "
            "Cũng có thể tìm số lớn = (tổng + hiệu) : 2. Với số lượng nguyên, kết quả phải là số nguyên không âm.",
            "Hai kệ có 48 cuốn sách, kệ trên nhiều hơn kệ dưới 8 cuốn. Kệ dưới có (48 − 8) : 2 = 20 cuốn, "
            "kệ trên có 20 + 8 = 28 cuốn. Kiểm tra: 20 + 28 = 48 và 28 − 20 = 8.",
            "Kiểm tra cả tổng lẫn hiệu. Không lấy tổng trừ hiệu rồi coi đó là một trong hai số.",
            ["Giải bài toán tổng và hiệu.", "Kiểm tra đáp số theo hai điều kiện."],
            [
                "Xác định tổng và số lượng nhiều hơn.",
                "Bớt phần hơn rồi chia đều cho hai.",
                "Cộng lại và trừ lại để kiểm tra.",
            ],
            [
                blank(
                    "Hai kệ có 48 sách, kệ trên hơn kệ dưới 8 sách. Kệ dưới có mấy sách?",
                    ["20"],
                    "(48 − 8) : 2 = 20.",
                ),
                blank(
                    "Hai kệ có 48 sách, kệ trên hơn kệ dưới 8 sách. Kệ trên có mấy sách?",
                    ["28"],
                    "(48 + 8) : 2 = 28.",
                ),
                choice(
                    "Hai số có tổng 70, hiệu 10. Số bé là?",
                    ["60", "40", "30", "35"],
                    2,
                    "(70 − 10) : 2 = 30.",
                ),
                multiple(
                    "Cặp 20 và 28 thỏa mãn những điều kiện nào?",
                    ["Tổng 48", "Hiệu 8", "Tổng 8", "Hiệu 48"],
                    [0, 1],
                    "20 + 28 = 48; 28 − 20 = 8.",
                ),
                ordering(
                    "Xếp bước tìm số bé khi tổng 48, hiệu 8.",
                    ["Chia 40 cho 2 được 20", "Xác định tổng 48 và hiệu 8", "Lấy 48 − 8 = 40"],
                    [1, 2, 0],
                    "Xác định dữ kiện, bớt phần hơn, chia hai.",
                ),
                choice(
                    "Hai nhóm có 36 bạn và bằng nhau. Mỗi nhóm có?",
                    ["36 bạn", "18 bạn", "0 bạn", "72 bạn"],
                    1,
                    "Hiệu bằng 0; (36 − 0) : 2 = 18.",
                ),
            ],
        ),
        unit(
            "measurement",
            "area-mass-time",
            "Đổi đơn vị diện tích, khối lượng và thời gian",
            "1 m² = 100 dm², 1 dm² = 100 cm², 1 cm² = 100 mm². Hai đơn vị diện tích liền nhau trong "
            "dãy này gấp hoặc kém nhau 100 lần. Về khối lượng: 1 tấn = 10 tạ = 1 000 kg; 1 tạ = 100 kg. "
            "Về thời gian: 1 phút = 60 giây, 1 giờ = 60 phút, 1 thế kỉ = 100 năm. Các dãy đơn vị không dùng chung một hệ số.",
            "2 m² 35 dm² = 235 dm². 3 tạ 5 kg = 305 kg. Từ 8 giờ 45 phút đến 9 giờ 10 phút có "
            "15 phút đến 9 giờ và 10 phút nữa, tổng 25 phút.",
            "Ghi đơn vị ở mỗi bước và đổi về cùng đơn vị trước khi cộng. Không đổi diện tích như độ dài.",
            ["Đổi các đơn vị thông dụng của lớp 4.", "Tính khoảng thời gian qua mốc giờ."],
            [
                "Xác định đang đo diện tích, khối lượng hay thời gian.",
                "Viết quan hệ giữa hai đơn vị.",
                "Tách tại mốc giờ nếu cần.",
            ],
            [
                blank(
                    "2 m² 35 dm² bằng bao nhiêu dm²? Chỉ điền số.",
                    ["235"],
                    "2 × 100 + 35 = 235 dm².",
                ),
                blank("3 tạ 5 kg bằng bao nhiêu kg?", ["305"], "3 × 100 + 5 = 305 kg."),
                choice(
                    "1 tấn bằng?",
                    ["100 kg", "1 000 kg", "10 kg", "100 tạ"],
                    1,
                    "1 tấn = 10 tạ = 1 000 kg.",
                ),
                blank("Từ 8:45 đến 9:10 cùng buổi sáng là mấy phút?", ["25"], "15 + 10 = 25 phút."),
                choice(
                    "1 thế kỉ bằng?",
                    ["10 năm", "1 000 năm", "100 năm", "60 năm"],
                    2,
                    "Một thế kỉ gồm 100 năm.",
                ),
                choice(
                    "5 cm² bằng?",
                    ["50 mm²", "500 mm²", "5 mm²", "5 000 mm²"],
                    1,
                    "1 cm² = 100 mm² nên 5 cm² = 500 mm².",
                ),
            ],
        ),
        unit(
            "fractions",
            "fraction-products",
            "Nhân, chia phân số và tìm phân số của một số",
            "Nhân hai phân số: nhân các tử với nhau và các mẫu với nhau. Chia cho một phân số khác 0: "
            "nhân với phân số đảo ngược của số chia. Tìm a/b của một số: lấy số đó nhân a rồi chia b, "
            "hoặc chia b rồi nhân a khi chia hết. Rút gọn kết quả khi có thể.",
            "2/3 × 3/4 = 6/12 = 1/2. 3/5 : 2/5 = 3/5 × 5/2 = 3/2. "
            "Lớp có 24 bạn, 3/8 số bạn tham gia trồng cây: 24 : 8 × 3 = 9 bạn.",
            "Chỉ đảo phân số đứng sau dấu chia. Không đảo cả hai phân số và không chia cho 0.",
            ["Nhân và chia phân số đơn giản.", "Tìm phân số của một số trong tình huống thực tế."],
            [
                "Xác định phép nhân hay phép chia.",
                "Nếu chia, đảo đúng số chia.",
                "Rút gọn rồi kiểm tra đơn vị.",
            ],
            [
                choice(
                    "2/3 × 3/4 bằng?",
                    ["1/2", "5/7", "6/7", "1/3"],
                    0,
                    "Nhân được 6/12, rút gọn thành 1/2.",
                ),
                choice(
                    "3/5 : 2/5 bằng?", ["3/2", "6/25", "1/5", "2/3"], 0, "3/5 × 5/2 = 15/10 = 3/2."
                ),
                blank("3/8 của 24 bạn là mấy bạn?", ["9"], "24 : 8 × 3 = 9 bạn."),
                multiple(
                    "Chọn các phân số bằng 1/2.",
                    ["6/12", "2/4", "3/4", "1/3"],
                    [0, 1],
                    "6/12 và 2/4 đều rút gọn thành 1/2.",
                ),
                ordering(
                    "Xếp bước tính 1/2 : 3/4.",
                    ["Nhân 1/2 × 4/3 được 4/6", "Rút gọn thành 2/3", "Đảo số chia 3/4 thành 4/3"],
                    [2, 0, 1],
                    "Đảo số chia, nhân rồi rút gọn.",
                ),
                choice(
                    "Một rổ có 20 quả, dùng 2/5 số quả. Còn lại?",
                    ["8 quả", "12 quả", "18 quả", "10 quả"],
                    1,
                    "Dùng 20 : 5 × 2 = 8 quả; còn 20 − 8 = 12 quả.",
                ),
            ],
        ),
        unit(
            "wordproblems",
            "interval-riddles",
            "Đố mẹo: đếm khoảng, không chỉ đếm điểm",
            "Một hàng thẳng có n điểm mốc thì có n − 1 khoảng giữa các điểm liên tiếp. Nếu đường kín, "
            "số khoảng bằng số mốc. Đề phải nói rõ đường thẳng hay vòng kín và có mốc ở hai đầu không. "
            "Tiếng chuông cũng tạo các khoảng thời gian giữa hai tiếng liên tiếp; coi mỗi tiếng là một thời điểm.",
            "Trồng 6 cây trên đường thẳng, có cây ở cả hai đầu, hai cây liên tiếp cách 4 m: "
            "có 5 khoảng, đường dài 20 m. Đồng hồ gõ 4 tiếng, hai tiếng liên tiếp cách 2 giây: "
            "từ tiếng đầu đến tiếng cuối là 3 × 2 = 6 giây, không phải 8 giây.",
            "Vẽ dấu chấm và đoạn nối trước khi tính. Đố mẹo có dữ kiện rõ ràng; em không cần đoán ý người ra đề.",
            ["Phân biệt số mốc và số khoảng.", "Giải thích bẫy đếm thừa bằng hình vẽ."],
            [
                "Vẽ ít nhất ba mốc liên tiếp.",
                "Đếm đoạn nối, xác định đường thẳng hay vòng kín.",
                "Nhân số khoảng với khoảng cách.",
            ],
            [
                blank(
                    "6 cây trên đường thẳng, có cây ở cả hai đầu, cách đều 4 m. Đường dài mấy mét?",
                    ["20"],
                    "5 khoảng × 4 m = 20 m.",
                    3,
                ),
                blank(
                    "Chuông gõ 4 tiếng, hai tiếng liên tiếp cách 2 giây. Từ tiếng đầu đến tiếng cuối mấy giây?",
                    ["6"],
                    "Có 3 khoảng, 3 × 2 = 6 giây.",
                    3,
                ),
                choice(
                    "5 cọc chia đều trên một vòng kín. Có mấy khoảng giữa các cọc liên tiếp?",
                    ["4", "5", "6", "10"],
                    1,
                    "Vòng kín có thêm khoảng từ cọc cuối về cọc đầu: 5 khoảng.",
                    3,
                ),
                blank(
                    "Đoạn đường thẳng 24 m, cắm cọc cả hai đầu, hai cọc liên tiếp cách 6 m. Có mấy cọc?",
                    ["5"],
                    "24 : 6 = 4 khoảng; cần 4 + 1 = 5 cọc.",
                    3,
                ),
                choice(
                    "Cắt một thanh thẳng thành 4 đoạn bằng nhau; mỗi lần chỉ cắt một vị trí, không xếp chồng. Cần mấy lần cắt?",
                    ["4", "3", "2", "5"],
                    1,
                    "Ba điểm cắt trong thanh tạo bốn đoạn.",
                    3,
                ),
                multiple(
                    "7 cây trên đường thẳng, cây ở hai đầu, cách đều 3 m. Chọn nhận xét đúng.",
                    ["Có 6 khoảng", "Đường dài 18 m", "Có 7 khoảng", "Đường dài 21 m"],
                    [0, 1],
                    "7 − 1 = 6 khoảng; 6 × 3 = 18 m.",
                    3,
                ),
            ],
            thinking=True,
        ),
        unit(
            "wordproblems",
            "logic-table",
            "Nâng cao: loại trừ và kiểm tra đủ điều kiện",
            "Với bài ghép người và vật, lập một bảng: mỗi hàng là một người, mỗi cột là một vật. "
            "Đánh dấu các cặp không thể, chốt cặp được cho trực tiếp, rồi dùng điều kiện mỗi người chọn một "
            "vật khác nhau. Một kết luận phải thỏa mãn tất cả dữ kiện. Nếu có nhiều cách phù hợp, hãy nói chưa đủ thông tin.",
            "An, Bình, Chi mỗi bạn nhận đúng một bút đỏ, xanh hoặc vàng, không trùng màu. An nhận bút đỏ; "
            "Bình không nhận xanh. An đã lấy đỏ nên Bình chỉ còn vàng; Chi nhận xanh. "
            "Nếu chỉ biết An không nhận đỏ thì chưa thể xác định màu của cả ba bạn.",
            "Không thêm giả thiết ngoài đề. Phân biệt một cách có thể và đáp án duy nhất.",
            ["Giải bài ghép bằng loại trừ.", "Nhận ra trường hợp chưa đủ dữ kiện."],
            [
                "Ghi điều kiện mỗi người một vật, không trùng.",
                "Loại cặp bị cấm và màu đã dùng.",
                "Thử đối chiếu đáp án với từng câu của đề.",
            ],
            [
                choice(
                    "An, Bình, Chi nhận ba bút đỏ, xanh, vàng khác nhau. An đỏ; Bình không xanh. Bình nhận?",
                    ["Đỏ", "Xanh", "Vàng", "Chưa đủ dữ kiện"],
                    2,
                    "Đỏ đã thuộc An, xanh bị loại cho Bình; còn vàng.",
                    4,
                ),
                choice(
                    "Cùng dữ kiện: An đỏ, Bình không xanh, mỗi bạn một màu khác nhau. Chi nhận?",
                    ["Xanh", "Đỏ", "Vàng", "Hai bút"],
                    0,
                    "Bình vàng nên Chi xanh.",
                    4,
                ),
                choice(
                    "Ba bạn nhận ba màu khác nhau; chỉ biết An không đỏ. Có xác định duy nhất màu của cả ba không?",
                    ["Có", "Không", "An chắc chắn vàng", "Bình chắc chắn đỏ"],
                    1,
                    "An có thể xanh hoặc vàng; còn nhiều cách phù hợp.",
                    4,
                ),
                multiple(
                    "An đỏ; Bình không xanh; mỗi bạn một màu khác nhau. Chọn các kết luận chắc chắn.",
                    ["Bình vàng", "Chi xanh", "Bình đỏ", "Chi vàng"],
                    [0, 1],
                    "Loại màu đỏ đã dùng và màu xanh bị cấm cho Bình.",
                    4,
                ),
                ordering(
                    "Xếp cách giải bài An đỏ, Bình không xanh.",
                    [
                        "Gán màu còn lại xanh cho Chi",
                        "Gán đỏ cho An theo đề",
                        "Loại đỏ và xanh cho Bình, chốt vàng",
                    ],
                    [1, 2, 0],
                    "Dùng dữ kiện trực tiếp rồi loại trừ và hoàn tất.",
                    4,
                ),
                choice(
                    "Có hai phương án đều thỏa mọi dữ kiện của một bài ghép. Em nên kết luận?",
                    [
                        "Chọn đại một phương án",
                        "Chưa đủ dữ kiện để có đáp án duy nhất",
                        "Cả hai đều sai",
                        "Đề luôn có một đáp án",
                    ],
                    1,
                    "Hai phương án hợp lệ chứng tỏ dữ kiện chưa xác định duy nhất.",
                    4,
                ),
            ],
            plan="vip",
            thinking=True,
        ),
    ],
    "VIETNAMESE": [
        unit(
            "writing",
            "description",
            "Quan sát và lập dàn ý tả cây cối, con vật",
            "Trước khi viết, chọn một cây hoặc con vật em đã quan sát. Ghi đặc điểm nổi bật và hoạt động, "
            "tránh chỉ dùng từ đẹp, hay. Bài văn có mở bài giới thiệu, thân bài miêu tả theo thứ tự hợp lí "
            "và kết bài chia sẻ tình cảm. Có thể dùng nhân hóa phù hợp nhưng không bỏ các chi tiết quan sát thật.",
            "Tả cây ổi: mở bài giới thiệu cây ở sân; thân bài tả thân nâu, lá có gân rõ, quả xanh, "
            "mùi thơm khi chín; kết bài kể việc em tưới cây. Câu 'Những chiếc lá vẫy tay trong gió' "
            "nhân hóa lá bằng hoạt động của người, làm hình ảnh sinh động.",
            "Chọn chi tiết cụ thể, nối ý và đọc lại. Dàn ý là gợi ý; bài của em có thể khác bài mẫu.",
            ["Lập dàn ý ba phần.", "Chọn chi tiết quan sát và dùng nhân hóa phù hợp."],
            [
                "Quan sát hình dáng, màu sắc và hoạt động.",
                "Xếp chi tiết theo từng phần.",
                "Bỏ chi tiết lặp và kiểm tra dấu câu.",
            ],
            [
                choice(
                    "Chi tiết nào cụ thể khi tả cây ổi?",
                    [
                        "Cây rất đẹp",
                        "Lá có gân rõ, quả xanh tròn",
                        "Cây rất hay",
                        "Em thích mọi thứ",
                    ],
                    1,
                    "Chi tiết lá và quả giúp người đọc hình dung.",
                ),
                choice(
                    "Phần mở bài nên làm gì?",
                    [
                        "Giới thiệu cây hoặc con vật được tả",
                        "Liệt kê đáp án",
                        "Kể việc không liên quan",
                        "Chỉ ghi kết luận",
                    ],
                    0,
                    "Mở bài giới thiệu đối tượng.",
                ),
                multiple(
                    "Chọn các chi tiết có thể quan sát khi tả mèo.",
                    [
                        "Màu lông",
                        "Cách mèo bước đi",
                        "Mèo nghĩ chính xác điều gì",
                        "Mèo biết mọi đáp án",
                    ],
                    [0, 1],
                    "Màu lông và hoạt động quan sát được; suy nghĩ không biết chắc.",
                ),
                ordering(
                    "Xếp ba phần của bài tả cây.",
                    [
                        "Nêu tình cảm và việc chăm cây",
                        "Giới thiệu cây",
                        "Tả thân, lá, hoa hoặc quả",
                    ],
                    [1, 2, 0],
                    "Mở bài, thân bài, kết bài.",
                ),
                choice(
                    "Câu nào dùng nhân hóa?",
                    ["Lá xanh", "Lá vẫy tay chào gió", "Lá dài", "Lá mọc trên cành"],
                    1,
                    "Lá được gán hành động vẫy tay chào của người.",
                ),
                choice(
                    "Sau khi viết nháp, bước phù hợp nhất là?",
                    [
                        "Nộp mà không đọc",
                        "Đọc lại, sửa ý lặp và lỗi câu",
                        "Xóa hết chi tiết",
                        "Chép nguyên bài của bạn",
                    ],
                    1,
                    "Chỉnh sửa giúp ý rõ và câu đúng.",
                ),
            ],
            reflection=["Lập ba ý cho thân bài tả một cây hoặc con vật em biết."],
        ),
        unit(
            "writing",
            "recount",
            "Thuật lại một sự việc và chia sẻ cảm xúc",
            "Chọn sự việc em đã chứng kiến hoặc tham gia. Nêu thời gian, nơi chốn và người tham gia; "
            "kể diễn biến theo trình tự, sau đó nêu kết quả và cảm xúc. Dùng trước tiên, tiếp theo, cuối cùng "
            "để nối các bước. Phân biệt điều em nhìn thấy với điều chỉ nghe người khác kể.",
            "Sáng thứ bảy, em cùng mẹ dọn góc học tập. Trước tiên, em lấy sách ra khỏi kệ. "
            "Tiếp theo, em lau kệ và xếp sách theo môn. Cuối cùng, em đặt một chậu cây nhỏ bên cửa sổ. "
            "Em vui vì góc học tập gọn gàng và tìm sách dễ hơn.",
            "Không chỉ liệt kê hành động; chọn chi tiết và giải thích cảm xúc gắn với sự việc.",
            ["Thuật lại sự việc theo trình tự.", "Nêu cảm xúc có lí do."],
            [
                "Ghi ai, ở đâu và khi nào.",
                "Chọn ba việc theo thứ tự xảy ra.",
                "Nói điều em cảm thấy và vì sao.",
            ],
            [
                choice(
                    "Khi thuật lại một sự việc em tham gia, cần nêu?",
                    [
                        "Chỉ tên bài",
                        "Diễn biến, kết quả và cảm xúc",
                        "Chỉ các từ khó",
                        "Một sự việc không liên quan",
                    ],
                    1,
                    "Bài thuật việc kể diễn biến và chia sẻ cảm xúc.",
                ),
                ordering(
                    "Xếp diễn biến dọn kệ theo ví dụ.",
                    ["Xếp sách vào kệ sạch", "Lấy sách ra", "Lau kệ"],
                    [1, 2, 0],
                    "Lấy sách ra trước khi lau, rồi xếp lại.",
                ),
                choice(
                    "Từ nào phù hợp để bắt đầu bước sau bước đầu?",
                    ["Tiếp theo", "Chưa bao giờ", "Không liên quan", "Bất kể"],
                    0,
                    "Tiếp theo báo trình tự.",
                ),
                multiple(
                    "Chọn câu nêu cảm xúc có lí do.",
                    [
                        "Em vui vì tìm sách dễ hơn",
                        "Em tự hào vì đã giúp mẹ",
                        "Kệ có ba ngăn",
                        "Sách đặt bên trái",
                    ],
                    [0, 1],
                    "Hai câu đầu có cảm xúc và nguyên nhân.",
                ),
                choice(
                    "Em chỉ nghe bạn kể về một buổi tham quan. Cách viết trung thực là?",
                    [
                        "Nói mình trực tiếp đi",
                        "Nêu rõ đây là điều bạn kể",
                        "Thêm mọi chi tiết như đã thấy",
                        "Khẳng định biết tất cả",
                    ],
                    1,
                    "Phân biệt nguồn thông tin với điều trực tiếp chứng kiến.",
                ),
                choice(
                    "Phần kết bài thuật việc có thể viết?",
                    [
                        "Kết quả và suy nghĩ của em",
                        "Chỉ một phép tính",
                        "Thông tin không liên quan",
                        "Lặp nguyên toàn bộ thân bài",
                    ],
                    0,
                    "Kết bài nêu kết quả và cảm xúc.",
                ),
            ],
            reflection=["Thuật lại một việc em đã giúp gia đình, rồi nêu cảm xúc."],
        ),
        unit(
            "speaking",
            "discussion",
            "Thảo luận: lắng nghe, ghi ý và nêu lí lẽ",
            "Khi thảo luận, tập trung vào đề tài, chờ lượt, nghe hết ý và ghi ý chính. Nêu ý kiến kèm lí do "
            "hoặc ví dụ. Khi chưa hiểu, hỏi lại lịch sự. Nhóm thống nhất ý bằng trao đổi, không bằng nói lớn hơn. "
            "Em có thể dùng tranh hoặc dàn ý để trình bày ngắn gọn.",
            "Nhóm chọn hoạt động cuối tuần. Lan đề nghị đổi sách vì mỗi bạn có thể đọc thêm mà không cần "
            "mua sách mới. Minh hỏi: 'Chúng ta ghi tên sách thế nào?' Thư kí ghi hoạt động, lí do và việc "
            "cần chuẩn bị. Cả nhóm chờ từng bạn phát biểu rồi chốt kế hoạch.",
            "Góp ý vào nội dung, tôn trọng người nói. Bài đọc này hướng dẫn thực hành; hãy luyện nói và nghe với người thân.",
            ["Nêu ý kiến có lí do.", "Thực hiện luân phiên lượt lời và ghi ý quan trọng."],
            [
                "Xác định câu hỏi nhóm đang bàn.",
                "Ghi từ khóa thay vì chép mọi câu.",
                "Dùng 'Em đề nghị… vì…' rồi mời bạn khác.",
            ],
            [
                choice(
                    "Bạn đang nói, em muốn góp ý. Em nên?",
                    ["Ngắt lời ngay", "Chờ lượt rồi phát biểu", "Nói to hơn", "Đổi đề tài"],
                    1,
                    "Luân phiên lượt lời giúp nhóm nghe rõ.",
                ),
                choice(
                    "Ý kiến nào có lí do?",
                    [
                        "Đổi sách đi",
                        "Em đề nghị đổi sách vì mỗi bạn được đọc thêm",
                        "Ý em luôn đúng",
                        "Không cần nghe ai",
                    ],
                    1,
                    "Có đề nghị và lí do rõ ràng.",
                ),
                multiple(
                    "Chọn việc giúp nghe hiệu quả.",
                    [
                        "Tập trung vào người nói",
                        "Ghi ý chính",
                        "Trò chuyện riêng",
                        "Đoán ý rồi bỏ nghe",
                    ],
                    [0, 1],
                    "Tập trung và ghi ý chính hỗ trợ hiểu nội dung.",
                ),
                choice(
                    "Chưa hiểu lời bạn, em có thể nói?",
                    [
                        "Bạn sai hết",
                        "Bạn giải thích thêm ý này được không?",
                        "Không cần nói nữa",
                        "Em biết rồi dù chưa nghe",
                    ],
                    1,
                    "Hỏi lại lịch sự để hiểu đúng.",
                ),
                ordering(
                    "Xếp các bước góp ý.",
                    ["Nêu ý kiến kèm lí do", "Nghe bạn nói hết", "Chờ đến lượt"],
                    [1, 2, 0],
                    "Nghe hết, chờ lượt, rồi nêu ý.",
                ),
                choice(
                    "Thư kí nhóm nên ghi gì?",
                    [
                        "Chỉ tên mình",
                        "Ý chính, việc đã thống nhất và phân công",
                        "Mọi tiếng động",
                        "Nhận xét ngoại hình các bạn",
                    ],
                    1,
                    "Ghi nội dung quan trọng của thảo luận.",
                ),
            ],
            reflection=["Mời người thân thảo luận một việc nhỏ. Em ghi lại hai ý đã nghe."],
        ),
        unit(
            "sentences",
            "adverbial-punctuation",
            "Trạng ngữ và dấu câu trong lời kể",
            "Trạng ngữ bổ sung thời gian, nơi chốn, nguyên nhân, mục đích hoặc cách thức cho sự việc trong câu. "
            "Thử hỏi khi nào, ở đâu, vì sao hoặc để làm gì. Dấu ngoặc kép có thể đánh dấu lời nói trực tiếp; "
            "dấu hai chấm có thể báo phần giải thích hoặc lời nói được dẫn. Dùng dấu câu theo ý nghĩa, không đặt tùy tiện.",
            "'Sáng thứ hai, chúng em chăm cây.' Trạng ngữ 'Sáng thứ hai' nêu thời gian. "
            "Câu 'Mai nói: “Mình sẽ tưới cây.”' dùng hai chấm trước lời nói và ngoặc kép quanh lời trực tiếp.",
            "Đọc cả câu để nhận ra phần bổ sung và nòng cốt. Trạng ngữ đầu câu thường được ngăn bằng dấu phẩy.",
            ["Nhận biết trạng ngữ chỉ thời gian, nơi chốn.", "Hiểu dấu câu khi dẫn lời trực tiếp."],
            [
                "Tìm phần trả lời khi nào hoặc ở đâu.",
                "Tách lời người kể và lời nhân vật.",
                "Đọc lại để kiểm tra dấu câu.",
            ],
            [
                choice(
                    "Trong 'Sáng thứ hai, chúng em chăm cây', trạng ngữ là?",
                    ["Sáng thứ hai", "Chúng em", "Chăm cây", "Em"],
                    0,
                    "Sáng thứ hai bổ sung thời gian.",
                ),
                choice(
                    "'Trong thư viện, Lan đọc sách.' Trạng ngữ cho biết?",
                    ["Thời gian", "Nơi chốn", "Số lượng", "Màu sắc"],
                    1,
                    "Trong thư viện trả lời ở đâu.",
                ),
                choice(
                    "Dấu ngoặc kép trong 'Mai nói: “Mình sẽ tưới cây.”' đánh dấu?",
                    ["Lời nói trực tiếp", "Phép nhân", "Một số đo", "Tên môn học"],
                    0,
                    "Phần trong ngoặc kép là lời của Mai.",
                ),
                multiple(
                    "Chọn các cụm có thể làm trạng ngữ chỉ thời gian.",
                    ["Sáng hôm qua", "Vào mùa hè", "Ở sân trường", "Bạn Lan"],
                    [0, 1],
                    "Hai cụm đầu chỉ thời gian; ở sân trường chỉ nơi chốn.",
                ),
                choice(
                    "Dấu hai chấm sau 'Mai nói' trong ví dụ báo hiệu?",
                    [
                        "Phần lời nói sắp được dẫn",
                        "Kết thúc mọi đoạn",
                        "Một câu hỏi",
                        "Không có chức năng",
                    ],
                    0,
                    "Dấu hai chấm giới thiệu lời trực tiếp.",
                ),
                choice(
                    "Thêm 'Để cây xanh tốt,' vào 'em tưới cây mỗi sáng' bổ sung?",
                    ["Mục đích", "Màu áo", "Tên người", "Số cây"],
                    0,
                    "Để cây xanh tốt nêu mục đích tưới cây.",
                ),
            ],
        ),
        unit(
            "reading",
            "information",
            "Đọc văn bản thông tin và hướng dẫn theo bước",
            "Đọc nhan đề để biết mục đích văn bản, sau đó tìm thông tin về thời gian, nơi chốn và quy định. "
            "Với hướng dẫn, xác định từng bước và giữ đúng thứ tự. Không suy ra quy định mà văn bản không nêu.",
            INFORMATION,
            "Khi trả lời, chỉ ra dòng hoặc chi tiết làm bằng chứng. Nêu điểm khác nhau giữa quy định và lời mong muốn.",
            ["Tìm thông tin cụ thể trong văn bản.", "Sắp xếp các bước theo hướng dẫn."],
            [
                "Đọc phần nói về hoạt động được hỏi.",
                "Gạch từ chỉ thời gian, số lượng và thứ tự.",
                "Đối chiếu lựa chọn với nguyên văn ngữ liệu.",
            ],
            [
                choice(
                    INFORMATION + "\nGóc đổi sách mở ở đâu?",
                    ["Thư viện", "Sân bóng", "Nhà ăn", "Phòng y tế"],
                    0,
                    "Đoạn đầu nêu tại thư viện.",
                ),
                choice(
                    INFORMATION + "\nMỗi bạn được mang tối đa mấy cuốn?",
                    ["Một", "Hai", "Ba", "Không giới hạn"],
                    1,
                    "Văn bản nêu tối đa hai cuốn.",
                ),
                ordering(
                    INFORMATION + "\nXếp các bước đổi sách.",
                    [
                        "Chọn sách và ghi tên sách nhận",
                        "Ghi tên mình và tên sách vào phiếu",
                        "Nhóm trực kiểm tra và xếp sách",
                    ],
                    [1, 2, 0],
                    "Trước tiên ghi phiếu, tiếp theo kiểm tra, cuối cùng chọn sách.",
                ),
                multiple(
                    INFORMATION + "\nChọn các quy định có trong văn bản.",
                    [
                        "Sách còn đủ trang và sạch",
                        "Trả sách sau một tuần",
                        "Được vẽ lên sách",
                        "Bắt buộc chọn sách ngay",
                    ],
                    [0, 1],
                    "Văn bản yêu cầu sách sạch đủ trang, trả sau một tuần; không vẽ và không chọn vội.",
                ),
                choice(
                    INFORMATION + "\nVì sao trả sách về góc đổi sách?",
                    [
                        "Để bạn khác tiếp tục đọc",
                        "Để bỏ đi",
                        "Vì mọi sách đều hỏng",
                        "Để không ai đọc nữa",
                    ],
                    0,
                    "Đoạn cuối nêu để bạn khác tiếp tục đọc.",
                ),
                choice(
                    INFORMATION + "\nSách nào không được đưa vào góc đổi sách?",
                    [
                        "Truyện sạch đủ trang",
                        "Sách tìm hiểu phù hợp tuổi",
                        "Sách giáo khoa đang dùng",
                        "Sách có tên người mang",
                    ],
                    2,
                    "Đoạn đầu nêu rõ sách giáo khoa đang dùng không được đưa vào.",
                ),
            ],
        ),
        unit(
            "reading",
            "evidence-riddle",
            "Đố tư duy: ai đọc cuốn nào?",
            "Đọc một câu chuyện có điều kiện ghép, tách điều được nói rõ và điều cần suy ra. "
            "Điều 'mỗi bạn một cuốn, không trùng' rất quan trọng. Dùng bảng loại trừ và kiểm tra bằng hành động "
            "trong đoạn. Không coi vật làm dấu trang là bằng chứng chắc chắn về tên sách.",
            LOGIC_STORY
            + "\nMai đọc thơ. Nam không đọc truyện khu vườn và không thể lấy thơ đã thuộc Mai, "
            "nên Nam đọc sách chim. Hoa đọc truyện khu vườn. Chiếc lá không phải dữ kiện cần để suy ra phép ghép.",
            "Kết luận cần bằng chứng. Có thể có một chi tiết thú vị nhưng không liên quan đến câu hỏi đang giải.",
            ["Suy luận từ nhiều chi tiết trong truyện.", "Phân biệt bằng chứng và suy đoán."],
            [
                "Ghi ba bạn và ba cuốn sách.",
                "Chốt lựa chọn Mai; loại lựa chọn Nam không nhận.",
                "Dùng điều kiện không trùng để tìm cuốn còn lại.",
            ],
            [
                choice(
                    LOGIC_STORY + "\nNam đọc sách nào hôm nay?",
                    ["Tập thơ", "Truyện khu vườn", "Sách tìm hiểu chim", "Cả ba cuốn"],
                    2,
                    "Mai đã lấy thơ, Nam không chọn truyện khu vườn; còn sách chim.",
                    4,
                ),
                choice(
                    LOGIC_STORY + "\nHoa nhận cuốn nào?",
                    ["Truyện khu vườn", "Tập thơ", "Sách chim", "Không cuốn nào"],
                    0,
                    "Mai thơ, Nam sách chim, Hoa nhận cuốn còn lại.",
                    4,
                ),
                multiple(
                    LOGIC_STORY + "\nChọn các bằng chứng để xác định cuốn của Nam.",
                    [
                        "Mai chọn thơ",
                        "Nam chọn khác truyện khu vườn",
                        "Mỗi bạn một cuốn, không trùng",
                        "Hoa có chiếc lá",
                    ],
                    [0, 1, 2],
                    "Ba điều kiện đầu đủ loại trừ; chiếc lá không xác định sách của Nam.",
                    4,
                ),
                choice(
                    LOGIC_STORY + "\nVì sao Hoa đổi lá tươi sang thẻ giấy?",
                    [
                        "Cô nhắc lá có thể làm ẩm sách",
                        "Nam lấy chiếc lá",
                        "Mai không thích lá",
                        "Vì cuốn sách nói về cây",
                    ],
                    0,
                    "Ngữ liệu nói rõ lời nhắc của cô.",
                    3,
                ),
                choice(
                    LOGIC_STORY
                    + "\nChi tiết Hoa dùng lá đánh dấu có đủ để khẳng định Hoa thích cây nhất không?",
                    [
                        "Có, chắc chắn",
                        "Không, đoạn không đủ bằng chứng",
                        "Có vì mọi người đều thế",
                        "Hoa không đọc sách",
                    ],
                    1,
                    "Việc dùng lá làm dấu không xác định sở thích mạnh nhất.",
                    4,
                ),
                ordering(
                    LOGIC_STORY + "\nXếp các bước suy ra sách của ba bạn.",
                    [
                        "Chốt Hoa nhận truyện còn lại",
                        "Chốt Mai nhận thơ",
                        "Loại thơ và truyện khu vườn cho Nam",
                    ],
                    [1, 2, 0],
                    "Dùng dữ kiện Mai, loại trừ Nam, rồi nhận cuốn còn lại cho Hoa.",
                    4,
                ),
            ],
            plan="vip",
            thinking=True,
        ),
        unit(
            "writing",
            "editing",
            "Nâng cao: sửa đoạn văn để ý rõ và có bằng chứng",
            "Khi sửa bài, xem ý chính trước, rồi xem thứ tự chi tiết, từ dùng, câu và chính tả. "
            "Thay từ quá chung bằng chi tiết cụ thể. Chỉ dùng kết luận vừa với bằng chứng. "
            "Khi nhân hóa, giữ hình ảnh hợp lí và tránh làm người đọc hiểu sai sự thật.",
            "Nháp: 'Cây đẹp. Cây tốt. Cây rất hay.' Sửa: 'Cây ổi trước sân có tán lá xanh, "
            "những quả non tròn nhỏ nép dưới cành. Mỗi sáng, em tưới nước quanh gốc.' "
            "Đoạn sửa giữ cùng đối tượng, thêm chi tiết và hoạt động thay cho lời khen lặp.",
            "Sửa để diễn đạt tốt hơn, không bịa chi tiết. Em tự viết và nhờ người thân đọc góp ý; phần này không chấm tự động bài văn mở.",
            ["Phát hiện ý lặp và chi tiết thiếu rõ.", "Chọn cách sửa giữ đúng ý và bằng chứng."],
            [
                "Nêu ý chính bằng một câu.",
                "Tìm từ lặp và chi tiết chung chung.",
                "Thay bằng điều quan sát được, rồi đọc lại.",
            ],
            [
                choice(
                    "Đoạn 'Cây đẹp. Cây tốt. Cây rất hay.' nên sửa theo hướng nào?",
                    [
                        "Thêm nhiều lần từ đẹp",
                        "Thêm chi tiết lá, quả quan sát được",
                        "Đổi sang chuyện khác",
                        "Bỏ mọi chi tiết",
                    ],
                    1,
                    "Chi tiết cụ thể giúp hình dung, giảm khen chung chung.",
                    3,
                ),
                choice(
                    "Thứ tự kiểm tra bài phù hợp là?",
                    [
                        "Ý chính rồi bố cục, câu từ và chính tả",
                        "Chỉ màu mực",
                        "Chỉ đếm chữ",
                        "Chỉ xem tên người viết",
                    ],
                    0,
                    "Kiểm tra nội dung trước, rồi cách diễn đạt.",
                    3,
                ),
                multiple(
                    "Chọn việc giúp đoạn văn rõ hơn.",
                    [
                        "Bỏ ý lặp",
                        "Thêm chi tiết đúng với quan sát",
                        "Bịa số liệu",
                        "Đổi đối tượng liên tục",
                    ],
                    [0, 1],
                    "Bỏ lặp và dùng chi tiết thật giúp ý rõ.",
                    3,
                ),
                choice(
                    "Chỉ thấy mèo nằm bên cửa sổ một lần. Câu nào vừa với bằng chứng?",
                    [
                        "Mèo luôn nằm đó mọi ngày",
                        "Lúc em quan sát, mèo nằm bên cửa sổ",
                        "Mèo không bao giờ đi đâu",
                        "Mèo biết tất cả suy nghĩ của em",
                    ],
                    1,
                    "Một lần quan sát không đủ khẳng định luôn hay không bao giờ.",
                    4,
                ),
                ordering(
                    "Xếp các bước tự sửa bài.",
                    [
                        "Đọc lại sau khi sửa",
                        "Đọc nháp và tìm chỗ chưa rõ",
                        "Sửa ý, câu hoặc từ đã xác định",
                    ],
                    [1, 2, 0],
                    "Tìm vấn đề, sửa rồi kiểm tra lại.",
                    3,
                ),
                choice(
                    "Câu 'Cây ổi vẫy những cánh tay lá trong gió' là?",
                    [
                        "Nhân hóa để gợi hình",
                        "Số liệu đo thân cây",
                        "Kết luận cây là người thật",
                        "Quy định chăm cây",
                    ],
                    0,
                    "Hành động người được gán cho cây để tạo hình ảnh.",
                    3,
                ),
            ],
            plan="vip",
            reflection=["Viết một đoạn 4–5 câu, tự tìm và sửa ít nhất hai chỗ chưa rõ."],
        ),
    ],
    "ENGLISH": [
        unit(
            "abilities",
            "can-cannot",
            "Can / can't: nói về việc em có thể làm",
            "Dùng can + động từ nguyên mẫu để nói có thể làm việc gì; can't để nói chưa thể. "
            "Hỏi Can you swim? Trả lời Yes, I can hoặc No, I can't. Sau can không thêm s vào động từ, "
            "kể cả với he hoặc she. Có thể dùng and để nối hai khả năng.",
            "Mai can draw and sing. She can't swim. 'Can Mai sing?' — 'Yes, she can.' "
            "Em thử nói hai việc mình làm được và một việc muốn tập thêm với người thân.",
            "I can swim; she can swim. Dùng nguyên mẫu sau can, không dùng can swims.",
            ["Đọc hiểu và viết câu về khả năng.", "Luyện hỏi đáp Can you…? với người thân."],
            [
                "Xác định can hay can't.",
                "Giữ động từ sau can ở dạng nguyên mẫu.",
                "Chọn câu trả lời khớp chủ ngữ.",
            ],
            [
                choice(
                    "Choose the correct sentence.",
                    ["She can swims.", "She can swim.", "She cans swim.", "She can swimming."],
                    1,
                    "Sau can dùng động từ nguyên mẫu swim.",
                ),
                blank("I ___ draw. Điền can để nói em có thể vẽ.", ["can"], "I can draw."),
                choice(
                    "'Can you sing?' — 'Yes, ___.'",
                    ["I can", "I can't", "she can", "I am"],
                    0,
                    "Câu hỏi với you được trả lời bằng I can.",
                ),
                multiple(
                    "Mai can draw and sing. She can't swim. What can Mai do?",
                    ["Draw", "Sing", "Swim", "Fly"],
                    [0, 1],
                    "Đoạn nói rõ Mai vẽ và hát được.",
                ),
                ordering(
                    "Put the words in order.", ["swim.", "can", "He"], [2, 1, 0], "He can swim."
                ),
                choice(
                    "'No, I can't' means?",
                    ["Em có thể", "Em chưa thể làm việc được hỏi", "Em đang ăn", "Em ở trường"],
                    1,
                    "Can't là cannot: không thể trong câu hỏi này.",
                ),
            ],
            reflection=["Nói hai câu I can… và hỏi một người thân Can you…?"],
        ),
        unit(
            "places",
            "directions",
            "Go straight, turn left: đọc chỉ dẫn và biển báo",
            "Go straight: đi thẳng; turn left: rẽ trái; turn right: rẽ phải; stop: dừng lại. "
            "Left và right được hiểu từ hướng người đang di chuyển trong tình huống. "
            "Don't run là không chạy. Khi đi ngoài đường, luôn đi cùng người lớn và tuân thủ tín hiệu thật.",
            "At the school gate, go straight. Turn left at the library. The art room is next to the library. "
            "Trong chỉ dẫn này, đến thư viện rồi rẽ trái. Em dùng sơ đồ trên giấy để thực hành với người thân.",
            "Đọc theo thứ tự. Don't + động từ là lời nhắc không thực hiện hành động.",
            ["Hiểu các chỉ dẫn đơn giản.", "Sắp xếp bước và nhận biết biển Stop / Don't run."],
            [
                "Tìm động từ chỉ hành động.",
                "Theo từng bước từ điểm bắt đầu.",
                "Đọc Don't trước động từ để hiểu điều bị nhắc tránh.",
            ],
            [
                choice(
                    "'Turn left' means?",
                    ["Rẽ trái", "Rẽ phải", "Dừng lại", "Quay về nhà"],
                    0,
                    "Left là trái.",
                ),
                choice(
                    "'Go straight' means?",
                    ["Đi thẳng", "Chạy nhanh", "Rẽ trái", "Ngồi xuống"],
                    0,
                    "Go straight: đi thẳng.",
                ),
                choice(
                    "You see 'Don't run' in the library. You should?",
                    ["Run", "Walk calmly", "Shout", "Jump on tables"],
                    1,
                    "Don't run: không chạy, đi bình tĩnh.",
                ),
                ordering(
                    "At the gate, go straight, then turn left at the library. Xếp chỉ dẫn.",
                    ["Turn left at the library", "Start at the gate", "Go straight"],
                    [1, 2, 0],
                    "Bắt đầu tại cổng, đi thẳng, rẽ trái ở thư viện.",
                ),
                blank(
                    "'Turn ___' means rẽ phải. Điền một từ tiếng Anh.",
                    ["right"],
                    "Turn right là rẽ phải.",
                ),
                choice(
                    "The art room is next to the library. Where is it?",
                    ["Bên cạnh thư viện", "Trong bếp", "Trên mái nhà", "Xa mọi nơi"],
                    0,
                    "Next to nghĩa là bên cạnh.",
                ),
            ],
            reflection=["Vẽ sơ đồ đơn giản và đọc hai chỉ dẫn tiếng Anh cho người thân."],
        ),
        unit(
            "food",
            "preferences",
            "Sở thích và lời mời lịch sự trong bữa ăn",
            "Dùng I like… để nói sở thích, I don't like… để nói không thích. Hỏi What food do you like? "
            "Khi mời, dùng Would you like some water? Có thể trả lời Yes, please hoặc No, thank you. "
            "Food là thức ăn, drink là đồ uống. Không suy ra mọi sở thích của một bạn từ một câu đơn lẻ.",
            "'What food do you like?' — 'I like rice and chicken.' 'Would you like some water?' "
            "— 'Yes, please.' 'Would you like some milk?' — 'No, thank you.' Nói lịch sự cả khi nhận lẫn từ chối.",
            "I like nói sở thích; Would you like…? mời ở tình huống hiện tại. Chọn đáp lời đúng câu hỏi.",
            ["Hỏi đáp sở thích bằng câu đơn giản.", "Nhận và từ chối lời mời lịch sự."],
            [
                "Xác định hỏi sở thích hay lời mời.",
                "Tìm food hoặc drink.",
                "Thêm please hoặc thank you khi đáp lời mời.",
            ],
            [
                choice(
                    "'Would you like some water?' Nhận lời lịch sự là?",
                    ["Yes, please.", "Water blue.", "I nine.", "Go left."],
                    0,
                    "Yes, please là đáp lời nhận lời mời.",
                ),
                choice(
                    "Từ chối lời mời lịch sự là?",
                    ["No, thank you.", "Go away!", "Give me!", "You wrong."],
                    0,
                    "No, thank you từ chối kèm cảm ơn.",
                ),
                multiple(
                    "Choose the drinks.",
                    ["Water", "Milk", "Rice", "Chicken"],
                    [0, 1],
                    "Water và milk là đồ uống.",
                ),
                blank("I ___ rice. Điền like để nói em thích cơm.", ["like"], "I like rice."),
                ordering(
                    "Put the words in order.",
                    ["you", "Do", "apples?", "like"],
                    [1, 0, 3, 2],
                    "Do you like apples?",
                ),
                choice(
                    "Tom says 'I like rice.' What do we know?",
                    [
                        "Tom likes rice",
                        "Tom likes every food",
                        "Tom never drinks water",
                        "Tom dislikes all fruit",
                    ],
                    0,
                    "Chỉ biết Tom thích cơm, không suy ra những điều khác.",
                ),
            ],
        ),
        unit(
            "routines",
            "schedule-riddle",
            "Đố tư duy tiếng Anh: chọn hoạt động phù hợp",
            "Khi đọc lịch, tìm ngày, giờ bắt đầu, giờ kết thúc và điều kiện của người tham gia. "
            "Before ten nghĩa là trước 10 giờ. Muốn tham gia từ đầu, giờ đến phải không muộn hơn giờ bắt đầu. "
            "Đối chiếu cả sở thích lẫn thời gian; một điều kiện đúng chưa đủ.",
            SCHEDULE
            + "\nBen thích art và reading, nhưng không đến trước ten. Art đã bắt đầu lúc nine; "
            "reading bắt đầu ten nên phù hợp để tham gia từ đầu.",
            "Dùng bằng chứng từ câu tiếng Anh, không chọn chỉ vì tên hoạt động quen thuộc.",
            [
                "Đọc lịch ngắn và kết hợp hai điều kiện.",
                "Giải thích lựa chọn bằng chi tiết về giờ và sở thích.",
            ],
            [
                "Gạch giờ bắt đầu mỗi hoạt động.",
                "Đánh dấu các hoạt động Ben thích.",
                "Loại hoạt động bắt đầu trước lúc Ben có thể đến.",
            ],
            [
                choice(
                    SCHEDULE
                    + "\nWhich activity fits Ben's likes and lets him join from the start?",
                    ["Art", "Reading", "Football", "None"],
                    1,
                    "Reading bắt đầu lúc 10 và thuộc sở thích đã nêu.",
                    4,
                ),
                choice(
                    SCHEDULE + "\nWhy can't Ben join art from the start?",
                    [
                        "Art starts before ten",
                        "He dislikes art",
                        "Art is on Monday",
                        "There is no art",
                    ],
                    0,
                    "Art bắt đầu lúc 9; Ben không đến trước 10.",
                    3,
                ),
                blank(
                    SCHEDULE + "\nReading starts at ___. Điền từ chỉ giờ bằng tiếng Anh.",
                    ["ten"],
                    "Reading starts at ten.",
                    3,
                ),
                multiple(
                    SCHEDULE + "\nChoose the facts stated in the text.",
                    [
                        "Ben likes reading",
                        "Art ends at ten",
                        "Ben likes football",
                        "The club meets on Monday",
                    ],
                    [0, 1],
                    "Hai ý đầu được nói rõ; football không phải sở thích được nêu.",
                    4,
                ),
                ordering(
                    SCHEDULE + "\nPut the activities in order of start time.",
                    ["Football", "Art", "Reading"],
                    [1, 2, 0],
                    "Art 9 giờ, reading 10 giờ, football 11 giờ.",
                    3,
                ),
                choice(
                    SCHEDULE + "\nDo we know whether Ben likes football?",
                    [
                        "Yes, he likes it",
                        "No, the text does not tell us",
                        "Yes, he hates it",
                        "There is no football",
                    ],
                    1,
                    "Không được nêu không có nghĩa là không thích.",
                    4,
                ),
            ],
            plan="vip",
            thinking=True,
        ),
    ],
}

# Diagrams use exactly the numbers discussed in the worked examples.
GRADE4["MATH"][1]["lesson"]["content"]["illustration"] = {
    "kind": "angles",
    "angle": 120,
    "caption": "Góc 120°: lớn hơn góc vuông 90° và nhỏ hơn góc bẹt 180°.",
}
GRADE4["MATH"][2]["lesson"]["content"]["illustration"] = {
    "kind": "bars",
    "labels": ["Tổ 1", "Tổ 2", "Tổ 3"],
    "values": [12, 16, 20],
    "caption": "Số cây ba tổ trồng: 12, 16, 20 cây. Mỗi vạch của trục đứng ứng với 4 cây.",
}
