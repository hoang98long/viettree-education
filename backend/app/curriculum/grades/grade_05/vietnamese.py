"""Reading, language and guided writing with original Vietnamese texts."""

from app.curriculum.grades.grade_05.builders import language_unit
from app.curriculum.grades.grade_05.readings import PERSON, POEM, RAIN, SCENERY, SEEDLING, UMBRELLA

VIETNAMESE = []


def add(topic, code, title, teaching, context, remember, rows, reflection=None):
    VIETNAMESE.append(
        language_unit(
            "VIETNAMESE",
            len(VIETNAMESE),
            topic,
            code,
            title,
            teaching,
            context,
            remember,
            [
                "Đọc lại câu hỏi, tìm từ hoặc chi tiết có liên quan trong ngữ liệu.",
                teaching,
                "Thử giải thích lựa chọn bằng một câu trích ngắn hoặc lí do; loại đáp án trái dữ kiện.",
            ],
            rows,
            reflection=reflection,
        )
    )


add(
    "reading",
    "shared-umbrella",
    "Đọc truyện: Chiếc ô chung",
    "Đọc lướt để biết ai, ở đâu và việc chính; đọc kĩ để nối hành động với lí do. Tóm tắt giữ sự việc quan trọng, không kể mọi chi tiết. Một lời giải thích cần có bằng chứng từ truyện.",
    UMBRELLA,
    "Chi tiết Minh quay lại và nghiêng ô giúp hiểu sự quan tâm; cảm xúc phải dựa vào hành động hoặc lời nói.",
    """
Vì sao An đứng chờ? | Bạn quên áo mưa và lo vở ướt | Bạn muốn tưới cây | Bạn đợi mua ô mới | Truyện nêu An quên áo mưa và ôm chồng vở.
Minh đề nghị đi cùng đến đâu? | Nhà chờ xe buýt | Vườn của ông | Một lớp học khác | Minh nói cùng đi đến nhà chờ xe buýt.
Chi tiết nào cho thấy An cũng quan tâm Minh? | An đề nghị đổi chỗ và cùng giữ ô | An bỏ đi không nói | An lấy ô về nhà | An nhận ra vai bạn ướt và đề nghị cùng giữ cán ô.
Tóm tắt nào đúng việc chính? | Minh chia sẻ ô giúp bạn và em nhỏ rồi về nhà | Minh mua ô mới ở cửa hàng | An làm mất vở rồi tìm cả ngày | Bản tóm tắt giữ hành động giúp người và kết thúc có trong truyện.
""",
    ["Tóm tắt truyện trong 3–4 câu, rồi nêu một chi tiết khiến em chú ý."],
)

add(
    "reading",
    "seedling-journal",
    "Đọc truyện: Mầm cây bên cửa",
    "Phân biệt điều nhân vật đã quan sát với điều đang đoán. Theo dõi sự thay đổi trước và sau một lời khuyên, rồi giải thích bài học rút ra bằng chi tiết cụ thể.",
    SEEDLING,
    "Chưa thấy mầm không đủ chứng minh hạt hỏng. Nhật kí ghi điều thấy được giúp theo dõi và sửa nhận xét.",
    """
Lan ghi nhật kí bằng cách nào? | Bảng ngày quan sát, việc làm, điều nhìn thấy | Chỉ vẽ một bức tranh cuối tuần | Ghi toàn bộ lời bạn bằng trí nhớ | Truyện nêu ba cột cụ thể của bảng.
Vì sao Lan đề nghị tưới bằng thìa nhỏ? | Muốn đất vừa đủ ẩm và nhớ hạt cần không khí | Muốn làm hạt khô hoàn toàn | Muốn thay hạt đậu bằng cây khác | Lan nhớ lời cô và không muốn tưới quá nhiều.
Lan sửa câu nào? | Hạt không mọc thành hôm nay chưa thấy mầm | Cây cao thành cây thấp | Hai tuần thành hai tháng | Truyện phân biệt kết luận vội với quan sát trong ngày.
Nhóm đã học được điều gì? | Cần quan sát, trao đổi và kiên nhẫn | Có thể bỏ nhật kí khi chưa thấy cây | Tưới càng nhiều càng tốt | Kết truyện nhấn mạnh thử, quan sát, trao đổi và kiên nhẫn.
""",
)

add(
    "vocabulary",
    "synonyms-context",
    "Chọn từ đồng nghĩa theo ngữ cảnh",
    "Từ đồng nghĩa có nghĩa gần nhau nhưng sắc thái hoặc phạm vi dùng có thể khác. Thay từ phải giữ ý trong câu và phù hợp người, sự vật được nói đến.",
    "Bà dịu dàng hỏi Lan có mệt không. Lan nhìn dòng sông yên ả rồi kể về buổi học. Khi nói về bà, em dùng giọng kính trọng. Khi tả cảnh, em chọn những từ giúp người đọc hình dung sự êm đềm.",
    "Không phải mọi từ gần nghĩa đều thay được trong mọi câu.",
    """
Từ gần nghĩa dịu dàng trong ngữ liệu? | Hiền hậu | Ồn ào | Vội vã | Hiền hậu phù hợp cách bà hỏi han, hai từ còn lại khác sắc thái.
Từ gần nghĩa yên ả khi tả dòng sông? | Êm đềm | Náo nhiệt | Chật chội | Êm đềm cùng gợi cảnh thanh bình.
Giọng kính trọng phù hợp với ai trong ngữ liệu? | Người bà | Một tiếng còi | Dòng sông | Lan nói về bà bằng thái độ kính trọng.
Khi thay từ, cần giữ điều gì? | Ý câu và sắc thái phù hợp | Chỉ số chữ trong câu | Chỉ chữ cái đầu | Từ đồng nghĩa cần được chọn theo ngữ cảnh và mục đích.
""",
)

