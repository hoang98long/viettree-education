"""Grade-five maths: exact decimal/fraction arithmetic and familiar situations."""

from decimal import Decimal as D
from fractions import Fraction as F

from app.curriculum.grades.grade_05.builders import numeric, question_count, unit


def exercise(code, position):
    n = position + 1
    if code == "natural-review":
        a, b = 120 + n, 30 + n
        if position % 4 == 0:
            return (
                f"Có {a} quyển sách và thêm {b} quyển. Tổng số sách?",
                a + b,
                f"Cộng hai số: {a} + {b} = {a + b}.",
            )
        if position % 4 == 1:
            return (
                f"Có {a} quyển, cho mượn {b} quyển. Còn bao nhiêu?",
                a - b,
                f"Số còn lại là {a} − {b} = {a - b}.",
            )
        if position % 4 == 2:
            return (
                f"Có {n + 2} hộp, mỗi hộp 12 bút. Tổng số bút?",
                (n + 2) * 12,
                "Nhân số hộp với số bút trong một hộp.",
            )
        return f"Chia đều {n * 8} bút vào 8 hộp. Mỗi hộp bao nhiêu bút?", n, f"{n * 8} : 8 = {n}."
    if code == "fraction-review":
        if position == 0:
            return "Tính 2/5 + 2/5; viết tối giản.", F(4, 5), "Cộng tử số, giữ mẫu số."
        if position == 1:
            return "Tính 5/5 − 2/5; viết tối giản.", F(3, 5), "Trừ tử số, giữ mẫu số."
        if position == 2:
            return (
                "Tính 4/5 × 2/3; viết tối giản.",
                F(8, 15),
                "Nhân tử với tử, mẫu với mẫu rồi rút gọn.",
            )
        return (
            "Tính 5/5 : 2/3; viết tối giản.",
            F(3, 2),
            "Nhân phân số thứ nhất với phân số đảo của số chia: 5/5 × 3/2.",
        )
    if code == "decimal-place":
        return (
            f"Trong số 12,{n}6, chữ số {n} ở hàng phần mười có giá trị bao nhiêu?",
            D(n) / 10,
            "Hàng phần mười có giá trị bằng chữ số đó chia 10.",
        )
    if code == "decimal-order":
        a = D(n) + D("0.46")
        if position % 2 == 0:
            return (
                f"Làm tròn {str(a).replace('.', ',')} đến số tự nhiên gần nhất.",
                n,
                "Chữ số hàng phần mười là 4 nên giữ phần nguyên.",
            )
        return (
            f"Làm tròn {str(a).replace('.', ',')} đến hàng phần mười.",
            D(n) + D("0.5"),
            "Hàng phần trăm là 6 nên tăng hàng phần mười một đơn vị.",
        )
    if code == "decimal-add-subtract":
        if position % 2 == 0:
            return (
                f"Tính {n + 2},35 + 1,4.",
                D(n) + D("3.75"),
                "Đặt các dấu phẩy thẳng cột; viết 1,4 thành 1,40 rồi cộng.",
            )
        return (
            f"Tính {n + 5},7 − 2,45.",
            D(n) + D("3.25"),
            "Viết thêm chữ số 0 ở phần thập phân, đặt dấu phẩy thẳng cột rồi trừ.",
        )
    if code == "decimal-multiply-divide":
        if position % 2 == 0:
            return (
                f"Tính {n + 1},5 × 2.",
                2 * n + 3,
                "Nhân như số tự nhiên rồi đặt dấu phẩy; kiểm tra bằng cộng hai lần.",
            )
        return (
            f"Tính {n + 3} : 0,5.",
            2 * n + 6,
            "Nhân số bị chia và số chia với 10: chia cho 5 rồi kiểm tra bằng phép nhân.",
        )
    if code == "percent-basics":
        if position % 2 == 0:
            return (
                f"Có {n} bạn trong nhóm 20 bạn. Nhóm nhỏ chiếm bao nhiêu phần trăm?",
                5 * n,
                "Lấy số bạn nhóm nhỏ chia 20 rồi nhân 100.",
            )
        return f"Tìm 25% của {8 * n} quyển sách.", 2 * n, "25% là một phần tư; chia số sách cho 4."
    if code == "sum-difference-ratio":
        if position % 2 == 0:
            return (
                f"Hai ngăn có tổng {4 * n} quyển, tỉ số ngăn ít : ngăn nhiều là 1 : 3. Ngăn nhiều có bao nhiêu?",
                3 * n,
                "Tổng có 4 phần; một phần bằng tổng chia 4, ngăn nhiều có 3 phần.",
            )
        return (
            f"Hai ngăn chênh {2 * n} quyển, tỉ số ít : nhiều là 1 : 3. Ngăn nhiều có bao nhiêu?",
            3 * n,
            "Hiệu có 2 phần; một phần bằng hiệu chia 2, ngăn nhiều có 3 phần.",
        )
    if code == "area-units":
        if position % 3 == 0:
            return f"Đổi {n},5 ha sang m².", (D(n) + D("0.5")) * 10000, "1 ha = 10 000 m²."
        if position % 3 == 1:
            return f"Đổi {n} km² sang m².", n * 1000000, "1 km² = 1 000 000 m²."
        return f"Đổi {n * 10000} m² sang ha.", n, "Chia số mét vuông cho 10 000."
    if code == "volume-units":
        if position % 2 == 0:
            return (
                f"Đổi {n} dm³ sang cm³.",
                1000 * n,
                "1 dm³ = 1000 cm³, vì mỗi chiều đổi từ dm sang cm tăng 10 lần.",
            )
        return f"Đổi {1000 * n} cm³ sang dm³.", n, "Chia số xăng-ti-mét khối cho 1000."
    if code == "triangle-area":
        base, height = n + 5, 4 if position % 2 == 0 else 6
        return (
            f"Tam giác có đáy {base} cm, chiều cao vuông góc {height} cm. Diện tích bao nhiêu cm²?",
            base * height // 2,
            "Diện tích = đáy × chiều cao : 2; chiều cao vuông góc với đáy.",
        )
    if code == "trapezoid-area":
        return (
            f"Hình thang có hai đáy {n + 7} cm, {n + 3} cm và chiều cao 3 cm. Diện tích bao nhiêu cm²?",
            3 * n + 15,
            "Diện tích = (đáy lớn + đáy bé) × chiều cao : 2.",
        )
    if code == "circle-measures":
        r = n + 1
        if position % 3 == 0:
            return (
                f"Đường tròn bán kính {r} cm. Lấy π ≈ 3,14; chu vi bao nhiêu cm?",
                D("6.28") * r,
                "Chu vi = 2 × bán kính × 3,14.",
            )
        if position % 3 == 1:
            return (
                f"Hình tròn bán kính {r} cm. Lấy π ≈ 3,14; diện tích bao nhiêu cm²?",
                D("3.14") * r * r,
                "Diện tích = bán kính × bán kính × 3,14.",
            )
        return (
            f"Đường tròn có đường kính {2 * r} cm. Bán kính bao nhiêu cm?",
            r,
            "Bán kính bằng một nửa đường kính.",
        )
    if code == "solid-nets":
        tasks = [
            (
                "Hình lập phương có bao nhiêu mặt hình vuông?",
                6,
                "Hình lập phương có 6 mặt bằng nhau.",
            ),
            ("Hình lập phương có bao nhiêu cạnh?", 12, "Mỗi trong ba hướng có 4 cạnh: 3 × 4 = 12."),
            (
                "Hình lập phương có bao nhiêu đỉnh?",
                8,
                "Quan sát 4 đỉnh phía trên và 4 đỉnh phía dưới.",
            ),
            (
                f"Sáu mặt hình vuông cạnh {n} cm của hình lập phương có tổng diện tích bao nhiêu cm²?",
                6 * n * n,
                "Tính diện tích một mặt rồi nhân 6.",
            ),
            (
                "Hình khai triển của hình trụ có bao nhiêu mặt đáy hình tròn?",
                2,
                "Hai đáy của hình trụ là hai hình tròn bằng nhau.",
            ),
            (
                "Sáu mặt của hình hộp chữ nhật tạo thành bao nhiêu cặp mặt đối diện?",
                3,
                "Mặt trên/dưới, trước/sau, trái/phải tạo thành 3 cặp.",
            ),
        ]
        return tasks[position]
    if code == "surface-area":
        if position % 2 == 0:
            return (
                f"Hộp chữ nhật dài {n + 5} cm, rộng 4 cm, cao 3 cm. Diện tích xung quanh bao nhiêu cm²?",
                6 * n + 54,
                "Lấy chu vi mặt đáy nhân chiều cao: 2 × (dài + rộng) × cao.",
            )
        return (
            f"Hộp chữ nhật dài {n + 5} cm, rộng 4 cm, cao 3 cm. Diện tích toàn phần bao nhiêu cm²?",
            14 * n + 94,
            "Cộng diện tích xung quanh với hai lần diện tích đáy.",
        )
    if code == "solid-volume":
        if position % 2 == 0:
            return (
                f"Hộp chữ nhật dài {n + 5} cm, rộng 4 cm, cao 3 cm. Thể tích bao nhiêu cm³?",
                12 * n + 60,
                "Thể tích = chiều dài × chiều rộng × chiều cao.",
            )
        return (
            f"Hình lập phương cạnh {n + 1} cm. Thể tích bao nhiêu cm³?",
            (n + 1) ** 3,
            "Nhân cạnh với chính nó ba lần; không nhầm với diện tích 6 mặt.",
        )
    if code == "steady-motion":
        if position % 3 == 0:
            return (
                f"Xe đi đều {20 * (n + 1)} km trong 2 giờ. Vận tốc bao nhiêu km/h?",
                10 * (n + 1),
                "Vận tốc = quãng đường : thời gian.",
            )
        if position % 3 == 1:
            return (
                f"Xe đi đều {10 * (n + 1)} km/h trong 3 giờ. Quãng đường bao nhiêu km?",
                30 * (n + 1),
                "Quãng đường = vận tốc × thời gian.",
            )
        return (
            f"Đi đều quãng đường {12 * (n + 1)} km với vận tốc 6 km/h. Thời gian bao nhiêu giờ?",
            2 * (n + 1),
            "Thời gian = quãng đường : vận tốc; thống nhất đơn vị trước khi tính.",
        )
    if code == "statistics-basics":
        if position % 3 == 0:
            total = 20 * (n + 1)
            return (
                f"Biểu đồ: đọc sách 50%, thể thao 30%, âm nhạc 20%; có {total} bạn. Bao nhiêu bạn chọn đọc sách?",
                total // 2,
                "50% bằng một nửa tổng số bạn.",
            )
        if position % 3 == 1:
            return (
                f"Có {10 * (n + 1)} bạn, 30% chọn thể thao. Bao nhiêu bạn chọn thể thao?",
                3 * (n + 1),
                "Nhân tổng số bạn với 30 rồi chia 100.",
            )
        return (
            f"Thí nghiệm có {2 * n} lần mặt sấp trong {5 * n} lần tung. Tỉ số số lần sấp trên tổng lần tung, viết tối giản?",
            F(2, 5),
            "Tỉ số là số lần đã quan sát chia tổng lần thực hiện; không bảo đảm kết quả lần tung sau.",
        )
    if code == "map-scale":
        if position % 2 == 0:
            return (
                f"Bản đồ tỉ lệ 1 : 1000; đoạn đường dài {n},5 cm trên bản đồ. Thực tế bao nhiêu mét?",
                D(n * 10 + 5),
                "Nhân độ dài bản đồ với 1000 để được cm; chia 100 để đổi sang m.",
            )
        return (
            f"Đường thực dài {200 * n} m, bản đồ tỉ lệ 1 : 10 000. Trên bản đồ dài bao nhiêu cm?",
            2 * n,
            "Đổi m sang cm rồi chia 10 000.",
        )
    if code == "discount-budget":
        price = 40000 * n
        return (
            f"Áo giá {price} đồng, giảm 15%. Giá phải trả bao nhiêu đồng?",
            34000 * n,
            "Tính 15% giá ban đầu rồi trừ đi số tiền giảm; không lấy 15% của giá mới.",
        )
    if code == "pie-reasoning":
        total = 20 * (n + 1)
        return (
            f"Trong {total} bạn: đọc sách 50%, thể thao 30%, âm nhạc 20%. Đọc sách nhiều hơn thể thao bao nhiêu bạn?",
            4 * (n + 1),
            "Chênh lệch 50% − 30% = 20% của tổng số bạn.",
        )
    if code == "observed-ratios":
        return (
            f"Lấy bóng rồi trả lại hộp: {3 * n} lần đỏ trong {10 * n} lần thử. Tỉ số quan sát, viết tối giản?",
            F(3, 10),
            "Viết số lần đỏ trên tổng lần thử rồi rút gọn; đó là kết quả đã quan sát.",
        )
    if code == "composite-area":
        return (
            f"Tấm giấy chữ nhật {n + 2} cm × 6 cm; cắt đi tam giác đáy 2 cm, cao 3 cm. Diện tích còn lại bao nhiêu cm²?",
            6 * n + 9,
            "Tính diện tích chữ nhật, tính diện tích tam giác rồi lấy hiệu.",
        )
    if code == "motion-with-rest":
        return (
            f"Xe đi {24 * n} km với vận tốc đều 12 km/h, nghỉ thêm 30 phút. Tổng thời gian cả nghỉ bao nhiêu giờ?",
            D(2 * n) + D("0.5"),
            "Thời gian chạy = quãng đường : vận tốc; 30 phút = 0,5 giờ, cộng thời gian nghỉ.",
        )
    if code == "four-step-budget":
        return (
            f"Mua {3 * n} vở giá 12 000 đồng/vở và {2 * n} bút giá 5000 đồng/bút; trả {50000 * n} đồng. Tiền thừa bao nhiêu?",
            4000 * n,
            "Bước 1 tính tiền vở; bước 2 tiền bút; bước 3 cộng; bước 4 lấy tiền trả trừ tiền mua.",
        )
    raise ValueError(code)


