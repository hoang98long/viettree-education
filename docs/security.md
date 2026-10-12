# Quyền và vận hành

| Tài nguyên                | Student                                  | Admin                                                        | Teacher / Guardian                                   |
| ------------------------- | ---------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| Nội dung published        | Đúng lớp và đủ gói                       | Xem trước                                                    | Chỉ metadata; nội dung học sinh yêu cầu role student |
| Bắt đầu/lưu/nộp bài       | Chỉ bài của mình, đúng lớp và assignment | Không đóng vai học sinh                                      | Chưa mở                                              |
| Kết quả, lịch sử, mastery | Của mình                                 | Xem attempt/result và thống kê tổng hợp                      | Chưa mở                                              |
| Câu hỏi/đáp án nội bộ     | Không                                    | Biên soạn, duyệt, xuất bản, audit                            | Chưa mở                                              |
| Hồ sơ học sinh            | Xem của mình                             | Xem/cập nhật tên/lớp, audit                                  | Chưa mở                                              |
| Form tạo bài              | Không                                    | Ghép đề, duyệt, xuất bản và giao cho học sinh                | Teacher scaffold disabled                            |
| Gói học                   | Xem gói của mình                         | Cấp/gia hạn/thu hồi và audit                                 | Guardian chỉ xem gói trẻ có liên kết verified_at     |
| Chính sách Free/VIP       | Không sửa                                | Sửa nhãn/preview, CSRF và audit                              | Không sửa                                            |
| Nháp và biên soạn bài học | Không đọc/ghi                            | Nháp riêng, review/publish, revision/fingerprint, CSRF/audit | Chưa mở                                              |

Phiên opaque ngẫu nhiên 48 bytes, DB chỉ giữ SHA-256 token và CSRF token. Cookie
HttpOnly/SameSite=Lax; Cookie Secure bật qua môi trường production. CSRF header
phải khớp hash của session cho mọi request ghi có đăng nhập. Login dùng JSON, kiểm
tra Origin allowlist và Sec-Fetch-Site để tránh login CSRF; CORS cho origin cụ thể.
Logout/reset password thu hồi phiên tại DB. Thời hạn phiên tuyệt đối, không refresh.
Phiên thường mặc định 8 giờ; học sinh không có role admin/teacher có thể chọn ghi
nhớ 7 ngày. API kiểm tra DB ở mỗi request bảo vệ, không cache quyền xác thực.
Cache `/auth/me` 30 giây chỉ nằm trong bộ nhớ giao diện, có kiểm tra lại và đồng bộ
đăng xuất giữa tab. Chi tiết: [quản lý phiên và cache](session-management.md).

Argon2id lưu password_hash. Không serialize password/hash/session_hash. Validation
errors không phản chiếu input. Structured log không chứa body/IP/user/đáp án/SQL.
IP dùng cho rate limit được SHA-256, không phải dữ liệu ẩn danh tuyệt đối; cần
retention được xác định khi vận hành. `cleanup-auth` mặc định chỉ thống kê;
`--apply` dọn auth đã hết hạn/thu hồi và cửa sổ login cũ hơn retention, mặc định
30 ngày. Không xóa lịch sử học tập/audit. Người vận hành đặt lịch sau backup.

SQLAlchemy Core parameterized. Composite FK của schema gốc + checks phía server
chặn IDOR/nhầm assessment/question_version. Bài published không bị seed chỉnh
sửa. API trước nộp whitelist prompt/options, mỗi option chỉ id/text; không grading
hoặc explanation. React render JSON thành text, không dangerouslySetInnerHTML.