add(
    "vocabulary",
    "multiple-meanings",
    "Từ đa nghĩa và đồng âm khác nghĩa",
    "Từ đa nghĩa có các nghĩa liên quan nhau. Từ đồng âm giống hình thức nhưng nghĩa khác, không cùng quan hệ chuyển nghĩa. Dựa vào câu để xác định nghĩa đang dùng.",
    "Mai thấy một bàn chân in trên cát. Ở nhà, em lau chân bàn. Mẹ cho một thìa đường vào cốc nước, còn bố hỏi đường đến thư viện. Mai nhận ra cùng một tiếng có thể mang những nghĩa khác nhau.",
    "Chân người và chân bàn có liên hệ với phần dưới nâng đỡ; đường ăn và đường đi là hai nghĩa khác nhau của từ đồng âm.",
    """
Chân trong chân bàn chỉ gì? | Bộ phận đỡ bàn | Bàn chân người thật | Một con đường | Ngữ cảnh nói về bộ phận của bàn.
Quan hệ chân người và chân bàn? | Các nghĩa liên quan của từ đa nghĩa | Hai tên riêng nước ngoài | Hai dấu câu | Cả hai gợi phần dưới nâng đỡ, là quan hệ chuyển nghĩa.
Đường trong thìa đường là gì? | Chất có vị ngọt | Lối đi đến thư viện | Chân của cái bàn | Vật được cho vào cốc là đường ăn.
Hai từ đường ăn và đường đi thuộc trường hợp nào? | Đồng âm khác nghĩa | Đồng nghĩa hoàn toàn | Cùng chỉ một vật | Hai nghĩa không có quan hệ chuyển nghĩa ở ví dụ này.
""",
)

add(
    "sentences",
    "pronouns-connectors",
    "Đại từ và kết từ nối ý",
    "Đại từ giúp thay thế hoặc chỉ người, sự vật đã nói. Kết từ nối các từ hoặc các vế câu, thể hiện quan hệ như thêm ý, nguyên nhân hay đối lập. Đọc cả câu để hiểu quan hệ ấy.",
    "Lan mượn sách rồi mang nó về lớp. Em đọc chậm vì muốn hiểu từng chi tiết. Tuấn thích tranh, còn Lan thích những câu chuyện. Hai bạn khác sở thích nhưng cùng giữ sách cẩn thận.",
    "Từ nó phải có đối tượng được nhắc rõ; vì nêu lí do, nhưng nối hai ý đối lập.",
    """
Nó trong câu đầu thay cho gì? | Cuốn sách | Lớp học | Tuấn | Trước nó, câu đã nhắc việc Lan mượn sách.
Vì nối quan hệ gì? | Nguyên nhân | Chọn nơi ở | So sánh kích thước | Muốn hiểu chi tiết là lí do đọc chậm.
Nhưng trong câu cuối nối những ý nào? | Khác sở thích và cùng giữ sách | Sách mới và sách cũ | Tranh và bút màu | Hai ý có vẻ trái nhau được nối bằng nhưng.
Đại từ em ở câu thứ hai chỉ ai? | Lan | Người đọc bất kì | Cô giáo chưa xuất hiện | Hai câu liên tiếp nói về Lan.
""",
)

add(
    "sentences",
    "simple-compound",
    "Câu đơn, câu ghép và quan hệ giữa vế",
    "Câu ghép có từ hai cụm chủ ngữ–vị ngữ tạo thành các vế, mỗi vế diễn đạt một ý. Dấu phẩy hoặc kết từ giúp nối vế. Không đếm số động từ một cách máy móc để kết luận là câu ghép.",
    "Trời tạnh mưa, sân trường sáng hơn. Lan và Minh cùng lau bàn. Vì gió mạnh nên cửa sổ được đóng lại. Những chiếc lá rơi chậm trên lối đi.",
    "Trong câu đầu có vế trời tạnh mưa và vế sân trường sáng hơn; Lan và Minh là một nhóm chủ ngữ.",
    """
Câu nào có hai vế rõ trong ngữ liệu? | Trời tạnh mưa, sân trường sáng hơn | Những chiếc lá rơi chậm trên lối đi | Lan và Minh cùng lau bàn | Câu đầu có hai cụm chủ ngữ–vị ngữ.
Chủ ngữ ở vế sân trường sáng hơn? | Sân trường | Sáng hơn | Mưa | Sân trường là đối tượng được nói đến trong vế.
Vì... nên... thể hiện quan hệ gì? | Nguyên nhân và kết quả | Tăng dần số lượng | So sánh hai đồ vật | Gió mạnh dẫn đến việc đóng cửa sổ.
Lan và Minh cùng lau bàn là câu đơn vì sao? | Một nhóm chủ ngữ cùng một vị ngữ | Có hai tên nên luôn là hai vế | Có từ cùng nên không phải câu | Câu có một cụm chủ ngữ–vị ngữ, dù chủ ngữ gồm hai người.
""",
)

add(
    "writing",
    "describe-scenery",
    "Lập dàn ý và tả phong cảnh",
    "Quan sát theo một trật tự như từ xa đến gần hoặc theo thời gian. Chọn chi tiết nhìn, nghe, ngửi được; dùng so sánh, nhân hóa phù hợp. Bài có mở đầu, phần tả chính và cảm xúc ở cuối.",
    SCENERY,
    "Chi tiết cụ thể làm cảnh hiện lên rõ hơn việc chỉ nói đẹp. Không cần dùng thật nhiều từ hoa mĩ.",
    """
Đối tượng được tả là gì? | Sân trường sau mưa | Một khu rừng xa | Một chợ đêm | Nhan đề và các đoạn cùng nói sân trường sau mưa.
Người viết bắt đầu quan sát từ đâu? | Từ cổng nhìn vào | Từ đỉnh núi | Từ một chuyến xe | Đoạn đầu nêu rõ từ cổng nhìn vào.
Chi tiết dùng thính giác? | Tiếng chổi đi đều trên lối nhỏ | Gạch đỏ | Màu vàng chen tím | Tiếng chổi là âm thanh nghe được.
Đoạn cuối có tác dụng gì? | Nêu cảm xúc và ý thức giữ sân sạch | Giới thiệu một nhân vật mới | Chỉ liệt kê giá đồ dùng | Đoạn cuối nói em thích cảnh và muốn giữ sân sạch.
""",
    ["Lập dàn ý ba phần rồi viết một đoạn tả cảnh em quan sát, dùng dữ kiện thật."],
)