# Topic, stable suffix, title, rule. First four topic pairs share foundation assessments.
SPECS = [
    (
        "fractions",
        "natural-review",
        "Ôn số tự nhiên và tính hợp lí",
        "Đọc kĩ việc thêm, bớt, gộp nhóm hoặc chia đều trước khi chọn phép tính. Có thể ước lượng rồi kiểm tra bằng phép tính ngược.",
    ),
    (
        "fractions",
        "fraction-review",
        "Phân số, rút gọn và hỗn số",
        "Cộng/trừ cùng mẫu: cộng/trừ tử, giữ mẫu; khác mẫu cần quy đồng. Nhân: tử nhân tử, mẫu nhân mẫu. Chia: nhân với phân số đảo của số chia khác 0. Rút gọn tử và mẫu cùng số; 7/5 = 1 và 2/5.",
    ),
    (
        "decimals",
        "decimal-place",
        "Đọc số thập phân và các hàng",
        "Số thập phân có phần nguyên và phần thập phân. Sau dấu phẩy lần lượt là phần mười, phần trăm, phần nghìn. Chữ số có giá trị tùy vị trí, không phải chỉ tùy hình dạng.",
    ),
    (
        "decimals",
        "decimal-order",
        "So sánh và làm tròn số thập phân",
        "So phần nguyên trước, rồi từng hàng thập phân; có thể viết thêm 0 bên phải. Làm tròn nhìn hàng ngay sau hàng cần giữ: từ 5 trở lên tăng 1, dưới 5 giữ nguyên.",
    ),
    (
        "operations",
        "decimal-add-subtract",
        "Cộng và trừ số thập phân",
        "Đặt dấu phẩy thẳng cột; viết thêm 0 khi cần. Thực hiện cộng hoặc trừ như số tự nhiên, giữ dấu phẩy đúng cột và kiểm tra bằng ước lượng.",
    ),
    (
        "operations",
        "decimal-multiply-divide",
        "Nhân, chia số thập phân đơn giản",
        "Nhân chú ý số chữ số thập phân của thừa số. Chia cho số thập phân thì cùng nhân số bị chia và số chia với 10 hoặc 100 để số chia là số tự nhiên. Chia cho 0,5 tương đương nhân 2.",
    ),
    (
        "ratio",
        "percent-basics",
        "Tỉ số và tỉ số phần trăm",
        "Tỉ số phần trăm = số phần cần xét : tổng × 100%. Tìm p% của một số bằng số đó × p : 100. Phải xác định đúng tổng đang được nói đến.",
    ),
    (
        "ratio",
        "sum-difference-ratio",
        "Tìm hai số từ tổng hoặc hiệu và tỉ số",
        "Vẽ sơ đồ đoạn thẳng theo các phần bằng nhau. Tổng thì cộng số phần, hiệu thì trừ số phần; tìm một phần rồi nhân số phần của từng đại lượng. Kiểm tra lại tổng hoặc hiệu.",
    ),
    (
        "measurement",
        "area-units",
        "Héc-ta, ki-lô-mét vuông và mét vuông",
        "1 ha = 10 000 m²; 1 km² = 1 000 000 m² = 100 ha. Đơn vị diện tích đổi theo bình phương độ dài, không đổi như cm sang m.",
    ),
    (
        "measurement",
        "volume-units",
        "Đơn vị thể tích và thời gian",
        "1 dm³ = 1000 cm³; 1 m³ = 1000 dm³. Thể tích đo phần không gian vật chiếm. Với thời gian, 1 giờ = 60 phút; 30 phút = 0,5 giờ, không phải 0,30 giờ.",
    ),
    (
        "geometry",
        "triangle-area",
        "Đáy, chiều cao và diện tích tam giác",
        "Chiều cao là đoạn vuông góc từ một đỉnh đến đường chứa đáy. Diện tích tam giác = đáy × chiều cao : 2. Không dùng cạnh xiên thay chiều cao.",
    ),
    (
        "geometry",
        "trapezoid-area",
        "Hai đáy và diện tích hình thang",
        "Hai đáy của hình thang nằm trên hai đường song song. Chiều cao là khoảng cách vuông góc giữa chúng. Diện tích = (đáy lớn + đáy bé) × chiều cao : 2.",
    ),
    (
        "geometry",
        "circle-measures",
        "Bán kính, đường kính và hình tròn",
        "Đường kính gấp đôi bán kính. Với π lấy gần đúng 3,14: chu vi = 2 × r × 3,14; diện tích = r × r × 3,14. Ghi đúng đơn vị cm hoặc cm².",
    ),
    (
        "solids",
        "solid-nets",
        "Hình khai triển và các mặt của khối",
        "Hình lập phương có 6 mặt vuông, 12 cạnh, 8 đỉnh. Hộp chữ nhật có ba cặp mặt đối diện bằng nhau; hình trụ có hai đáy tròn và mặt bên khi trải phẳng. Hãy thử gấp mô hình giấy cùng người lớn.",
    ),
    (
        "solids",
        "surface-area",
        "Diện tích xung quanh và toàn phần",
        "Hộp chữ nhật: diện tích xung quanh = chu vi đáy × chiều cao; toàn phần = xung quanh + hai đáy. Hình lập phương cạnh a: xung quanh gồm 4 mặt, toàn phần gồm 6 mặt vuông.",
    ),
    (
        "solids",
        "solid-volume",
        "Thể tích hộp chữ nhật và lập phương",
        "Thể tích hộp chữ nhật = dài × rộng × cao; lập phương = cạnh × cạnh × cạnh. Các chiều cùng đơn vị; kết quả là đơn vị khối. Thực hành xếp các khối đơn vị để hiểu thể tích.",
    ),
    (
        "motion",
        "steady-motion",
        "Vận tốc, quãng đường và thời gian",
        "Trong chuyển động đều: vận tốc = quãng đường : thời gian; quãng đường = vận tốc × thời gian; thời gian = quãng đường : vận tốc. Thống nhất km/giờ hoặc m/giây trước khi tính.",
    ),
    (
        "statistics",
        "statistics-basics",
        "Đọc biểu đồ quạt tròn và tỉ số quan sát",
        "Các phần trăm trên biểu đồ quạt tròn cộng thành 100%. Phần lớn hơn đại diện tỉ lệ lớn hơn. Tỉ số quan sát = số lần một kết quả đã xảy ra : tổng lần thử; không khẳng định lần sau sẽ giống.",
    ),
    (
        "ratio",
        "map-scale",
        "Tư duy: tỉ lệ bản đồ và đổi đơn vị",
        "Tỉ lệ 1 : k nghĩa là 1 đơn vị trên bản đồ bằng k đơn vị thực tế. Nhân hoặc chia theo tỉ lệ rồi đổi đơn vị, không bỏ qua bước cm sang m.",
    ),
    (
        "ratio",
        "discount-budget",
        "Tư duy: giá giảm và tiền phải trả",
        "Giá giảm là phần trăm của giá ban đầu. Tính tiền giảm rồi trừ khỏi giá ban đầu; kiểm tra số phải trả nhỏ hơn giá gốc và không âm.",
    ),
    (
        "statistics",
        "pie-reasoning",
        "Tư duy: so sánh nhóm từ biểu đồ",
        "Hai nhóm dùng chung tổng thì chênh lệch số lượng bằng chênh lệch phần trăm của tổng. Tính từng nhóm hoặc tính phần trăm chênh lệch rồi đối chiếu.",
    ),
    (
        "statistics",
        "observed-ratios",
        "Tư duy: thí nghiệm nói được điều gì?",
        "Ghi số lần đã thử và số lần mỗi kết quả, rút gọn tỉ số. Dữ liệu là quan sát của lượt thử này; một tỉ số không cho phép nói chắc kết quả tiếp theo.",
    ),
    (
        "geometry",
        "composite-area",
        "Tư duy: diện tích phần còn lại",
        "Tách hình thành những phần đã biết công thức. Phần bị cắt phải trừ, phần ghép thêm phải cộng. Phân biệt diện tích và chu vi khi giải thích kết quả.",
    ),
    (
        "motion",
        "motion-with-rest",
        "Tư duy: thời gian chạy và nghỉ",
        "Công thức chuyển động đều chỉ tính lúc đang chạy. Tổng hành trình cộng thêm thời gian nghỉ, đổi phút sang giờ đúng trước khi cộng. Không lấy thời gian nghỉ để tính thêm quãng đường.",
    ),
    (
        "operations",
        "four-step-budget",
        "Tư duy: lập kế hoạch mua trong ngân sách",
        "Tính riêng từng loại hàng, cộng tiền mua rồi so với tiền trả. Ghi các bước có đơn vị đồng; kiểm tra tiền mua không vượt ngân sách và đối chiếu tiền thừa.",
    ),
]

