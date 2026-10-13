# Học liệu lớp 5 và nâng cấp thư viện bài học

Đợt này bổ sung ba môn **Toán, Tiếng Việt, Tiếng Anh lớp 5** vào hệ thống LMS.
Mỗi khối từ lớp 1 đến lớp 5 có 68 bài, 384 câu hỏi riêng biệt và 56 đề luyện tập.
Kho năm khối có **340 bài / 1920 câu / 280 đề**, chưa tính AI Academy hay bài
do giáo viên tự tạo. Bộ lớp 5 có 22 chủ đề/kỹ năng; Toán thêm mạch chuyển động
riêng nên có 9 chủ đề, so với 8 ở bộ lớp 3–4.

| Môn | Chủ đề | Bài Free / VIP | Câu Free / VIP | Đề Free / VIP |
| --- | ---: | ---: | ---: | ---: |
| Toán | 9 | 18 / 7 | 92 / 50 | 14 / 7 |
| Tiếng Việt | 6 | 15 / 8 | 74 / 56 | 11 / 8 |
| Tiếng Anh | 7 | 13 / 7 | 62 / 50 | 9 / 7 |
| Tổng lớp 5 | 22 | 46 / 22 | 228 / 156 | 34 / 22 |

Mỗi môn có bốn cặp bài nền tảng dùng chung bốn đề, mỗi đề tám câu.
Các bài tiếp theo có đề riêng sáu hoặc tám câu. Liên kết một câu vào hai bài
không làm tăng số câu của ngân hàng. Xem [danh mục 68 bài](grade5-lessons.csv)
để rà soát từng bài, quyền, thời lượng và số câu.
Cột số câu là phần biên soạn theo bài; mỗi cặp nền tảng ghép thành đề tám câu
và liên kết cả bộ tám câu vào hai bài trong database.

## Căn cứ chương trình Việt Nam

Đối chiếu ngày **13/10/2026** với các phụ lục chương trình ban hành kèm
Thông tư 32/2018/TT-BGDĐT, bản được các trường công lập đăng lại:

