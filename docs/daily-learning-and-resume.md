# Học thuận tiện hơn và bộ Mỗi ngày một khám phá

Cập nhật **17/10/2026**: 15 bài mới, 60 câu hỏi, 15 đề luyện tập cho lớp 1–5;
trang chủ học tiếp được bài đọc, lượt luyện và bước AI; bài AI giúp tìm lại
thẻ chưa đúng để sửa. Database local đã nạp sau backup, không có migration mới.

## Học tiếp trên trang chủ

Nút **Học tiếp** mở việc đang dở có hoạt động gần nhất. Vùng **Bài em đang học**
có tối đa ba thẻ: một bài đọc, một lượt luyện, một bài AI. Bài luyện mở đúng
lượt đã lưu, không tạo lượt mới; AI tiếp tục theo bước đã lưu. Bài đọc mở lại
đúng bài, chưa lưu vị trí cuộn hoặc đoạn đang đọc.

Server lọc theo tài khoản và quyền hiện tại: bỏ bài hoàn thành, bài lưu trữ,
môn/chủ đề ngừng hoạt động, bài sai lớp và bài luyện đã hết giờ/đóng giao bài.
AI cho phép ôn lớp dưới như chính sách hiện có. Thu hồi VIP ẩn bài VIP khỏi
học tiếp; một lượt luyện đã thu hồi không xuất hiện lại chỉ vì được cấp lại VIP.
Thời gian được tiếp tục lượt VIP sau hết hạn vẫn theo grant cũ, không mở bài
VIP mới. Trạng thái được kiểm tra lại khi mở bài; thẻ học tiếp không cấp quyền.

Không tạo bảng hoặc ghi tiến độ giả khi xem trang chủ. Dữ liệu này không cache
dùng chung giữa học sinh. Endpoint dashboard có `resume_items`, giữ
`continue_lesson` để tương thích; chi tiết ở [API](api.md).

## Thử lại trong bài AI

Sau chấm, các nút **Thẻ/Câu … · Xem lại** đưa tới đúng phần chưa khớp.
Mỗi lần chỉ hiện giải thích của thẻ/câu đang nhìn, tránh lặp cả danh sách dài.
Đổi lựa chọn sẽ bỏ kết quả cũ và yêu cầu kiểm tra lại trước khi học tiếp.
Các lượt gửi lại do mất phản hồi vẫn giữ idempotency đã có.

Phản hồi sau chấm giúp học lại, tách với thang gợi ý trước chấm: Free vẫn một
mức gợi ý, VIP ba mức. Không gọi model. Bố cục phản hồi thành từng dòng, cỡ chữ
theo lựa chọn của học sinh, có kiểm tra trên màn hình điện thoại.

Tham khảo nguyên tắc giúp học sinh dùng phản hồi để sửa chỗ chưa hiểu trong
[hướng dẫn EEF](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/feedback).
Đây là lựa chọn thiết kế UX; kiểm thử kỹ thuật chưa chứng minh hiệu quả học tập.

## Bài học mới

Mã bộ học liệu: `daily-2026-03`. Mỗi khối thêm ba bài, bốn câu/bài và một đề/bài.

| Khối | Toán — Free              | Tiếng Việt                         | Tiếng Anh — VIP, tự chọn |
| ---- | ------------------------ | ---------------------------------- | ------------------------ |
| 1    | Bảy giờ sáng rồi!        | Sách đặt lên bàn — Free            | Thank you, my friend!    |
| 2    | Nửa giờ trên đồng hồ     | Góc bàn gọn gàng — Free            | Where is my book?        |
| 3    | Đọc sách trong bao lâu?  | Chia việc làm thẻ sách — VIP       | Meet my family           |
| 4    | Xếp lịch học và nghỉ     | Đọc kỹ hướng dẫn làm hộp bút — VIP | My morning               |
| 5    | Chuyến đi trong bài toán | Đọc thông báo trước khi đi — VIP   | A polite meal            |

Tổng **7 Free / 8 VIP**. Bài ngắn 6–8 phút, Free một gợi ý/VIP ba gợi ý.
Toán có đồng hồ/biểu đồ khớp dữ kiện; tiếng Việt có văn bản gốc trong mỗi câu
hỏi; tiếng Anh có nghĩa từ mẫu và ngữ cảnh hội thoại. Thêm tranh SVG bát cơm,
dùng cùng tranh nước uống và các hình sẵn có, chỉ ghép hình với nhãn cụ thể.

Nội dung dựa trên các mạch đã có trong registry: thời gian/đo lường/chuyển động,
đọc hiểu và giao tiếp quen thuộc. Không tự nhận bao phủ một bộ sách giáo khoa.
Nguồn chương trình theo môn/khối vẫn hiển thị tại quản trị Chương trình học.
Tiếng Anh lớp 1–2 là phần làm quen tự chọn, có thể nhờ người lớn đọc mẫu.

Sau baseline và bốn bộ applied/explorers/review/daily: mỗi khối **83 bài /
450 câu / 71 đề**, tổng **415 bài / 2250 câu / 355 đề** ba môn. Không tính
190 bài AI hoặc học liệu giáo viên tự tạo. Các bộ bổ sung được nạp riêng.

## Nạp trên máy khác hoặc VPS

Sao lưu trước khi nâng cấp. Trong thư mục backend trên Windows:

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-supplement-content --release daily-2026-03
../.venv/Scripts/python.exe -m app.cli verify-supplement-content --release daily-2026-03
../.venv/Scripts/python.exe -m app.cli check-system
```

Head vẫn `0012_lesson_bookmarks`. Trên local hiện tại chỉ cần khởi động lại
backend/frontend; không cần seed tài khoản hoặc đổi mật khẩu.

VPS: backup, build image mới, migrate/grant nếu môi trường còn ở head cũ,
rồi dùng hàm `dc` trong [hướng dẫn deploy](deploy-vps.md):

```bash
dc run --rm -T --no-deps backend python -m app.cli seed-supplement-content --release daily-2026-03
dc run --rm -T --no-deps backend python -m app.cli verify-supplement-content --release daily-2026-03
dc up -d backend frontend caddy
```

Máy/VPS chưa có các bộ trước cần nạp chúng theo hướng dẫn tương ứng:
[applied](applied-learning.md), [explorers](bookmarks-and-explorers.md),
[review và AI 16/10](learning-upgrade-2026-10-16.md).
Giữ `AI_TRAINING_ONLY=true`; không thêm Redis/model hoặc dịch vụ mới.

[Kết quả kiểm thử và bảo toàn dữ liệu](audits/daily-quality-2026-10-17.md).
