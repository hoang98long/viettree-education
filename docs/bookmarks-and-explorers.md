# Bài học đã lưu và bộ Khám phá

Cập nhật **15/10/2026**. Database local đã được sao lưu, nâng lên migration
`0012_lesson_bookmarks` và nạp bộ `explorers-2026-01`. Khởi động lại backend
và frontend để dùng bản mới.

## Lưu bài theo tài khoản

Học sinh bấm **Lưu bài học** trong thư viện hoặc ngay đầu bài đang đọc.
Mở **Bài học đã lưu** ở menu hoặc trang chủ để học lại. Có thể tìm không dấu,
lọc môn, gói, tiến độ và phân trang như thư viện thông thường.
Bộ lọc chi tiết thu gọn trong **Chọn thêm bộ lọc** để bài học xuất hiện sớm
hơn trên điện thoại. Bỏ thẻ cuối trang sẽ tự quay về trang còn bài.

- Dữ liệu lưu trên PostgreSQL theo tài khoản, dùng được ở các phiên đăng nhập
  và thiết bị khác; không phụ thuộc bộ nhớ của trình duyệt.
- Cả Free và VIP đều có chức năng này. Chỉ lưu mới bài đã xuất bản, đang hoạt
  động, thuộc khối hiện tại và tài khoản đang có quyền học.
- Hết hoặc bị thu hồi VIP: bài VIP đã lưu vẫn hiện trạng thái khóa, không mở
  nội dung; học sinh vẫn được bỏ lưu. Chức năng lưu không cấp thêm quyền học.
- Đổi khối: danh sách chỉ hiện bài thuộc khối hiện tại; dữ liệu đã lưu ở khối
  cũ giữ nguyên. Bài bị lưu trữ không còn hiện trong thư viện.
- Mạng lỗi không đổi trạng thái thành công giả; nút cho phép thử lại. Trong
  khi chờ, nút tạm khóa để tránh thao tác trùng.

API dùng `PUT /api/v1/students/me/lessons/{lesson_id}/bookmark`, body
`{"saved": true}` hoặc `{"saved": false}`. Gửi lại cùng trạng thái không tạo
bản ghi trùng hoặc đảo trạng thái. Chủ tài khoản lấy từ phiên đăng nhập;
request không nhận `student_id`. Mọi thao tác ghi kiểm tra CSRF/Origin.

Schema mới `student_lesson_bookmarks(student_id, lesson_id, created_at)`, khóa
chính ghép hai ID, khóa ngoại tới hồ sơ học sinh và bài học, thêm index theo
bài học. Không thay đổi bảng điểm, đáp án, VIP hoặc phiên đăng nhập cũ.
`LessonResponse` và item thư viện thêm `is_bookmarked`; thư viện nhận
`bookmarked_only=true`, thống kê thêm `bookmarked`. API dữ liệu riêng không cache.

## 15 bài luyện ngắn mới

Mỗi khối thêm một bài cho mỗi môn, mỗi bài bốn câu, khoảng 6–8 phút.
Tổng **15 bài, 60 câu hỏi, 15 đề**, gồm **7 bài Free và 8 bài VIP**.
Lớp 1–2 thao tác chọn; Toán lớp 3–5 có thêm câu điền số ngắn. Từng câu có
ngữ liệu/dữ kiện đủ để làm độc lập và lời giải sau khi nộp.

| Lớp | Toán                             | Tiếng Việt                   | Tiếng Anh                           |
| --- | -------------------------------- | ---------------------------- | ----------------------------------- |
| 1   | Free · Thước kẻ tí hon           | VIP · Bát nước cho mèo       | Free · Hello, little animals!       |
| 2   | Free · Một mét ruy băng          | VIP · Lời nhắn của mẹ        | Free · My breakfast cards           |
| 3   | VIP · Khung giấy có khe hở       | Free · Mầm non sau mưa       | VIP · What can our friends do?      |
| 4   | VIP · Mục tiêu đọc sách của tổ   | Free · Lá thư cảm ơn thủ thư | VIP · Rose's Tuesday timetable      |
| 5   | VIP · Hộp quà và khối lập phương | Free · Sửa đoạn văn lặp từ   | VIP · Follow the library directions |