add(
    "writing",
    "describe-person",
    "Tả người bằng hành động và chi tiết",
    "Tả người chọn nét ngoại hình tiêu biểu, kết hợp hoạt động hoặc lời nói để thể hiện tính cách. Không chỉ liệt kê hình dáng; một hành động có thể giúp người đọc hiểu sự kiên nhẫn hay quan tâm.",
    PERSON,
    "Nhận xét về tính cách cần gắn với một việc làm hoặc lời nói cụ thể.",
    """
Nhân vật chính làm công việc gì? | Phụ trách thư viện | Lái xe buýt | Bán đồ chơi | Đoạn đầu giới thiệu cô Hạnh phụ trách thư viện.
Chi tiết ngoại hình nào có trong bài? | Đôi kính mảnh và tóc buộc gọn | Áo choàng bạc | Mái tóc xanh | Hai nét này được nêu ở đoạn đầu.
Việc cô không kể hộ nội dung cho thấy gì? | Cô khuyến khích học sinh tự suy nghĩ | Cô không cho mượn sách | Cô luôn bỏ qua câu hỏi | Cô hỏi chi tiết và hướng dẫn đọc lại để em tự tìm được ý.
Kết bài thể hiện điều gì? | Tình cảm quý mến và mong giữ sách cẩn thận | Một phép tính về số sách | Chỉ một danh sách tên người | Đoạn cuối nói em quý cô và muốn giữ sách như cô.
""",
    ["Viết đoạn tả một người em quý, kèm hành động cụ thể thể hiện tính cách."],
)

add(
    "reading",
    "rain-information",
    "Đọc văn bản giải thích: Vì sao có mưa?",
    "Văn bản giải thích cho biết một hiện tượng diễn ra thế nào. Theo dõi quan hệ nguyên nhân, quá trình và kết quả; nhan đề giúp xác định đề tài. Có thể ghi các ý chính thành sơ đồ bằng lời.",
    RAIN,
    "Tóm tắt một quá trình cần giữ đúng thứ tự và các mối liên hệ, không chỉ chép một câu.",
    """
Đề tài chính của văn bản? | Quá trình tạo mưa và vòng tuần hoàn nước | Cách sửa mái nhà | Mùa thi của học sinh | Nhan đề và các đoạn giải thích nước chuyển dạng, tạo mây, mưa.
Điều gì khiến một phần nước chuyển thành hơi? | Nhận nhiệt từ Mặt Trời | Được bỏ vào giỏ sách | Có tiếng trống trường | Đoạn đầu nêu tác động của nhiệt Mặt Trời.
Mây trong bài được giải thích thế nào? | Tập hợp nhiều giọt nhỏ hoặc tinh thể băng | Một túi lớn đựng nước | Một tấm gỗ trên trời | Đoạn hai nói rõ thành phần của mây.
Khi nào giọt nước rơi tạo mưa? | Khi kết hợp và đủ lớn | Khi được đặt lên bàn | Khi trở thành cây xanh | Văn bản nêu các giọt kết hợp và lớn lên rồi rơi xuống.
Sau mưa, nước có thể đi đâu? | Vào sông, đất hoặc được cây sử dụng | Chỉ đứng yên trong mây | Biến mất hoàn toàn ngay lập tức | Đoạn ba liệt kê nhiều đường đi của nước.
Đoạn cuối liên hệ với việc nào? | Giữ nguồn nước sạch và tiết kiệm | Mua một chiếc ô đắt nhất | Ngừng quan sát thiên nhiên | Đoạn cuối nêu bỏ rác đúng nơi và tiết kiệm nước.
""",
)

add(
    "reading",
    "garden-poem",
    "Đọc thơ: hình ảnh, so sánh và nhân hóa",
    "Chú ý hình ảnh, cách nói gợi cảm và nhịp thơ. So sánh có thể dùng từ như; nhân hóa gán cách gọi hoặc hành động của người cho vật. Hiểu tác dụng trong cả bài, không chỉ tìm tên biện pháp.",
    POEM,
    "Cách nói đất uống giúp việc tưới cây trở nên gần gũi; bài thơ gợi sự chăm chút và kiên nhẫn.",
    """
Hình ảnh nào có biện pháp so sánh? | Lấp lánh như món quà | Một chiếc lá mới non | Góc vườn tuy bé xíu | Từ như nối giọt sương với hình ảnh món quà.
Đất uống từng ngụm là cách nói gì? | Nhân hóa | Một số đo vận tốc | Tên riêng địa lí | Đất được gán hành động uống như người.
Người viết chăm cây bằng gì? | Gáo nhỏ | Xe tải | Một chiếc trống | Khổ hai nêu em tưới bằng gáo nhỏ.
Chi tiết nào cho biết có quan sát và ghi lại? | Chiều về em ghi lại một chiếc lá mới non | Em đóng cửa và bỏ vườn | Em không nhìn cây | Khổ bốn nêu ghi lại sự thay đổi của cây.
Tình cảm chính trong bài? | Yêu góc vườn và học kiên nhẫn | Muốn phá cây để xây nhà | Chê mọi việc nhỏ | Các khổ cuối nói chăm chút, lớn từng ngày và trưởng thành.
Nắng ghé xuống thềm làm hình ảnh thế nào? | Gần gũi như một vị khách | Trở thành một vật để cân | Mất hết ý nghĩa | Cách nói ghé gợi hành động thân quen của người.
""",
)

