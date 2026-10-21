# Kiểm chứng tổng thể — 20/10/2026

Kết quả tổng hợp theo ca kiểm thử, loại trùng các lần chạy lại; không cộng dồn
số lượt chạy thành số ca khác nhau.

| Phạm vi                      | Kết quả                                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Backend                      | **1109 ca khác nhau đã đạt**, PostgreSQL test thật; không bỏ qua ca cần DB                                         |
| Frontend unit                | **92 passed**, 23 file                                                                                             |
| Browser HTTPS desktop/mobile | **133 ca được kiểm chứng**, một biến thể mobile bỏ qua có chủ đích vì ca desktop đã thử đồng thời ba loại thiết bị |
| Đóng gói/mã                  | Next production build, typecheck, ESLint, Prettier, Ruff đạt; wheel đủ 1702 SVG/schema/module mới                  |
| Học liệu DB                  | 2250 phiên bản câu hỏi trong đề xuất bản không có lỗi schema; AI 200 bài, manifest 1702 SVG hợp lệ                 |
| Cài từ DB trống              | Import → migrate → bộ nền → AI → bốn bộ bổ sung → check-system đạt, đủ 415 bài/355 đề/200 AI                       |
| Backup/restore               | Snapshot nhất quán; 83 bảng khớp số hàng và dấu vân tay dữ liệu; DB nguồn chỉ đọc                                  |
| Dependency                   | npm audit 357 dependency, pip-audit 42 package; không có lỗ hổng đã biết được báo tại thời điểm tra cứu            |

## Cách tính và các lỗi kiểm thử đã sửa

Bộ backend đầy đủ chạy **1104 ca**: 1103 đạt; một assertion cũ vẫn kỳ vọng ba
bài Free lớp 4. Đã sửa thành đối chiếu đúng năm mã Free và kiểm lại đạt. Bốn ca
API/chẩn đoán mới đạt; bộ 15 ca Bash/backup/smoke đạt, gồm một tình huống mới
chặn triển khai khi `check-release` chưa đạt. Tổng ca khác nhau: **1109**.

Browser chạy ban đầu 134 biến thể: 115 đạt, 6 lỗi kiểm thử cũ, 13 bỏ qua.
Đã bổ sung fixture còn thiếu cho 12 biến thể, tách học sinh của từng nhóm để
tránh dùng chung tiến độ, sửa bộ lọc/nút bấm theo giao diện hiện tại và chờ
đúng lúc dữ liệu tải lại. Chạy lại từng nhóm đã xác nhận đủ **133** biến thể;
chỉ giữ một bỏ qua có chủ đích. Không thay đổi hoặc xóa tiến độ thật để làm
kiểm thử đạt. [Danh mục và kết quả gộp](browser-release-2026-10-20.json).

Một lần kiểm tra reload chạm thời hạn assertion 5 giây trong lúc probe tải
cũng chạy trên host; đã thêm bước chờ nội dung tải lại tối đa 15 giây, vẫn kiểm
tra đáp án đã lưu và kết quả nộp. Các ca liên quan đã chạy lại đạt.

Giao diện kiểm tra admin được xem lại qua screenshot. Đã đổi bảng trạng thái
thành danh sách co giãn để luôn thấy “Đạt/Cần xử lý” trên điện thoại; hai ca
desktop/mobile và 92 unit tests được kiểm tra lại sau thay đổi đó.

CI đã thêm seed AI và các bộ bổ sung. Helper `scripts/prepare_e2e.py` tạo
tài khoản riêng cho AI reasoning, daily, verification, applied, bài đọc Free/VIP
và explorers; chỉ chạy trên DB có tên test. Các context TLS phụ dùng cùng cờ
localhost đã giới hạn, không bỏ xác minh chứng chỉ của tên miền VPS thật.

## Tải 50 người qua HTTPS

| Tình huống          | Kết quả                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------- |
| Đăng nhập đồng thời | 50/50, HTTP 200; p95 8398,06 ms                                                          |
| Luyện ba môn        | 750/750 HTTP 200; 50 bài đã chấm, thống kê đối chiếu không lệch; p95 2632,17 ms          |
| Học AI              | 800/800 HTTP 200; 50 hoàn thành, 10 điểm/em, hai lượt chấm/em dù gửi lại; p95 2570,06 ms |

Probe xác minh chứng chỉ bằng CA local; backend production hai worker được
giới hạn vào bốn CPU, pool 4+2 mỗi worker; Next standalone heap 512 MiB. Có
lưu lượng browser kiểm thử trên cùng Windows host. Đây là kiểm tra có tải,
không đại diện cho giới hạn RAM container, mạng Việt Nam–Nhật hoặc SLA VPS.
Đăng nhập có hàng đợi xác minh mật khẩu hai luồng/worker; request học đo riêng.

[Kết quả ba môn](core-https-load-50-2026-10-20.json) ·
[Kết quả AI](academy-https-load-50-2026-10-20.json).

## Bảo toàn dữ liệu và giới hạn còn lại

Database nguồn giữ tài khoản/mật khẩu/VIP/lịch sử. Các ghi thử, đổi mật khẩu,
khóa demo, tạo user/role và chấm bài đều ở hai DB clone tên mới. Sau kiểm tra đã
dừng các server test, xóa hai clone và role riêng; giữ DB local và DB test cũ.
[Biên bản dọn tài nguyên](cleanup-release-2026-10-20.json).

DB nguồn vẫn development và còn 21 demo chưa xử lý, chưa có admin đáp ứng dấu
mốc mật khẩu riêng, đang dùng DB quản trị. Đây là các điều kiện phải xử lý
trên VPS sau restore, trước mở công khai. Bản sao production dùng role runtime
ít quyền đã qua `check-release`. [Preflight](preflight-release-2026-10-20.json).

Chưa có kiểm chứng SSH/VPS/tên miền thật. Docker Engine local chưa chạy nên
không báo build/chạy Compose Linux là đã đạt; workflow image trên Linux chưa
được chạy trong phiên này. Kết quả kỹ thuật và kiểm tra schema không thay thế
đánh giá sư phạm với học sinh thật.

[Hướng dẫn cập nhật và mở web](../pre-deployment-review-2026-10-20.md).