Mỗi bài có một mục tiêu cụ thể, ba phần ngắn, minh họa SVG/thẻ tranh và ba
gợi ý theo bước. Free đọc bài được phép và mở gợi ý đầu; VIP mở đủ ba gợi ý.
Không dùng model AI hoặc dịch vụ ảnh bên ngoài. Nội dung bổ trợ theo bản đồ
chủ đề của dự án; tài liệu chương trình nằm trong [lớp 1–2](grades1-2-curriculum.md),
[lớp 3](grade3-curriculum.md), [lớp 4](grade4-curriculum.md), [lớp 5](grade5-curriculum.md).
Tiếng Anh lớp nhỏ dùng thẻ Việt–Anh và đọc cùng người hướng dẫn, không thay
thế thực hành nghe/nói; [hướng dẫn tiểu học](https://xaydungchinhsach.chinhphu.vn/huong-dan-to-chuc-day-hoc-cac-mon-ngoai-ngu-1-cap-tieu-hoc-119230810082407558.htm).

Khi nạp đủ nền tảng, bộ Tình huống và bộ Khám phá, mỗi khối có **77 bài,
426 câu, 65 đề**; năm khối tổng **385 bài, 2.130 câu, 325 đề** đang phục vụ,
chưa tính AI Academy hoặc nội dung giáo viên tự tạo. Lớp 1–2: 51 bài Free/26
VIP; lớp 3–5: 50 Free/27 VIP mỗi khối. Bản nháp đã lưu trữ không tính vào các số này.

## Cải thiện hệ thống và quản trị

Trang chủ đếm đầy đủ số lượt đã nộp và chấm, thay vì đếm tối đa 200 dòng lịch
sử đang tải. Có kiểm tra tình huống 205 lượt nhưng danh sách chỉ trả 200 dòng.
Số này là số lượt làm, có thể gồm nhiều lần luyện cùng một đề.

Admin **Chương trình** hiển thị riêng dự kiến/đã xuất bản của từng bộ học liệu.
CSV và bảng chủ đề cộng các nội dung đang hoạt động. Bộ Tình huống cũ tiếp
tục có lệnh tương thích; bộ Khám phá dùng chung cơ chế release để thêm bộ mới
không cần sao chép logic seed/verify hoặc thêm một loạt lệnh CLI riêng.

## Cập nhật máy khác hoặc VPS

Máy hiện tại đã áp dụng. Với máy khác, sao lưu DB, tạm bảo trì khi nâng phiên
bản, giữ cấu hình và thông tin tài khoản. Đã có bộ nền tảng của các khối thì chạy
từ `backend`:

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
../.venv/Scripts/python.exe -m app.cli supplement-inventory --release explorers-2026-01
../.venv/Scripts/python.exe -m app.cli seed-supplement-content --release explorers-2026-01
../.venv/Scripts/python.exe -m app.cli verify-supplement-content --release explorers-2026-01
```

Thêm `--grades 1 2` nếu chỉ nạp/kiểm tra hai khối. Inventory đọc source, không
ghi DB. Lệnh seed dùng một transaction cho các khối được chọn và khóa phối
hợp với các seed khác; chỉ thêm nội dung. Gặp câu hỏi/đề đã khác source thì
báo lỗi và rollback, không ghi đè bản giáo viên đã chỉnh.

VPS dùng wrapper `dc` đã cấu hình trong [hướng dẫn deploy](deploy-vps.md):

```bash
dc run --rm --no-deps migrate
dc exec -T db psql -X -v ON_ERROR_STOP=1 -U viettree_owner -d viettree-education < deploy/grant-runtime.sql
dc run --rm -T --no-deps backend python -m app.cli seed-supplement-content --release explorers-2026-01
dc run --rm -T --no-deps backend python -m app.cli verify-supplement-content --release explorers-2026-01
```

Sau đó cập nhật/recreate API và frontend theo quy trình deploy, kiểm tra
`check-schema`, `/ready`, đăng nhập và thao tác lưu/bỏ lưu trước khi mở bảo trì.
Nếu chuyển database local đã cập nhật sang VPS thì chỉ cần verify, không nạp lại.

## Bảo toàn dữ liệu

Backup local được tạo trước migration và nạp. Đối chiếu **81 bảng/21.910 dòng
có trước đợt này** không thay đổi; chỉ thêm bảng lưu bài và học liệu mới.
[Bằng chứng migration/nạp](audits/explorers-local-2026-10-15.json).

Một câu thơ bản nháp được biên tập lại trước phát hành. Bài cũ chưa có lượt
học/làm được đưa vào lưu trữ, bài thay thế mang mã `words-around-us-r2`;
bốn phiên bản câu hỏi cũ giữ nguyên. Không sửa đáp án hoặc phiên bản của bài
đã làm. [Bằng chứng biên tập](audits/explorers-editorial-2026-10-15.json).

## Kiểm chứng

- 810 kiểm thử backend không integration đạt; 9 ca cần DB bị bỏ qua trong
  lượt này. Nhóm nội dung/API liên quan có 45 ca đạt, gồm 23 integration thực
  trên PostgreSQL riêng; 22 ca nội dung nằm trong cả hai nhóm nên không cộng
  dồn thành tổng kiểm thử độc lập.
- 83 kiểm thử frontend đạt; TypeScript, ESLint, Ruff, kiểm tra định dạng và
  build production đạt.
- 12 kịch bản Chrome desktop/mobile đạt: 10 mới và 2 hồi quy lớp 5. Có thử
  ngắt mạng khi lưu, đăng nhập hai phiên, ghi 13 bài rồi bỏ thẻ cuối trang,
  làm/chấm đủ bốn câu mới, gợi ý VIP, cấp/thu hồi VIP và kiểm kê cả năm khối.
  Kiểm tra không tràn ngang ở 320/390/768/1280 px, gồm trang có thẻ bài đã lưu.
- Schema và verify cả hai bộ bổ sung đạt trên database local. Bản build local
  trỏ API về cổng 8000; các server test cổng 8001/3001 đã dừng.

Chưa chạy lại toàn bộ integration suite hoặc đo sức tải thực trên VPS/mạng
Việt–Nhật trong đợt này. Browser chạy trên server dev local với database test;
build production được kiểm tra riêng. [Kết quả kiểm chứng](audits/explorers-quality-2026-10-15.json).