add(
    "vocabulary",
    "dictionary-han-viet",
    "Tra từ điển và hiểu yếu tố Hán Việt",
    "Tra từ cần tìm đúng mục từ, đọc nghĩa rồi đối chiếu ví dụ với câu đang dùng. Một yếu tố Hán Việt quen giúp đoán nghĩa nhưng vẫn cần kiểm tra ngữ cảnh.",
    "Phiếu từ: thiên nhiên — thế giới tự nhiên quanh con người; hữu nghị — quan hệ thân thiện giữa các bên; độc lập — tự chủ, không phụ thuộc. Lan tra mục từ trước khi viết: Các bạn cùng giữ gìn thiên nhiên và xây dựng tình hữu nghị.",
    "Tra cứu để dùng từ đúng, không chọn nghĩa đầu tiên một cách máy móc.",
    """
Thiên nhiên trong phiếu chỉ gì? | Thế giới tự nhiên | Chỉ một người bạn | Một chiếc thước | Phiếu nêu nghĩa rõ của mục từ.
Hữu nghị phù hợp với cụm nào? | Quan hệ thân thiện | Chiều dài cuốn vở | Tiếng chuông báo giờ | Hữu nghị nói về quan hệ thân thiện giữa các bên.
Độc lập trong phiếu có nghĩa gì? | Tự chủ, không phụ thuộc | Luôn làm theo mọi người | Chỉ đứng một chân | Dựa vào nghĩa đã cho, không dựa vào tách chữ tùy ý.
Muốn tra một từ, trước tiên tìm gì? | Đúng mục từ | Đáp án mình muốn | Giá bìa của sách | Cần xác định đúng mục từ để đọc nghĩa phù hợp.
Sau khi đọc nghĩa, cần làm gì? | Đối chiếu câu và ví dụ | Dùng ngay ở mọi câu | Bỏ qua ngữ cảnh | Một từ có thể có nhiều nghĩa hoặc sắc thái.
Câu Lan viết dùng hữu nghị để nói điều gì? | Tình thân thiện giữa các bạn | Thời tiết mưa | Số trang sách | Ngữ cảnh xây dựng tình hữu nghị nói về quan hệ giữa người.
""",
)

add(
    "sentences",
    "sentence-links",
    "Liên kết câu bằng lặp, thay thế và nối",
    "Các câu trong đoạn cùng phát triển một ý. Có thể lặp từ khóa, dùng đại từ hoặc từ đồng nghĩa để thay thế, dùng từ nối để cho thấy quan hệ. Thay thế cần rõ đối tượng, tránh đại từ mơ hồ.",
    "Lan đặt cuốn sách lên bàn. Cuốn sách có một trang bị gấp. Em vuốt nhẹ trang giấy rồi kẹp lại ngay ngắn. Sau đó, Lan ghi ngày trả vào sổ để không quên.",
    "Liên kết giúp người đọc theo dõi cùng người và cùng việc qua nhiều câu.",
    """
Từ ngữ được lặp giữa hai câu đầu? | Cuốn sách | Ngày trả | Cửa sổ | Cụm cuốn sách xuất hiện ở cả hai câu.
Em ở câu thứ ba chỉ ai? | Lan | Cuốn sách | Trang giấy | Chủ thể xuyên suốt đoạn là Lan.
Sau đó biểu thị quan hệ gì? | Trình tự thời gian | Giá sách | Độ dài trang | Từ nối báo một việc diễn ra tiếp theo.
Chủ đề chung của đoạn? | Lan giữ sách và nhớ ngày trả | Lan mua xe mới | Các mùa trong năm | Các câu đều nói việc sử dụng, giữ và trả sách.
Vì sao không nên thay em bằng họ ở câu ba? | Làm sai số người và đối tượng | Làm câu có thêm dấu phẩy | Làm trang giấy đổi màu | Đoạn chỉ nói Lan, đại từ họ không phù hợp.
Câu cuối giúp bổ sung ý nào? | Trách nhiệm trả sách đúng hẹn | Cách chế tạo giấy | Một sự việc không liên quan | Ghi ngày trả liên quan việc dùng sách có trách nhiệm.
""",
)

add(
    "spelling",
    "names-hyphen-dash",
    "Tên nước ngoài, gạch nối và gạch ngang",
    "Khi viết tên nước ngoài phiên âm, đối chiếu dạng tên trong tài liệu. Gạch nối trong một tên khác gạch ngang để chú thích giữa câu. Không tự thay mọi dấu gạch cho nhau.",
    "Phiếu tên trong bài: An-đéc-xen; Pa-ri. Câu mẫu: Cô Hạnh — người phụ trách thư viện — giới thiệu truyện mới. Trong phiếu, các tiếng của tên phiên âm nối bằng gạch nối; phần người phụ trách thư viện là lời chú thích.",
    "Bài này dùng đúng dạng tên đã cho; khi gặp tên khác cần tra tài liệu đáng tin cậy.",
    """
Dạng tên nào đúng theo phiếu? | An-đéc-xen | an đéc Xen | Anđécxen | Phiếu đưa dạng phiên âm cần đối chiếu.
Tên địa lí nào có trong phiếu? | Pa-ri | Lan | Cô Hạnh | Pa-ri là tên địa lí được dùng làm ví dụ.
Gạch nối trong An-đéc-xen làm gì? | Nối các tiếng của tên phiên âm | Đánh dấu lời chú thích của câu | Ghi một phép chia | Phân biệt gạch nối của tên và gạch ngang trong câu mẫu.
Phần nào được chú thích bằng gạch ngang? | Người phụ trách thư viện | Truyện mới | Phiếu tên | Cụm giữa hai gạch ngang giải thích cô Hạnh là ai.
Bỏ lời chú thích, câu còn ý chính nào? | Cô Hạnh giới thiệu truyện mới | Pa-ri là người phụ trách | Cô Hạnh không đọc sách | Bộ phận chú thích có thể bỏ mà giữ ý chính của câu.
Khi chưa biết cách viết tên khác, nên làm gì? | Tra tài liệu và đối chiếu | Tự bỏ mọi dấu gạch | Viết hoa mọi chữ cái | Cần tra cứu thay vì suy đoán tùy ý.
""",
)

