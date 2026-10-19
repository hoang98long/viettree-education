# AI Academy: giải thích lựa chọn và học tiếp — 19/10/2026

AI Academy có **200 bài / 1400 bước / 600 câu checkpoint**, chia đều lớp 1–5.
Mỗi khối có **40 bài thuộc 11 chủ đề**, mặc định **5 Free / 35 VIP**;
toàn module **25 Free / 175 VIP**. Quyền từng bài đã chỉnh trong CMS được giữ.
Ba môn Toán, Tiếng Việt, Tiếng Anh không đổi ở đợt này.

## Thao tác học

- **Hành trình:** thẻ “Bài em đang học” ưu tiên bài chưa xong có hoạt động
  gần nhất và còn quyền truy cập; khi chưa có bài dở thì chọn bài mở tiếp theo.
- **Tìm bài:** tìm theo tên bài hoặc chủ đề, chấp nhận chữ không dấu. Bốn nút
  lọc: tất cả, em có thể học, đang học, đã xong. Kết quả tự mở các chủ đề phù hợp;
  có nút xóa bộ lọc khi tìm không thấy.
- **Trò chơi:** lấy đúng khối từ hồ sơ học sinh; mỗi chủ đề gợi ý một bài có
  hoạt động. Ưu tiên bài đang dở/bài còn mở. Có bộ lọc bỏ bài VIP đang khóa.
  Trước đây màn hình này cố định các mã bài lớp 4.
- Danh mục khối hiện tại dùng dữ liệu sẵn trong `/home`, bỏ lần gọi `/catalog`
  trùng. Chọn khối khác mới tải danh mục riêng. Không cache quyền học phía client.
- Free có một mức gợi ý; VIP có ba mức. Nút chạm, cỡ chữ theo thiết bị và phản
  hồi từng thẻ tiếp tục dùng chung với bài cũ. Các lớp dưới được mở theo chính
  sách hiện hành; xem khối cao hơn chỉ là xem trước danh mục.

## Mười bài mới

Chủ đề **Giải thích lựa chọn**, mã `AI{lớp}-reason`, bài `39` Free và `40` VIP.

| Lớp | Bài 39 — Free                  | Bài 40 — VIP                   |
| --- | ------------------------------ | ------------------------------ |
| 1   | Robot tìm sách                 | Thẻ bị che kín                 |
| 2   | Không chỉ nhìn màu             | Hỏi rõ trước khi làm           |
| 3   | Hai câu hỏi tìm đồ vật         | Dừng ở chỗ chưa biết           |
| 4   | Lời giải thích có đúng căn cứ? | Hai công cụ nói khác nhau      |
| 5   | Gợi ý nhiều chưa chắc phù hợp  | Con người duyệt trước khi dùng |

Lớp 1 có hai thẻ/bài, người lớn có thể đọc cùng. Lớp 2 có ba thẻ; lớp 3 tập
theo quy tắc và nêu giới hạn. Lớp 4–5 dùng bốn thẻ, tìm căn cứ và phân biệt
gợi ý với quyết định đã được con người kiểm tra. Mỗi bài có ba checkpoint,
ba mức gợi ý biên soạn sẵn, hoạt động vận dụng và hướng dẫn giáo viên.
Thẻ bị che được vẽ kín với dấu hỏi, không lộ hình để trẻ đoán theo tranh.

Định hướng theo nhóm tuổi K–2 và 3–5 trong
[AI4K12 — bản hướng dẫn dự thảo](https://ai4k12.org/gradeband-progression-charts/),
và hoạt động dự đoán/phân loại cho lớp 3–5 của
[Code.org — How AI Makes Decisions](https://code.org/en-US/artificial-intelligence).
Các tình huống và hình ở đây do VietTree biên soạn; đây là cách vận dụng vào
thẻ nội bộ, không phải khóa được các tổ chức trên chứng nhận. Giữ
`AI_TRAINING_ONLY=true`; không cần model, GPU hoặc API trả phí.

## Dữ liệu và vận hành

Thêm **77 SVG**, tổng **1702 SVG** gồm cả hình lịch sử. Kiểm tra đủ XML,
hash, alt và liên kết trong bài. Giữ nguyên 1625 media cũ và payload của 190 bài
cũ. Không thay bản published để tránh làm lệch lượt học đang gắn phiên bản cũ.

Danh mục chỉ lấy `hero` và `estimated_minutes` từ JSONB thay vì chuyển toàn bộ
payload từ PostgreSQL sang API; tiến độ truy vấn theo đúng học sinh và khối.
Quyền vẫn kiểm ở server khi mở bài, gửi đáp án, mở gợi ý hoặc tải hình riêng.

Local đã backup trước nạp và đối chiếu từng hàng của **82 bảng**: **23600 hàng
cũ giữ nguyên**; chỉ cập nhật ba trường thông tin chương trình trong năm hàng
`ai_grades`. Thêm 10 bài, 10 phiên bản, 5 chủ đề và media mới. Tài khoản, mật
khẩu, phiên, gói VIP, bài làm và thành tích không đổi. Chi tiết:
[biên bản database](audits/academy-local-2026-10-19.json).

**Máy hiện tại:** khởi động lại backend/frontend, vào **AI Academy → Hành trình**
hoặc **Khám phá thêm → Trò chơi**. Không cần nạp lại tài khoản hoặc reset DB.

**Máy khác:** backup trước, cập nhật source và dùng terminal backend:

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
../.venv/Scripts/python.exe -m app.cli check-system
```

Không có migration mới; head vẫn `0012_lesson_bookmarks`. VPS dùng hàm `dc`
trong [hướng dẫn deploy](deploy-vps.md), backup và build image mới trước:

```bash
dc run --rm -T --no-deps backend python -m app.cli seed-ai-academy
dc run --rm -T --no-deps backend python -m app.cli verify-ai-academy
dc up -d backend frontend caddy
```

Kiểm tra trả 40 bài mỗi khối và `quality.issues=[]` cho bộ gốc. Không cần Redis
hay dịch vụ mới. [Kiểm thử và giới hạn](audits/academy-quality-2026-10-19.md).
