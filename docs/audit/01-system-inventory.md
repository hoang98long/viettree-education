# 01 · Bản đồ hệ thống · 11/11/2026

Kiểm toán theo master prompt người dùng cung cấp, trên nhánh
`audit/2026-11-11-system-review`, từ commit `2676328`. Git sạch khi bắt đầu.
Không triển khai production, không đổi `.env`, không dùng dữ liệu học sinh
thật làm fixture. Database đang dùng chỉ được đọc để đối chiếu hash trước/sau.
Mọi ghi dữ liệu kiểm thử nằm trong database mới có hậu tố `-test` hoặc `_test`, được giữ
lại; không DROP/TRUNCATE/reset.

## Kiến trúc thực tế

| Thành phần  | Code/cấu hình                                                                                               | Trạng thái xác minh                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Frontend    | Next.js App Router 16.4.5, React 19.2, TypeScript, Tailwind 4; `frontend/src/app`, `features`, `components` | VERIFIED bằng package/lock và baseline component/typecheck         |
| Backend     | FastAPI, Python, Pydantic, SQLAlchemy Core; `backend/app/api/router.py`                                     | VERIFIED bằng source và test                                       |
| Database    | PostgreSQL 18; SQL gốc 34 bảng, Alembic head `0012_lesson_bookmarks`; 82 bảng ứng dụng                      | VERIFIED bằng database test mới và migration                       |
| Đăng nhập   | Opaque cookie HttpOnly, hash token tại DB, CSRF/Origin, Argon2, giới hạn đăng nhập                          | Có implementation và regression; kết quả đợt này tại 07            |
| Phân quyền  | admin/student/teacher/guardian; owner checks, Free/VIP live, revoke/expire                                  | Có implementation; không chỉ ẩn nút UI                             |
| Học liệu    | `curriculum/registry.py`, grades và 5 supplements; 445 bài/2.370 câu/385 đề                                 | Đối chiếu source và DB test                                        |
| AI Academy  | 200 bài, 11 chủ đề/khối, 7 bước/bài, 600 checkpoint, 2.617 SVG                                              | Training-only mặc định; module có version và progress ghim version |
| Media       | SVG bundled theo manifest/hash; private uploads qua `academy/uploads.py` và volume `academy_media`          | Không có dịch vụ cloud storage bắt buộc                            |
| Cá nhân hóa | `personalization/engine.py`, rule_v1/plan_v2, prerequisites, ôn tập, sổ lỗi                                 | Existing; dựa dữ liệu kết quả, không có ML profiling bắt buộc      |
| Cache       | Static/SVG cache, schema reflection và readiness TTL 60s; dữ liệu cá nhân `no-store`                        | Không có Redis; quyền VIP không cache                              |
| Triển khai  | Docker Compose, Caddy HTTPS, backend workers, Next standalone, DB role owner/runtime                        | Có profile VPS nhỏ và Nhật 8GB; VPS thật chưa được truy cập        |
| Quan sát    | Structured request ID, status/duration; `/health`, `/ready`, CLI check-system/check-release                 | Existing; chưa có hệ metrics/alert bên ngoài                       |
| Jobs        | CLI backup, auth cleanup, rebuild; vận hành bằng lịch hệ điều hành                                          | Không có Celery/queue tự chạy                                      |

Local: browser → Next `/api/v1` rewrite → FastAPI dependency/session
→ service và SQL transaction → PostgreSQL. Production Caddy kết thúc TLS và chuyển `/api/v1` trực tiếp tới backend;
app không dùng thông tin forwarded từ nguồn tùy ý. `main.py` ẩn Swagger trong
production, không phản chiếu nội dung validation/password trong lỗi.

## Ma trận chức năng

Existing nghĩa là có mã và đường đi; không đồng nghĩa đã kiểm thử toàn bộ.
Chứng cứ thực chạy và từng giới hạn được ghi trong 04/07/09.

| Vai trò       | Chức năng                                                             | Tình trạng                                                                  |
| ------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Học sinh      | Đăng nhập, ghi nhớ, đổi mật khẩu, thu hồi phiên, cỡ chữ theo thiết bị | Existing                                                                    |
| Học sinh      | Thư viện lớp/môn, hình bài học, gợi ý, bookmark, học tiếp             | Existing                                                                    |
| Học sinh      | Làm bài, tự lưu, nộp lặp, chấm tại server, lịch sử/mastery            | Existing                                                                    |
| Học sinh      | AI player/quiz/lab/studio/project/portfolio và Free/VIP               | Existing; gợi ý sai version là lỗi được sửa trong đợt này                   |
| Học sinh      | Bỏ một attempt quá hạn và bắt đầu lại theo chính sách rõ ràng         | Partial; cần chốt chính sách, không tự reset bài làm                        |
| Admin         | Tài khoản/vai trò/khóa/mật khẩu/phiên, VIP cấp/gia hạn/thu hồi        | Existing                                                                    |
| Admin         | Bài học/câu hỏi/đề, nháp/preview/công bố, audit log                   | Existing                                                                    |
| Admin         | Lớp/học sinh/giao bài, kiểm kê và kiểm tra trước mở web               | Existing                                                                    |
| Teacher       | Lớp được giao, bài tập, báo cáo, biên soạn AI/chấm rubric theo quyền  | Existing; giới hạn truy vấn theo lớp/quyền                                  |
| Guardian      | Liên kết đã xác minh, theo dõi trẻ, consent/export/privacy workflows  | Existing; không giả định mọi phụ huynh được xem mọi học sinh                |
| Nội dung nghe | Học liệu có trường/support liên quan; kho hiện tại thiên về đọc/hình  | Partial; chưa có chương trình nghe có thu âm chuẩn cho toàn bộ bài          |
| Vận hành      | Thanh toán tự động, SMS/email reset, 2FA, metrics hosted              | Missing; không được tự bổ sung thành yêu cầu bắt buộc hoặc bật dịch vụ thật |

Đối chiếu sâu file/service: [kiến trúc](../architecture.md). Các trạng thái
Broken được ghi thành issue cụ thể trong [risk register](02-risk-register.md).

## Số đo kiểm kê

[inventory.json](evidence/inventory.json): **140 API paths / 156 operations**;
**82 bảng ứng dụng, 152 foreign keys, 174 indexes**, cộng bảng Alembic là 83
bảng public trong snapshot. Không thêm migration trong đợt này.
[Đối chiếu dữ liệu nguồn](evidence/source-preservation.json) xác nhận 83/83
bảng không thay đổi hash trước/sau; không đưa row/hash riêng tư vào báo cáo.

Kho ba môn có single_choice 1.989, fill_blank 266, ordering 56,
multiple_choice 59; không có free_text trong corpus bundled hiện tại.
Authoring có trạng thái pending manual cho câu mở; không được hiểu là
đã có workflow chấm tự luận hoàn chỉnh cho toàn bộ môn.

AI có 40 bài/khối, Free 5/VIP 35; 200 bài chưa khai báo prerequisites.
Lint/schema và test không thay kiểm duyệt sư phạm. Chi tiết tại [06](06-ux-learning-review.md).