add(
    "speaking",
    "listen-and-note",
    "Nghe, ghi ý chính và nói có mục đích",
    "Trước khi nghe, xác định thông tin cần ghi. Ghi từ khóa thay vì cố chép từng tiếng. Khi nói, dùng âm lượng, tốc độ và cách diễn đạt phù hợp người nghe; có thể dùng phiếu hỗ trợ.",
    "Lời trao đổi để người hướng dẫn đọc: Cô nhắc nhóm chuẩn bị góc đọc vào thứ sáu. An phụ trách chọn sách, Minh chuẩn bị nhãn, Lan ghi danh sách. Các bạn sẽ báo cáo ba việc đã làm và một việc còn cần hỗ trợ. Khi bạn trình bày, nhóm nghe hết rồi hỏi thêm.",
    "Phần này luyện cùng người hướng dẫn; đọc chữ trên màn hình chưa thay thế việc đánh giá nghe/nói.",
    """
Nhóm chuẩn bị việc gì? | Góc đọc | Một cuộc đua xe | Dọn cả thành phố | Nội dung lời trao đổi tập trung chuẩn bị góc đọc.
An phụ trách việc gì? | Chọn sách | Chuẩn bị nhãn | Ghi danh sách | Lời trao đổi chia nhiệm vụ rõ từng bạn.
Nhóm sẽ báo cáo gì? | Ba việc đã làm và một việc cần hỗ trợ | Chỉ tên người nhanh nhất | Tất cả mật khẩu | Yêu cầu báo cáo nêu rõ hai nhóm thông tin.
Ghi chép hiệu quả nên ưu tiên gì? | Việc, người phụ trách, thời điểm | Mọi tiếng kể cả lời ngập ngừng | Chỉ màu áo người nói | Từ khóa giúp giữ thông tin cần dùng.
Khi bạn đang nói, nhóm nên làm gì? | Nghe hết rồi hỏi thêm | Cắt ngang mỗi câu | Nói chuyện khác thật lớn | Đây là quy tắc nghe và nói theo lượt trong ngữ liệu.
Đọc đoạn này đã đủ kiểm tra nghe chưa? | Chưa, cần thực hành với người đọc hướng dẫn | Có, luôn tương đương nghe thật | Có, dù không nghe gì | Luyện đọc là hỗ trợ, không phải bản thu hoặc kiểm tra nghe.
""",
    ["Nhờ người hướng dẫn đọc lời trao đổi, ghi 3 từ khóa rồi nói lại nhiệm vụ."],
)

add(
    "writing",
    "activity-report",
    "Viết báo cáo và chương trình hoạt động",
    "Báo cáo nêu việc, kết quả và điều cần tiếp tục. Chương trình hoạt động cho biết thời gian, việc làm, người phụ trách. Bảng biểu phải có tiêu đề cột rõ, số liệu phù hợp nội dung.",
    "BÁO CÁO GÓC ĐỌC: Nhóm đã kiểm tra 24 cuốn; 20 cuốn có nhãn, 4 cuốn cần dán nhãn. Kế hoạch thứ sáu: 8:00 chọn sách — An; 8:15 dán nhãn — Minh; 8:30 xếp sách — cả nhóm. Lan tổng hợp kết quả cuối buổi.",
    "Tách kết quả đã làm với kế hoạch sẽ làm; không ghi dự định như việc đã hoàn thành.",
    """
Nhóm đã kiểm tra bao nhiêu cuốn? | 24 | 20 | 4 | Báo cáo nêu tổng 24 cuốn.
Việc nào chưa xong theo báo cáo? | Dán nhãn 4 cuốn | Kiểm tra toàn bộ 24 cuốn | Viết tên nhóm | Có 4 cuốn cần dán nhãn, chưa phải kết quả hoàn thành.
Ai dán nhãn lúc 8:15? | Minh | An | Lan | Kế hoạch ghi việc và người cùng thời điểm.
8:30 là thời điểm nào? | Xếp sách | Chọn sách | Tổng kết cuối ngày | Dòng 8:30 ghi xếp sách.
Đâu là kết quả đã làm? | 20 cuốn có nhãn | Cả nhóm sẽ xếp sách | An sẽ chọn sách | Báo cáo và chương trình có mốc thời gian khác nhau.
Một bảng kế hoạch cần cột nào? | Thời gian, việc làm, phụ trách | Chỉ số thứ tự | Chỉ màu nền | Ba cột giúp theo dõi hoạt động và trách nhiệm.
""",
    ["Viết bảng kế hoạch một việc học tập với thời gian, việc làm và người phụ trách."],
)

add(
    "reading",
    "evidence-inference",
    "Tư duy: nội dung hàm ẩn và bằng chứng",
    "Suy luận đơn giản cần dựa trên chi tiết, không thêm việc truyện không nói. Ghép lời nói và hành động để hiểu nhân vật; phân biệt một khả năng hợp lí với một kết luận chắc chắn.",
    UMBRELLA,
    "Có thể suy ra Minh biết quan tâm người khác; không thể suy ra chiếc ô rất đắt chỉ từ màu ô.",
    """
Minh nghiêng ô về phía An cho thấy điều gì? | Minh ưu tiên giữ vở và bạn khỏi ướt | Minh muốn làm bạn ướt hơn | Minh không biết trời mưa | Hành động nghiêng ô hợp với việc giúp An che vở.
An nhận ra vai Minh ướt rồi đổi chỗ cho thấy gì? | Sự quan tâm qua lại | An không muốn đi cùng nữa | An định bỏ ô | Lời đề nghị cùng giữ ô cho thấy bạn quan tâm Minh.
Kết luận nào thiếu bằng chứng? | Chiếc ô chắc rất đắt | An quên áo mưa | Minh đưa em nhỏ qua đoạn đường | Truyện không nói giá ô, còn hai việc kia được nêu.
Vì sao hai bạn bước chậm? | Tránh nước bắn vào người khác | Muốn lỡ chuyến xe bằng mọi giá | Muốn làm ông lo | Truyện nêu rõ lí do bước chậm.
Chiếc ô che nhiều hơn em tưởng gợi ý gì? | Sự sẻ chia giúp giảm nỗi lo | Ô tự lớn ra thành mái nhà | Chiếc ô tạo ra xe buýt | Câu cuối nói che cả nỗi lo, là ý nghĩa tinh thần.
Chi tiết nào cho thấy Minh cũng có việc riêng? | Muốn về giúp ông tưới cây | Muốn mua vé máy bay | Định mở cửa hàng | Đoạn đầu nêu dự định về sớm giúp ông.
Thái độ của ông dựa vào chi tiết nào? | Hỏi chuyện rồi bảo cháu thay áo khô | Phạt cháu không được đọc sách | Không cho cháu vào nhà | Đây là hành động chăm sóc có trong truyện.
Cách giải thích tốt nhất cần điều gì? | Nêu nhận xét kèm chi tiết của truyện | Chỉ đoán theo điều mình thích | Chọn câu dài nhất | Bằng chứng giúp suy luận có căn cứ.
""",
)

