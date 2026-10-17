# Kiểm chứng học liệu — 16/10/2026

| Kiểm tra                                | Kết quả                                                                                                     |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Backend, nhóm không yêu cầu integration | 837 đạt; 9 ca cần database bỏ qua; 209 integration tách riêng                                               |
| Integration PostgreSQL chọn lọc         | 32 ca riêng biệt đạt, ghi chú bên dưới                                                                      |
| Frontend unit                           | 84 đạt                                                                                                      |
| Playwright desktop + iPhone 13 mô phỏng | 12 ca mới đạt; 2 ca lớp 1 kiểm tra lại sau sửa hình cũng đạt                                                |
| Tải API local                           | 50 đăng nhập thành công; 700/700 HTTP 200 trong lượt học; 50/50 bài nộp hoàn tất                            |
| Thống kê sau tải                        | 50 bài chấm, 50 kết quả ngày; 0 sai lệch thống kê câu hỏi                                                   |
| Nội dung cũ                             | Payload nguồn 180 bài AI và metadata/bytes của 1547 SVG giữ nguyên                                          |
| Seed local                              | Backup custom, kiểm `pg_restore --list`; giữ 22369 dòng cũ; chỉ đổi mô tả chương trình ở 5 dòng `ai_grades` |

32 integration thuộc `test_academy`, `test_visual_learning`,
`test_academy_management`, `test_review_content`, `test_verification_content`.
Vòng chọn lọc có 27 ca đạt; 5 ca mới ban đầu sửa trạng thái thu hồi trực tiếp
không đáp ứng constraint database. Fixture được sửa để gọi service thu hồi
thực tế; chạy lại 6 integration của file mới đều đạt (một ca trùng vòng trước).
Một vòng trước đó bị ảnh hưởng khi tái tạo SVG; kiểm tra sau cùng dùng artifact
hoàn chỉnh. Không tính các lỗi fixture này là lỗi sản phẩm đã sửa.

Kiểm tra gồm học/chấm/hoàn thành cả năm khối, đáp án đối chiếu độc lập,
Free/VIP, gợi ý, cấp/thu hồi VIP, media VIP, không gọi provider,
idempotency và seed giữ phiên bản/tiến độ. Browser kiểm tra từng bước học,
reload tiếp tục, bài đọc mới, admin kiểm kê năm khối và không tràn ngang mobile.
Đã mô phỏng server lưu bài nhưng phản hồi bị mất: gửi lại cùng mã trả đúng kết quả.

Tranh lớp 1 đã kiểm tra lại: 2 + 3 có đúng 5 chấm, không thêm chấm trang trí;
tranh bút/táo mới có màu khớp nhãn. Kiểm thử kỹ thuật/biên tập nội bộ chưa thay
cho đánh giá hiệu quả học tập với học sinh thực tế.

## Tải và giới hạn

[JSON tải](verification-load-50-2026-10-16.json): Windows 12 logical CPU,
HTTP local, PostgreSQL thật, 25 Free/25 VIP đủ năm khối. Đăng nhập tuần tự,
sau đó 50 luồng học đồng thời gồm trả lời/lưu/nộp/chấm bài. 700 request trong
12,76 giây, p95 **1708 ms**, p99 **2297 ms**, khoảng 54,86 request/giây.
50 request đăng nhập thống kê riêng.

Không đo Next/Caddy/TLS, mạng Việt Nam–Nhật, đăng nhập đồng thời hoặc tải dài.
Không suy ra VPS bảo đảm cùng độ trễ. Docker Linux và chứng chỉ công khai vẫn
cần kiểm tra trên server đích. Không thêm dịch vụ model, RAM/GPU.

## Bảo toàn database

Biên tập cuối: câu Toán lớp 3 được hỏi rõ "thử riêng thương 8" để tránh hai lựa
chọn đều có thể giúp phát hiện lỗi. Đã tạo mã bài `check-my-math-r2`; bản đầu chưa
có bài làm/tiến độ được lưu trữ, giữ nguyên bốn phiên bản câu hỏi cũ. Có backup
và [biên bản riêng](verification-editorial-2026-10-16.json). Năm integration của
bộ review được chạy lại và đạt sau chỉnh câu hỏi; không đổi quy mô học liệu hoạt động.

[Biên bản local](verification-local-2026-10-16.json) lưu checksum/path backup,
đếm hàng thêm và metadata được phép cập nhật. So sánh dòng cũ trong 82 bảng
nghiệp vụ; tài khoản/mật khẩu/phiên/VIP, tiến độ, bài làm, phiên bản cũ giữ nguyên.
Không reset, xóa hoặc tạo kết quả demo trên database chính.

Học liệu đã nạp vào `viettree-education`; `check-system` đạt, head
`0012_lesson_bookmarks`, không có bài/đề/câu thiếu quyền hay đề lỗi cấu trúc.
Khởi động lại backend/frontend để dùng code mới.

Log ở `.tools/verification-*.log`; không đưa credential vào báo cáo. Pytest còn
cảnh báo deprecation upstream của Starlette/httpx, không làm hỏng các ca kiểm thử.

TypeScript, ESLint, Ruff, kiểm tra format và production build đều đạt.
Build cuối dùng API mặc định localhost:8000; các server test riêng đã dừng.
