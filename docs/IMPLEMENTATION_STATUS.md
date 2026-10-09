# Bàn giao VietTree Education — 09/10/2026 (Asia/Bangkok)

Đã triển khai trực tiếp toàn bộ monorepo theo prompt. Luồng demo login và học sinh
làm bài đã kiểm chứng với PostgreSQL thật; không có API điểm/thống kê giả.

| Checkpoint | Kết quả |
| --- | --- |
| 1 · Đọc SQL, mapping constraints | Hoàn thành: 34 bảng, UUID/JSONB/checks/composite FK; SQL gốc giữ nguyên |
| 2 · Cấu hình, auth, migration | Hoàn thành: FastAPI/Next, root env, session/CSRF/RBAC/rate limit, baseline + 2 bảng auth |
| 3 · Seed | Hoàn thành: admin/longnh; 12 topics, 24 lessons, 96 questions, 12 assessments, 12 skills |
| 4 · API làm bài | Hoàn thành: assignment self, exact version, start/resume/save/submit/result/history |
| 5 · Personalization | Hoàn thành: rule_v1, confidence, ôn 1/3/7 ngày, prerequisite/weak skills, rebuild statistics |
| 6 · Frontend | Hoàn thành: public/login, mọi route student/admin yêu cầu, responsive; teacher/guardian layout |
| 7 · Kiểm chứng | Pass backend/unit/integration/concurrency, frontend component/type/lint/build/format, browser desktop/mobile, smoke PostgreSQL |
| 8 · Tài liệu | README tiếng Việt, architecture/API/security/personalization, SQL kiểm chứng seed |

## Chứng cứ đã chạy

| Lệnh/kiểm chứng | Kết quả |
| --- | --- |
| `alembic upgrade head` trên DB thật/test | Pass; revision 0002_auth_sessions; không import lại DB thật |
| `python -m app.cli check-schema` | Pass, đối chiếu đủ bảng và cột |
| `python -m app.cli seed` chạy lặp | Pass; cùng số lượng, không reset password/kết quả |
| `python -m app.cli import-schema` trên DB test | Pass, dùng nguyên SQL gốc, không reset |
| `pytest -q` + TEST_DATABASE_URL riêng | **121 passed**, 1 warning deprecation từ Starlette/httpx |
| `ruff check` / `ruff format --check` | Pass sau formatter |
| `python scripts/smoke.py` trên DB thật | **SMOKE PASS** toàn luồng admin/longnh/chấm/kết quả/history/mastery/stats, rollback |
| `npm run typecheck`, `npm run lint` | Pass |
| `npm test` | **4 passed**, bốn dạng input |
| `npm run build` | Pass, Next.js 16.4.0 production build |
| `npm run format:check` | Pass |
| `npm audit` | **0 vulnerabilities** sau cập nhật toolchain |
| `npm run test:e2e` | **4 passed**: student/admin trên desktop/mobile Chrome, sau reload và route guard |
| `docker compose config --quiet` | Pass |
| SQL `database/seeds/verify.sql` | Mỗi môn 4/8/32/4; 12 đề đều 8 items; 0 câu thiếu skill |
| SQL count attempts DB thật sau smoke | **0**; lịch sử/điểm demo vẫn sạch |
| Browser với backend nối DB thật sau kiểm thử | Pass login/dashboard/logout admin và longnh, history=0; `/ready` trả ready |

Integration từ chối DB thật. Các test concurrency và browser có dữ liệu ghi thật
trong viettree-education-test; không xóa/reset cả database test. Browser lần đầu dùng
longnh, lần kiểm chứng cuối dùng học sinh test riêng do create_test_student.py tạo.

## Các phần chủ động để chờ theo prompt

Form tạo bài tập cho admin/teacher đầy đủ trường nhưng tất cả thao tác lưu/xuất bản
disabled; không có write CRUD câu hỏi. Guardian/teacher quản lý lớp/phụ huynh chưa
mở. Nội dung lớp 1/2/3/5 và bốn môn còn lại đang xây dựng. Không có AI trả phí,
upload/audio, chấm tự luận, public signup, Redis/MinIO hay leaderboard công khai.
Lộ trình MVP dùng lessons/progress/recommendations; chưa tự sinh learning_plan_items.

Docker daemon không chạy trong môi trường này: **chưa kiểm thử build/run container**,
chỉ cấu hình đã validate. Không tuyên bố Docker runtime pass. Local host full stack
và kết nối PostgreSQL đã được kiểm chứng. Tài liệu có hạn chế rate limit sau proxy,
rebuild toàn lịch sử, retention auth và yêu cầu consent trước khi vận hành thực tế.

Khởi động, tài khoản local DEV và lệnh kiểm chứng xem README. Không có bước deploy
Internet/commit/push tự động; toàn bộ thay đổi nguồn nằm trong workspace.

Khi bàn giao, frontend dev ở http://localhost:3000 và backend ở
http://localhost:8000 đang chạy, kết nối lại database thật `viettree-education`.
