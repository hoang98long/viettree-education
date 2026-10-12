"""Grade 1: no-carry arithmetic to 100; grade 2: to 1000, tables 2/5, one-step problems."""

from app.early_primary_support import build, cards, counters, numeric


def curriculum(grade):
    items = []
    maximum = 100 if grade == 1 else 1000

    def n(prompt, value, why):
        return numeric(prompt, value, why, maximum)

    def c(prompt, answer, first, second, why):
        return prompt, answer, [first, second], why

    def calc(pairs, sign):
        return [
            n(
                f"{a} {sign} {b} = ?",
                a + b if sign == "+" else a - b,
                f"{a} {sign} {b} = {a + b if sign == '+' else a - b}.",
            )
            for a, b in pairs
        ]

    def add(topic, code, title, teaching, example, hints, rows, illustration=None, thinking=False):
        items.append(
            build(
                grade,
                "MATH",
                len(items),
                topic,
                code,
                title,
                teaching,
                example,
                "Em có thể dùng que tính, chỉ vào hình hoặc nhờ người lớn đọc yêu cầu.",
                hints,
                rows,
                illustration=illustration,
                thinking=thinking,
            )
        )

    if grade == 1:
        add(
            "numbers",
            "count-five",
            "Đếm từng vật từ 1 đến 5",
            "Chỉ vào từng chấm, đọc một số. Mỗi chấm chỉ đếm một lần.",
            "● ● ● có 3 chấm. Số cuối khi đếm cho biết có bao nhiêu chấm.",
            "Chỉ vào chấm đầu.|Chỉ lần lượt và đọc một, hai, ba.|Đếm lại, không bỏ hoặc đếm hai lần một chấm.",
            [
                n("● ● có mấy chấm?", 2, "Có 2 chấm."),
                n("● ● ● ● có mấy chấm?", 4, "Có 4 chấm."),
                n("● có mấy chấm?", 1, "Có 1 chấm."),
                n("● ● ● ● ● có mấy chấm?", 5, "Có 5 chấm."),
            ],
            counters(3),
        )
        add(
            "numbers",
            "zero-ten",
            "Số 0 và đếm đến 10",
            "Không có vật nào thì viết 0. Đếm thêm từ 6 đến 10 bằng từng ngón tay hoặc chấm.",
            "Đĩa trống có 0 quả. Hai nhóm 5 chấm có tất cả 10 chấm.",
            "Nhìn xem có vật nào không.|Đếm từng vật; đĩa trống dùng số 0.|Kiểm tra số cuối em vừa đọc.",
            [
                n("Đĩa không có quả nào. Có mấy quả?", 0, "Không có quả nào là 0 quả."),
                n("● ● ● ● ● ● có mấy chấm?", 6, "Đếm được 6 chấm."),
                n("● ● ● ● ● ● ● ● có mấy chấm?", 8, "Đếm được 8 chấm."),
                n("Số liền sau 9 là số nào?", 10, "Đếm tiếp sau 9 là 10."),
            ],
            counters(8),
        )
        add(
            "operations",
            "add-ten",
            "Gộp hai nhóm trong phạm vi 10",
            "Gộp hai nhóm đồ vật là thêm vào. Ta dùng dấu cộng +.",
            "Có 3 bút, thêm 2 bút: 3 + 2 = 5.",
            "Nhìn hai nhóm.|Đếm nhóm đầu rồi đếm tiếp nhóm sau.|Đếm cả hai nhóm để thử lại.",
            calc([(1, 2), (3, 1), (2, 3), (4, 2)], "+"),
            counters(5),
        )
        add(
            "operations",
            "subtract-ten",
            "Bớt đi trong phạm vi 10",
            "Bớt một số đồ vật thì dùng dấu trừ −. Đếm những vật còn lại.",
            "Có 5 quả, lấy đi 2 quả: 5 − 2 = 3.",
            "Tìm số vật lúc đầu.|Bớt đúng số vật được nói.|Đếm số vật còn lại.",
            calc([(4, 1), (5, 2), (6, 3), (8, 2)], "−"),
            counters(3),
        )
        add(
            "geometry",
            "flat-shapes",
            "Hình tròn, vuông, tam giác và chữ nhật",
            "Quan sát đường bao của hình. Có thể đặt ngón tay đi theo đường bao.",
            "○ là hình tròn; △ là hình tam giác; □ là hình vuông; ▭ là hình chữ nhật.",
            "Nhìn đường bao.|Hình tam giác có 3 cạnh; hình tròn có đường bao cong.|Đối chiếu hình với ví dụ.",
            [
                c(
                    "○ là hình gì?",
                    "Hình tròn",
                    "Hình vuông",
                    "Hình tam giác",
                    "○ có đường bao tròn.",
                ),
                c("△ là hình gì?", "Hình tam giác", "Hình tròn", "Hình chữ nhật", "△ có 3 cạnh."),
                c("□ là hình gì?", "Hình vuông", "Hình tròn", "Hình tam giác", "□ là hình vuông."),
                c(
                    "▭ là hình gì?",
                    "Hình chữ nhật",
                    "Hình tròn",
                    "Hình tam giác",
                    "▭ là hình chữ nhật.",
                ),
            ],
            cards(["○", "△", "□", "▭"], "Bốn hình phẳng: tròn, tam giác, vuông, chữ nhật."),
        )
        add(
            "geometry",
            "solid-shapes",
            "Nhìn khối hộp và khối lập phương",
            "Hộp là vật có thể cầm được. Khối lập phương có các mặt đều là hình vuông bằng nhau.",
            "Xúc xắc dạng khối lập phương. Hộp giày thường dạng khối hộp chữ nhật.",
            "Quan sát hộp thật cùng người lớn.|Xem các mặt đều vuông hay có mặt chữ nhật.|Gọi lại tên khối trong ví dụ.",
            [
                c(
                    "Xúc xắc có các mặt vuông bằng nhau giống khối nào?",
                    "Khối lập phương",
                    "Hình tròn",
                    "Hình tam giác",
                    "Xúc xắc có dạng khối lập phương.",
                ),
                c(
                    "Hộp giày dài giống khối nào?",
                    "Khối hộp chữ nhật",
                    "Hình tròn",
                    "Hình tam giác",
                    "Hộp giày thường có dạng khối hộp chữ nhật.",
                ),
                c(
                    "Hình vẽ ○ trên giấy là gì?",
                    "Hình phẳng",
                    "Khối hộp",
                    "Khối lập phương",
                    "○ trên giấy là hình phẳng.",
                ),
                c(
                    "Vật nào giống khối lập phương?",
                    "Xúc xắc",
                    "Tờ giấy tròn",
                    "Thước thẳng",
                    "Xúc xắc là vật có dạng khối lập phương.",
                ),
            ],
        )
        add(
            "measurement",
            "long-short",
            "Dài hơn, ngắn hơn",
            "Đặt hai vật chung một đầu rồi nhìn đầu kia. Vật vươn xa hơn thì dài hơn.",
            "Dải A dài 5 cm. Dải B dài 3 cm. A dài hơn B.",
            "Đặt chung một đầu.|Nhìn đầu còn lại hoặc so số đo.|Đọc lại vật dài hơn và ngắn hơn.",
            [
                c(
                    "A dài 5 cm, B dài 3 cm. Dải nào dài hơn?",
                    "A",
                    "B",
                    "Bằng nhau",
                    "5 cm dài hơn 3 cm.",
                ),
                c(
                    "A dài 2 cm, B dài 4 cm. Dải nào ngắn hơn?",
                    "A",
                    "B",
                    "Bằng nhau",
                    "2 cm ngắn hơn 4 cm.",
                ),
                c(
                    "So hai bút nên đặt thế nào?",
                    "Chung một đầu",
                    "Mỗi bút một nơi",
                    "Che cả hai bút",
                    "Đặt chung một đầu giúp so đúng.",
                ),
                c(
                    "Hai dải đều dài 6 cm thì thế nào?",
                    "Dài bằng nhau",
                    "A dài hơn",
                    "B dài hơn",
                    "Số đo đều là 6 cm.",
                ),
            ],
        )
        add(
            "measurement",
            "centimetres",
            "Đo bằng xăng-ti-mét",
            "Đặt đầu vật ở vạch 0 trên thước. Nhìn vạch ở đầu còn lại; đơn vị viết cm.",
            "Bút từ vạch 0 đến vạch 7 dài 7 cm.",
            "Tìm vạch 0.|Đặt đầu vật ở vạch 0 rồi đọc đầu kia.|Kiểm tra đơn vị cm.",
            [
                n(
                    f"Dải giấy từ vạch 0 đến vạch {v}. Dài mấy cm?",
                    v,
                    f"Đầu dải ở vạch {v}, nên dài {v} cm.",
                )
                for v in [3, 5, 8, 10]
            ],
        )
        add(
            "numbers",
            "eleven-twenty",
            "Một chục và các số đến 20",
            "10 que là một chục. Thêm que rời để có các số 11 đến 20.",
            "10 que và 4 que rời là 14 que.",
            "Tìm bó 10 que.|Đếm tiếp các que rời sau 10.|Kiểm tra có bao nhiêu chục, bao nhiêu đơn vị.",
            [
                n(f"10 que và {v} que rời có tất cả mấy que?", 10 + v, f"10 + {v} = {10 + v}.")
                for v in [1, 2, 4, 5, 7, 9]
            ],
            counters(14),
        )
        add(
            "numbers",
            "tens-units",
            "Chục và đơn vị của số có hai chữ số",
            "Bó 10 que thành một chục. Chữ số bên trái chỉ chục, bên phải chỉ đơn vị.",
            "23 có 2 chục và 3 đơn vị.",
            "Nhìn số chục.|Ghép số chục với số đơn vị.|Tách số vừa chọn để thử lại.",
            [
                n(
                    f"{a} chục và {b} đơn vị viết số nào?",
                    a * 10 + b,
                    f"{a} chục là {a * 10}; thêm {b} được {a * 10 + b}.",
                )
                for a, b in [(2, 1), (3, 4), (4, 2), (5, 6), (6, 0), (8, 7)]
            ],
        )
        add(
            "numbers",
            "compare",
            "Chọn số lớn hơn, bé hơn",
            "So hàng chục trước. Nếu số chục bằng nhau thì so số đơn vị.",
            "42 lớn hơn 24 vì 4 chục nhiều hơn 2 chục.",
            "Nhìn chữ số hàng chục.|Nếu chục bằng nhau, so đơn vị.|Đọc lại yêu cầu lớn hơn hay bé hơn.",
            [
                n(
                    f"Trong {a} và {b}, số nào lớn hơn?",
                    max(a, b),
                    f"{max(a, b)} lớn hơn {min(a, b)}.",
                )
                for a, b in [(14, 12), (21, 31), (43, 42), (50, 40), (66, 68), (91, 89)]
            ],
        )
        add(
            "numbers",
            "round-tens",
            "Đếm các số tròn chục",
            "Các số 10, 20, 30 có số đơn vị bằng 0. Đếm thêm từng bó 10 que.",
            "20 que thêm 10 que thành 30 que.",
            "Mỗi bó là 10 que.|Cộng hoặc bớt theo bó.|Đọc lại các số tròn chục.",
            calc([(10, 10), (20, 10), (30, 20), (40, 10), (50, 20), (60, 30)], "+"),
        )
        add(
            "operations",
            "add-hundred",
            "Cộng không nhớ trong phạm vi 100",
            "Cộng đơn vị với đơn vị, chục với chục. Bài này chưa cần đổi 10 đơn vị thành 1 chục.",
            "23 + 14 = 37: 3 + 4 = 7, 2 chục + 1 chục = 3 chục.",
            "Nhìn số đơn vị.|Cộng đơn vị rồi cộng chục.|Tách kết quả thành chục và đơn vị.",
            calc([(12, 13), (21, 16), (34, 12), (42, 23), (53, 14), (60, 20)], "+"),
        )
        add(
            "operations",
            "subtract-hundred",
            "Trừ không nhớ trong phạm vi 100",
            "Trừ đơn vị trước, rồi trừ chục. Không cần mượn một chục ở các ví dụ này.",
            "47 − 23 = 24: 7 − 3 = 4, 4 chục − 2 chục = 2 chục.",
            "Đọc số lúc đầu.|Trừ đơn vị rồi trừ chục.|Cộng phần còn lại với phần đã bớt để thử.",
            calc([(25, 12), (38, 16), (46, 21), (67, 34), (89, 25), (90, 40)], "−"),
        )
        add(
            "time",
            "whole-hours",
            "Đọc giờ đúng",
            "Kim dài chỉ số 12 là giờ đúng. Kim ngắn chỉ số mấy thì đọc bấy nhiêu giờ.",
            "Kim dài chỉ 12, kim ngắn chỉ 8: 8 giờ.",
            "Nhìn kim dài.|Kim dài ở 12 thì nhìn kim ngắn.|Đọc số kim ngắn chỉ và nói giờ.",
            [
                n(
                    f"Kim dài chỉ 12, kim ngắn chỉ {v}. Mấy giờ?",
                    v,
                    f"Kim ngắn chỉ {v}, nên là {v} giờ.",
                )
                for v in [2, 4, 6, 8, 10, 11]
            ],
            {
                "kind": "clock",
                "hour": 8,
                "minute": 0,
                "caption": "Kim dài chỉ 12, kim ngắn chỉ 8: 8 giờ đúng.",
            },
        )
        add(
            "time",
            "week",
            "Các ngày trong tuần",
            "Một tuần có 7 ngày. Đọc theo thứ tự từ thứ hai đến chủ nhật.",
            "Thứ hai, thứ ba, thứ tư, thứ năm, thứ sáu, thứ bảy, chủ nhật.",
            "Đọc dãy ngày trong ví dụ.|Tìm ngày được hỏi rồi nhìn ngày ngay sau.|Đọc cả hai ngày để thử.",
            [
                c(
                    f"Sau {a} là ngày nào?",
                    b,
                    w,
                    next(v for v in ["Thứ ba", "Thứ tư", "Chủ nhật"] if v not in [b, w]),
                    f"Trong tuần, {b.lower()} ở ngay sau {a}.",
                )
                for a, b, w in [
                    ("thứ hai", "Thứ ba", "Thứ năm"),
                    ("thứ ba", "Thứ tư", "Thứ sáu"),
                    ("thứ tư", "Thứ năm", "Thứ hai"),
                    ("thứ năm", "Thứ sáu", "Thứ hai"),
                    ("thứ sáu", "Thứ bảy", "Thứ tư"),
                    ("thứ bảy", "Chủ nhật", "Thứ hai"),
                ]
            ],
        )
        add(
            "wordproblems",
            "more",
            "Có thêm bao nhiêu vật?",
            "Đọc số vật lúc đầu và số được thêm. Dùng phép cộng để tìm tất cả.",
            "An có 4 bút, được thêm 2 bút. An có 4 + 2 = 6 bút.",
            "Tìm số lúc đầu.|Thêm vào thì dùng cộng.|Đếm thử hai nhóm.",
            [
                n(
                    f"Có {a} bút, thêm {b} bút. Có tất cả mấy bút?",
                    a + b,
                    f"{a} + {b} = {a + b} bút.",
                )
                for a, b in [(2, 1), (3, 2), (4, 3), (5, 2), (6, 3), (7, 1)]
            ],
            counters(6),
        )
        add(
            "wordproblems",
            "left",
            "Còn lại bao nhiêu vật?",
            "Đọc số vật lúc đầu và số đã lấy đi. Dùng phép trừ để tìm số còn lại.",
            "Có 7 quả, lấy 3 quả. Còn 7 − 3 = 4 quả.",
            "Tìm số lúc đầu.|Lấy đi thì dùng trừ.|Đếm các vật còn lại.",
            [
                n(f"Có {a} quả, lấy đi {b} quả. Còn mấy quả?", a - b, f"{a} − {b} = {a - b} quả.")
                for a, b in [(4, 1), (5, 2), (6, 2), (7, 3), (8, 4), (9, 2)]
            ],
        )
        add(
            "numbers",
            "number-gaps",
            "Tư duy: tìm số còn thiếu",
            "Đọc dãy số tăng từng 1. Dùng ngón tay hoặc que để tìm ô trống.",
            "3, 4, □, 6: ô trống là 5.",
            "Đọc số trước ô trống.|Đếm thêm đúng 1.|Đọc lại dãy có số vừa tìm.",
            [
                n(
                    f"{v}, {v + 1}, □, {v + 3}. Điền số nào?",
                    v + 2,
                    f"Dãy tăng từng 1, số còn thiếu là {v + 2}.",
                )
                for v in [1, 3, 5, 11, 13, 21, 32, 46]
            ],
            thinking=True,
        )
        add(
            "operations",
            "hidden-add",
            "Tư duy: thêm mấy để đủ?",
            "Dùng que tính. Đếm từ số đã có đến số cần đủ để tìm số thêm.",
            "Có 3 que, cần đủ 5 que: thêm 2 que.",
            "Xếp số que đã có.|Thêm từng que cho đến số cần đủ.|Đếm số que vừa thêm.",
            [
                n(f"Có {a} que. Thêm mấy que để đủ {b} que?", b - a, f"{a} + {b - a} = {b}.")
                for a, b in [(1, 3), (2, 5), (3, 7), (4, 6), (5, 9), (6, 8), (2, 8), (7, 10)]
            ],
            thinking=True,
        )
        add(
            "wordproblems",
            "relevant",
            "Tư duy: chỉ dùng số cần hỏi",
            "Chỉ đếm loại đồ vật được hỏi. Số của loại khác không dùng để tính.",
            "Có 3 bút đỏ, 2 bút xanh và 1 cặp. Hỏi số bút: 3 + 2 = 5 bút.",
            "Đề hỏi loại vật nào?|Chỉ gộp các nhóm của loại đó.|Nói vì sao không cộng số của vật khác.",
            [
                n(
                    f"Có {a} bút đỏ, {b} bút xanh, 1 cặp. Có mấy bút?",
                    a + b,
                    f"Chỉ đếm bút: {a} + {b} = {a + b}; không đếm cặp.",
                )
                for a, b in [(1, 2), (2, 2), (3, 1), (4, 2), (2, 5), (3, 4), (5, 3), (4, 5)]
            ],
            thinking=True,
        )
        add(
            "patterns",
            "repeat",
            "Tư duy: mẫu hai hình lặp lại",
            "Nhìn hai hình đầu và đọc mẫu lặp. Chỉ thay đúng hình tiếp theo.",
            "○ △ ○ △: mẫu là tròn rồi tam giác.",
            "Tìm hai hình lặp.|Đọc tròn, tam giác theo từng cặp.|Thử đặt hình em chọn vào cuối dãy.",
            [
                c(f"{pattern} □. Ô trống là hình nào?", answer, wrong, "Hình chữ nhật", why)
                for pattern, answer, wrong, why in [
                    ("○ △ ○", "Hình tam giác", "Hình tròn", "Sau tròn là tam giác."),
                    ("△ ○ △", "Hình tròn", "Hình tam giác", "Sau tam giác là tròn."),
                    ("○ △ ○ △", "Hình tròn", "Hình tam giác", "Mẫu bắt đầu lại bằng tròn."),
                    ("△ ○ △ ○", "Hình tam giác", "Hình tròn", "Mẫu bắt đầu lại bằng tam giác."),
                    (
                        "○ ○ △ ○ ○",
                        "Hình tam giác",
                        "Hình tròn",
                        "Mẫu gồm hai tròn rồi một tam giác.",
                    ),
                    (
                        "△ △ ○ △ △",
                        "Hình tròn",
                        "Hình tam giác",
                        "Mẫu gồm hai tam giác rồi một tròn.",
                    ),
                    (
                        "○ △ △ ○ △",
                        "Hình tam giác",
                        "Hình tròn",
                        "Mỗi nhóm có một tròn rồi hai tam giác.",
                    ),
                    (
                        "△ ○ ○ △ ○",
                        "Hình tròn",
                        "Hình tam giác",
                        "Mỗi nhóm có một tam giác rồi hai tròn.",
                    ),
                ]
            ],
            cards(["○", "△", "○", "△"], "Mẫu hai hình: tròn, tam giác, tròn, tam giác."),
            thinking=True,
        )
        add(
            "sorting",
            "different",
            "Tư duy: tìm hình khác nhóm",
            "Nhìn hình dạng, không đoán theo chỗ đặt. Chọn hình khác các hình còn lại.",
            "○ ○ △ ○: tam giác khác ba hình tròn.",
            "Tìm hình xuất hiện nhiều.|So đường bao các hình.|Nói tên hình khác nhóm.",
            [
                c(f"{s}. Hình nào khác nhóm?", a, b, "Hình chữ nhật", why)
                for s, a, b, why in [
                    ("○ ○ △ ○", "Hình tam giác", "Hình tròn", "Ba hình tròn, một tam giác."),
                    ("△ △ ○ △", "Hình tròn", "Hình tam giác", "Ba tam giác, một tròn."),
                    ("□ ○ □ □", "Hình tròn", "Hình vuông", "Ba vuông, một tròn."),
                    ("△ □ △ △", "Hình vuông", "Hình tam giác", "Ba tam giác, một vuông."),
                    ("○ □ ○ ○", "Hình vuông", "Hình tròn", "Ba tròn, một vuông."),
                    ("□ □ △ □", "Hình tam giác", "Hình vuông", "Ba vuông, một tam giác."),
                ]
            ],
            thinking=True,
        )
        add(
            "geometry",
            "shape-objects",
            "Tư duy: đồ vật giống hình nào?",
            "Nhìn mặt phẳng của đồ vật được nêu, rồi ghép với hình đã học.",
            "Mặt đồng hồ tròn giống ○. Mặt quyển vở thường giống ▭.",
            "Đề đang hỏi mặt của vật nào?|Nhìn đường bao của mặt đó.|Ghép với hình tròn, vuông, tam giác hoặc chữ nhật.",
            [
                c(p, a, w1, w2, why)
                for p, a, w1, w2, why in [
                    (
                        "Mặt đồng hồ tròn giống hình nào?",
                        "Hình tròn",
                        "Hình vuông",
                        "Hình tam giác",
                        "Đường bao mặt đồng hồ tròn.",
                    ),
                    (
                        "Mặt quyển vở dài giống hình nào?",
                        "Hình chữ nhật",
                        "Hình tròn",
                        "Hình tam giác",
                        "Mặt vở thường là hình chữ nhật.",
                    ),
                    (
                        "Miếng giấy □ giống hình nào?",
                        "Hình vuông",
                        "Hình tròn",
                        "Hình tam giác",
                        "□ là hình vuông.",
                    ),
                    (
                        "Cờ giấy △ giống hình nào?",
                        "Hình tam giác",
                        "Hình vuông",
                        "Hình tròn",
                        "△ là hình tam giác.",
                    ),
                    (
                        "Miếng bánh có mặt ○ giống hình nào?",
                        "Hình tròn",
                        "Hình vuông",
                        "Hình chữ nhật",
                        "Mặt ○ là hình tròn.",
                    ),
                    (
                        "Khăn giấy có mặt □ giống hình nào?",
                        "Hình vuông",
                        "Hình tam giác",
                        "Hình tròn",
                        "Mặt □ là hình vuông.",
                    ),
                ]
            ],
            thinking=True,
        )
        add(
            "time",
            "before-after",
            "Tư duy: trước và sau một giờ đúng",
            "Đọc các giờ theo thứ tự trên đồng hồ. Các câu hỏi ở đây cùng một buổi.",
            "Trong buổi sáng, 7 giờ ở trước 8 giờ.",
            "Xác định cùng một buổi.|So thứ tự hai giờ.|Đọc giờ trước rồi giờ sau.",
            [
                n(
                    f"Cùng buổi sáng, giữa {a} giờ và {b} giờ, giờ nào đến trước?",
                    min(a, b),
                    f"{min(a, b)} giờ đến trước {max(a, b)} giờ.",
                )
                for a, b in [(7, 8), (9, 8), (6, 7), (10, 9), (8, 10), (11, 10)]
            ],
            thinking=True,
        )
    else:
        add(
            "numbers",
            "read-tens",
            "Ôn đọc số và chục, đơn vị",
            "Tách số có hai chữ số thành chục và đơn vị.",
            "46 là 4 chục và 6 đơn vị.",
            "Nhìn hàng chục.|Ghép chục và đơn vị.|Tách lại số để thử.",
            [
                n(
                    f"{a} chục và {b} đơn vị viết số nào?",
                    10 * a + b,
                    f"{10 * a} + {b} = {10 * a + b}.",
                )
                for a, b in [(3, 2), (4, 6), (5, 0), (7, 8)]
            ],
        )
        add(
            "numbers",
            "compare-tens",
            "Ôn so sánh số đến 100",
            "So hàng chục trước, rồi so đơn vị khi chục bằng nhau.",
            "68 > 65 vì cùng 6 chục nhưng 8 > 5.",
            "Đọc hai số.|So chục rồi đơn vị.|Đọc rõ yêu cầu lớn hơn.",
            [
                n(
                    f"Số lớn hơn trong {a} và {b} là số nào?",
                    max(a, b),
                    f"{max(a, b)} > {min(a, b)}.",
                )
                for a, b in [(32, 23), (56, 59), (70, 68), (91, 89)]
            ],
        )
        add(
            "operations",
            "carry-hundred",
            "Cộng có nhớ trong phạm vi 100",
            "10 đơn vị đổi thành 1 chục. Cộng hàng đơn vị, nhớ 1 vào hàng chục.",
            "27 + 15 = 42: 7 + 5 = 12, viết 2 và nhớ 1 chục.",
            "Cộng đơn vị.|Nếu đủ 10, đổi thành 1 chục.|Cộng chục và chục nhớ.",
            calc([(18, 7), (26, 15), (37, 24), (48, 16)], "+"),
        )
        add(
            "operations",
            "borrow-hundred",
            "Trừ có nhớ trong phạm vi 100",
            "Nếu đơn vị chưa đủ để trừ, đổi 1 chục thành 10 đơn vị.",
            "42 − 15 = 27: đổi 1 chục, 12 − 5 = 7; 3 − 1 = 2 chục.",
            "So hai hàng đơn vị.|Đổi một chục khi cần.|Trừ chục còn lại, rồi thử bằng cộng.",
            calc([(32, 15), (41, 24), (53, 27), (62, 18)], "−"),
        )
        for base in [2, 5]:
            add(
                "groups",
                f"times-{base}",
                f"Các nhóm đều và bảng nhân {base}",
                f"Mỗi nhóm có {base} vật. Gộp các nhóm bằng nhau để tìm tất cả.",
                f"3 nhóm, mỗi nhóm {base} vật: {base} × 3 = {base * 3}.",
                "Đếm số nhóm.|Cộng số vật mỗi nhóm hoặc dùng bảng nhân.|Kiểm tra tổng số vật.",
                [
                    n(
                        f"{v} nhóm, mỗi nhóm {base} bút. Có tất cả mấy bút?",
                        base * v,
                        f"{base} × {v} = {base * v}.",
                    )
                    for v in [2, 3, 4, 6]
                ],
                counters(base * 3),
            )
        add(
            "measurement",
            "length-units",
            "Xăng-ti-mét, đề-xi-mét và mét",
            "1 dm = 10 cm. 1 m = 100 cm. Đổi đơn vị trước khi so sánh.",
            "2 dm = 20 cm; 3 m = 300 cm.",
            "Xem đơn vị cần đổi.|Dùng 1 dm = 10 cm hoặc 1 m = 100 cm.|Đọc lại số kèm đơn vị.",
            [
                n(f"{v} dm bằng mấy cm?", v * 10, f"Mỗi dm có 10 cm; {v} dm = {v * 10} cm.")
                for v in [1, 2, 4, 6]
            ],
        )
        add(
            "measurement",
            "mass-volume",
            "Ki-lô-gam và lít",
            "kg đo khối lượng; lít đo lượng chất lỏng. Chỉ cộng các số cùng đơn vị.",
            "Túi 2 kg và túi 3 kg nặng 5 kg. Bình 2 lít và bình 1 lít có 3 lít.",
            "Xem là kg hay lít.|Cộng các số cùng đơn vị.|Ghi đúng đơn vị được hỏi.",
            [
                n(
                    f"Có {a} {u} và thêm {b} {u}. Có tất cả mấy {u}?",
                    a + b,
                    f"{a} + {b} = {a + b} {u}.",
                )
                for a, b, u in [(2, 3, "kg"), (4, 2, "kg"), (2, 1, "lít"), (5, 3, "lít")]
            ],
        )
        add(
            "numbers",
            "read-thousand",
            "Số trong phạm vi 1000",
            "Ghép trăm, chục, đơn vị. Chữ số 0 giữ chỗ của hàng không có đơn vị.",
            "305 gồm 3 trăm, 0 chục, 5 đơn vị.",
            "Tìm hàng trăm.|Ghép ba hàng, giữ chữ số 0.|Đọc lại số.",
            [
                n(
                    f"{a} trăm, {b} chục, {d} đơn vị viết số nào?",
                    100 * a + 10 * b + d,
                    f"{100 * a} + {10 * b} + {d} = {100 * a + 10 * b + d}.",
                )
                for a, b, d in [(1, 2, 3), (2, 0, 5), (3, 4, 0), (4, 1, 6), (6, 0, 8), (9, 9, 9)]
            ],
        )
        add(
            "numbers",
            "hundreds",
            "Giá trị hàng trăm, chục, đơn vị",
            "Giá trị chữ số phụ thuộc hàng. Hàng trăm bằng số trăm nhân với 100.",
            "Trong 427, chữ số 4 có giá trị 400.",
            "Xác định chữ số được hỏi.|Nhìn nó ở hàng nào.|Viết số thành tổng để thử.",
            [
                n(
                    f"Chữ số {v // 100} trong {v} có giá trị bao nhiêu?",
                    v // 100 * 100,
                    f"Chữ số {v // 100} ở hàng trăm có giá trị {v // 100 * 100}.",
                )
                for v in [235, 408, 517, 629, 740, 863]
            ],
        )
        add(
            "numbers",
            "number-line",
            "Số liền trước, liền sau",
            "Trên dãy tăng từng 1, số liền sau hơn 1, số liền trước kém 1.",
            "Liền trước 300 là 299; liền sau 300 là 301.",
            "Đọc yêu cầu trước hay sau.|Bớt 1 hoặc thêm 1.|Kiểm tra hai số đứng cạnh nhau.",
            [
                n(
                    f"Số liền {w} {v} là số nào?",
                    v + d,
                    f"{v} {'+' if d == 1 else '−'} 1 = {v + d}.",
                )
                for v, w, d in [
                    (199, "sau", 1),
                    (300, "trước", -1),
                    (408, "sau", 1),
                    (620, "trước", -1),
                    (899, "sau", 1),
                    (1000, "trước", -1),
                ]
            ],
        )
        add(
            "operations",
            "add-thousand",
            "Cộng không nhớ đến 1000",
            "Đặt các hàng thẳng cột. Cộng đơn vị, chục, trăm.",
            "234 + 125 = 359.",
            "Đặt các hàng thẳng cột.|Cộng từ đơn vị sang trăm.|Tách tổng theo từng hàng để kiểm tra.",
            calc([(123, 214), (205, 132), (341, 126), (420, 150), (612, 203), (730, 140)], "+"),
        )
        add(
            "operations",
            "subtract-thousand",
            "Trừ không nhớ đến 1000",
            "Đặt đúng hàng rồi trừ từ đơn vị đến trăm.",
            "578 − 234 = 344.",
            "Đặt đúng hàng.|Trừ đơn vị, chục, trăm.|Dùng cộng để thử lại.",
            calc([(345, 123), (567, 234), (789, 456), (908, 305), (670, 230), (854, 421)], "−"),
        )
        add(
            "operations",
            "single-carry",
            "Cộng đến 1000 có nhớ một lần",
            "Chỉ đổi 10 đơn vị thành 1 chục một lần ở những phép tính này.",
            "236 + 128 = 364: 6 + 8 = 14, nhớ 1 chục.",
            "Cộng đơn vị.|Ghi đơn vị, nhớ 1 chục nếu đủ 10.|Cộng chục kèm số nhớ, rồi cộng trăm.",
            calc([(126, 137), (238, 125), (347, 216), (456, 127), (628, 135), (719, 142)], "+"),
        )
        add(
            "geometry",
            "lines",
            "Độ dài đường gấp khúc",
            "Đường gấp khúc gồm các đoạn nối tiếp. Cộng độ dài các đoạn đã cho.",
            "Đường có hai đoạn 3 cm và 4 cm dài 7 cm.",
            "Tìm các đoạn.|Cộng số đo cùng đơn vị.|Kiểm tra đã tính đủ từng đoạn.",
            [
                n(
                    f"Đường gấp khúc có hai đoạn {a} cm, {b} cm. Dài mấy cm?",
                    a + b,
                    f"{a} + {b} = {a + b} cm.",
                )
                for a, b in [(2, 3), (4, 5), (6, 2), (7, 4), (8, 5), (9, 6)]
            ],
        )
        add(
            "geometry",
            "four-sides",
            "Hình tứ giác và các khối quanh em",
            "Hình có 4 cạnh là tứ giác. Quả bóng giống khối cầu, lon thẳng giống khối trụ.",
            "□ có 4 cạnh. Quả bóng tròn có dạng khối cầu.",
            "Quan sát đường bao hoặc vật thật.|Đếm cạnh của hình phẳng; xem dạng khối của vật.|Gọi đúng tên.",
            [
                c(p, a, w1, w2, why)
                for p, a, w1, w2, why in [
                    ("Tứ giác có mấy cạnh?", "4", "3", "5", "Tứ giác có 4 cạnh."),
                    (
                        "Quả bóng tròn giống khối nào?",
                        "Khối cầu",
                        "Khối lập phương",
                        "Hình tam giác",
                        "Quả bóng có dạng khối cầu.",
                    ),
                    (
                        "Lon có hai đáy tròn giống khối nào?",
                        "Khối trụ",
                        "Khối cầu",
                        "Hình vuông",
                        "Lon có dạng khối trụ.",
                    ),
                    ("□ có phải tứ giác không?", "Có", "Không", "Chưa có cạnh", "□ có 4 cạnh."),
                    (
                        "△ có phải tứ giác không?",
                        "Không",
                        "Có",
                        "Mọi hình đều là tứ giác",
                        "△ chỉ có 3 cạnh.",
                    ),
                    (
                        "Đường gấp khúc gồm gì?",
                        "Các đoạn nối tiếp",
                        "Chỉ một điểm",
                        "Các hình tròn rời",
                        "Các đoạn nối nhau thành đường gấp khúc.",
                    ),
                ]
            ],
            cards(["○", "△", "□", "▭"], "Hình vuông và chữ nhật đều có bốn cạnh."),
        )
        add(
            "time",
            "quarter-half",
            "Giờ, phút và xem lịch",
            "Một giờ có 60 phút. Kim phút ở 3 là 15 phút, ở 6 là 30 phút.",
            "Kim giờ ở giữa 8 và 9, kim phút ở 6: 8 giờ 30 phút.",
            "Nhìn kim phút.|Ở 3 đọc 15 phút, ở 6 đọc 30 phút.|Đọc giờ và phút cùng nhau.",
            [
                n(p, a, why)
                for p, a, why in [
                    ("Một giờ có mấy phút?", 60, "Một giờ có 60 phút."),
                    ("Một ngày có mấy giờ?", 24, "Một ngày có 24 giờ."),
                    ("Kim phút ở 3 chỉ mấy phút?", 15, "Kim phút ở 3 là 15 phút."),
                    ("Kim phút ở 6 chỉ mấy phút?", 30, "Kim phút ở 6 là 30 phút."),
                    ("Tháng Ba có mấy ngày?", 31, "Tháng Ba có 31 ngày."),
                    ("Ngày liền sau ngày 18 trong tháng là ngày mấy?", 19, "18 + 1 = 19."),
                ]
            ],
            {
                "kind": "clock",
                "hour": 8,
                "minute": 30,
                "caption": "8 giờ 30 phút: kim phút ở 6, kim giờ ở giữa 8 và 9.",
            },
        )
        add(
            "statistics",
            "picture-count",
            "Đếm trên biểu đồ tranh",
            "Mỗi chấm trong bài này là 1 đồ vật. Đếm số chấm ở từng hàng.",
            "Táo: ● ● ●. Cam: ● ●. Có 3 táo và 2 cam.",
            "Đọc mỗi chấm là mấy vật.|Đếm từng hàng.|So số vừa đếm nếu cần.",
            [
                n(
                    f"Hàng quả có {'● ' * v}. Mỗi chấm là 1 quả. Có mấy quả?",
                    v,
                    f"Đếm được {v} chấm nên có {v} quả.",
                )
                for v in [2, 4, 5, 3, 6, 8]
            ],
            counters(6),
        )
        add(
            "wordproblems",
            "more-than",
            "Tư duy: nhiều hơn một số vật",
            "Biết số của nhóm đầu. Nhóm sau nhiều hơn thì cộng phần hơn.",
            "An có 12 bút. Bình nhiều hơn An 3 bút. Bình có 15 bút.",
            "Tìm nhóm đã biết.|Nhiều hơn thì cộng phần hơn.|Lấy kết quả trừ số đã biết để kiểm tra phần hơn.",
            [
                n(
                    f"An có {a} bút. Bình nhiều hơn {b} bút. Bình có mấy bút?",
                    a + b,
                    f"{a} + {b} = {a + b} bút.",
                )
                for a, b in [(12, 3), (15, 4), (21, 6), (28, 5), (32, 7), (43, 8), (54, 6), (65, 9)]
            ],
            thinking=True,
        )
        add(
            "wordproblems",
            "less-than",
            "Tư duy: ít hơn một số vật",
            "Nhóm sau ít hơn thì bớt phần chênh lệch từ nhóm đã biết.",
            "Mai có 18 nhãn vở. Hà ít hơn Mai 4 nhãn: 18 − 4 = 14.",
            "Tìm số đã biết.|Ít hơn thì trừ phần ít hơn.|Lấy kết quả cộng phần chênh lệch để thử.",
            [
                n(
                    f"Mai có {a} nhãn. Hà ít hơn {b} nhãn. Hà có mấy nhãn?",
                    a - b,
                    f"{a} − {b} = {a - b} nhãn.",
                )
                for a, b in [(18, 4), (21, 3), (32, 5), (45, 7), (56, 8), (67, 9), (70, 6), (84, 7)]
            ],
            thinking=True,
        )
        add(
            "groups",
            "share",
            "Tư duy: chia đều theo bảng 2 và 5",
            "Chia đều nghĩa là mỗi nhóm có số vật bằng nhau. Dùng bảng chia 2 hoặc 5.",
            "10 bút chia đều cho 2 bạn: mỗi bạn 5 bút.",
            "Đọc số vật và số nhóm.|Chia đều bằng bảng 2 hoặc 5.|Nhân số mỗi nhóm với số nhóm để thử.",
            [
                n(
                    f"{a} bút chia đều cho {b} bạn. Mỗi bạn có mấy bút?",
                    a // b,
                    f"{a} : {b} = {a // b}.",
                )
                for a, b in [(6, 2), (10, 2), (14, 2), (18, 2), (10, 5), (20, 5), (30, 5), (40, 5)]
            ],
            thinking=True,
        )
        add(
            "operations",
            "missing",
            "Tư duy: tìm số trong ô trống",
            "Ô trống là số chưa biết. Dùng phép tính ngược rồi thay vào để kiểm tra.",
            "□ + 6 = 15: 15 − 6 = 9, thử 9 + 6 = 15.",
            "Đọc phép tính.|Tìm số chưa biết bằng phép tính ngược.|Thay số vừa tìm vào ô trống.",
            [
                n(
                    f"□ + {a} = {b}. Điền số nào?",
                    b - a,
                    f"{b} − {a} = {b - a}; thử {b - a} + {a} = {b}.",
                )
                for a, b in [
                    (6, 15),
                    (8, 21),
                    (9, 32),
                    (7, 40),
                    (15, 52),
                    (24, 70),
                    (32, 81),
                    (45, 94),
                ]
            ],
            thinking=True,
        )
        add(
            "statistics",
            "chance",
            "Tư duy: có thể, chắc chắn, không thể",
            "Xem trong túi có những màu nào trước khi lấy. Không đoán màu chưa có trong túi.",
            "Túi chỉ có bi đỏ: lấy một viên chắc chắn đỏ, không thể xanh.",
            "Đọc các màu trong túi.|Chỉ có một màu thì chắc chắn màu đó.|Nếu màu không có trong túi thì không thể lấy được.",
            [
                c(p, a, w1, w2, why)
                for p, a, w1, w2, why in [
                    (
                        "Túi chỉ có bi đỏ. Lấy một viên đỏ là điều gì?",
                        "Chắc chắn",
                        "Không thể",
                        "Không biết trong túi có gì",
                        "Mọi viên đều đỏ.",
                    ),
                    (
                        "Túi chỉ có bi đỏ. Lấy một viên xanh là điều gì?",
                        "Không thể",
                        "Chắc chắn",
                        "Có thể",
                        "Không có bi xanh.",
                    ),
                    (
                        "Túi có bi đỏ và xanh. Lấy một viên đỏ là điều gì?",
                        "Có thể",
                        "Không thể",
                        "Chắc chắn",
                        "Có bi đỏ nhưng còn bi xanh.",
                    ),
                    (
                        "Túi chỉ có bi vàng. Lấy một viên vàng là điều gì?",
                        "Chắc chắn",
                        "Không thể",
                        "Túi trống",
                        "Mọi viên đều vàng.",
                    ),
                    (
                        "Túi có bi đỏ và vàng. Lấy bi xanh là điều gì?",
                        "Không thể",
                        "Chắc chắn",
                        "Có thể",
                        "Không có bi xanh.",
                    ),
                    (
                        "Túi có bi đỏ và vàng. Lấy bi vàng là điều gì?",
                        "Có thể",
                        "Không thể",
                        "Chắc chắn",
                        "Có bi vàng nhưng còn bi đỏ.",
                    ),
                ]
            ],
            thinking=True,
        )
        add(
            "time",
            "schedule",
            "Tư duy: đọc lịch và thứ tự giờ",
            "Đọc thông tin đã cho. So các giờ trong cùng một buổi và ngày liền nhau.",
            "Sáng: ăn lúc 7 giờ, học lúc 8 giờ. Ăn trước khi học.",
            "Xem đang hỏi giờ hay ngày.|So hai mốc cùng buổi.|Đọc lại theo thứ tự.",
            [
                n(p, a, why)
                for p, a, why in [
                    ("Cùng buổi sáng, 8 giờ và 9 giờ: giờ nào trước?", 8, "8 giờ trước 9 giờ."),
                    ("Cùng buổi sáng, 10 giờ và 9 giờ: giờ nào sau?", 10, "10 giờ sau 9 giờ."),
                    ("Ngày liền sau 20 trong tháng là ngày mấy?", 21, "20 + 1 = 21."),
                    ("Ngày liền trước 15 là ngày mấy?", 14, "15 − 1 = 14."),
                    ("Kim phút ở 6 chỉ mấy phút?", 30, "Kim phút ở 6 chỉ 30 phút."),
                    ("Kim phút ở 3 chỉ mấy phút?", 15, "Kim phút ở 3 chỉ 15 phút."),
                ]
            ],
            thinking=True,
        )
        add(
            "geometry",
            "line-check",
            "Tư duy: kiểm tra độ dài đường đi",
            "Chỉ cộng những đoạn của đường đi được hỏi, giữ cùng đơn vị cm.",
            "Đường A gồm đoạn 4 cm và 5 cm: dài 9 cm.",
            "Tìm các đoạn của đường cần hỏi.|Cộng số đo từng đoạn.|Kiểm tra không cộng nhầm đường khác.",
            [
                n(
                    f"Đường A dài {a} cm rồi {b} cm. Đường B dài 2 cm. A dài mấy cm?",
                    a + b,
                    f"Chỉ cộng đường A: {a} + {b} = {a + b} cm.",
                )
                for a, b in [(3, 4), (5, 6), (7, 8), (9, 4), (12, 5), (15, 7)]
            ],
            thinking=True,
        )
    assert len(items) == 25
    return items