- [Chương trình môn Toán, phần lớp 5, trang in 40–46](https://fileth.hcm.shieldix.app/data/hcmedu/thbausen/2020_3/cttoan_193202020.pdf).
- [Chương trình Ngữ văn, phần Tiếng Việt lớp 5, trang in 35–40](https://fileth.hcm.shieldix.app/data/hcmedu/thleductho/attachments/2019_8/2_ctngu_van_18201918.pdf).
- [Chương trình Tiếng Anh, phần lớp 5, trang in 30–32](https://fileth.hcm.shieldix.app/data/hcmedu/thlamsonbinhthanh/2020_1/chuong_trinh_mon_tieng_anh_lop_3_den_lop_12_101202010.pdf).

Đã xem [Thông tư 17/2025/TT-BGDĐT trên Cổng Chính phủ](https://xaydungchinhsach.chinhphu.vn/thong-tu-so-17-2025-tt-bgddt-sua-doi-bo-sung-mot-so-noi-dung-trong-chuong-trinh-giao-duc-pho-thong-119250916145653739.htm)
và [văn bản ký](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/9/17-bgddt.pdf):
đợt sửa đổi đó không thay phần lớp 5 của ba môn này. Không dùng thông tin
dự thảo để tự thay yêu cầu đã ban hành. Khi triển khai, giáo viên đối chiếu thêm
kế hoạch năm học, bộ sách của trường và văn bản mới có hiệu lực.

Đây là **học liệu bổ trợ**, chưa phải toàn bộ kế hoạch cả năm hay bằng chứng
học sinh đã đạt mọi yêu cầu. Ngữ liệu, ví dụ, câu hỏi và lời giải do VietTree
tự biên soạn; không chép bài đọc từ sách giáo khoa.

## Toán: nội dung và cách học

| Mạch | Nội dung đã có |
| --- | --- |
| Số và phân số | Ôn tự nhiên; bốn phép tính phân số, rút gọn; giới thiệu hỗn số. |
| Thập phân | Giá trị chữ số, so sánh/làm tròn, cộng–trừ–nhân–chia. |
| Tỉ số và phần trăm | Phần trăm, tổng/hiệu theo tỉ số; VIP có bản đồ, giá giảm và ngân sách. |
| Đo lường | Ha, km²; cm³, dm³, m³ và đổi đơn vị. |
| Hình phẳng | Diện tích tam giác/hình thang; chu vi và diện tích hình tròn. |
| Hình khối | Nhận biết khai triển, diện tích và thể tích hộp/lập phương. |
| Chuyển động | Vận tốc–quãng đường–thời gian; VIP thêm thời gian nghỉ. |
| Thống kê | Biểu đồ quạt tròn, so sánh nhóm và tỉ số của kết quả đã quan sát. |

Các câu số học dùng `Decimal`/`Fraction` để tạo đáp án chính xác. Với câu điền,
chấp nhận dấu phẩy hoặc dấu chấm thập phân; phân số yêu cầu tối giản, bỏ đơn vị.
Hình tròn dùng π gần đúng 3,14, nêu rõ trong bài. Tỉ số quan sát không dự báo
chắc chắn kết quả lần thử tiếp theo. Ví dụ VIP yêu cầu lập các bước và kiểm tra
đơn vị, không đưa kiến thức đại số của cấp học cao hơn thành điều kiện làm bài.

Cần bổ sung thực hành đo/vẽ, gấp mô hình, số đo thời gian ở nhiều tình huống
và thu thập dữ liệu thực tế; phần mềm hiện hỗ trợ luyện đọc số liệu và tính toán.

## Tiếng Việt: đọc, dùng tiếng và viết có hướng dẫn

Hai truyện tự viết **Chiếc ô chung** và **Mầm cây bên cửa** dài khoảng 310–330
tiếng; có thêm miêu tả người/cảnh khoảng 220–230 tiếng, thơ khoảng 120 tiếng và
văn bản giải thích khoảng 230 tiếng. Các độ dài này đối chiếu mốc ngữ liệu của
chương trình lớp 5; bài từ/câu riêng dùng ngữ liệu ngắn hơn để tập trung kĩ năng.

Nội dung có tìm chi tiết, tóm tắt, suy luận có bằng chứng; đồng nghĩa/đa nghĩa,
tra từ điển; đại từ, kết từ, câu ghép, liên kết câu; tên phiên âm và dấu câu.
Phần viết hướng dẫn tả người/cảnh, nêu ý kiến, kết thúc sáng tạo, báo cáo và
kế hoạch. VIP tăng câu kết hợp dữ kiện, chọn từ chính xác và rà soát đoạn viết.

Câu đọc luôn mang theo ngữ liệu. Những bài nghe, nói, thảo luận và văn mở cần
người hướng dẫn thực hành/nhận xét; chọn đáp án trên màn hình chưa đánh giá được
toàn bộ năng lực đó. Không tự chấm bài văn theo độ dài hoặc thao tác đọc xong.

## Tiếng Anh: đọc và giao tiếp trong bối cảnh quen thuộc

Hai mươi bài có đoạn đọc/hội thoại **60–80 từ**. Chủ điểm gồm bản thân,
trường học, sức khỏe, đi lại, thời tiết, đồ ăn, ngày nghỉ và nghề mong muốn.
Ôn hiện tại, trạng từ tần suất; thực hành quá khứ đơn, tương lai `will`,
`should` và lời đề nghị lịch sự `could/would`. VIP có bưu thiếp, lịch câu lạc bộ,
kế hoạch chuyến đi, hội thoại và suy luận từ truyện.

Gợi ý viết đoạn 30–40 từ có người hướng dẫn; nghe/nói cần thực hành cùng người
lớn. Chưa có audio, thu âm, nhận dạng tiếng nói hay chấm phát âm. Bộ này chưa
bao phủ vốn từ tích lũy của toàn giai đoạn lớp 3–5 và không chứng nhận trình độ.

## Quyền Free/VIP và gợi ý

- Free học 46 bài, làm 34 đề miễn phí; nhận gợi ý định hướng đầu tiên.
- VIP mở thêm 22 bài/22 đề và cả ba gợi ý **định hướng → cách làm → tự kiểm tra**.
- Gợi ý của bài học giúp tìm cách làm; đáp án bài luyện tập được bảo vệ trước
  khi nộp. Hai gói dùng cùng cách chấm điểm.
- Hết hạn/thu hồi giảm quyền ở request tiếp theo. Lịch sử và kết quả của chính
  học sinh được giữ. Gói không cho phép tự học khối khác với hồ sơ.
- Bài lớp 5 nền tảng dự kiến 12 phút; bài VIP 15 phút, có thể dừng và học tiếp.

## Giao diện và quản trị

Học sinh có **Thư viện bài học** tại `/student/lessons`: tìm theo tên bài/chủ đề,
hỗ trợ tìm không dấu; lọc môn, gói, tiến độ đọc và bài tư duy. Mỗi trang 12 bài,
hiển thị quyền, thời lượng và đường dẫn mở bài. Bấm **Làm mới** sau thay đổi gói
nếu vẫn ở cùng trang. Mục **Danh mục lớp** chọn khối để tham khảo; lớp học thực
tế theo hồ sơ do admin quản lý.

**Đã đọc xong** là tiến độ đọc, không phải điểm hay mức thành thạo. Luyện tập,
kế hoạch học, sổ ôn lỗi, kết quả, giao bài và thành tích dùng luồng LMS đã có.

Admin chọn **Lớp học liệu → Lớp 5** ở đầu trang chương trình, xem tổng theo bộ
lọc, mở/thu gọn các chủ đề và xuất CSV. Trình soạn thêm năm minh họa SVG:
tam giác, hình thang, hình tròn, hộp chữ nhật, biểu đồ quạt tròn. Nhập các số đo
cùng đơn vị cm; hình là sơ đồ học tập. Biểu đồ có chú giải chữ và tổng đúng 100%.
Backend từ chối số đo không dương, không hữu hạn, nhãn sai hoặc tổng phần trăm sai.
Số đo hiển thị thêm bên dưới hình với chữ 20 px, hoặc 24 px ở chế độ chữ lớn;
chú giải biểu đồ cũng theo cỡ chữ của tài khoản.

## Nạp và chạy

Trong thư mục `backend`, sau backup và cập nhật code:

```powershell
../.venv/Scripts/python.exe -m app.cli curriculum-inventory --grade 5
../.venv/Scripts/python.exe -m app.cli seed-grade-content --grade 5
../.venv/Scripts/python.exe -m app.cli verify-seed --grade 5
```

`seed-grade5-content` là tên lệnh tương đương. Nạp theo transaction; mã/UUID
ổn định, chạy lại không nhân bản, không ghi đè bài giáo viên chỉnh hoặc phiên bản
câu hỏi đã xuất bản. Nếu câu/đề cùng mã đã khác nguồn, lệnh dừng để kiểm tra.
Không đổi mật khẩu, phiên, VIP, kết quả hay tiến độ cũ. Không cần migration mới;
schema hiện có đã hỗ trợ lớp 5 và các thông số hình được lưu trong JSON bài học.

Khởi động lại backend/frontend rồi đăng nhập học sinh có hồ sơ lớp 5.
Development có thể tạo tài khoản thử bằng:

```powershell
../.venv/Scripts/python.exe -m app.cli seed-demo-learners --grades 5
```

Xem [tài khoản demo](demo-accounts.md) và [chạy local](run-local.md).
Production tạo học sinh thật trong quản trị và dùng lệnh nạp nội dung riêng;
không chạy fixture demo. Hướng dẫn: [deploy VPS](deploy-vps.md).

## Cấu trúc kỹ thuật và kiểm thử

Học liệu ở `backend/app/curriculum/grades/grade_05`: `pack.py`, `builders.py`,
`math.py`, `vietnamese.py`, `readings.py`, `english.py`. Registry giữ số kiểm kê
theo từng pack thay vì giả định số chủ đề mọi khối giống nhau.

API mới `GET /api/v1/students/me/lesson-library` chỉ trả metadata bài đã xuất
bản, môn/chủ đề hoạt động và tiến độ của chính tài khoản, theo lớp hiện tại.
`subject_code`, `plan`, `progress`, `category`, `search`, `page` là bộ lọc.
Từ khóa tối đa 80 ký tự; `%`, `_`, dấu gạch chéo được xử lý như chữ tìm kiếm.
Quyền và tiến độ dùng `no-store`; không thêm cache chia sẻ cho dữ liệu học sinh.
Với kho hiện tại, tìm kiếm SQL bỏ dấu đủ dùng; cần đo tải trước khi thêm chỉ mục
tìm kiếm ở kho lớn hơn. Mở bài luôn qua API kiểm quyền hiện hành.

Kiểm thử riêng bao gồm schema của 68 bài/384 câu, đáp án Toán tính độc lập,
độ dài đoạn đọc, mọi đề lưu/đọc lại/nộp/chấm, seed lặp, tiến độ riêng từng người,
bài nháp/chủ đề đóng, tìm kiếm, phân trang và cấp/thu hồi VIP. Browser kiểm tra
máy tính/điện thoại, hình minh họa, CSV và điền số thập phân. Kết quả chạy thực
tế được ghi tại [tình trạng triển khai](IMPLEMENTATION_STATUS.md).
