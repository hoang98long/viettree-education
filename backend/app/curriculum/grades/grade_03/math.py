"""25 original mathematics lessons: eight foundations, ten extensions, seven challenges."""

from app.curriculum.grades.grade_03.builders import unit as build


def unit(*args, **kwargs):
    return build(*args, numeric=True, **kwargs)


MATH = [
    unit(
        "numbers",
        "read-four",
        "Đọc và viết số có bốn chữ số",
        "Số có bốn chữ số gồm hàng nghìn, trăm, chục, đơn vị. Đọc từ trái sang phải; chữ số 0 vẫn giữ vị trí của hàng.",
        "3 405 gồm 3 nghìn, 4 trăm, 0 chục và 5 đơn vị; đọc là ba nghìn bốn trăm linh năm.",
        "Viết đủ các hàng; không bỏ chữ số 0 ở giữa.",
        "Tách số thành các hàng.|Dùng bảng nghìn, trăm, chục, đơn vị để đặt từng chữ số.|Đọc lại số vừa viết, chú ý hàng có chữ số 0.",
        """Số gồm 2 nghìn, 7 trăm, 0 chục, 3 đơn vị là số nào?|2703|Ghép bốn hàng được 2 703.
Trong số 4 582, chữ số 5 có giá trị bao nhiêu?|500|Chữ số 5 ở hàng trăm nên có giá trị 500.
6 000 + 200 + 40 + 8 bằng bao nhiêu?|6248|Ghép nghìn, trăm, chục, đơn vị được 6 248.
Số liền sau 3 999 là số nào?|4000|Thêm một đơn vị vào 3 999 được 4 000.""",
    ),
    unit(
        "numbers",
        "compare-four",
        "So sánh và sắp xếp số trong phạm vi 10 000",
        "So sánh số chữ số trước, rồi so sánh lần lượt từ hàng lớn nhất. Khi sắp xếp, chọn số nhỏ nhất hoặc lớn nhất theo yêu cầu.",
        "4 208 < 4 280 vì hàng nghìn và trăm giống nhau, ở hàng chục có 0 < 8.",
        "Phải đọc rõ yêu cầu tăng dần hay giảm dần.",
        "Xem hai số có bao nhiêu chữ số.|Đối chiếu từng hàng từ trái sang phải; dừng ở hàng đầu tiên khác nhau.|Đọc lại toàn bộ dãy số theo chiều đề yêu cầu.",
        """Trong 5 012, 5 120, 5 102, số bé nhất là số nào?|5012|Cùng 5 nghìn, số 5 012 có hàng trăm nhỏ nhất.
Trong 8 901 và 8 910, số lớn hơn là số nào?|8910|Hàng chục: 1 lớn hơn 0.
Số liền trước 7 000 là số nào?|6999|Bớt một đơn vị từ 7 000 được 6 999.
Số lớn nhất có bốn chữ số là số nào?|9999|Mỗi hàng đều chọn chữ số 9.""",
    ),
    unit(
        "operations",
        "multiply-tables",
        "Bảng nhân và những nhóm bằng nhau",
        "Phép nhân biểu diễn tổng nhiều số hạng bằng nhau. Có thể dựa vào bảng đã biết để tìm bảng nhân 6, 7, 8, 9.",
        "7 × 6 = 7 × 5 + 7 = 35 + 7 = 42. Sáu nhóm, mỗi nhóm 7 vật có 42 vật.",
        "Đọc cả số nhóm và số vật trong mỗi nhóm.",
        "Tìm xem các nhóm có bằng nhau không.|Vẽ từng nhóm hoặc dùng kết quả bảng nhân gần nhất rồi thêm một nhóm.|Cộng lại các nhóm để kiểm tra phép nhân.",
        """6 × 7 bằng bao nhiêu?|42|Sáu lần bảy bằng 42.
8 × 9 bằng bao nhiêu?|72|Bảng nhân 8: 8 × 9 = 72.
5 túi, mỗi túi 9 viên bi. Có tất cả bao nhiêu viên bi?|45|5 × 9 = 45 viên bi.
7 × 8 bằng bao nhiêu?|56|Bảy nhóm tám có 56 vật.""",
        illustration={
            "kind": "garden",
            "caption": "Ba hàng cây, mỗi hàng có bốn cây.",
            "rows": 3,
            "columns": 4,
        },
    ),
    unit(
        "operations",
        "division-tables",
        "Chia đều và tìm số nhóm",
        "Phép chia giúp chia đều một số đồ vật hoặc tìm số nhóm bằng nhau. Kiểm tra thương bằng phép nhân.",
        "48 chiếc bút chia đều vào 6 hộp; mỗi hộp có 48 : 6 = 8 chiếc.",
        "Nêu đơn vị của kết quả: đồ vật mỗi nhóm hay số nhóm.",
        "Đề cho tổng số vật hay số vật trong một nhóm?|Tìm phép nhân có tích bằng tổng số đã cho.|Lấy thương nhân số chia để kiểm tra.",
        """54 : 6 bằng bao nhiêu?|9|6 × 9 = 54 nên 54 : 6 = 9.
63 : 7 bằng bao nhiêu?|9|7 × 9 = 63.
32 quả cam chia đều vào 8 đĩa. Mỗi đĩa có bao nhiêu quả?|4|32 : 8 = 4 quả.
56 học sinh chia thành nhóm 7 bạn. Có bao nhiêu nhóm?|8|56 : 7 = 8 nhóm.""",
    ),
    unit(
        "parts",
        "equal-parts",
        "Nhận biết một phần của hình",
        "Chia một hình thành các phần bằng nhau. Một phần hai là một trong hai phần bằng nhau; tương tự với một phần ba, một phần tư.",
        "Một tờ giấy chia thành 4 phần bằng nhau, tô 1 phần. Phần tô là một phần tư tờ giấy.",
        "Các phần phải bằng nhau mới gọi là một phần hai, một phần ba...",
        "Đếm tổng số phần bằng nhau.|Chú ý số phần đã tô; bài này chỉ nhận biết một phần của hình.|Kiểm tra hình có được chia đều thực sự không.",
        """Một hình chia đều thành 2 phần. Một phần gọi là một phần mấy? Điền số ở mẫu.|2|Một phần trong hai phần bằng nhau là một phần hai.
Một hình chia đều thành 3 phần. Một phần gọi là một phần mấy? Điền số ở mẫu.|3|Một phần trong ba phần bằng nhau là một phần ba.
Một hình chia đều thành 4 phần, tô một phần. Tổng số phần là bao nhiêu?|4|Tổng số phần bằng nhau là 4.
Một hình chia đều thành 8 phần, tô một phần. Có bao nhiêu phần chưa tô?|7|8 − 1 = 7 phần chưa tô.""",
        illustration={
            "kind": "fraction",
            "caption": "Một trong bốn phần bằng nhau được tô màu.",
            "numerator": 1,
            "denominator": 4,
        },
    ),
    unit(
        "parts",
        "part-of-group",
        "Tìm một phần của một nhóm đồ vật",
        "Muốn tìm một phần ba của nhóm đồ vật, chia đều nhóm thành 3 phần rồi lấy 1 phần. Dùng phép chia phù hợp với số phần.",
        "Một phần tư của 20 quả là 20 : 4 = 5 quả.",
        "Không cộng hoặc nhân tổng số vật với số phần khi cần lấy một phần.",
        "Xác định cần một phần mấy.|Chia tổng số vật thành đúng số phần bằng nhau.|Nhân số vật một phần với số phần để kiểm tra tổng.",
        """Một phần hai của 18 viên bi là bao nhiêu viên?|9|18 : 2 = 9.
Một phần ba của 24 quả là bao nhiêu quả?|8|24 : 3 = 8.
Một phần tư của 28 bông hoa là bao nhiêu bông?|7|28 : 4 = 7.
Một phần năm của 30 chiếc bút là bao nhiêu chiếc?|6|30 : 5 = 6.""",
    ),
    unit(
        "measurement",
        "length",
        "Mi-li-mét và đo độ dài",
        "Thước có vạch mi-li-mét giúp đo vật ngắn. 1 cm = 10 mm; 1 m = 100 cm. Khi đo, đặt đầu vật trùng vạch 0.",
        "Một đoạn dài 3 cm 5 mm có độ dài 30 mm + 5 mm = 35 mm.",
        "Đổi về cùng đơn vị trước khi so sánh hay cộng trừ.",
        "Gạch chân đơn vị đề yêu cầu.|Đổi từng phần của số đo theo 1 cm = 10 mm.|Kiểm tra đã cộng cả phần mi-li-mét còn lại chưa.",
        """4 cm bằng bao nhiêu mm?|40|4 × 10 = 40 mm.
2 cm 8 mm bằng bao nhiêu mm?|28|20 + 8 = 28 mm.
70 mm bằng bao nhiêu cm?|7|70 : 10 = 7 cm.
Một dây dài 80 cm, cắt đi 25 cm. Còn bao nhiêu cm?|55|80 − 25 = 55 cm.""",
    ),
    unit(
        "measurement",
        "mass-volume",
        "Gam và mi-li-lít trong đời sống",
        "Dùng gam để đo khối lượng vật nhẹ, mi-li-lít để đo dung tích ít. 1 kg = 1 000 g; 1 l = 1 000 ml.",
        "Hai chai, mỗi chai 250 ml có tổng dung tích 500 ml. Không đổi gam sang mi-li-lít bằng một quy tắc chung.",
        "Khối lượng và dung tích là hai đại lượng khác nhau.",
        "Nhìn nhãn đơn vị: g, kg hay ml, l.|Đổi cùng một đại lượng về cùng đơn vị rồi tính.|Ước lượng kết quả có phù hợp kích thước vật không.",
        """1 kg bằng bao nhiêu g?|1000|1 kg = 1 000 g.
2 l bằng bao nhiêu ml?|2000|2 × 1 000 = 2 000 ml.
Gói bánh 150 g và gói bánh 200 g nặng tổng cộng bao nhiêu g?|350|150 + 200 = 350 g.
Chai có 500 ml nước, rót ra 120 ml. Còn bao nhiêu ml?|380|500 − 120 = 380 ml.""",
    ),
    unit(
        "numbers",
        "five-digits",
        "Số đến 100 000 và cấu tạo số",
        "Số có năm chữ số thêm hàng chục nghìn. Đọc theo nhóm nghìn rồi phần còn lại. Giá trị chữ số phụ thuộc vào hàng.",
        "42 306 = 40 000 + 2 000 + 300 + 6. Chữ số 2 có giá trị 2 000.",
        "Số 100 000 là một trăm nghìn; không học đến lớp triệu trong bài này.",
        "Kẻ bảng chục nghìn đến đơn vị.|Điền từng chữ số; hàng trống viết 0.|Cộng giá trị các hàng để kiểm tra số ban đầu.",
        """30 000 + 5 000 + 200 + 4 bằng bao nhiêu?|35204|Ghép các hàng được 35 204.
Trong 68 215, chữ số 6 có giá trị bao nhiêu?|60000|6 ở hàng chục nghìn.
Số liền sau 99 999 là số nào?|100000|Thêm một đơn vị được 100 000.
Trong 40 580, chữ số 5 có giá trị bao nhiêu?|500|5 ở hàng trăm.
Số gồm 7 chục nghìn và 9 đơn vị là số nào?|70009|Các hàng nghìn, trăm, chục đều là 0.
Trong 82 307 và 82 370, số bé hơn là số nào?|82307|Hàng chục 0 nhỏ hơn 7.""",
    ),
    unit(
        "numbers",
        "rounding",
        "Làm tròn số và ước lượng",
        "Khi làm tròn đến một hàng, nhìn chữ số bên phải hàng đó: từ 5 trở lên tăng một, nhỏ hơn 5 giữ nguyên; các hàng phía sau viết 0.",
        "2 346 làm tròn đến hàng trăm là 2 300 vì hàng chục là 4.",
        "Luôn xác định hàng cần làm tròn trước.",
        "Khoanh hàng cần làm tròn.|Nhìn ngay chữ số bên phải, dùng mốc 5.|Kiểm tra các hàng nhỏ hơn đã trở thành 0.",
        """Làm tròn 4 263 đến hàng chục được số nào?|4260|Hàng đơn vị 3 nhỏ hơn 5.
Làm tròn 4 267 đến hàng chục được số nào?|4270|Hàng đơn vị 7 nên tăng hàng chục.
Làm tròn 7 450 đến hàng trăm được số nào?|7500|Hàng chục 5 nên tăng hàng trăm.
Làm tròn 12 399 đến hàng nghìn được số nào?|12000|Hàng trăm 3 nhỏ hơn 5.
Làm tròn 28 700 đến hàng chục nghìn được số nào?|30000|Hàng nghìn 8 nên tăng hàng chục nghìn.
Làm tròn 16 500 đến hàng nghìn được số nào?|17000|Hàng trăm 5 nên làm tròn lên.""",
    ),
    unit(
        "numbers",
        "roman",
        "Đọc chữ số La Mã đến XX",
        "I chỉ 1, V chỉ 5, X chỉ 10. IV là 4, IX là 9. Sau X có thể thêm các nhóm để viết đến XX.",
        "XIV = X + IV = 10 + 4 = 14; XIX = 10 + 9 = 19.",
        "IV và VI khác nhau; IX và XI cũng khác nhau.",
        "Nhận ra I, V, X.|Tách nhóm IV hoặc IX trước khi cộng với X.|So lại vị trí các chữ để không đảo IV thành VI.",
        """IV biểu diễn số nào?|4|I đứng trước V tạo thành IV = 4.
VI biểu diễn số nào?|6|V + I = 6.
IX biểu diễn số nào?|9|IX = 9.
XII biểu diễn số nào?|12|X + II = 12.
XVIII biểu diễn số nào?|18|X + V + III = 18.
XX biểu diễn số nào?|20|Hai chữ X biểu diễn 20.""",
    ),
    unit(
        "operations",
        "add-subtract",
        "Cộng trừ số có nhiều chữ số",
        "Đặt tính để các hàng thẳng nhau, tính từ phải sang trái. Phép cộng có nhớ và phép trừ có đổi cần ghi rõ từng bước.",
        "23 456 + 12 307 = 35 763; lấy 35 763 − 12 307 sẽ trở lại 23 456.",
        "Dùng phép tính ngược để kiểm tra.",
        "Viết hai số thẳng hàng.|Tính từ đơn vị; chú ý số nhớ hoặc hàng đã đổi.|Dùng phép tính ngược và ước lượng để kiểm tra.",
        """2 368 + 1 457 bằng bao nhiêu?|3825|Cộng có nhớ được 3 825.
8 000 − 2 456 bằng bao nhiêu?|5544|Trừ có đổi qua các hàng được 5 544.
14 205 + 23 670 bằng bao nhiêu?|37875|Cộng từng hàng được 37 875.
50 000 − 18 725 bằng bao nhiêu?|31275|18 725 + 31 275 = 50 000.
6 789 + 211 bằng bao nhiêu?|7000|Cộng có nhớ liên tiếp được 7 000.
72 340 − 20 120 bằng bao nhiêu?|52220|Trừ các hàng được 52 220.""",
    ),
    unit(
        "operations",
        "one-digit",
        "Nhân chia với số có một chữ số",
        "Nhân từng hàng từ phải sang trái. Chia từ trái sang phải theo từng lượt; mỗi lượt tìm thương, nhân lại rồi trừ.",
        "234 × 3 = 702; 702 : 3 = 234.",
        "Ở phép chia có dư, số dư phải nhỏ hơn số chia.",
        "Xác định phép nhân hay phép chia.|Viết từng lượt tính; ghi số nhớ hoặc số dư.|Nhân thương với số chia rồi cộng số dư để kiểm tra.",
        """123 × 4 bằng bao nhiêu?|492|Nhân từng hàng được 492.
206 × 3 bằng bao nhiêu?|618|3 × 206 = 618.
848 : 4 bằng bao nhiêu?|212|4 × 212 = 848.
936 : 3 bằng bao nhiêu?|312|3 × 312 = 936.
1 205 × 5 bằng bao nhiêu?|6025|Nhân có nhớ được 6 025.
6 048 : 6 bằng bao nhiêu?|1008|6 × 1 008 = 6 048.""",
    ),
    unit(
        "operations",
        "expressions",
        "Thứ tự tính và dấu ngoặc",
        "Biểu thức có cộng, trừ, nhân, chia: thực hiện nhân chia trước cộng trừ. Có dấu ngoặc thì tính trong ngoặc trước.",
        "18 + 6 × 3 = 18 + 18 = 36; (18 + 6) × 3 = 24 × 3 = 72.",
        "Hai biểu thức có cùng số nhưng dấu ngoặc khác có thể cho kết quả khác.",
        "Tìm dấu ngoặc và các phép tính.|Đánh dấu phép cần làm trước rồi viết kết quả trung gian.|Đối chiếu lại thứ tự, đừng tính tất cả từ trái sang phải.",
        """24 + 8 × 2 bằng bao nhiêu?|40|8 × 2 = 16 rồi 24 + 16 = 40.
(24 + 8) × 2 bằng bao nhiêu?|64|Trong ngoặc là 32, nhân 2 được 64.
90 − 36 : 4 bằng bao nhiêu?|81|36 : 4 = 9 rồi 90 − 9 = 81.
(90 − 36) : 6 bằng bao nhiêu?|9|54 : 6 = 9.
7 × 8 − 12 bằng bao nhiêu?|44|56 − 12 = 44.
48 : 6 + 15 bằng bao nhiêu?|23|8 + 15 = 23.""",
    ),
    unit(
        "measurement",
        "clock-calendar",
        "Đọc giờ và tính thời gian ngắn",
        "Một giờ có 60 phút. Đọc kim phút theo các vạch 5 phút; tính thời gian ngắn bằng cách đi đến giờ tròn rồi cộng phần còn lại.",
        "Từ 8 giờ 40 phút đến 9 giờ 10 phút là 20 + 10 = 30 phút.",
        "Không coi 1 giờ là 100 phút.",
        "Đánh dấu giờ bắt đầu và kết thúc.|Tách đoạn qua giờ tròn nếu cần.|Kiểm tra số phút còn lại với mốc 60.",
        """1 giờ bằng bao nhiêu phút?|60|Một giờ có 60 phút.
Từ 7 giờ 15 phút đến 7 giờ 45 phút là bao nhiêu phút?|30|45 − 15 = 30 phút.
Từ 8 giờ 50 phút đến 9 giờ 10 phút là bao nhiêu phút?|20|10 phút đến 9 giờ và thêm 10 phút.
2 giờ bằng bao nhiêu phút?|120|2 × 60 = 120 phút.
Tháng 4 có bao nhiêu ngày?|30|Tháng 4 có 30 ngày.
Hôm nay là thứ ba; sau 3 ngày là thứ mấy? Điền số thứ.|6|Thứ tư, thứ năm, thứ sáu: sau 3 ngày là thứ sáu.""",
        illustration={
            "kind": "clock",
            "caption": "Đồng hồ chỉ 8 giờ 40 phút.",
            "hour": 8,
            "minute": 40,
        },
    ),
    unit(
        "geometry",
        "perimeter",
        "Chu vi hình chữ nhật và hình vuông",
        "Chu vi là độ dài đường bao quanh hình. Hình chữ nhật có hai cạnh dài bằng nhau và hai cạnh rộng bằng nhau; hình vuông có bốn cạnh bằng nhau.",
        "Hình chữ nhật dài 8 cm, rộng 3 cm có chu vi (8 + 3) × 2 = 22 cm.",
        "Chu vi dùng đơn vị độ dài, không dùng cm².",
        "Tìm chiều dài, chiều rộng hoặc cạnh hình vuông.|Vẽ hình, ghi số đo và cộng đủ bốn cạnh.|So sánh với cách tính nhanh để kiểm tra.",
        """Hình vuông cạnh 5 cm có chu vi bao nhiêu cm?|20|5 × 4 = 20 cm.
Hình chữ nhật dài 9 cm, rộng 4 cm có chu vi bao nhiêu cm?|26|(9 + 4) × 2 = 26 cm.
Hình vuông cạnh 12 cm có chu vi bao nhiêu cm?|48|12 × 4 = 48 cm.
Hình chữ nhật dài 15 m, rộng 5 m có chu vi bao nhiêu m?|40|(15 + 5) × 2 = 40 m.
Hình vuông chu vi 28 cm có cạnh bao nhiêu cm?|7|28 : 4 = 7 cm.
Hình chữ nhật dài 7 cm, rộng 2 cm có chu vi bao nhiêu cm?|18|(7 + 2) × 2 = 18 cm.""",
    ),
    unit(
        "geometry",
        "area",
        "Diện tích và ô vuông đơn vị",
        "Diện tích là phần mặt hình chiếm chỗ. Dùng ô vuông cạnh 1 cm làm đơn vị cm². Diện tích hình chữ nhật bằng dài nhân rộng cùng đơn vị.",
        "Hình chữ nhật dài 5 cm, rộng 3 cm có 3 hàng, mỗi hàng 5 ô cm², diện tích 15 cm².",
        "Chu vi là đường bao; diện tích là phần mặt bên trong.",
        "Đề hỏi đường bao hay phần mặt hình?|Đếm hàng và số ô trong mỗi hàng hoặc nhân hai kích thước.|Kiểm tra đơn vị diện tích có ghi cm² không.",
        """Hình chữ nhật dài 6 cm, rộng 4 cm có diện tích bao nhiêu cm²?|24|6 × 4 = 24 cm².
Hình vuông cạnh 3 cm có diện tích bao nhiêu cm²?|9|3 × 3 = 9 cm².
Hình có 4 hàng, mỗi hàng 7 ô vuông đơn vị. Diện tích bằng bao nhiêu ô?|28|4 × 7 = 28 ô.
Hình chữ nhật dài 9 cm, rộng 2 cm có diện tích bao nhiêu cm²?|18|9 × 2 = 18 cm².
Hình vuông cạnh 8 cm có diện tích bao nhiêu cm²?|64|8 × 8 = 64 cm².
Hình chữ nhật diện tích 35 cm², rộng 5 cm. Dài bao nhiêu cm?|7|35 : 5 = 7 cm.""",
    ),
    unit(
        "statistics",
        "tables",
        "Đọc bảng số liệu và kiểm đếm",
        "Bảng ghi tên nhóm và số lượng. Đọc đúng hàng, so sánh các nhóm và cộng khi cần tìm tổng. Không suy ra điều mà bảng chưa ghi.",
        "Số cây ba tổ trồng: tổ 1 có 8, tổ 2 có 12, tổ 3 có 10. Tổng là 30 cây, tổ 2 nhiều nhất.",
        "Xem nhãn và đơn vị trước khi tính.",
        "Tìm hàng hoặc nhóm mà câu hỏi nhắc đến.|Viết các số cần dùng; không cộng những nhóm ngoài yêu cầu.|Kiểm tra kết quả với từng số trong bảng.",
        """Bảng cây trồng: tổ 1: 8; tổ 2: 12; tổ 3: 10. Tổng bao nhiêu cây?|30|8 + 12 + 10 = 30.
Bảng cây trồng: tổ 1: 8; tổ 2: 12; tổ 3: 10. Tổ 2 hơn tổ 1 bao nhiêu cây?|4|12 − 8 = 4.
Bảng sách: truyện 15, thơ 9, khoa học 12. Có tất cả bao nhiêu cuốn?|36|15 + 9 + 12 = 36.
Bảng sách: truyện 15, thơ 9, khoa học 12. Truyện và thơ có tổng bao nhiêu cuốn?|24|15 + 9 = 24.
Bảng bình nước: thứ hai 6, thứ ba 8, thứ tư 7. Tổng ba ngày bao nhiêu bình?|21|6 + 8 + 7 = 21.
Bảng bình nước: thứ hai 6, thứ ba 8, thứ tư 7. Ngày nhiều nhất có bao nhiêu bình?|8|So sánh 6, 8, 7: số lớn nhất là 8.""",
    ),
    unit(
        "wordproblems",
        "two-steps",
        "Bài toán hai bước và dữ kiện thừa",
        "Đọc câu hỏi cuối, chọn dữ kiện cần thiết rồi tìm một kết quả trung gian. Dữ kiện như màu hộp không nhất thiết dùng để tính.",
        "Có 3 hộp, mỗi hộp 8 bút, tặng 5 bút. Còn 3 × 8 − 5 = 19 bút.",
        "Viết lời giải cho mỗi bước và nêu đơn vị.",
        "Đề cần biết số còn lại hay tổng ban đầu?|Tìm tổng trước khi bớt hoặc chia.|Thay kết quả vào tình huống để xem có hợp lý không.",
        """4 túi, mỗi túi 6 cam, ăn 5 cam. Còn bao nhiêu cam?|19|4 × 6 − 5 = 19.
3 giá, mỗi giá 9 sách, thêm 7 sách. Có tổng bao nhiêu sách?|34|3 × 9 + 7 = 34.
5 hộp, mỗi hộp 8 bút, chia đều 4 bạn. Mỗi bạn bao nhiêu bút?|10|5 × 8 = 40; 40 : 4 = 10.
Có 36 hoa, thêm 12 hoa, cắm đều 6 lọ. Mỗi lọ bao nhiêu hoa?|8|(36 + 12) : 6 = 8.
2 rổ màu đỏ, mỗi rổ 15 táo, bán 9 táo. Còn bao nhiêu táo?|21|Màu đỏ không dùng để tính: 2 × 15 − 9 = 21.
Lan có 18 nhãn, Minh có hơn Lan 7 nhãn. Hai bạn có tổng bao nhiêu nhãn?|43|Minh có 25; tổng 18 + 25 = 43.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "operations",
        "remainders",
        "Chia có dư và kiểm tra sai lầm",
        "Trong phép chia có dư, số bị chia bằng số chia nhân thương rồi cộng số dư. Số dư luôn nhỏ hơn số chia.",
        "29 : 4 được thương 7, dư 1 vì 4 × 7 + 1 = 29. Thương 6 dư 5 chưa đúng quy tắc.",
        "Không bỏ số dư trong bài toán chia đồ vật.",
        "Nhìn số chia và số dư.|Thử nhân thương với số chia, cộng số dư rồi so với số bị chia.|Nếu số dư không nhỏ hơn số chia, phải chia thêm một lượt.",
        """29 : 4 có số dư là bao nhiêu?|1|4 × 7 = 28; 29 − 28 = 1.
38 : 5 có thương là bao nhiêu?|7|5 × 7 = 35, còn dư 3.
47 : 6 có số dư là bao nhiêu?|5|6 × 7 = 42, còn dư 5.
Số chia là 7, thương là 8, dư 3. Số bị chia là bao nhiêu?|59|7 × 8 + 3 = 59.
26 : 3 có thương là bao nhiêu?|8|3 × 8 = 24, còn dư 2.
Số dư lớn nhất trong phép chia cho 9 là bao nhiêu?|8|Số dư nhỏ hơn 9 nên lớn nhất là 8.
65 : 8 có số dư là bao nhiêu?|1|8 × 8 + 1 = 65.
Số chia 6, thương 12, dư 4. Số bị chia là bao nhiêu?|76|6 × 12 + 4 = 76.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "wordproblems",
        "enough-boxes",
        "Đủ hộp cho tất cả đồ vật",
        "Nếu còn đồ vật sau khi chia thành các hộp đầy, cần thêm một hộp. Phân biệt số hộp đầy với số hộp đủ để chứa tất cả.",
        "17 quả, mỗi hộp chứa tối đa 5 quả: có 3 hộp đầy và dư 2 quả, cần ít nhất 4 hộp.",
        "Từ ít nhất và tối đa quyết định cách trả lời.",
        "Tìm sức chứa tối đa mỗi hộp.|Chia có dư để biết số hộp đầy; còn dư thì thêm một hộp.|Nhân số hộp với sức chứa và kiểm tra bớt một hộp có đủ không.",
        """23 bánh, mỗi hộp tối đa 6 bánh. Cần ít nhất bao nhiêu hộp?|4|3 hộp chứa 18, còn 5 bánh nên cần hộp thứ tư.
32 bút, mỗi hộp tối đa 8 bút. Cần ít nhất bao nhiêu hộp?|4|Chia hết 32 : 8 = 4.
19 học sinh, mỗi nhóm tối đa 4 bạn. Cần ít nhất bao nhiêu nhóm?|5|4 nhóm mới chứa 16 bạn, cần nhóm thứ năm.
45 hoa, mỗi lọ tối đa 7 hoa. Cần ít nhất bao nhiêu lọ?|7|6 lọ chứa 42, còn 3 hoa cần thêm lọ.
26 quyển, mỗi túi tối đa 5 quyển. Cần ít nhất bao nhiêu túi?|6|5 túi chứa 25, còn một quyển.
50 viên, mỗi hộp tối đa 9 viên. Cần ít nhất bao nhiêu hộp?|6|5 hộp chứa 45, còn 5 viên cần hộp thứ sáu.
36 bánh, mỗi hộp tối đa 6 bánh. Cần ít nhất bao nhiêu hộp?|6|36 chia hết cho 6.
41 cam, mỗi rổ tối đa 8 cam. Cần ít nhất bao nhiêu rổ?|6|5 rổ chứa 40, còn một cam.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "measurement",
        "shopping",
        "Đi chợ nhỏ và tính tiền thừa",
        "Tính tiền mua đủ số món rồi so với số tiền mang theo. Nếu mua được, lấy tiền đưa trừ tiền hàng để tìm tiền thừa.",
        "Ba bút giá 4 000 đồng mỗi chiếc hết 12 000 đồng; đưa 20 000 đồng, nhận lại 8 000 đồng.",
        "Giá một món khác với tiền của tất cả món.",
        "Ghi số món và giá mỗi món.|Nhân để tính tổng tiền hàng, sau đó mới trừ tiền đưa.|Cộng tiền hàng và tiền thừa để kiểm tra.",
        """Mua 4 bút giá 3 000 đồng/bút. Hết bao nhiêu đồng?|12000|4 × 3 000 = 12 000 đồng.
Mua 2 vở giá 7 000 đồng/vở, đưa 20 000 đồng. Thừa bao nhiêu đồng?|6000|20 000 − 14 000 = 6 000 đồng.
Mua 3 bánh giá 5 000 đồng/bánh, đưa 50 000 đồng. Thừa bao nhiêu đồng?|35000|50 000 − 15 000 = 35 000 đồng.
Có 24 000 đồng, bút giá 4 000 đồng/chiếc. Mua tối đa bao nhiêu bút?|6|24 000 : 4 000 = 6.
Một vở 8 000 đồng, một bút 3 000 đồng. Mua cả hai hết bao nhiêu đồng?|11000|8 000 + 3 000 = 11 000.
Mua 5 nhãn giá 2 000 đồng/nhãn, đưa 20 000 đồng. Thừa bao nhiêu đồng?|10000|20 000 − 5 × 2 000 = 10 000.
Mua 2 vở 6 000 đồng/vở và bút 4 000 đồng. Hết bao nhiêu đồng?|16000|2 × 6 000 + 4 000 = 16 000.
Có 15 000 đồng; món đồ giá 18 000 đồng. Thiếu bao nhiêu đồng?|3000|18 000 − 15 000 = 3 000 đồng.""",
        vip=True,
    ),
    unit(
        "geometry",
        "same-perimeter",
        "Cùng chu vi, khác diện tích",
        "Hai hình có cùng đường bao chưa chắc có cùng diện tích. Lập bảng chiều dài, chiều rộng rồi tính riêng chu vi và diện tích.",
        "Hình 5 cm × 1 cm và hình 4 cm × 2 cm đều có chu vi 12 cm nhưng diện tích lần lượt 5 và 8 cm².",
        "Không dùng kết quả chu vi để kết luận diện tích.",
        "Ghi rõ hai kích thước của từng hình.|Tính chu vi và diện tích ở hai cột khác nhau.|So sánh từng đại lượng, chú ý đơn vị.",
        """Hình 6 cm × 2 cm có chu vi bao nhiêu cm?|16|(6 + 2) × 2 = 16.
Hình 6 cm × 2 cm có diện tích bao nhiêu cm²?|12|6 × 2 = 12.
Hình 5 cm × 3 cm có chu vi bao nhiêu cm?|16|(5 + 3) × 2 = 16.
Hình 5 cm × 3 cm có diện tích bao nhiêu cm²?|15|5 × 3 = 15.
Hình chữ nhật 6 cm × 2 cm và hình chữ nhật 5 cm × 3 cm có diện tích chênh nhau bao nhiêu cm²?|3|15 − 12 = 3.
Hình vuông chu vi 16 cm có diện tích bao nhiêu cm²?|16|Cạnh là 16 : 4 = 4; diện tích 4 × 4 = 16.
Hình chữ nhật chu vi 20 cm, rộng 3 cm. Dài bao nhiêu cm?|7|Nửa chu vi là 10, dài 10 − 3 = 7.
Hình chữ nhật dài 7 cm, rộng 3 cm có diện tích bao nhiêu cm²?|21|7 × 3 = 21.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "wordproblems",
        "intervals",
        "Khoảng cách giữa các cột mốc",
        "Với các cột xếp trên một đường thẳng và có cột ở cả hai đầu, số khoảng ít hơn số cột một. Vẽ hình để phân biệt cột và khoảng.",
        "Bốn cột có ba khoảng. Mỗi khoảng 2 m, khoảng cách từ cột đầu đến cột cuối là 6 m.",
        "Quy tắc này chỉ áp dụng khi đã nói rõ có cột ở cả hai đầu đoạn thẳng.",
        "Vẽ các cột thành chấm trên một đường.|Đếm các đoạn nối giữa chấm liền nhau, không đếm chấm.|Nhân số khoảng với độ dài một khoảng rồi kiểm tra bằng hình.",
        """6 cột trên đường thẳng, cả hai đầu có cột. Có bao nhiêu khoảng giữa cột liền nhau?|5|Sáu cột tạo năm khoảng.
5 cột thẳng hàng, mỗi khoảng 3 m. Hai cột đầu cuối cách nhau bao nhiêu m?|12|4 khoảng × 3 m = 12 m.
Đoạn 20 m, hai đầu có cột và cứ 5 m một cột. Có bao nhiêu cột?|5|20 : 5 = 4 khoảng, có 5 cột.
8 cột thẳng hàng, mỗi khoảng 2 m. Hai cột đầu cuối cách nhau bao nhiêu m?|14|7 × 2 = 14 m.
4 cột thẳng hàng, mỗi khoảng 6 m. Hai cột đầu cuối cách nhau bao nhiêu m?|18|3 × 6 = 18 m.
Đoạn 24 m, hai đầu có cột, mỗi khoảng 4 m. Có bao nhiêu cột?|7|6 khoảng nên có 7 cột.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "chance",
        "possible",
        "Có thể, chắc chắn, không thể",
        "Xem tất cả đồ vật có trong túi trước khi nhận xét. Chắc chắn là mọi lựa chọn đều đúng; không thể là không có lựa chọn phù hợp; có thể là có nhưng chưa chắc.",
        "Túi chỉ có bi đỏ và xanh: lấy được đỏ là có thể; lấy được vàng là không thể; lấy được đỏ hoặc xanh là chắc chắn.",
        "Không cần công thức xác suất hay đoán màu sẽ xuất hiện tiếp theo.",
        "Liệt kê các loại đồ vật thật sự có trong túi.|Đối chiếu điều kiện với tất cả loại đã liệt kê.|Đừng coi kết quả lần trước là điều đảm bảo cho lần sau.",
        """Túi có 4 bi đỏ và 3 bi xanh. Có bao nhiêu màu có thể lấy được?|2|Có đỏ và xanh: hai màu.
Túi chỉ có 5 bi đỏ. Có bao nhiêu bi vàng trong túi?|0|Không có bi vàng nên không thể lấy bi vàng.
Túi có 2 bi xanh và 6 bi đỏ. Tổng bao nhiêu bi?|8|2 + 6 = 8 bi.
Hộp có 3 thẻ ghi A, 4 thẻ ghi B. Có bao nhiêu loại chữ có thể lấy được?|2|Chỉ có hai chữ A và B.
Túi chỉ có 9 bi xanh. Có bao nhiêu bi mang màu xanh?|9|Cả chín bi đều xanh nên chắc chắn lấy được xanh.
Túi có 3 bi đỏ, 2 bi vàng, 1 bi xanh. Có bao nhiêu màu có thể lấy được?|3|Ba màu khác nhau có mặt trong túi.""",
        vip=True,
        thinking=True,
    ),
]