add(
    "vocabulary",
    "precise-word-choice",
    "Tư duy: sắc thái từ và câu văn chính xác",
    "Chọn từ theo sự vật và cảm xúc cần thể hiện. Từ gần nghĩa có thể khác mức độ, cách dùng; đặt vào câu để kiểm tra. Không dùng từ mạnh hơn dữ kiện chỉ để câu nghe hay.",
    "Buổi sáng, dòng suối róc rách bên vườn. Cô Hạnh nhắc nhóm giữ bàn gọn gàng. Một bạn lỡ làm rơi sách, cô nhẹ nhàng giúp bạn nhặt lên. Cả nhóm chăm chú nghe hướng dẫn rồi cẩn thận dán từng nhãn.",
    "Róc rách tả tiếng nước chảy nhỏ; chăm chú gợi tập trung, cẩn thận gợi chú ý tránh sai sót.",
    """
Từ róc rách gợi âm thanh nào? | Nước chảy nhỏ | Sấm nổ rất lớn | Tiếng xe hú | Ngữ cảnh dòng suối và sắc thái từ gợi tiếng nước nhỏ.
Chăm chú trong bài nói điều gì? | Tập trung nghe | Ngủ quên | Chạy thật nhanh | Nhóm chú ý vào hướng dẫn.
Cẩn thận khi dán nhãn nghĩa gì? | Chú ý tránh sai sót | Làm cho thật ồn | Cố tình dán lệch | Cách làm đòi hỏi chú ý để nhãn đúng vị trí.
Nhẹ nhàng giúp bạn cho thấy thái độ nào? | Bình tĩnh, quan tâm | Giận dữ, xua đuổi | Vội kết luận bạn xấu | Ngữ liệu nêu giúp bạn nhặt sách với thái độ nhẹ nhàng.
Thay róc rách bằng ầm ầm có phù hợp không? | Không, làm đổi mức độ âm thanh | Có, hai từ luôn giống hệt | Có, vì đều có hai tiếng | Hai từ khác sắc thái và mức độ âm thanh.
Từ nào hợp với bàn đã sắp đúng chỗ? | Gọn gàng | Mênh mông | Róc rách | Gọn gàng phù hợp cách sắp đồ trên bàn.
Vì sao không gọi bạn làm rơi sách là phá hoại? | Chỉ là việc lỡ tay, chưa có bằng chứng cố ý | Vì mọi việc đều được bỏ qua | Vì từ ấy dài hơn | Không dùng từ đánh giá nặng hơn dữ kiện.
Muốn chọn từ đúng, cần đối chiếu gì? | Ngữ cảnh và ý muốn nói | Chỉ số chữ của từ | Chỉ vần cuối | Nghĩa và sắc thái phải phù hợp câu.
""",
)

add(
    "sentences",
    "connector-reasoning",
    "Tư duy: nối vế và dùng dấu để giữ ý",
    "Kết từ phải thể hiện đúng quan hệ giữa hai ý. Vì... nên... nêu nguyên nhân–kết quả; tuy... nhưng... nêu sự đối lập. Dấu gạch ngang có thể bao phần chú thích, không làm mất ý chính.",
    "Vì trời mưa nên nhóm chuyển hoạt động vào thư viện. Tuy phòng nhỏ nhưng các bạn vẫn có chỗ đọc. Cô Hạnh — người phụ trách thư viện — sắp thêm ghế. Nhóm giữ trật tự và cùng dọn bàn sau buổi đọc.",
    "Đừng đổi kết từ nếu làm đổi quan hệ; lời chú thích giải thích thêm một thành phần của câu.",
    """
Nguyên nhân chuyển hoạt động là gì? | Trời mưa | Phòng nhỏ | Có thêm ghế | Cặp vì... nên... nêu trời mưa dẫn đến chuyển hoạt động.
Tuy... nhưng... nối quan hệ nào? | Đối lập giữa phòng nhỏ và vẫn có chỗ | Hai mức giá sách | Thứ tự ba ngày | Sự việc sau xảy ra dù có điều kiện tưởng như cản trở.
Phần chú thích giải thích ai? | Cô Hạnh | Nhóm giữ trật tự | Những chiếc ghế | Cụm người phụ trách thư viện giải thích cô Hạnh.
Bỏ chú thích, ý chính là gì? | Cô Hạnh sắp thêm ghế | Phòng nhỏ không có chỗ | Trời mưa vì có ghế | Bỏ phần giữa gạch ngang vẫn giữ chủ ngữ và vị ngữ chính.
Và ở câu cuối nối điều gì? | Hai việc nhóm cùng thực hiện | Nguyên nhân trời mưa | Một lời chú thích tên cô | Giữ trật tự và dọn bàn là hai việc thêm vào nhau.
Đổi vì thành tuy trong câu đầu có giữ đúng quan hệ không? | Không, làm đổi quan hệ đã nêu | Có, mọi kết từ đều giống nhau | Có, nếu viết hoa | Quan hệ nguyên nhân khác quan hệ nhượng bộ, đối lập.
Cụm nào là vị ngữ của Cô Hạnh khi bỏ chú thích? | Sắp thêm ghế | Người phụ trách thư viện | Tuy phòng nhỏ | Vị ngữ nêu hành động của cô.
Cách sửa dấu phù hợp nhất cần gì? | Giữ nghĩa và ranh giới các phần câu | Thêm dấu sau mọi tiếng | Xóa hết kết từ | Sửa dấu phải giúp rõ ý, không thay nội dung tùy ý.
""",
)

