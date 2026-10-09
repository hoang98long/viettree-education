# Quyền và vận hành

| Tài nguyên | Student | Admin | Teacher / Guardian |
| --- | --- | --- | --- |
| Nội dung published | Đọc | Đọc | Đọc chung |
| Bắt đầu/lưu/nộp bài | Chỉ bài của mình, đúng lớp và assignment | Không đóng vai học sinh | Chưa mở |
| Kết quả, lịch sử, mastery | Của mình | Xem attempt/result và thống kê tổng hợp | Chưa mở |
| Câu hỏi/đáp án nội bộ | Không | Read-only | Chưa mở |
| Hồ sơ học sinh | Xem của mình | Xem/cập nhật tên/lớp, audit | Chưa mở |
| Form tạo bài | Không | Scaffold disabled | Teacher scaffold disabled |

Phiên opaque ngẫu nhiên 48 bytes, DB chỉ giữ SHA-256 token và CSRF token. Cookie
HttpOnly/SameSite=Lax; Cookie Secure bật qua môi trường production. CSRF header
phải khớp hash của session cho mọi request ghi có đăng nhập. Login dùng JSON, kiểm
tra Origin allowlist và Sec-Fetch-Site để tránh login CSRF; CORS cho origin cụ thể.
Logout/reset password thu hồi phiên tại DB. Thời hạn phiên tuyệt đối, không refresh.

Argon2id lưu password_hash. Không serialize password/hash/session_hash. Validation
errors không phản chiếu input. Structured log không chứa body/IP/user/đáp án/SQL.
IP dùng cho rate limit được SHA-256, không phải dữ liệu ẩn danh tuyệt đối; cần
retention được xác định khi vận hành. Chưa có job dọn auth tables trong MVP.

SQLAlchemy Core parameterized. Composite FK của schema gốc + checks phía server
chặn IDOR/nhầm assessment/question_version. Bài published không bị seed chỉnh
sửa. API trước nộp whitelist prompt/options, mỗi option chỉ id/text; không grading
hoặc explanation. React render JSON thành text, không dangerouslySetInnerHTML.

Production cần reverse proxy HTTPS, secrets bên ngoài repo/image, DB role riêng
không có DDL (migration do role vận hành riêng), backup mã hóa, restore rehearsal,
retention/consent đúng quy trình đơn vị vận hành và kiểm tra truy cập định kỳ.
APP_ENV=production từ chối cookie không secure, postgres superuser, DB password
ngắn và origins không HTTPS. Không tự thay quyền của PostgreSQL hiện có.
MVP không triển khai legal consent UI, xóa dữ liệu trẻ hay export PII. Cần xây quy
trình consent, đối chiếu guardian_students xác minh và chính sách audit trước
khi dùng thực tế cho trẻ; tài khoản demo chỉ phục vụ development.
