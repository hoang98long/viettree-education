# Kiểm chứng học liệu và học tiếp — 17/10/2026

| Kiểm tra                                        | Kết quả                                                                     |
| ----------------------------------------------- | --------------------------------------------------------------------------- |
| Backend, toàn bộ nhóm không yêu cầu integration | 848 đạt; 9 ca cần DB được bỏ qua; 221 integration tách riêng                |
| Integration PostgreSQL có chọn lọc              | 17 ca riêng biệt đạt: 5 daily, 7 resume, 5 learning                         |
| Frontend unit                                   | 87 đạt                                                                      |
| Browser desktop + iPhone 13 mô phỏng            | 18 ca riêng biệt đạt; 2 ca AI kiểm tra lại sau tinh chỉnh bố cục cũng đạt   |
| Tải API HTTP local, 50 học sinh                 | 50 đăng nhập, 750/750 request học HTTP 200, 50/50 bài nộp hoàn tất          |
| Đối chiếu sau tải                               | 50 bài chấm/50 kết quả ngày, 0 sai lệch thống kê câu                        |
| Source database                                 | Backup custom + `pg_restore --list`, giữ nguyên 23170 dòng cũ trong 82 bảng |

## Nội dung và quyền

60 câu mới kiểm tra schema, một đáp án chấm đúng và nguồn ngữ liệu trong câu đọc.
Đáp án Toán được đối chiếu riêng: giờ/phút, qua giờ mới, tổng thời gian và đổi
30 phút thành 0,5 giờ trước tính quãng đường. Bài/câu cũ không được ghi lại.
Các bài Free/VIP, gợi ý 1/3 và số liệu quản trị được kiểm tra cả năm khối.

Học tiếp kiểm tra quyền sở hữu, sai khối, hoàn thành, lưu trữ, hết giờ, đóng
giao bài, lớp AI thấp/cao hơn, cấp/thu hồi VIP, grace sau hết hạn và cấp lại VIP
sau thu hồi lượt làm. Kiểm tra riêng không ghi DB và số query có giới hạn.
Chỉ trả metadata, không gửi đáp án/payload của bài khóa. Việc mở bài vẫn qua
authorization hiện có, không tin URL hoặc dữ liệu thẻ.

Resume dùng ba truy vấn loại nội dung và membership; bài luyện kiểm tối đa năm
ứng viên gần nhất sau lọc sơ bộ, rồi xác minh policy/grant thực tế trước khi chọn.
Không quét toàn lịch sử, không gọi model và không thêm bảng/cache dùng chung.

## Trình duyệt và hình ảnh

Mười ca cho năm khối × hai thiết bị: mở bài mới, gợi ý, về trang chủ qua logo,
tiếp tục đúng lượt/câu trả lời đã lưu và nộp cả bốn câu đạt 4/4.
Bốn ca kiểm tra sửa thẻ AI và gộp ba loại học tiếp; hai ca kiểm kê admin;
hai ca bổ sung hội thoại VIP với hình cơm/nước và đủ ba gợi ý.
Đã chụp và xem giao diện mobile, bỏ cách trình bày phản hồi thành nhiều cột hẹp.

Vòng browser đầu có lỗi selector khớp đuôi “5 phút” vào “85 phút” hoặc
“30 phút” vào “7 giờ 30 phút”; đã đổi sang tên lựa chọn đầy đủ. Fixture ba
thẻ cũng được chuẩn bị với một bài đọc còn dở vì bài Toán đạt điểm đã tự hoàn
thành theo hành vi sẵn có. Sau sửa bộ kiểm thử, cả 16 ca gốc và hai ca hình
bổ sung đạt; không coi lỗi fixture/selector là lỗi sản phẩm.

## Tải và giới hạn

[JSON tải local](daily-load-50-2026-10-17.json): Windows 12 logical CPU,
PostgreSQL thật, 25 Free/25 VIP đủ lớp 1–5. Đăng nhập tuần tự ngoài lượt đo;
50 luồng học đồng thời, gồm lưu, kiểm tra dashboard khi đang làm, nộp lặp và
đọc lại kết quả. **750 request/16,88 giây**, p95 **2237 ms**, p99 **2681 ms**.
Lượt thử xác nhận đúng attempt trong `resume_items` của mỗi học sinh.

Không đo Next/Caddy/TLS, đăng nhập dồn, tải dài hoặc mạng Việt Nam–Nhật.
Không suy ra VPS thật có cùng độ trễ. Cần build Docker Linux, HTTPS, backup/
restore và kiểm tra từ mạng học sinh khi có server/domain.

## Local

[Biên bản seed](daily-local-2026-10-17.json) có checksum/path backup và số dòng
thêm. Không đổi tài khoản, mật khẩu, phiên, VIP, điểm, tiến độ hoặc các phiên
bản đã xuất bản. Chỉ thêm học liệu daily; head vẫn `0012_lesson_bookmarks`.
Các fixture/browser/load chỉ ghi vào DB test riêng. Server test do đợt này
mở đã dừng trước bàn giao; log ở `.tools/daily-*.log`.

TypeScript, ESLint, Ruff, format và production build đều đạt. Build cuối dùng
API mặc định localhost:8000. check-system trên database local đạt, không có
bài/đề/câu thiếu chính sách quyền hoặc đề lỗi cấu trúc.