add(
    "writing",
    "opinion-and-reason",
    "Tư duy: nêu ý kiến có lí do và ví dụ",
    "Một đoạn nêu ý kiến cần nói rõ đồng ý hay không, đưa lí do phù hợp và ví dụ. Lí do liên quan trực tiếp ý kiến, không chỉ nói ai cũng làm thế. Có thể tôn trọng ý khác khi trao đổi.",
    "Em đồng ý mở góc đổi sách trong lớp. Khi đổi những cuốn đã đọc, các bạn có thêm lựa chọn mà không phải mua ngay. Chẳng hạn, em có thể cho bạn mượn truyện về cây và mượn sách về biển. Tuy nhiên, nhóm cần ghi người mượn và ngày trả để giữ sách cẩn thận. Em mong mọi bạn cùng có trách nhiệm với góc sách.",
    "Ý kiến, lí do, ví dụ và điều kiện cần thực hiện là những phần khác nhau của một lập luận.",
    """
Ý kiến chính là gì? | Đồng ý mở góc đổi sách | Muốn đóng thư viện | Chỉ thích sách về biển | Câu đầu nêu rõ quan điểm về việc mở góc đổi sách.
Lí do nào được nêu? | Có thêm lựa chọn mà chưa phải mua ngay | Vì mọi sách đều có cùng số trang | Vì không cần giữ sách | Lí do liên quan lợi ích của đổi sách.
Ví dụ cụ thể nào có trong đoạn? | Đổi truyện về cây để mượn sách về biển | Mua một chiếc xe | Chỉ đọc một trang mỗi năm | Ví dụ làm rõ cách góc đổi sách hoạt động.
Tuy nhiên chuyển sang ý nào? | Điều kiện quản lí mượn và trả | Một thời tiết mới | Đổi hết chủ đề | Tác giả bổ sung điều cần chú ý để hoạt động có trách nhiệm.
Ghi người mượn, ngày trả nhằm gì? | Giữ và quản lí sách cẩn thận | Xếp hạng ai giàu hơn | Làm mất quyền đọc | Ngữ liệu nêu rõ mục đích giữ sách.
Lí do vì ai cũng làm thế có đủ thuyết phục không? | Chưa đủ, cần lí do liên quan việc đang bàn | Luôn đủ cho mọi ý kiến | Tốt hơn mọi bằng chứng | Cần giải thích lợi ích, tác động hoặc điều kiện cụ thể.
Kết đoạn thể hiện mong muốn nào? | Mọi bạn có trách nhiệm | Mọi bạn bỏ việc ghi chép | Chỉ một bạn được đọc | Câu cuối nhấn mạnh trách nhiệm chung.
Khi bạn có ý khác, nên làm gì? | Nghe lí do và trao đổi lịch sự | Cắt lời ngay lập tức | Chê bạn không biết đọc | Trao đổi cần tôn trọng và tập trung vào vấn đề.
""",
    ["Viết 5–7 câu nêu ý kiến về một việc ở lớp, có lí do và một ví dụ."],
)

add(
    "writing",
    "creative-ending",
    "Tư duy: viết kết thúc khác có căn cứ",
    "Kết thúc sáng tạo có thể đổi một sự việc nhưng phải hợp nhân vật, bối cảnh và những chi tiết đã có. Lập dàn ý ngắn trước khi viết; kiểm tra kết thúc có giải quyết việc chính không.",
    SEEDLING,
    "Sáng tạo không có nghĩa bỏ mọi dữ kiện của truyện hoặc đưa một việc không liên quan vào cuối.",
    """
Kết thúc mới nào hợp bối cảnh nhất? | Nhóm tặng cây cho góc đọc và tiếp tục ghi nhật kí | Cây biến thành tàu vũ trụ không được báo trước | Nhóm quên toàn bộ việc chăm cây | Việc tặng cây và tiếp tục quan sát nối với hoạt động đã có.
Chi tiết nào nên giữ để kết nối truyện? | Cuốn nhật kí của Lan | Giá chiếc xe không xuất hiện | Một nhân vật chưa được giới thiệu | Nhật kí là chi tiết quan trọng xuyên suốt.
Trước khi viết, nên làm gì? | Lập ý và chọn kết thúc phù hợp | Chép mọi câu đã có | Bỏ qua nhân vật | Quy trình viết bắt đầu từ mục đích và ý chính.
Kết thúc cần giải quyết việc nào? | Việc chăm cây và điều nhóm học được | Một cuộc thi chưa từng nhắc | Giá sách ở cửa hàng | Đây là vấn đề chính của truyện.
Một câu nối phù hợp cần gì? | Cho thấy sự việc mới tiếp tục sau quan sát cây | Đổi tên Lan thành mọi nhân vật | Dùng thật nhiều dấu chấm than | Câu nối cần giữ quan hệ sự việc và mạch kể.
Khi soát bản viết, ưu tiên điều gì? | Mạch kể, dùng từ, dấu câu và sự phù hợp | Chỉ đếm chữ cái đầu | Chỉ dùng từ khó | Chỉnh sửa cả ý và cách diễn đạt.
""",
    ["Viết kết thúc khác 5–7 câu cho Mầm cây bên cửa, giữ chi tiết nhật kí."],
)