FIGURES = {
    "triangle-area": dict(
        kind="triangle",
        base=6,
        height=4,
        caption="Ví dụ: tam giác đáy 6 cm, cao 4 cm vuông góc; diện tích 12 cm².",
    ),
    "trapezoid-area": dict(
        kind="trapezoid",
        base=8,
        upper_base=4,
        height=3,
        caption="Ví dụ: hai đáy 8 cm và 4 cm, cao 3 cm; diện tích 18 cm².",
    ),
    "circle-measures": dict(
        kind="circle",
        radius=2,
        caption="Ví dụ: bán kính 2 cm, đường kính 4 cm; chu vi gần đúng 12,56 cm.",
    ),
    "surface-area": dict(
        kind="box",
        length=6,
        width=4,
        height=3,
        caption="Ví dụ: hộp chữ nhật dài 6 cm, rộng 4 cm, cao 3 cm; xung quanh 60 cm².",
    ),
    "solid-volume": dict(
        kind="box",
        length=6,
        width=4,
        height=3,
        caption="Ví dụ: hộp 6 × 4 × 3 cm có thể tích 72 cm³.",
    ),
    "statistics-basics": dict(
        kind="pie",
        values=[50, 30, 20],
        labels=["Đọc sách", "Thể thao", "Âm nhạc"],
        caption="Ví dụ: đọc sách 50%, thể thao 30%, âm nhạc 20%; tổng 100%.",
    ),
    "pie-reasoning": dict(
        kind="pie",
        values=[50, 30, 20],
        labels=["Đọc sách", "Thể thao", "Âm nhạc"],
        caption="Cùng một tổng: đọc sách hơn thể thao 20 điểm phần trăm.",
    ),
}

MATH = []
for index, (topic, code, title, rule) in enumerate(SPECS):
    questions = []
    for position in range(question_count("MATH", index)):
        prompt, value, reason = exercise(code, position)
        questions.append(numeric(prompt, value, reason, position, 3 if index >= 18 else 2))
    prompt, value, reason = exercise(code, 0)
    worked = f"{prompt}\nKết quả: {str(value).replace('.', ',')}. {reason}"
    MATH.append(
        unit(
            "MATH",
            index,
            topic,
            code,
            title,
            rule,
            worked,
            "Viết rõ dữ kiện, thống nhất đơn vị, tính từng bước rồi kiểm tra bằng cách khác.",
            [
                "Đọc lại yêu cầu và xác định số nào là tổng, số nào là phần hoặc số đo.",
                rule,
                "Kiểm tra đơn vị, ước lượng kết quả; phép cộng/trừ có thể kiểm tra bằng phép tính ngược.",
            ],
            questions,
            illustration=FIGURES.get(code),
        )
    )
