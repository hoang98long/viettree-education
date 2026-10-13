"""Original literacy practice: sound/rime/short sentences in grade 1, short texts in grade 2."""

from app.curriculum.grades.early_primary.builders import build, cards


def curriculum(grade):
    items = []

    def add(topic, code, title, teaching, example, hints, sheet, labels=None, thinking=False):
        rows = []
        for line in sheet.strip().splitlines():
            p, a, w, v, why = line.split("|")
            rows.append((p, a, [w, v], why))
        items.append(
            build(
                grade,
                "VIETNAMESE",
                len(items),
                topic,
                code,
                title,
                teaching,
                example,
                "Đọc chậm từng tiếng. Có thể nhờ người lớn đọc mẫu; em chỉ hoặc chọn đáp án.",
                hints,
                rows,
                illustration=cards(labels, "Thẻ chữ và từ của bài; đọc từng thẻ cùng người thân.")
                if labels
                else None,
                thinking=thinking,
            )
        )

    if grade == 1:
        add(
            "letters",
            "a-family",
            "Nhìn và đọc chữ a, ă, â",
            "Nhìn dấu trên chữ để phân biệt a, ă, â. Nhờ người lớn đọc mẫu từng âm.",
            "a – ca; ă – ăn; â – cân.",
            "Nhìn phần trên chữ.|ă có dấu cong, â có dấu mũ.|Đối chiếu với chữ mẫu.",
            """Chữ có dấu mũ là chữ nào?|â|a|ă|â có dấu mũ.
Chữ trong tiếng ca là chữ nào?|a|ă|â|Ca có chữ a.
Chữ trong tiếng ăn là chữ nào?|ă|a|â|Ăn có chữ ă.
Chữ trong tiếng cân là chữ nào?|â|a|ă|Cân có chữ â.""",
            ["a", "ă", "â"],
        )
        add(
            "letters",
            "first-letters",
            "Ghép b, c, m với a",
            "Đọc âm đầu, rồi ghép với a thành một tiếng.",
            "b + a = ba; c + a = ca; m + a = ma.",
            "Nhìn chữ đứng đầu.|Ghép chữ đầu với a.|Nhờ người lớn đọc mẫu rồi đọc lại.",
            """b ghép với a thành tiếng nào?|ba|ca|ma|b và a thành ba.
c ghép với a thành tiếng nào?|ca|ba|ma|c và a thành ca.
m ghép với a thành tiếng nào?|ma|ca|ba|m và a thành ma.
Tiếng ba bắt đầu bằng chữ nào?|b|c|m|Ba có chữ b đứng đầu.""",
            ["ba", "ca", "ma"],
        )
        add(
            "rhymes",
            "an-at",
            "Đọc vần an và at",
            "Đọc a với n thành an, với t thành at. Chú ý chữ cuối.",
            "an: bàn, đàn. at: bát, hát.",
            "Nhìn chữ cuối.|n tạo an; t tạo at.|Đọc lại cả tiếng.",
            """Tiếng bàn có vần nào?|an|at|on|Bàn có vần an.
Tiếng bát có vần nào?|at|an|on|Bát có vần at.
Tiếng đàn có vần nào?|an|at|ot|Đàn có vần an.
Tiếng hát có vần nào?|at|an|on|Hát có vần at.""",
            ["an", "at", "bàn", "bát"],
        )
        add(
            "rhymes",
            "on-ot",
            "Đọc vần on và ot",
            "Nhìn chữ o và chữ cuối. Đọc chậm vần rồi cả tiếng.",
            "on: con, lon. ot: hót, ngọt.",
            "Tìm chữ o.|Nhìn n hay t ở cuối.|Đọc tiếng theo vần vừa tìm.",
            """Tiếng con có vần nào?|on|ot|an|Con có vần on.
Tiếng hót có vần nào?|ot|on|at|Hót có vần ot.
Tiếng lon có vần nào?|on|ot|an|Lon có vần on.
Tiếng ngọt có vần nào?|ot|on|at|Ngọt có vần ot.""",
            ["on", "ot", "con", "hót"],
        )
        add(
            "reading",
            "home",
            "Đọc: bé giúp bà",
            "Đọc từng câu, tìm người và việc được nói rõ.",
            "Bé Na ở nhà với bà. Na lấy cốc nước cho bà. Bà cười và nói: Cảm ơn cháu. Na rất vui.",
            "Tìm tên người.|Đọc câu có việc người đó làm.|Chọn đúng chi tiết trong câu.",
            """Bé tên là gì?|Na|Mai|An|Câu đầu nói bé Na.
Na ở nhà với ai?|Bà|Cô|Bạn|Na ở nhà với bà.
Na lấy gì cho bà?|Cốc nước|Bút|Áo|Na lấy cốc nước.
Bà nói gì?|Cảm ơn cháu|Đi ngủ|Đóng cửa|Bà cảm ơn Na.""",
        )
        add(
            "reading",
            "school",
            "Đọc: chiếc bút của bạn",
            "Tìm tên bạn và đồ vật trong từng câu.",
            "Nam thấy một chiếc bút dưới bàn. Nam đưa bút cho cô. Cô hỏi cả lớp. Lan nhận lại bút và cảm ơn Nam.",
            "Đọc câu đầu.|Tìm ai nhặt và ai nhận bút.|Đọc lại câu có đáp án.",
            """Ai thấy bút?|Nam|Lan|Bà|Nam thấy bút.
Bút ở đâu?|Dưới bàn|Trên cây|Trong sân|Bút dưới bàn.
Nam đưa bút cho ai?|Cô|Bà|Bố|Nam đưa bút cho cô.
Ai nhận lại bút?|Lan|Na|Nam|Lan nhận lại bút.""",
        )
        add(
            "vocabulary",
            "family",
            "Từ chỉ người và đồ vật trong nhà",
            "Đọc từ ngắn. Chỉ vào người hoặc đồ vật tương ứng khi có thể.",
            "Người: bà, mẹ, bé. Đồ vật: bàn, cốc, áo.",
            "Xem đề hỏi người hay vật.|Đối chiếu hai nhóm trong ví dụ.|Chỉ vào vật thật hoặc nói lại từ.",
            """Từ nào chỉ người?|Mẹ|Cốc|Áo|Mẹ là người.
Từ nào chỉ đồ vật?|Bàn|Bà|Mẹ|Bàn là đồ vật.
Từ nào chỉ người nhỏ tuổi?|Bé|Cốc|Bàn|Bé chỉ người nhỏ tuổi.
Vật dùng để uống nước là gì?|Cốc|Áo|Bàn|Cốc dùng uống nước.""",
            ["bà", "mẹ", "bé", "cốc"],
        )
        add(
            "vocabulary",
            "school-words",
            "Từ quen thuộc ở trường",
            "Gọi tên đồ dùng và việc ở lớp. Em không cần học tên loại từ.",
            "Đồ dùng: bút, vở, thước. Việc làm: đọc, viết.",
            "Nhìn đồ vật hoặc việc làm.|Đọc từ trong ví dụ.|Chọn từ đúng với yêu cầu.",
            """Đồ vật dùng để viết là gì?|Bút|Bàn|Cốc|Bút dùng để viết.
Đồ vật có trang giấy để ghi bài là gì?|Vở|Thước|Cốc|Vở có trang giấy.
Từ nào nói một việc làm?|Đọc|Bút|Vở|Đọc là việc làm.
Đồ vật giúp kẻ đường thẳng là gì?|Thước|Cốc|Áo|Thước giúp kẻ đường thẳng.""",
            ["bút", "vở", "thước"],
        )
        add(
            "rhymes",
            "tones",
            "Nhìn dấu thanh trong tiếng",
            "So các tiếng có cùng chữ nhưng khác dấu. Đọc theo người lớn, không đoán theo màu chữ.",
            "ma, má, mà, mả, mã, mạ có dấu thanh khác nhau.",
            "Nhìn dấu trên hoặc dưới tiếng.|Sắc là nét nghiêng lên; nặng là chấm dưới.|Đọc lại cùng người lớn.",
            """Tiếng nào có dấu sắc?|má|ma|mà|Má có dấu sắc.
Tiếng nào có dấu huyền?|mà|má|ma|Mà có dấu huyền.
Tiếng nào có dấu nặng?|mạ|má|mã|Mạ có chấm dưới.
Tiếng nào không có dấu thanh?|ma|má|mạ|Ma không có dấu thanh.
Tiếng nào có dấu hỏi?|mả|mã|má|Mả có dấu hỏi.
Tiếng nào có dấu ngã?|mã|mả|mà|Mã có dấu ngã.""",
            ["ma", "má", "mà", "mả", "mã", "mạ"],
        )
        add(
            "writing",
            "c-k",
            "Viết c hoặc k trong tiếng quen",
            "Trước e, ê, i thường viết k. Với a, o, u trong bài này viết c.",
            "ca, co, cu; kê, kì, ke.",
            "Nhìn chữ đứng sau chỗ trống.|e, ê, i đi với k.|Đọc cả tiếng để kiểm tra.",
            """Chọn tiếng viết đúng.|ca|ka|qa|Ca viết c trước a.
Chọn tiếng viết đúng.|kê|cê|qê|Kê viết k trước ê.
Chọn tiếng viết đúng.|co|ko|qo|Co viết c trước o.
Chọn tiếng viết đúng.|kì|cì|qì|Kì viết k trước i.
Chọn tiếng viết đúng.|cu|ku|quu|Cu viết c trước u.
Chữ đầu trong kê là gì?|k|c|m|Kê bắt đầu bằng k.""",
            ["c", "k", "ca", "kê"],
        )
        add(
            "writing",
            "g-ng",
            "Viết g, gh, ng và ngh",
            "Trước e, ê, i dùng gh hoặc ngh. Các tiếng ga, ngô dùng g hoặc ng.",
            "ga, ghế; ngô, nghe.",
            "Nhìn chữ ngay sau âm đầu.|e, ê, i đi với gh hoặc ngh.|Đối chiếu từ mẫu, không bỏ h.",
            """Chọn từ viết đúng.|ghế|gế|gghế|Ghế có gh trước ê.
Chọn từ viết đúng.|ga|gha|ggha|Ga dùng g trước a.
Chọn từ viết đúng.|nghe|nge|nghhe|Nghe dùng ngh trước e.
Chọn từ viết đúng.|ngô|nghô|nggô|Ngô dùng ng trước ô.
Từ ghế có h sau chữ nào?|g|n|c|Gh là g và h.
Từ nghe bắt đầu bằng nhóm chữ nào?|ngh|ng|gh|Nghe bắt đầu bằng ngh.""",
            ["ga", "ghế", "ngô", "nghe"],
        )
        add(
            "writing",
            "stops",
            "Dấu chấm và dấu hỏi",
            "Câu kể kết thúc bằng dấu chấm. Câu hỏi kết thúc bằng dấu hỏi.",
            "Na đọc sách. Bạn đọc sách gì?",
            "Đọc ý câu.|Câu hỏi điều gì dùng dấu hỏi.|Đọc lại câu với dấu vừa chọn.",
            """Câu Na đọc sách kết thúc bằng dấu nào?|Dấu chấm|Dấu hỏi|Dấu phẩy|Đây là câu kể.
Câu Bạn tên gì kết thúc bằng dấu nào?|Dấu hỏi|Dấu chấm|Dấu phẩy|Đây là câu hỏi.
Câu nào là câu hỏi?|Bạn đi đâu?|Em đi học.|Na đọc sách.|Bạn đi đâu hỏi một điều.
Câu nào kể một việc?|Na đọc sách.|Bạn tên gì?|Bạn ở đâu?|Câu kể việc Na đọc sách.
Dấu ? dùng ở cuối câu nào?|Bạn thích gì?|Em có bút.|Bà uống nước.|Câu này hỏi sở thích.
Dấu . dùng ở cuối câu nào?|Em đi học.|Bạn tên gì?|Bạn đi đâu?|Em đi học là câu kể.""",
        )
        add(
            "writing",
            "capitals",
            "Viết hoa đầu câu và tên",
            "Chữ đầu câu và chữ đầu tên người viết hoa. Đọc lại câu để kiểm tra.",
            "Na đọc sách. Em chào bà.",
            "Tìm chữ đầu câu.|Tìm tên người.|Viết hoa đúng chữ, giữ các chữ còn lại.",
            """Chọn câu đúng.|Na đọc sách.|na đọc sách.|Na Đọc Sách.|Viết hoa Na ở đầu câu.
Chọn câu đúng.|Em chào bà.|em chào bà.|Em Chào Bà.|Viết hoa chữ đầu câu Em.
Tên nào được viết hoa đúng?|Lan|lan|lAn|Lan viết hoa chữ L.
Tên nào được viết hoa đúng?|Nam|nam|nAm|Nam viết hoa chữ N.
Chữ nào trong Em đi học viết hoa?|E|h|i|E là chữ đầu câu.
Chọn câu đúng.|Bé Na vui.|bé Na vui.|Bé na vui.|Bé đầu câu và tên Na viết hoa.""",
        )
        add(
            "reading",
            "poem",
            "Đọc thơ: nắng trong sân",
            "Đọc từng dòng, nghỉ ở cuối dòng. Tìm cảnh được nói trong thơ.",
            "Nắng vàng trên sân nhỏ\nChim hót cạnh hàng cây\nBé mang bình nước mát\nTưới hoa vào sáng nay.",
            "Đọc từng dòng.|Tìm dòng có chi tiết được hỏi.|Chỉ vào chữ giúp em chọn.",
            """Nắng có màu gì?|Vàng|Đen|Xanh|Dòng đầu nói nắng vàng.
Chim ở cạnh đâu?|Hàng cây|Bàn học|Cửa lớp|Chim hót cạnh hàng cây.
Bé mang gì?|Bình nước|Cặp sách|Bút|Bé mang bình nước mát.
Bé tưới gì?|Hoa|Áo|Vở|Bé tưới hoa.
Bé tưới vào lúc nào?|Sáng nay|Đêm qua|Tối mai|Dòng cuối nói sáng nay.
Bài thơ có mấy dòng?|Bốn dòng|Hai dòng|Sáu dòng|Có bốn dòng thơ.""",
        )
        add(
            "speaking",
            "greetings",
            "Chào hỏi, cảm ơn và xin lỗi",
            "Nói một câu ngắn với đúng người. Nhìn người nghe và nói nhẹ nhàng.",
            "Em chào cô ạ. Cảm ơn bạn. Mình xin lỗi bạn.",
            "Xem em đang gặp ai.|Chọn lời chào, cảm ơn hoặc xin lỗi.|Thử nói cùng người thân.",
            """Gặp cô, em nói gì?|Em chào cô ạ.|Đưa bút đây!|Đi đi!|Chào cô lễ phép.
Bạn giúp em, em nói gì?|Cảm ơn bạn.|Tránh ra!|Im đi!|Cảm ơn khi được giúp.
Em làm bạn buồn, em nói gì?|Mình xin lỗi bạn.|Kệ bạn!|Không nghe!|Xin lỗi khi làm bạn buồn.
Muốn mượn bút, em nói gì?|Bạn cho mình mượn bút nhé.|Đưa ngay!|Bỏ đi!|Nhờ bạn lịch sự.
Bạn đang nói, em làm gì?|Lắng nghe|Nói chen|Quay đi ngay|Lắng nghe người nói.
Chưa nghe rõ, em nói gì?|Bạn nói lại giúp mình nhé.|Bạn im đi.|Không cần nghe.|Nhờ nói lại nhẹ nhàng.""",
        )
        add(
            "reading",
            "rain",
            "Tư duy: tìm chi tiết trong chuyện mưa",
            "Đọc thành hai phần cùng người lớn. Chọn chi tiết được kể, không thêm việc chưa có.",
            "Sáng nay, Na cùng mẹ đi học. Trời có mây xám. Mẹ đưa Na áo mưa màu vàng. Na bỏ áo vào cặp. Đến cổng trường, mưa bắt đầu rơi. Na mặc áo mưa và bước chậm vào lớp. Cô giúp Na treo áo lên móc. Na cảm ơn cô rồi ngồi vào bàn. Chiếc cặp của Na vẫn khô.",
            "Tìm câu nói về điều đang hỏi.|Chỉ vào từ trong câu làm bằng chứng.|Nếu chuyện không nói thì không tự đoán.",
            """Na đi học với ai?|Mẹ|Bố|Bà|Chuyện nói Na cùng mẹ.
Mây có màu gì?|Xám|Hồng|Vàng|Chuyện nói mây xám.
Áo mưa màu gì?|Vàng|Đỏ|Xanh|Mẹ đưa áo mưa vàng.
Na để áo mưa vào đâu?|Cặp|Tủ bếp|Sân|Na bỏ áo vào cặp.
Khi nào mưa rơi?|Đến cổng trường|Khi ngủ|Tối hôm trước|Mưa rơi lúc đến cổng trường.
Na bước như thế nào?|Chậm|Chạy rất nhanh|Nhảy trên bàn|Na bước chậm.
Ai giúp Na treo áo?|Cô|Bà|Bạn Nam|Cô giúp treo áo.
Cặp Na thế nào?|Vẫn khô|Bị rách|Mất rồi|Chuyện nói cặp vẫn khô.""",
            thinking=True,
        )
        add(
            "reading",
            "before-after",
            "Tư duy: việc nào trước, việc nào sau?",
            "Đọc từng câu theo thứ tự. Trả lời bằng việc được nói rõ.",
            "An thức dậy. An rửa mặt. Sau đó An ăn sáng. Cuối cùng An đeo cặp đi học.",
            "Đọc từ đầu.|Tìm từ sau đó hoặc cuối cùng.|Kể lại các việc theo thứ tự.",
            """Việc đầu tiên là gì?|Thức dậy|Ăn sáng|Đi học|Câu đầu nói thức dậy.
Sau thức dậy, An làm gì?|Rửa mặt|Đi ngủ|Đọc sách|Câu tiếp nói rửa mặt.
Sau rửa mặt, An làm gì?|Ăn sáng|Thức dậy|Đi ngủ|An ăn sáng sau rửa mặt.
Việc cuối cùng là gì?|Đeo cặp đi học|Rửa mặt|Thức dậy|Cuối cùng đi học.
Ai làm các việc?|An|Na|Lan|Các câu đều kể về An.
An đeo vật gì?|Cặp|Mũ bơi|Áo mưa|An đeo cặp.
Trước ăn sáng là việc nào?|Rửa mặt|Đi học|Đi ngủ|Rửa mặt ở trước ăn sáng.
Chuyện có nói An đi xe gì không?|Không nói|Xe đạp|Xe máy|Không có thông tin về xe.""",
            thinking=True,
        )
        add(
            "vocabulary",
            "match",
            "Tư duy: ghép vật với việc dùng",
            "Chọn đồ dùng phù hợp với một việc quen thuộc.",
            "Bút để viết. Thước để kẻ. Cốc để uống. Khăn để lau.",
            "Đề đang hỏi việc gì?|Tìm vật làm được việc ấy.|Nói một câu vật dùng để làm gì.",
            """Muốn viết, em dùng gì?|Bút|Cốc|Khăn|Bút dùng để viết.
Muốn kẻ đường, em dùng gì?|Thước|Cốc|Áo|Thước dùng kẻ đường.
Muốn uống nước, em dùng gì?|Cốc|Bút|Vở|Cốc dùng uống nước.
Muốn lau tay, em dùng gì?|Khăn|Bút|Thước|Khăn dùng lau tay.
Vật nào dùng để viết?|Bút|Cốc|Khăn|Bút dùng để viết.
Việc phù hợp với thước là gì?|Kẻ đường|Uống nước|Lau tay|Thước dùng kẻ đường.
Việc phù hợp với khăn là gì?|Lau tay|Kẻ đường|Viết|Khăn dùng lau tay.
Việc phù hợp với cốc là gì?|Uống nước|Viết|Kẻ đường|Cốc dùng uống nước.""",
            thinking=True,
        )
        add(
            "writing",
            "fix-word",
            "Tư duy: tìm tiếng viết đúng",
            "Đọc từ mẫu rồi nhìn chữ bị thiếu hoặc nhầm. Chọn từ đúng, không học quy tắc mới.",
            "Từ mẫu: ghế, nghe, kê, cá.",
            "Nhìn từ mẫu.|So từng chữ từ đầu đến cuối.|Đọc lại tiếng em chọn.",
            """Chọn từ đúng theo mẫu.|ghế|gế|ghhé|Mẫu là ghế.
Chọn từ đúng theo mẫu.|nghe|nge|nghhe|Mẫu là nghe.
Chọn từ đúng theo mẫu.|kê|cê|kêê|Mẫu là kê.
Chọn từ đúng theo mẫu.|cá|ká|cáá|Mẫu là cá.
Trong ghế cần chữ h sau chữ nào?|g|n|c|Gh có h sau g.
Trong nghe cần h sau nhóm nào?|ng|g|c|Ngh gồm n, g, h.
Chữ đầu của kê là gì?|k|c|g|Kê bắt đầu bằng k.
Chữ đầu của cá là gì?|c|k|g|Cá bắt đầu bằng c.""",
            ["ghế", "nghe", "kê", "cá"],
            True,
        )
        add(
            "rhymes",
            "same-rime",
            "Tư duy: hai tiếng có cùng vần",
            "Nhìn phần sau âm đầu. Các tiếng cùng vần có phần vần giống nhau.",
            "bàn – đàn cùng vần an. bát – hát cùng vần at.",
            "Đọc chậm hai tiếng.|Nhìn phần an hoặc at ở cuối.|Đối chiếu vần của cả hai tiếng.",
            """Tiếng nào cùng vần với bàn?|đàn|bát|hót|Bàn và đàn cùng an.
Tiếng nào cùng vần với bát?|hát|bàn|con|Bát và hát cùng at.
Tiếng nào cùng vần với con?|lon|bàn|bát|Con và lon cùng on.
Tiếng nào cùng vần với hót?|ngọt|con|bàn|Hót và ngọt cùng ot.
Bàn và đàn cùng vần nào?|an|at|on|Cùng vần an.
Bát và hát cùng vần nào?|at|an|ot|Cùng vần at.""",
            thinking=True,
        )
        add(
            "writing",
            "sentence",
            "Tư duy: chọn câu đúng với việc",
            "Chọn câu ngắn nói đúng người và việc đã cho.",
            "Na đang tưới hoa. Nam đang đọc sách.",
            "Tìm người được hỏi.|Tìm việc người đó đang làm.|Chọn câu giữ đúng cả người và việc.",
            """Câu nào đúng về Na?|Na tưới hoa.|Na đọc sách.|Na ngủ.|Ví dụ nói Na tưới hoa.
Câu nào đúng về Nam?|Nam đọc sách.|Nam tưới hoa.|Nam ngủ.|Ví dụ nói Nam đọc sách.
Ai tưới hoa?|Na|Nam|Bà|Na tưới hoa.
Ai đọc sách?|Nam|Na|Mẹ|Nam đọc sách.
Na tưới gì?|Hoa|Sách|Áo|Na tưới hoa.
Nam đọc gì?|Sách|Hoa|Áo|Nam đọc sách.""",
            thinking=True,
        )
        add(
            "reading",
            "directions",
            "Tư duy: đọc một chỉ dẫn ngắn",
            "Đọc mỗi câu một lần, làm theo thứ tự với người thân.",
            "Rửa tay trước khi ăn. Dùng khăn sạch lau tay. Sau đó ngồi vào bàn.",
            "Đọc câu đầu.|Tìm việc cần làm trước.|Đọc câu cuối để kiểm tra thứ tự.",
            """Việc cần làm trước là gì?|Rửa tay|Ngồi vào bàn|Ăn ngay|Câu đầu yêu cầu rửa tay.
Dùng gì lau tay?|Khăn sạch|Vở|Bút|Chỉ dẫn dùng khăn sạch.
Sau lau tay, làm gì?|Ngồi vào bàn|Chơi bóng|Tưới hoa|Câu cuối nói ngồi vào bàn.
Rửa tay trước khi làm gì?|Ăn|Ngủ|Đọc sách|Rửa tay trước khi ăn.
Khăn cần thế nào?|Sạch|Bẩn|Rách|Chỉ dẫn nói khăn sạch.
Chỉ dẫn có yêu cầu chạy không?|Không|Có|Chạy thật nhanh|Không có câu nào yêu cầu chạy.""",
            thinking=True,
        )
        add(
            "speaking",
            "turns",
            "Tư duy: nghe và chờ đến lượt",
            "Nhìn người đang nói. Chờ bạn nói xong rồi nói một ý ngắn.",
            "Lan nói: Mình thích vẽ. Nam nghe hết rồi nói: Mình thích đọc.",
            "Ai đang nói?|Đợi bạn nói xong.|Nói điều của mình nhẹ nhàng.",
            """Lan thích làm gì?|Vẽ|Đọc|Bơi|Lan nói mình thích vẽ.
Nam thích làm gì?|Đọc|Vẽ|Bơi|Nam nói mình thích đọc.
Khi Lan nói, Nam làm gì?|Nghe|Nói chen|Bỏ đi|Nam nghe hết.
Nam nói khi nào?|Sau Lan|Cùng lúc Lan|Trước khi nghe|Nam nghe hết rồi nói.
Muốn hỏi lại, nên nói gì?|Bạn nói lại giúp mình nhé.|Im đi!|Kệ bạn!|Nhờ bạn nói lại lịch sự.
Ai đã nói trước?|Lan|Nam|Cô|Lan nói trước Nam.""",
            thinking=True,
        )
    else:
        add(
            "reading",
            "seed",
            "Đọc: hạt đậu của Mai",
            "Tìm người, nơi và việc làm trong từng câu.",
            "Mai gieo một hạt đậu vào chiếc cốc có đất. Mỗi sáng, Mai tưới ít nước. Mai đặt cốc cạnh cửa sổ. Vài ngày sau, một mầm xanh nhú lên. Mai gọi bà đến xem. Bà nhắc Mai chăm cây đều đặn.",
            "Tìm từ được hỏi.|Đọc câu có từ đó.|Dùng chi tiết trong câu để chọn.",
            """Mai gieo hạt gì?|Hạt đậu|Hạt lúa|Hạt cam|Mai gieo hạt đậu.
Mai đặt cốc ở đâu?|Cạnh cửa sổ|Trong tủ|Dưới giường|Cốc cạnh cửa sổ.
Mai tưới lúc nào?|Mỗi sáng|Mỗi đêm|Buổi trưa duy nhất|Mai tưới mỗi sáng.
Mai gọi ai xem mầm?|Bà|Bạn|Cô|Mai gọi bà.""",
        )
        add(
            "reading",
            "shared-book",
            "Đọc: quyển sách chung",
            "Tìm các việc của từng bạn và điều các bạn cùng làm.",
            "Nam mang một quyển sách đến lớp. Bìa sách có hình con mèo. Nam rủ Hà cùng đọc giờ nghỉ. Hai bạn giữ sách bằng tay sạch. Đọc xong, Hà giúp Nam cất sách vào ngăn bàn. Nam cảm ơn Hà.",
            "Tìm tên bạn.|Đọc việc bạn làm.|Không thêm việc chuyện chưa nói.",
            """Ai mang sách?|Nam|Hà|Mai|Nam mang sách.
Bìa có hình gì?|Con mèo|Con cá|Con chim|Bìa có hình mèo.
Hai bạn đọc khi nào?|Giờ nghỉ|Nửa đêm|Khi đang ngủ|Hai bạn đọc giờ nghỉ.
Hà giúp việc gì?|Cất sách|Xé sách|Làm ướt sách|Hà giúp cất sách.""",
        )
        add(
            "vocabulary",
            "things-actions",
            "Từ chỉ sự vật và hoạt động",
            "Dùng từ để gọi tên vật hoặc nói việc đang làm.",
            "Sự vật: bàn, hoa, chim. Hoạt động: đọc, tưới, bay.",
            "Đề hỏi vật hay hoạt động?|Nhìn hai nhóm trong ví dụ.|Đặt một câu ngắn với từ vừa chọn.",
            """Từ nào chỉ sự vật?|Hoa|Tưới|Đọc|Hoa là sự vật.
Từ nào chỉ hoạt động?|Bay|Chim|Bàn|Bay là hoạt động.
Từ nào chỉ sự vật?|Chim|Đọc|Tưới|Chim là sự vật.
Từ nào chỉ hoạt động?|Tưới|Hoa|Bàn|Tưới là hoạt động.""",
            ["hoa", "chim", "đọc", "tưới"],
        )
        add(
            "vocabulary",
            "qualities",
            "Từ chỉ đặc điểm gần gũi",
            "Từ chỉ đặc điểm cho biết vật có màu, hình dáng hoặc tính chất gì.",
            "Áo đỏ. Cặp nhỏ. Sân sạch. Nước mát.",
            "Tìm vật được nói.|Đọc từ nói vật thế nào.|Kiểm tra từ theo đúng câu.",
            """Từ chỉ màu áo là gì?|Đỏ|Áo|Cặp|Đỏ là màu áo.
Cặp có đặc điểm gì?|Nhỏ|Sạch|Mát|Cặp nhỏ.
Sân có đặc điểm gì?|Sạch|Mát|Đỏ|Sân sạch.
Nước thế nào?|Mát|Nhỏ|Đỏ|Nước mát.""",
        )
        add(
            "sentences",
            "tell-ask",
            "Câu kể và câu hỏi",
            "Câu kể nói một việc. Câu hỏi cần câu trả lời.",
            "Lan đọc sách. Lan đọc sách gì?",
            "Đọc ý câu.|Câu hỏi dùng dấu hỏi, câu kể dùng dấu chấm.|Đọc câu lại với giọng phù hợp.",
            """Câu nào là câu kể?|Lan đọc sách.|Lan đọc gì?|Bạn tên gì?|Câu này kể việc đọc sách.
Câu hỏi kết thúc bằng dấu nào?|Dấu hỏi|Dấu chấm|Dấu phẩy|Câu hỏi dùng dấu hỏi.
Câu kể kết thúc bằng dấu nào?|Dấu chấm|Dấu hỏi|Dấu phẩy|Câu kể dùng dấu chấm.
Muốn hỏi tên, chọn câu nào?|Bạn tên gì?|Bạn đi học.|Em tên Lan.|Câu hỏi tên là Bạn tên gì.""",
        )
        add(
            "sentences",
            "comma-feeling",
            "Dấu phẩy và dấu chấm than",
            "Dấu phẩy tách các vật cùng được kể. Dấu chấm than có thể kết thúc lời cảm hoặc lời gọi.",
            "Cặp có bút, vở và thước. Ôi, hoa đẹp quá!",
            "Tìm chỗ liệt kê hoặc bộc lộ cảm xúc.|Dấu phẩy tách các vật; dấu chấm than kết thúc câu cảm.|Đọc chậm lại cả câu.",
            """Dấu giữa bút và vở là gì?|Dấu phẩy|Dấu hỏi|Dấu chấm|Dấu phẩy tách hai vật.
Câu Ôi, hoa đẹp quá kết thúc bằng dấu nào?|Dấu chấm than|Dấu hỏi|Dấu phẩy|Câu cảm kết thúc bằng chấm than.
Cặp có đồ nào trong ví dụ?|Thước|Cốc|Áo|Có bút, vở và thước.
Từ nào thể hiện cảm xúc trong câu mẫu?|Ôi|Cặp|Bút|Ôi thể hiện cảm xúc.""",
        )
        add(
            "writing",
            "spelling",
            "Viết đúng từ và tên riêng",
            "So với từ mẫu, viết hoa đầu câu và tên người.",
            "Ngọc có chiếc ghế nhỏ. Lan nghe bà kể chuyện.",
            "Nhìn từ mẫu.|So từng chữ và chữ đầu tên.|Đọc lại để kiểm tra.",
            """Tên nào đúng?|Ngọc|ngọc|nGọc|Ngọc viết hoa chữ đầu.
Từ nào đúng?|ghế|gế|ghhé|Ghế có gh.
Từ nào đúng?|nghe|nge|nghhe|Nghe dùng ngh.
Tên nào đúng?|Lan|lan|lAn|Lan viết hoa chữ đầu.""",
            ["Ngọc", "ghế", "Lan", "nghe"],
        )
        add(
            "writing",
            "short-description",
            "Viết vài câu giới thiệu đồ vật",
            "Nói đồ vật là gì, có đặc điểm gì và em dùng làm gì. Có thể nói trước rồi viết.",
            "Đây là chiếc cặp của em. Cặp màu xanh. Em dùng cặp để mang sách.",
            "Gọi tên đồ vật.|Nói một đặc điểm và việc dùng.|Đọc lại ba câu có cùng nói về cặp không.",
            """Đoạn giới thiệu vật gì?|Chiếc cặp|Cái cốc|Cây bút|Đoạn nói về cặp.
Cặp màu gì?|Xanh|Đỏ|Vàng|Cặp màu xanh.
Cặp dùng để làm gì?|Mang sách|Đựng nước uống|Kẻ đường|Cặp để mang sách.
Nên nói trước khi viết thế nào?|Nói tên và đặc điểm|Nói mọi chuyện không liên quan|Không cần biết vật gì|Nói ý chính trước khi viết.""",
        )
        add(
            "reading",
            "poem",
            "Đọc thơ: góc sân xanh",
            "Đọc từng dòng, tìm cảnh và hoạt động được kể.",
            "Sáng nay sân mới sạch\nLá nằm gọn bên thềm\nChim chuyền trên cành biếc\nTiếng hót nghe thật êm\nEm tưới chậu hoa nhỏ\nNắng vàng ghé bên em.",
            "Đọc từng dòng.|Tìm dòng có điều được hỏi.|Chỉ vào từ làm bằng chứng.",
            """Sân thế nào?|Sạch|Bẩn|Tối|Dòng đầu nói sân sạch.
Lá ở đâu?|Bên thềm|Trong cặp|Trên bàn|Lá nằm bên thềm.
Chim ở đâu?|Trên cành|Trong tủ|Dưới đất|Chim chuyền trên cành.
Em tưới gì?|Chậu hoa|Chiếc áo|Quyển sách|Em tưới chậu hoa.
Nắng có màu gì?|Vàng|Đen|Tím|Nắng vàng.
Thơ có mấy dòng?|Sáu dòng|Bốn dòng|Tám dòng|Có sáu dòng thơ.""",
        )
        add(
            "reading",
            "notice",
            "Đọc thông báo ngắn",
            "Tìm việc, giờ và nơi có trong thông báo.",
            "Lớp 2A đổi sách vào thứ sáu, lúc 9 giờ, tại góc đọc. Mỗi bạn mang một quyển sách sạch. Cô Mai giúp các bạn chọn sách.",
            "Thông báo nói việc gì?|Tìm giờ, ngày và nơi.|Đối chiếu từng chi tiết.",
            """Lớp nào đổi sách?|2A|1B|4C|Thông báo nói lớp 2A.
Đổi sách ngày nào?|Thứ sáu|Thứ hai|Chủ nhật|Thông báo nói thứ sáu.
Đổi sách lúc mấy giờ?|9 giờ|7 giờ|11 giờ|Thông báo nói 9 giờ.
Đổi sách ở đâu?|Góc đọc|Sân bóng|Nhà bếp|Thông báo nói góc đọc.
Mang sách thế nào?|Sạch|Ướt|Thiếu trang|Thông báo yêu cầu sách sạch.
Ai giúp chọn sách?|Cô Mai|Bà|Bác bảo vệ|Cô Mai giúp chọn sách.""",
        )
        add(
            "vocabulary",
            "opposites",
            "Từ có đặc điểm trái nhau",
            "So hai đặc điểm trong cùng tình huống, như cao và thấp.",
            "Cây A cao, cây B thấp. Nước C nóng, nước D lạnh. Hộp E to, hộp F nhỏ.",
            "Đọc cặp đặc điểm.|Chọn từ có ý trái lại.|Đặt hai từ vào ví dụ để thử.",
            """Trái với cao là gì?|Thấp|Nóng|To|Cao và thấp trái nhau.
Trái với nóng là gì?|Lạnh|Cao|To|Nóng và lạnh trái nhau.
Trái với to là gì?|Nhỏ|Cao|Nóng|To và nhỏ trái nhau.
Cây B thế nào?|Thấp|Cao|Nóng|Ví dụ nói cây B thấp.
Nước D thế nào?|Lạnh|Nóng|To|Ví dụ nói nước D lạnh.
Hộp F thế nào?|Nhỏ|To|Cao|Ví dụ nói hộp F nhỏ.""",
        )
        add(
            "writing",
            "message",
            "Đọc và viết lời nhắn",
            "Lời nhắn cần người nhận, việc chính và người gửi. Dùng tên mẫu, không cần nhập thông tin riêng.",
            "Mẹ ơi, con sang nhà bà cùng bố. Con về lúc 5 giờ. An.",
            "Tìm người được gọi.|Đọc việc và thời gian.|Tìm tên người gửi cuối lời nhắn.",
            """Lời nhắn gửi ai?|Mẹ|Cô|Bạn|Đầu lời nhắn gọi mẹ.
Người gửi là ai?|An|Bố|Bà|Cuối lời nhắn ghi An.
An sang đâu?|Nhà bà|Sân trường|Thư viện|An sang nhà bà.
An đi với ai?|Bố|Bạn|Cô|An đi cùng bố.
An về lúc nào?|5 giờ|7 giờ|9 giờ|Lời nhắn nói 5 giờ.
Cuối lời nhắn nên có gì?|Tên người gửi|Mọi số điện thoại|Đáp án bài tập|Tên giúp biết ai gửi.""",
        )
        add(
            "speaking",
            "ask-help",
            "Xin phép và nhờ giúp",
            "Chọn lời nói lịch sự, đúng với việc cần nhờ.",
            "Bạn cho mình mượn thước nhé. Em xin phép cô ra ngoài ạ. Cảm ơn bạn đã giúp.",
            "Em cần nhờ việc gì?|Chọn lời nói lịch sự.|Thử nói cùng người thân.",
            """Muốn mượn thước, nói gì?|Bạn cho mình mượn thước nhé.|Đưa ngay!|Bỏ đi!|Nhờ bạn lịch sự.
Muốn ra ngoài, nói với cô thế nào?|Em xin phép cô ra ngoài ạ.|Em tự đi.|Cô tránh ra.|Xin phép lễ phép.
Được giúp, nói gì?|Cảm ơn bạn.|Kệ bạn!|Im đi!|Cảm ơn khi được giúp.
Làm bạn buồn, nói gì?|Mình xin lỗi bạn.|Bạn phải chịu.|Không quan tâm.|Xin lỗi phù hợp.
Nghe chưa rõ, nói gì?|Bạn nói lại giúp mình nhé.|Im đi!|Đừng nói nữa!|Nhờ nói lại lịch sự.
Khi bạn đang nói, nên làm gì?|Lắng nghe|Nói chen|Bỏ đi|Lắng nghe đến hết lượt.""",
        )
        add(
            "speaking",
            "retell",
            "Kể lại một việc theo thứ tự",
            "Nói người làm, việc trước và việc sau. Dùng một câu cho mỗi việc.",
            "Bình nhặt lá trong sân. Bình bỏ lá vào giỏ. Sau đó Bình rửa tay. Sân sạch hơn.",
            "Ai làm việc?|Kể theo thứ tự trong câu.|Thêm một câu về kết quả được kể.",
            """Ai nhặt lá?|Bình|An|Lan|Chuyện nói Bình.
Bình nhặt ở đâu?|Sân|Bếp|Lớp|Bình nhặt trong sân.
Bình bỏ lá vào đâu?|Giỏ|Cặp|Cốc|Bình bỏ lá vào giỏ.
Sau bỏ lá, Bình làm gì?|Rửa tay|Đi ngủ|Vẽ|Bình rửa tay.
Sân sau đó thế nào?|Sạch hơn|Bẩn hơn|Tối hơn|Chuyện nói sân sạch hơn.
Nên kể thế nào?|Theo thứ tự|Đổi hết mọi việc|Thêm việc không có|Kể đúng thứ tự.""",
        )
        add(
            "reading",
            "instructions",
            "Đọc chỉ dẫn giữ góc học tập",
            "Đọc từng bước, tìm đồ vật và việc cần làm trước sau.",
            "Cất sách lên giá. Đặt bút vào hộp. Sau đó lau bàn bằng khăn sạch. Cuối cùng xếp ghế gọn vào bàn.",
            "Đọc bước đầu.|Tìm từ sau đó và cuối cùng.|Kể lại đúng thứ tự.",
            """Việc đầu tiên là gì?|Cất sách|Lau bàn|Xếp ghế|Câu đầu yêu cầu cất sách.
Sách đặt ở đâu?|Trên giá|Trong cốc|Dưới sân|Cất sách lên giá.
Bút đặt vào đâu?|Hộp|Giá sách|Cốc nước|Đặt bút vào hộp.
Dùng gì lau bàn?|Khăn sạch|Áo bẩn|Quyển vở|Lau bằng khăn sạch.
Việc cuối là gì?|Xếp ghế|Cất sách|Đặt bút|Cuối cùng xếp ghế.
Chỉ dẫn có yêu cầu chạy không?|Không|Có|Chạy quanh bàn|Không có yêu cầu chạy.""",
        )
        add(
            "reading",
            "evidence",
            "Tư duy: chọn chi tiết làm bằng chứng",
            "Tìm chi tiết trong chuyện để giải thích một điều đơn giản.",
            "Hòa đi học cùng mẹ. Trời có mây xám và gió mạnh. Mẹ đưa Hòa áo mưa. Hòa cất áo vào cặp. Khi mưa rơi, Hòa mặc áo rồi bước chậm đến cửa lớp. Cô treo áo giúp Hòa. Hòa cảm ơn cô. Sách trong cặp vẫn khô.",
            "Tìm điều cần giải thích.|Chỉ ra chi tiết đã viết trong chuyện.|Không chọn điều chuyện chưa nói.",
            """Chi tiết nào báo trời có thể mưa?|Mây xám và gió mạnh|Cặp màu đỏ|Bút dài|Chuyện nêu mây xám và gió mạnh.
Ai đưa áo mưa?|Mẹ|Bà|Bạn|Mẹ đưa áo.
Hòa cất áo ở đâu?|Cặp|Tủ|Sân|Hòa cất áo vào cặp.
Hòa mặc áo khi nào?|Khi mưa rơi|Khi ngủ|Khi ăn|Hòa mặc khi mưa rơi.
Hòa đi như thế nào?|Chậm|Chạy thật nhanh|Nhảy trên bàn|Hòa bước chậm.
Ai treo áo giúp?|Cô|Bố|Bà|Cô treo áo giúp.
Sách có thế nào?|Vẫn khô|Bị xé|Đã mất|Chuyện nói sách vẫn khô.
Chuyện có nói màu áo không?|Không nói|Đỏ|Xanh|Chuyện không nêu màu áo.""",
            thinking=True,
        )
        add(
            "vocabulary",
            "context",
            "Tư duy: hiểu từ ngay trong câu",
            "Dùng câu xung quanh để hiểu từ đơn giản, không yêu cầu định nghĩa dài.",
            "Lan nói nhỏ để không làm bạn thức giấc. Nam chăm cây mỗi sáng. Hà giữ vở sạch. Bình xếp bút gọn.",
            "Đọc cả câu chứa từ.|Xem người đang làm việc gì.|Chọn nghĩa phù hợp với câu.",
            """Nói nhỏ ở đây là nói thế nào?|Âm lượng nhẹ|Nói thật to|Không nói được|Lan nói nhẹ để bạn ngủ.
Vì sao Lan nói nhỏ?|Để bạn không thức|Để gọi cả lớp|Để tranh cãi|Câu nêu không làm bạn thức.
Nam chăm gì?|Cây|Vở|Bút|Nam chăm cây.
Nam chăm cây lúc nào?|Mỗi sáng|Mỗi đêm|Một lần duy nhất|Câu nêu mỗi sáng.
Hà giữ vở thế nào?|Sạch|Bẩn|Rách|Hà giữ vở sạch.
Bình xếp bút thế nào?|Gọn|Rơi khắp nơi|Trong nước|Bình xếp gọn.
Ai nói nhỏ?|Lan|Nam|Hà|Lan nói nhỏ.
Ai giữ vở sạch?|Hà|Bình|Nam|Hà giữ vở sạch.""",
            thinking=True,
        )
        add(
            "sentences",
            "fix-stop",
            "Tư duy: sửa dấu cuối câu",
            "Đọc ý trước khi chọn dấu. Giữ nguyên nội dung câu.",
            "Em đi học. Bạn đọc gì? Ôi, hoa đẹp quá!",
            "Câu đang kể, hỏi hay cảm?|Chọn chấm, hỏi hoặc chấm than.|Đọc lại ý câu sau khi sửa.",
            """Em đi học nên kết thúc bằng gì?|Dấu chấm|Dấu hỏi|Dấu phẩy|Đây là câu kể.
Bạn đọc gì nên kết thúc bằng gì?|Dấu hỏi|Dấu chấm|Dấu phẩy|Đây là câu hỏi.
Ôi, hoa đẹp quá dùng dấu cuối nào?|Dấu chấm than|Dấu hỏi|Dấu phẩy|Đây là câu cảm.
Chọn câu hỏi đúng.|Bạn ở đâu?|Bạn ở đâu.|Bạn ở đâu,|Câu hỏi dùng dấu hỏi.
Chọn câu kể đúng.|Em có bút.|Em có bút?|Em có bút,|Câu kể dùng dấu chấm.
Chọn câu cảm phù hợp.|Ôi, đẹp quá!|Ôi, đẹp quá?|Ôi, đẹp quá,|Lời cảm dùng chấm than.
Câu Bạn tên gì là loại nào?|Câu hỏi|Câu kể|Liệt kê đồ vật|Câu hỏi tên.
Câu Lan đang vẽ là loại nào?|Câu kể|Câu hỏi|Câu xin lỗi|Câu kể việc vẽ.""",
            thinking=True,
        )
        add(
            "writing",
            "paragraph-check",
            "Tư duy: giữ câu cùng một chủ đề",
            "Chọn câu giúp giới thiệu đồ vật; câu không liên quan để sang đoạn khác.",
            "Em có một chiếc cặp. Cặp màu đỏ, có hai ngăn. Em cất sách trong cặp. Em lau cặp mỗi tối.",
            "Đoạn đang nói về gì?|Giữ câu cùng nói về vật đó.|Đọc lại các câu thành một đoạn.",
            """Chủ đề đoạn là gì?|Chiếc cặp|Con cá|Cây hoa|Đoạn nói về cặp.
Cặp màu gì?|Đỏ|Xanh|Vàng|Cặp màu đỏ.
Cặp có mấy ngăn?|Hai ngăn|Một ngăn|Bốn ngăn|Đoạn nói hai ngăn.
Em cất gì trong cặp?|Sách|Nước|Cây|Em cất sách.
Em lau cặp khi nào?|Mỗi tối|Mỗi trưa|Một lần trong năm|Đoạn nói mỗi tối.
Câu nào cùng chủ đề?|Cặp giúp em mang sách.|Cá bơi trong bể.|Mưa ngoài sân.|Câu đầu nói về cặp.
Câu nào không cùng chủ đề?|Cá bơi trong bể.|Cặp có hai ngăn.|Em lau cặp.|Câu cá không nói về cặp.
Trước viết, nên làm gì?|Nói các ý về cặp|Chép mọi câu bất kỳ|Bỏ qua đồ vật|Nói ý cùng chủ đề trước khi viết.""",
            thinking=True,
        )
        add(
            "reading",
            "book-cover",
            "Tư duy: đọc thông tin bìa sách",
            "Đọc từng dòng trên bìa mẫu. Không suy ra nội dung cả sách chỉ từ tên.",
            "Bìa mẫu: Tên sách: Góc sân xanh. Người viết: Mai An. Tranh: một cây và hai bạn nhỏ. Nhà xuất bản: Mầm Non (tên minh họa).",
            "Tìm nhãn tên sách hoặc người viết.|Đọc đúng dòng theo nhãn.|Không tự thêm thông tin không có.",
            """Tên sách là gì?|Góc sân xanh|Mai An|Hai bạn|Nhãn tên sách ghi Góc sân xanh.
Người viết là ai?|Mai An|Góc sân xanh|Bạn nhỏ|Nhãn người viết ghi Mai An.
Tranh có gì?|Cây và hai bạn|Chỉ ô tô|Chỉ cá|Mẫu nói một cây và hai bạn.
Có mấy bạn trong tranh mô tả?|Hai|Ba|Bốn|Mẫu nói hai bạn.
Bìa có cho biết hết câu chuyện không?|Không|Có toàn bộ|Có mọi đáp án|Bìa chỉ có thông tin giới thiệu.
Muốn tìm tên người viết, nhìn dòng nào?|Người viết|Tên sách|Tranh|Nhãn Người viết nêu tên.""",
            thinking=True,
        )
        add(
            "speaking",
            "listen-turn",
            "Tư duy: trao đổi theo lượt",
            "Nghe bạn nói hết, rồi trả lời đúng ý bạn hỏi. Có thể nhờ nhắc lại.",
            "Lan hỏi: Bạn thích sách gì? Nam nghe xong rồi đáp: Mình thích sách về cây. Lan nói: Mình thích sách về con vật.",
            "Ai đang hỏi và hỏi điều gì?|Chờ hết câu rồi trả lời đúng điều hỏi.|Nhờ bạn nhắc lại khi chưa rõ.",
            """Lan hỏi về điều gì?|Sách yêu thích|Màu áo|Giờ ngủ|Lan hỏi thích sách gì.
Nam thích sách về gì?|Cây|Con vật|Ô tô|Nam thích sách về cây.
Lan thích sách về gì?|Con vật|Cây|Ô tô|Lan thích sách về con vật.
Nam trả lời khi nào?|Sau khi nghe xong|Khi Lan chưa hỏi|Nói chen giữa câu|Nam nghe xong rồi đáp.
Chưa nghe rõ, nên nói gì?|Bạn nhắc lại giúp mình nhé.|Im đi!|Không cần biết.|Nhờ bạn nhắc lịch sự.
Trả lời nào đúng câu hỏi thích sách gì?|Mình thích sách về cây.|Áo mình màu đỏ.|Mình ăn cơm.|Câu đầu nói loại sách yêu thích.""",
            thinking=True,
        )
        add(
            "writing",
            "note-check",
            "Tư duy: sửa lời nhắn cho rõ",
            "Lời nhắn cần việc chính và tên người gửi; không tự đổi thời gian.",
            "Bà ơi, cháu đến thư viện cùng mẹ. Cháu về lúc 4 giờ. Lan.",
            "Ai nhận và ai gửi?|Giữ đúng nơi, người đi cùng và giờ.|Đọc lại như người nhận lời nhắn.",
            """Ai nhận lời nhắn?|Bà|Cô|Bạn|Đầu lời nhắn gọi bà.
Ai gửi lời nhắn?|Lan|Mẹ|Bà|Cuối lời nhắn ghi Lan.
Lan đi đâu?|Thư viện|Sân bóng|Nhà bạn|Lời nhắn nói thư viện.
Lan đi cùng ai?|Mẹ|Bạn|Cô|Lan đi cùng mẹ.
Lan về lúc nào?|4 giờ|5 giờ|6 giờ|Lời nhắn ghi 4 giờ.
Có nên tự đổi giờ về không?|Không|Có, đổi bất kỳ|Đổi để vui|Phải giữ đúng thông tin.""",
            thinking=True,
        )
        add(
            "reading",
            "help-friend",
            "Tư duy: hiểu việc giúp bạn",
            "Tìm hành động trong chuyện để nói vì sao nhân vật được cảm ơn.",
            "Hà làm rơi hộp bút. Những chiếc bút lăn xuống sàn. Bình dừng lại, cùng Hà nhặt từng chiếc. Bình đặt hộp bút lên bàn. Hà cảm ơn Bình. Hai bạn cùng kiểm tra xem bút đã đủ chưa rồi vào lớp.",
            "Ai được cảm ơn?|Tìm việc bạn ấy làm trước lời cảm ơn.|Nói một câu ngắn có bằng chứng.",
            """Ai làm rơi hộp bút?|Hà|Bình|Lan|Hà làm rơi.
Bút rơi xuống đâu?|Sàn|Cây|Tủ|Bút lăn xuống sàn.
Bình giúp việc gì?|Nhặt bút|Giấu bút|Làm ướt bút|Bình cùng Hà nhặt bút.
Vì sao Hà cảm ơn Bình?|Bình giúp nhặt bút|Bình mang bánh|Bình đi trước|Hành động giúp nhặt bút là bằng chứng.
Hai bạn kiểm tra điều gì?|Bút đã đủ chưa|Màu trời|Giờ tàu|Hai bạn kiểm tra bút đã đủ.
Sau kiểm tra, hai bạn làm gì?|Vào lớp|Đi ngủ|Về nhà|Chuyện nói vào lớp.""",
            thinking=True,
        )
    assert len(items) == 23
    return items
