"""Six original grade-four extension lessons. No changes to published older versions."""

from app.curriculum import blank, choice, lesson, multiple, ordering

RIVER = (
    "Sau trận mưa, lối vào thư viện có nhiều vũng nước. Lan đặt một tấm biển nhắc các bạn đi chậm. "
    "Minh cùng bác bảo vệ quét nước sang rãnh thoát. Khi lối đi khô, hai bạn cất biển để mọi người đi lại dễ dàng."
)
GARDEN = (
    "Lớp 4 trồng rau trong ba khay. Khay gần cửa sổ xanh tốt, khay trong góc có lá nhạt màu. "
    "Cả hai khay được tưới như nhau. Các bạn chuyển khay trong góc ra chỗ sáng rồi ghi lại sự thay đổi mỗi ngày."
)
MARKET = (
    "On Saturday, Anna and her dad go to the market. They buy two apples and some bread. "
    "Anna carries a small bag. It starts to rain, so they wait under a roof. When the rain stops, they walk home."
)
PICNIC = (
    "Our class has a picnic on Sunday. We meet at school at eight o'clock. "
    "Tom brings water, and Lucy brings sandwiches. We play a game in the park. "
    "Before we leave, we put our rubbish in a bin. We go home at eleven o'clock."
)

VIP_EXTENSION = {
    "MATH": [
        dict(
            topic="fractions",
            code="vip-fraction-project",
            sort_order=31,
            title="Phân số trong một buổi làm bánh",
            lesson=lesson(
                "Phân số trong một buổi làm bánh",
                "Để so sánh phần bánh, hãy xác định cùng một cái bánh làm đơn vị. Với phân số cùng mẫu số, so sánh tử số; cộng và trừ tử số, giữ nguyên mẫu số. Khi khác mẫu số, chia lại thành những phần bằng nhau trước khi tính. Không cộng hai phần của những cái bánh có kích thước khác nhau như thể cùng một đơn vị.",
                "Một cái bánh chia 8 phần bằng nhau. Nhóm A dùng 3/8, nhóm B dùng 2/8. Đã dùng (3 + 2)/8 = 5/8, còn 3/8. Nếu dùng thêm 1/4 cái bánh, đổi 1/4 = 2/8, tổng dùng 7/8, còn 1/8.",
                "Xác định cùng một đơn vị, quy về cùng mẫu số khi cần và kiểm tra tổng phần đã dùng với phần còn lại bằng 1.",
            ),
            questions=[
                choice(
                    "Cùng một cái bánh: nhóm A dùng 3/8, nhóm B dùng 2/8. Hai nhóm dùng bao nhiêu?",
                    ["5/8", "5/16", "1/8", "6/8"],
                    0,
                    "Cùng mẫu số 8: (3 + 2)/8 = 5/8.",
                    3,
                ),
                choice(
                    "Đã dùng 5/8 một cái bánh. Phần còn lại là?",
                    ["3/8", "5/8", "3/5", "1/8"],
                    0,
                    "Một cái bánh là 8/8; 8/8 − 5/8 = 3/8.",
                    3,
                ),
                multiple(
                    "Chọn các phân số bằng 1/2.",
                    ["2/4", "4/8", "3/8", "1/4"],
                    [0, 1],
                    "Nhân cả tử và mẫu của 1/2 với 2 hoặc 4 được 2/4 và 4/8.",
                    3,
                ),
                blank(
                    "Một bánh chia 8 phần. Ăn 1/4 bánh, tức là mấy phần? Chỉ điền số.",
                    ["2"],
                    "1/4 = 2/8 nên đã ăn 2 phần.",
                    3,
                ),
                choice(
                    "Cùng một bánh: dùng 3/8 rồi thêm 1/4. Tổng phần đã dùng là?",
                    ["5/8", "4/12", "4/8", "1/2"],
                    0,
                    "Đổi 1/4 = 2/8; 3/8 + 2/8 = 5/8.",
                    4,
                ),
                ordering(
                    "Xếp các bước tìm phần còn lại khi đã ăn 1/4 và 3/8 cùng một bánh.",
                    ["Lấy 8/8 − 5/8 = 3/8", "Đổi 1/4 = 2/8", "Cộng 2/8 + 3/8 = 5/8"],
                    [1, 2, 0],
                    "Quy về cùng mẫu số, cộng phần đã dùng, rồi lấy cả bánh trừ đi.",
                    4,
                ),
                choice(
                    "Một bạn nói 2/8 + 3/8 = 5/16. Nhận xét nào đúng?",
                    [
                        "Sai vì cùng mẫu số thì giữ mẫu số 8",
                        "Đúng vì cộng cả tử và mẫu",
                        "Sai vì kết quả phải là 6/8",
                        "Đúng với mọi phân số",
                    ],
                    0,
                    "Các phần vẫn có kích thước 1/8, nên 2 phần cộng 3 phần là 5/8.",
                    3,
                ),
                blank(
                    "8/8 − 5/8 = ? Điền phân số dạng a/b.",
                    ["3/8"],
                    "Trừ tử số: (8 − 5)/8 = 3/8.",
                    3,
                ),
            ],
        ),
        dict(
            topic="measurement",
            code="vip-garden-design",
            sort_order=32,
            title="Thiết kế luống rau: chu vi và diện tích",
            lesson=lesson(
                "Thiết kế luống rau: chu vi và diện tích",
                "Chu vi cho biết chiều dài đường bao; diện tích cho biết phần mặt đất bên trong. Với hình chữ nhật, chu vi bằng (dài + rộng) × 2, diện tích bằng dài × rộng. Kiểm tra các độ dài cùng đơn vị trước khi tính. Khi tính dây rào có lối vào, tính chu vi rồi trừ chiều rộng lối vào.",
                "Luống rau dài 8 m, rộng 5 m: chu vi (8 + 5) × 2 = 26 m; diện tích 8 × 5 = 40 m². Chừa lối vào rộng 2 m thì cần 26 − 2 = 24 m dây rào. Diện tích không giảm vì chỉ bỏ một đoạn rào.",
                "Chu vi dùng m hoặc cm; diện tích dùng m² hoặc cm². Cùng chu vi chưa chắc cùng diện tích.",
            ),
            questions=[
                choice(
                    "Luống rau dài 8 m, rộng 5 m có chu vi?",
                    ["26 m", "40 m", "13 m", "26 m²"],
                    0,
                    "(8 + 5) × 2 = 26 m.",
                    3,
                ),
                choice(
                    "Luống rau dài 8 m, rộng 5 m có diện tích?",
                    ["40 m²", "26 m²", "13 m²", "40 m"],
                    0,
                    "8 × 5 = 40 m².",
                    3,
                ),
                blank(
                    "Chu vi luống rau 26 m, chừa lối vào 2 m. Cần mấy mét dây rào? Chỉ điền số.",
                    ["24"],
                    "26 − 2 = 24 m.",
                    3,
                ),
                multiple(
                    "Hai luống 8 m × 5 m và 9 m × 4 m. Chọn nhận xét đúng.",
                    [
                        "Cùng chu vi 26 m",
                        "Diện tích lần lượt 40 m² và 36 m²",
                        "Cùng diện tích",
                        "Luống thứ hai có chu vi 36 m",
                    ],
                    [0, 1],
                    "Hai chu vi đều 26 m; diện tích 40 m² và 36 m².",
                    4,
                ),
                choice(
                    "Luống dài 600 cm, rộng 4 m. Diện tích là?",
                    ["24 m²", "2400 m²", "20 m²", "10 m²"],
                    0,
                    "600 cm = 6 m; 6 × 4 = 24 m².",
                    4,
                ),
                ordering(
                    "Xếp các bước tính diện tích hình dài 500 cm, rộng 3 m.",
                    ["Tính 5 × 3 = 15", "Viết đáp số 15 m²", "Đổi 500 cm = 5 m"],
                    [2, 0, 1],
                    "Đổi về cùng đơn vị, tính rồi ghi đơn vị diện tích.",
                    3,
                ),
                blank(
                    "Luống hình chữ nhật có diện tích 36 m², rộng 4 m. Dài bao nhiêu mét? Chỉ điền số.",
                    ["9"],
                    "Chiều dài = 36 : 4 = 9 m.",
                    4,
                ),
                choice(
                    "Bỏ đoạn rào 2 m làm lối vào có làm giảm diện tích luống rau không?",
                    [
                        "Không, phần đất bên trong vẫn giữ nguyên",
                        "Có, giảm 2 m²",
                        "Có, giảm 2 m",
                        "Diện tích bằng chiều dài dây rào",
                    ],
                    0,
                    "Chỉ bỏ đoạn rào; kích thước luống rau không thay đổi.",
                    3,
                ),
            ],
        ),
    ],
    "VIETNAMESE": [
        dict(
            topic="reading",
            code="vip-evidence-detective",
            sort_order=31,
            title="Thám tử đọc hiểu: tìm bằng chứng",
            lesson=lesson(
                "Thám tử đọc hiểu: tìm bằng chứng",
                "Một suy luận tốt phải dựa vào chi tiết trong đoạn đọc. Em hãy phân biệt điều tác giả nói rõ với điều mình suy ra. Khi có nhiều cách giải thích, chọn cách được nhiều chi tiết ủng hộ nhất; không thêm sự việc chưa được kể.",
                RIVER
                + " Có thể suy ra Lan chú ý đến an toàn vì bạn đặt biển nhắc đi chậm. Không thể kết luận Lan đã bị ngã, vì đoạn không kể điều đó.",
                "Nêu ý kiến rồi chỉ ra chi tiết làm bằng chứng. Dùng 'có thể' khi suy luận; không nói chắc điều đoạn đọc chưa xác nhận.",
            ),
            questions=[
                choice(
                    RIVER + " Vì sao Lan đặt biển nhắc đi chậm?",
                    [
                        "Để các bạn chú ý an toàn khi lối đi có vũng nước",
                        "Để đóng cửa thư viện",
                        "Vì Lan muốn bán biển",
                        "Vì thư viện hết sách",
                    ],
                    0,
                    "Chi tiết lối đi có nhiều vũng nước hỗ trợ suy luận về an toàn.",
                    3,
                ),
                multiple(
                    RIVER + " Chọn sự việc được kể rõ trong đoạn.",
                    [
                        "Lan đặt biển nhắc đi chậm",
                        "Minh cùng bác bảo vệ quét nước",
                        "Lan đã bị ngã",
                        "Thư viện bị đóng cửa cả ngày",
                    ],
                    [0, 1],
                    "Đoạn nói rõ hai việc đầu; không kể hai việc sau.",
                    3,
                ),
                choice(
                    RIVER
                    + " Chi tiết nào cho thấy hai bạn biết điều chỉnh việc làm theo tình hình?",
                    [
                        "Lối đi khô thì cất biển",
                        "Đoạn có từ thư viện",
                        "Minh là bạn của Lan",
                        "Trời sẽ tiếp tục mưa",
                    ],
                    0,
                    "Biển được cất khi nguy cơ do vũng nước đã giảm.",
                    4,
                ),
                ordering(
                    RIVER + " Xếp các sự việc theo đoạn.",
                    ["Lối đi khô, cất biển", "Có nhiều vũng nước", "Đặt biển và quét nước"],
                    [1, 2, 0],
                    "Vũng nước xuất hiện; các bạn xử lí; khi khô thì cất biển.",
                    3,
                ),
                choice(
                    GARDEN + " Các bạn muốn kiểm tra điều gì?",
                    [
                        "Ánh sáng có liên quan đến màu lá và sự phát triển",
                        "Nước không cần cho cây",
                        "Khay rau không cần đất",
                        "Mọi cây đều sống trong góc tối",
                    ],
                    0,
                    "Hai khay được tưới như nhau nhưng nhận ánh sáng khác nhau.",
                    4,
                ),
                multiple(
                    GARDEN + " Chi tiết nào hỗ trợ việc tìm hiểu vai trò ánh sáng?",
                    [
                        "Khay gần cửa sổ xanh tốt",
                        "Hai khay được tưới như nhau",
                        "Các bạn đã thu hoạch rất nhiều rau",
                        "Khay trong góc có lá nhạt màu",
                    ],
                    [0, 1, 3],
                    "Đoạn có ba chi tiết này; chưa kể kết quả thu hoạch.",
                    4,
                ),
                choice(
                    GARDEN + " Kết luận nào vượt quá thông tin của đoạn?",
                    [
                        "Chuyển khay xong, rau chắc chắn lớn gấp đôi",
                        "Khay trong góc có lá nhạt màu",
                        "Các bạn ghi lại thay đổi mỗi ngày",
                        "Các bạn chuyển khay ra chỗ sáng",
                    ],
                    0,
                    "Đoạn chưa kể kết quả sau khi chuyển khay, nên không thể khẳng định lớn gấp đôi.",
                    3,
                ),
                blank(
                    "Điền từ còn thiếu: Một suy luận cần có ___ từ đoạn đọc để hỗ trợ.",
                    ["bằng chứng"],
                    "Bằng chứng là chi tiết cụ thể giúp giải thích suy luận.",
                    3,
                ),
            ],
        ),
        dict(
            topic="sentences",
            code="vip-editing-workshop",
            sort_order=32,
            title="Xưởng viết: nối ý và sửa câu",
            lesson=lesson(
                "Xưởng viết: nối ý và sửa câu",
                "Khi viết một đoạn ngắn, mỗi câu cần rõ người hoặc sự vật được nói đến và điều muốn nói. Dùng từ nối phù hợp để thể hiện trình tự, nguyên nhân hoặc sự đối lập. Đại từ thay thế chỉ nên dùng khi người đọc biết nó chỉ ai. Đọc lại để tìm từ lặp và thông tin chưa có căn cứ.",
                "'Nam thấy chậu cây khô. Nam tưới nước. Nam đặt chậu ở chỗ sáng.' Có thể sửa: 'Thấy chậu cây khô, Nam tưới vừa đủ nước. Sau đó, bạn đặt chậu ở chỗ sáng.' Giữ ý chính, giảm lặp tên và làm rõ thứ tự.",
                "Sửa câu để rõ nghĩa, không thêm sự việc mới. Từ nối phải đúng quan hệ giữa các ý.",
            ),
            questions=[
                choice(
                    "Chọn từ nối phù hợp: Trời mưa to, ___ chúng em ở trong lớp.",
                    ["nên", "nhưng", "tuy", "hoặc"],
                    0,
                    "Ở trong lớp là kết quả của việc trời mưa to; dùng 'nên'.",
                    3,
                ),
                choice(
                    "Câu nào thể hiện sự đối lập?",
                    [
                        "Trời lạnh nhưng Mai vẫn đến lớp đúng giờ.",
                        "Mai đến lớp rồi mở sách.",
                        "Vì trời lạnh nên Mai mặc áo ấm.",
                        "Mai mang sách và vở.",
                    ],
                    0,
                    "'Nhưng' nối hai ý có sự đối lập.",
                    3,
                ),
                multiple(
                    "Chọn các cách giúp đoạn văn rõ nghĩa.",
                    [
                        "Dùng từ nối đúng quan hệ",
                        "Làm rõ đại từ đang chỉ ai",
                        "Thêm sự việc chưa biết có thật",
                        "Đọc lại để giảm lặp từ không cần thiết",
                    ],
                    [0, 1, 3],
                    "Rõ quan hệ, rõ người được nói đến và giảm lặp giúp người đọc hiểu.",
                    3,
                ),
                ordering(
                    "Xếp trình tự viết và sửa một đoạn giới thiệu góc đọc sách.",
                    [
                        "Đọc lại, sửa câu và từ lặp",
                        "Chọn các ý chính",
                        "Viết thành các câu có thứ tự",
                    ],
                    [1, 2, 0],
                    "Chọn ý, viết câu, rồi đọc lại để sửa.",
                    3,
                ),
                choice(
                    "'Lan nhờ Hoa đưa sách cho Mai. Bạn ấy đồng ý.' Vì sao nên sửa câu sau?",
                    [
                        "Chưa rõ 'bạn ấy' chỉ Lan, Hoa hay Mai",
                        "Vì không được dùng đại từ",
                        "Vì câu không có từ sách",
                        "Vì mọi câu đều phải rất dài",
                    ],
                    0,
                    "Có nhiều người được nhắc tới, nên cần nói rõ ai đồng ý.",
                    4,
                ),
                blank(
                    "Điền từ nối chỉ trình tự: Em rửa tay. ___, em chuẩn bị bữa ăn.",
                    ["sau đó", "tiếp theo"],
                    "Sau đó/tiếp theo cho biết việc chuẩn bị bữa ăn diễn ra sau rửa tay.",
                    3,
                ),
                choice(
                    "Sửa 'Minh trồng cây. Minh tưới cây.' mà giữ nguyên ý:",
                    [
                        "Minh trồng cây rồi tưới cây.",
                        "Minh trồng cây vì cây đã ra quả.",
                        "Minh bán cây ở chợ.",
                        "Minh trồng rất nhiều cây cổ thụ.",
                    ],
                    0,
                    "Câu đầu nối đúng hai việc đã có, không thêm sự việc mới.",
                    3,
                ),
                choice(
                    "Đoạn tả thư viện nói 'Có kệ sách thấp. Các bạn dễ lấy sách.' Câu kết nào phù hợp?",
                    [
                        "Kệ sách thấp giúp các bạn chọn sách thuận tiện.",
                        "Thư viện có hàng triệu cuốn sách.",
                        "Mọi bạn đều đọc hết sách trong một ngày.",
                        "Không cần giữ gìn sách.",
                    ],
                    0,
                    "Câu kết dựa trên hai chi tiết đã được nêu.",
                    4,
                ),
            ],
        ),
    ],
    "ENGLISH": [
        dict(
            topic="routines",
            code="vip-market-story",
            sort_order=31,
            title="A trip to the market: đọc theo trình tự",
            lesson=lesson(
                "A trip to the market: đọc theo trình tự",
                "Khi đọc một câu chuyện tiếng Anh, tìm who, where, when và các hành động theo thứ tự. Từ 'so' nối nguyên nhân với kết quả; 'when' giúp nhận ra thời điểm xảy ra việc. Không chọn đáp án chỉ vì có một từ giống đoạn đọc.",
                MARKET
                + " Who goes to the market? Anna and her dad. Why do they wait? Because it starts to rain. They walk home after the rain stops.",
                "Đọc cả câu có thông tin cần tìm. Dùng chi tiết trong bài, không đoán thêm.",
            ),
            questions=[
                choice(
                    MARKET + " Who goes to the market with Anna?",
                    ["Her dad", "Her teacher", "Her brother", "Her friend"],
                    0,
                    "The first sentence says Anna and her dad go to the market.",
                    3,
                ),
                multiple(
                    MARKET + " What do they buy?",
                    ["Apples", "Bread", "Milk", "Books"],
                    [0, 1],
                    "They buy two apples and some bread.",
                    3,
                ),
                choice(
                    MARKET + " Why do they wait under a roof?",
                    [
                        "It starts to rain",
                        "They are reading",
                        "The market is closed",
                        "They want to sleep",
                    ],
                    0,
                    "'It starts to rain, so they wait under a roof.'",
                    3,
                ),
                ordering(
                    MARKET + " Put the events in order.",
                    ["They walk home", "They buy food", "They wait under a roof"],
                    [1, 2, 0],
                    "First they buy food, then wait for the rain to stop, then walk home.",
                    4,
                ),
                blank(
                    MARKET + " Complete: Anna carries a small ___.",
                    ["bag"],
                    "The story says Anna carries a small bag.",
                    3,
                ),
                choice(
                    MARKET + " When do they walk home?",
                    ["When the rain stops", "Before they buy food", "At night", "On Monday"],
                    0,
                    "The last sentence gives the time: when the rain stops.",
                    3,
                ),
                choice(
                    "Complete: It is raining, ___ we wait inside.",
                    ["so", "or", "but", "before"],
                    0,
                    "'So' introduces the result of the rain.",
                    3,
                ),
                choice(
                    MARKET + " Which sentence is NOT stated in the story?",
                    [
                        "Anna buys milk",
                        "Anna goes on Saturday",
                        "They buy bread",
                        "Anna carries a bag",
                    ],
                    0,
                    "Milk is not mentioned. The other details are stated.",
                    4,
                ),
            ],
        ),
        dict(
            topic="school",
            code="vip-picnic-planner",
            sort_order=32,
            title="Our class picnic: đọc kế hoạch và giờ",
            lesson=lesson(
                "Our class picnic: đọc kế hoạch và giờ",
                "Một kế hoạch tiếng Anh thường cho biết ngày, nơi gặp, giờ và việc cần chuẩn bị. Phân biệt 'at eight o'clock' (giờ) với 'on Sunday' (ngày). Dùng 'before' và 'after' để hiểu thứ tự hoạt động; đọc đúng chủ thể của từng việc.",
                PICNIC
                + " We meet at school, but play in the park. Tom brings water; Lucy brings sandwiches. From eight to eleven is three hours.",
                "Tìm bằng chứng về người, nơi và thời gian. Giữ gìn nơi công cộng khi tham gia hoạt động.",
            ),
            questions=[
                choice(
                    PICNIC + " Where do the children meet?",
                    ["At school", "At home", "At the market", "In a shop"],
                    0,
                    "They meet at school; the game happens in the park.",
                    3,
                ),
                choice(
                    PICNIC + " Who brings sandwiches?",
                    ["Lucy", "Tom", "Anna", "The driver"],
                    0,
                    "Lucy brings sandwiches; Tom brings water.",
                    3,
                ),
                multiple(
                    PICNIC + " Choose the correct statements.",
                    [
                        "The picnic is on Sunday",
                        "They meet at eight o'clock",
                        "They leave rubbish on the grass",
                        "They go home at eleven o'clock",
                    ],
                    [0, 1, 3],
                    "The class puts rubbish in a bin, so the third statement is wrong.",
                    4,
                ),
                ordering(
                    PICNIC + " Put the activities in order.",
                    ["Put rubbish in a bin", "Meet at school", "Play a game", "Go home"],
                    [1, 2, 0, 3],
                    "Meet, play, clean up, then go home.",
                    4,
                ),
                blank(
                    "Complete with at or on: We meet ___ eight o'clock.",
                    ["at"],
                    "Use 'at' with a clock time.",
                    3,
                ),
                blank(
                    "Complete with at or on: The picnic is ___ Sunday.",
                    ["on"],
                    "Use 'on' with a day of the week.",
                    3,
                ),
                choice(
                    PICNIC + " How long is it from eight to eleven o'clock?",
                    ["Three hours", "Two hours", "Four hours", "One hour"],
                    0,
                    "11 − 8 = 3 hours.",
                    4,
                ),
                choice(
                    PICNIC + " What do they do before leaving?",
                    ["Put rubbish in a bin", "Buy apples", "Read in the library", "Go to sleep"],
                    0,
                    "The text says they put rubbish in a bin before they leave.",
                    3,
                ),
            ],
        ),
    ],
}
