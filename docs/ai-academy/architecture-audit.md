# Khảo sát tương thích · 12/10/2026

Đã đọc đầy đủ prompt trong Downloads, README, manifests, SQL gốc, Alembic,
auth/session/CSRF, access, routing/Shell, component primitives, test fixtures,
Docker development/production và hướng dẫn Next.js cài trong node_modules.
Repo có thay đổi chưa commit từ các đợt trước; giữ toàn bộ các thay đổi này.

- FastAPI + SQLAlchemy Core reflection + PostgreSQL; Next.js 16 App Router,
  React/TypeScript. Giữ nguyên stack, không tạo ứng dụng thứ hai.
- SQL gốc 34 bảng; users/user_roles/student_profiles, schools/classes/
  class_enrollments, guardian_students, media_assets/privacy_consents đã tồn tại.
  Guardian phải có verified_at, teacher chỉ quản lý lớp được phân công.
- Role gốc chỉ student/guardian/teacher/admin: quyền editor/reviewer nằm ở bảng
  quyền riêng của Academy, không đổi constraint user_roles.
- Session opaque, CSRF, bắt đổi mật khẩu tạm, RBAC và rate-limit DB được tái sử dụng.
  Không tạo login riêng, không cache quyền, không đổi password hay gói học.
- Nội dung lớp 3/4 cũ dùng bảng lessons/questions/assessments. Academy dùng prefix
  ai_ để không sửa bài hoặc lịch sử cũ; cấu trúc nội dung có phiên bản JSONB được
  validate, các quan hệ giao bài/lượt làm/tiến độ vẫn FK và transaction.
- Chưa có storage uploader/AI provider/queue. Media SVG biên soạn chạy local;
  raster được chuẩn hóa/resize ở backend, không cho SVG tùy ý từ người dùng.
  Adapter Ollama chỉ gọi backend, mặc định simulation; không gọi API trả phí.
- CI chưa có; test PostgreSQL riêng hiện có, 402 backend/19 component/26 browser
  là mốc hồi quy. Cần chạy lại sau module. Docker Engine chưa chạy ở mốc khảo sát.

ADR: một deployment LMS, catalog chung; school scope theo lớp/enrollment/profile.
Không tuyên bố hỗ trợ SaaS tenant tách biệt. Academy nền tảng miễn phí; việc học
không yêu cầu provider/microphone/camera. Student nhập tự do chỉ xử lý local và
kiểm duyệt; provider chỉ nhận tham số được chọn và nội dung bài đã duyệt, không
nhận tên, user ID, hồ sơ hoặc nguyên văn bài làm trẻ. Consent và flag kiểm tra
ở server. Sản phẩm luôn riêng tư, cần giáo viên duyệt; không có gallery công khai.