Production cần reverse proxy HTTPS, secrets bên ngoài repo/image, DB role riêng
không có DDL (migration do role vận hành riêng), backup mã hóa, restore rehearsal,
retention/consent đúng quy trình đơn vị vận hành và kiểm tra truy cập định kỳ.
APP_ENV=production từ chối cookie không secure, postgres superuser, DB password
ngắn và origins không HTTPS. Mọi môi trường từ chối origin rỗng/wildcard/đường
dẫn và APP_ENV sai. Bộ production tách role migration/ứng dụng, không tự thay
quyền của PostgreSQL hiện có; chi tiết [deploy-vps.md](deploy-vps.md).
MVP không triển khai legal consent UI, xóa dữ liệu trẻ hay export PII. Cần xây quy
trình consent, đối chiếu guardian_students xác minh và chính sách audit trước
khi dùng thực tế cho trẻ; tài khoản demo chỉ phục vụ development.

Free/VIP được kiểm tra tại server, độc lập vai trò/owner. Đề kế thừa yêu cầu VIP
nếu gắn bài VIP hoặc dùng chung question_version với đề/bài VIP; không thể chỉ đổi
nhãn đề sang Free để lấy câu hỏi. Nội dung thiếu policy bị từ chối. Preview chỉ có
đoạn giới thiệu riêng, không có bản đầy đủ bị che ở trình duyệt.

Hết hạn chuyển Free theo starts_at <= server_now < ends_at, không chờ cron.
Ngoại lệ hoàn tất 60 phút chỉ dùng grant gắn chính attempt/chủ sở hữu đã bắt đầu;
thu hồi đánh dấu tất cả grant, không khôi phục khi cấp lại. Kết quả đã chấm vẫn theo
owner. Idempotency-Key UUID + fingerprint + khóa DB ngăn cấp/gia hạn lặp; input
không cho client quyết định ends_at, nguồn thanh toán hay đích học sinh của attempt.

Góc tư duy trả metadata của bài published ở môn/chủ đề hoạt động, đúng lớp lấy
từ hồ sơ; không nhận student_id hoặc grade do client chọn. Tiến độ join theo chính
user. Nội dung/gợi ý bài VIP vẫn được bảo vệ ở endpoint bài học. Bảng học liệu
chỉ admin; số liệu nội dung không được dùng để suy ra năng lực học sinh.
Nhóm bài và số liệu SVG đi qua schema biên soạn, giới hạn kích thước/giá trị;
không nhận HTML, JavaScript hay URL hình ngoài từ nội dung này.

Quản trị tài khoản mới có RBAC/CSRF, xác nhận mật khẩu người thực hiện, giới hạn
xác nhận dùng chung trong DB, revision và khóa transaction cho đổi vai trò/trạng
thái. Khóa/đổi tên đăng nhập/vai trò/reset thu hồi phiên. Mật khẩu tạm bị chặn ở
backend trước khi đọc học liệu hoặc quản trị. Tự đổi mật khẩu thay token/CSRF và
thu hồi mọi phiên cũ. Nhật ký không ghi bí mật hoặc email plaintext; error handler
chỉ log loại lỗi/tên constraint, không SQL/parameters. Chi tiết và giới hạn:
[account-management.md](account-management.md).

Đăng nhập giới hạn 120 lượt/IP/phút và 10 lượt/tên đăng nhập/phút, dùng bộ đếm
PostgreSQL giữa worker. Caddy ghi đè forwarded IP; Uvicorn chỉ tin IP Caddy cố
định, không tin header client trực tiếp. Local qua Next proxy vẫn dùng chung
IP cho giới hạn IP, nhưng có giới hạn từng username độc lập.

API có X-Request-ID tự sinh, header no-store và lỗi bất ngờ an toàn; nhật ký chỉ
loại lỗi/mã request và số liệu request, không exception text/SQL/body. Docs API
tắt production. `/ready` kiểm tra DB/revision mỗi lần, cache cấu trúc tối đa 60
giây; không cache phiên/quyền. Admin system-status chỉ đọc và chỉ trả kết quả
kiểm tra tổng hợp; không phải bằng chứng backup/HTTPS/khả năng chịu tải.