add(
    "reading",
    "advertisement-information",
    "Tư duy: đọc chương trình và quảng cáo",
    "Văn bản quảng cáo có mục đích thu hút; chương trình cho biết hoạt động cụ thể. Phân biệt thông tin kiểm tra được với lời giới thiệu cảm tính. Đọc ngày, giờ, điều kiện tham gia trước khi kết luận.",
    "ÁP PHÍCH GÓC SÁCH: Thứ sáu, 14:00–15:00 tại thư viện. Mang một cuốn sách còn sạch để đổi; đăng kí với cô phụ trách trước buổi sáng. Dòng giới thiệu: Một giờ đọc thật thú vị! Chương trình gồm chọn sách, chia sẻ một chi tiết yêu thích và trả góc đọc về trạng thái gọn gàng.",
    "Thời gian và điều kiện là dữ kiện; thú vị là lời giới thiệu, cảm nhận có thể khác nhau.",
    """
Hoạt động diễn ra lúc nào? | Thứ sáu, 14:00–15:00 | Mọi tối trong tháng | Không có thời gian | Áp phích ghi ngày và khoảng giờ cụ thể.
Điều kiện đổi sách là gì? | Mang một cuốn còn sạch | Phải mang đồ chơi mới | Không cần sách | Điều kiện được nêu rõ trong áp phích.
Câu nào là lời giới thiệu cảm tính? | Một giờ đọc thật thú vị | Thứ sáu 14:00–15:00 | Đăng kí với cô phụ trách | Thú vị là nhận xét, khác dữ kiện thời gian hoặc thủ tục.
Việc cuối chương trình là gì? | Dọn góc đọc gọn gàng | Bỏ sách lại sân | Đi mua xe | Chương trình nêu trả góc đọc về trạng thái gọn gàng.
Muốn biết mình có thể tham gia, cần đọc gì? | Thời gian và điều kiện | Chỉ màu áp phích | Chỉ câu hấp dẫn nhất | Cần đối chiếu yêu cầu cụ thể với khả năng tham gia.
Mục đích của áp phích là gì? | Thông báo và thu hút tham gia góc sách | Giải thích cách tạo mưa | Kể lại cả cuộc đời một người | Hình thức áp phích kết hợp thông tin hoạt động và lời mời hấp dẫn.
""",
)

add(
    "writing",
    "revise-paragraph",
    "Tư duy: chỉnh sửa đoạn để rõ chủ đề",
    "Soát đoạn theo thứ tự: ý chính, trật tự câu, liên kết, từ, chính tả và dấu. Câu đúng ngữ pháp vẫn có thể không phù hợp chủ đề. Ghi lí do sửa để học từ bản nháp.",
    "Bản nháp: (1) Nhóm em chuẩn bị góc đọc. (2) An chọn sách và Minh dán nhãn. (3) Chiếc xe đạp của em màu đỏ. (4) Sau đó, các bạn xếp sách lên kệ. (5) Nhờ phân công rõ, góc đọc hoàn thành đúng giờ.",
    "Câu về xe đạp không phát triển chủ đề chuẩn bị góc đọc, nên bỏ hoặc chuyển sang đoạn khác.",
    """
Chủ đề của đoạn? | Chuẩn bị góc đọc | Tả xe đạp | Dự báo thời tiết | Bốn câu cùng hướng vào hoạt động góc đọc.
Câu nào lạc chủ đề? | Câu 3 | Câu 1 | Câu 5 | Màu xe đạp không liên quan việc chuẩn bị góc đọc.
Sau đó ở câu 4 nối với việc nào? | Chọn sách và dán nhãn | Đi xe đạp | Ngủ trưa | Trình tự hoạt động trước là chọn sách và dán nhãn.
Câu 5 có vai trò gì? | Nêu kết quả và lí do hoàn thành đúng giờ | Mở chủ đề xe đạp | Thêm tên người chưa có | Kết câu cho thấy kết quả của phân công rõ.
Cách sửa câu 3 phù hợp nhất? | Bỏ hoặc chuyển sang đoạn tả xe | Thêm thật nhiều dấu phẩy | Đổi đỏ thành xanh là đủ | Cần sửa sự liên quan về ý, không chỉ sửa từ màu.
Một bản soát tốt kiểm tra gì? | Cả ý, liên kết và cách viết | Chỉ chiều dài chữ | Chỉ số dấu chấm | Chỉnh sửa có nhiều lớp, bắt đầu từ chủ đề và ý.
""",
    ["Viết lại bản nháp thành đoạn rõ chủ đề và ghi một lí do em sửa."],
)

add(
    "speaking",
    "respectful-discussion",
    "Tư duy: thảo luận và phản hồi có lí do",
    "Khi trao đổi, nghe trọn ý rồi hỏi hoặc phản hồi. Có thể không đồng ý nhưng vẫn lịch sự: nói rõ ý kiến, lí do và đề nghị. Ghi điểm thống nhất, việc còn khác và nhiệm vụ tiếp theo.",
    "An đề nghị mở góc sách ngay chiều nay. Minh nói: Mình đồng ý có góc sách, nhưng hôm nay nhãn chưa xong. Chúng mình có thể hoàn thiện nhãn rồi mở vào thứ sáu không? Lan ghi hai điểm: cả nhóm muốn mở góc sách; cần chốt thời gian sau khi chuẩn bị đủ. Nhóm phân công Minh dán nhãn và Lan kiểm tra danh sách.",
    "Phản hồi của Minh tập trung vào điều kiện chuẩn bị, không chê người đề nghị.",
    """
Điểm cả nhóm đã thống nhất? | Muốn có góc sách | Muốn bỏ hết sách | Muốn mở mà không chuẩn bị | Lan ghi rõ điểm thống nhất là có góc sách.
Minh chưa đồng ý điều gì? | Mở ngay khi nhãn chưa xong | Việc có góc sách | Việc giữ sách | Minh đồng ý mục tiêu nhưng đề nghị đổi thời gian.
Lí do Minh nêu? | Nhãn chưa xong | Bạn An luôn sai | Trời đã được dự báo mưa | Ngữ liệu có lí do cụ thể về công việc chưa hoàn thành.
Phản hồi nào lịch sự và có căn cứ? | Đề nghị hoàn thiện nhãn rồi mở thứ sáu | Chê An trước cả nhóm | Không nghe và bỏ đi | Minh đưa lí do và một phương án cụ thể.
Lan ghi gì để theo dõi thảo luận? | Điểm thống nhất và điều cần chốt | Chỉ cảm nhận ai nói to | Mọi tiếng không có chọn lọc | Ghi ý chính giúp giữ vấn đề và quyết định.
Việc tiếp theo của Minh? | Dán nhãn | Kiểm tra danh sách | Mua xe mới | Nhóm phân công Minh dán nhãn, Lan kiểm tra danh sách.
""",
    ["Đóng vai thảo luận với người hướng dẫn, nói một ý kiến khác kèm lí do lịch sự."],
)
