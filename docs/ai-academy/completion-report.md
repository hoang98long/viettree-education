# Báo cáo thực hiện prompt AI Academy · 12/10/2026

Đã đọc toàn bộ file VietTree_AI_Academy_Codex_Prompt.txt trong Downloads và
thực hiện mã nguồn, migration, học liệu, media, giao diện, kiểm thử và tài liệu
trong repository đang dùng. Các mục cần model/hạ tầng ngoài chưa được nhận là
đã chạy thật; xem phạm vi dưới đây.

Cập nhật theo yêu cầu tiếp theo: [AI đào tạo Free/VIP](../ai-training-vip.md)
thay chính sách nền tảng Free trước đây; head 0011, `AI_TRAINING_ONLY=true`
chặn gọi model. Xem [đợt triển khai và kiểm thử mới](../IMPLEMENTATION_STATUS.md),
[lớp/thành tích](../classes-achievements.md), [giá/ưu đãi](../vip-pricing-research.md).

## 1. Khảo sát

README, Next.js/React/FastAPI/PostgreSQL, SQL gốc 34 bảng, migrations 0001–0009,
auth/CSRF/session, Free/VIP, hồ sơ/lớp/phụ huynh/media/consent, editor cũ,
Docker/production guide và các kiểm thử. Giữ các thay đổi chưa commit trước đó.
Chi tiết [architecture-audit.md](architecture-audit.md).

## 2. Kiến trúc

Một ứng dụng, một DB, cùng auth. 29 bảng ai_ và nội dung phiên bản JSONB;
reuse users/profile/class/enrollment/guardian/media/consent. Editor/reviewer
ở grant riêng trên global teacher. Provider simulation mặc định, adapter
Ollama có cổng policy/flag/consent/quota/moderation. Không thêm Redis/worker nặng.
Nội dung và sản phẩm revision; learner pin phiên bản, grading/rewards ở server.

## 3. File và migration

- `backend/alembic/versions/0010_ai_academy.py`, `app/academy/schema.sql`,
  `tables.py`, `schemas.py`, `curriculum*.py`, `media.py`, `assets/*.svg`,
  `data/media-manifest.json`, `seed.py`, `learning.py`, `games.py`,
  `providers.py`, `tutor.py`, `safety.py`, `uploads.py`, `cms.py`,
  `api.py`, `management_api.py`.
- Registration ở main/db/CLI/config, httpx/Pillow, package-data và env mẫu.
- `frontend/src/features/academy/*`, routes student/teacher/guardian/admin,
  links trong shell, dashboard giáo viên.
- Production private volume, backup DB + media, backend image quyền ghi;
  `backend/tests/test_academy*.py`, fixture/browser tests và docs/ai-academy.

## 4. Chức năng chạy

Học/resume/chấm/điểm/huy hiệu; board tương tác và lab; Prompt Builder;
hint ladder theo Free/VIP, tutor mô phỏng/adapter; sản phẩm comic/poster/quiz/
báo cáo classifier từ mẫu, nháp tự lưu/revision/nộp/in; giao bài/báo cáo CSV/
rubric; verified guardian/consent/export/yêu cầu gỡ text; CMS chủ đề/nhân bản/
steps/câu hỏi/media/preview/draft/review/publish/ẩn/khôi phục thành nháp;
raster resize/approval, SVG jobs; prompt version/approval, moderation inbox,
admin lớp/ghi danh/quyền/chính sách/tổng quan.

## 5. Nội dung thật

48 bài: lớp 4 là 36 tiết/9 chủ đề, lớp 1/2/3/5 mỗi lớp 3 mẫu + khung năm.
336 bước, 144 checkpoint questions, 10 loại activity, 24 mẫu lab,
5 dự án/khối, 12 badges. 315 SVG: 8 mascot, 19 covers, 48 heroes,
144 support, 72 cards, 12 badge images, 12 UI. 315 brief minh họa trong JSON.
Không chỉ file rỗng hoặc báo cáo “đã sinh” khi không có asset.

Rà soát ảnh phát hiện phần giải thích 3/8 của AI4-12 gắn ví dụ 1/4;
đã tạo published v2 với hình 3/8 đúng. Giữ payload v1 và mọi progress đã pin,
có audit correction actor trống (không giả phê duyệt bởi giáo viên).
Bản mới/fresh seed có mapping đúng. Giáo viên vẫn cần rà soát chuyên môn.

## 6. Chạy

Backend: `alembic upgrade head`, `app.cli seed-ai-academy`,
`app.cli verify-ai-academy`; khởi động theo [run-local.md](../run-local.md).
Môi trường local hiện tại đã migrate/seed. Đăng nhập tài khoản hiện có rồi vào
`/ai-academy` hoặc `/admin/ai-academy`.
[Deployment](deployment.md) hướng dẫn VPS, volume, model và backup/restore.

## 7. Kiểm thử

Kết quả và lệnh tại [testing.md](testing.md) và
[IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md). Backend DB test riêng,
browser ports8001/3001, không test ghi DB thật. Dữ liệu thật có pg_dump trước
migration và hash từng hàng ban đầu; đối chiếu sau migration/seed/correction
vẫn nguyên vẹn. Schema/system/AI inventory thật đạt head0010, 48 bài/315 ảnh.

## 8. Phần chưa có hoặc chưa được kiểm chứng

| Hạng mục                                | Phạm vi hiện tại / lý do                                                                 |
| --------------------------------------- | ---------------------------------------------------------------------------------------- |
| Model thật                              | Adapter Ollama và mock tests có; chưa cài model/kiểm chất lượng thực                     |
| AI sinh bitmap                          | Chưa có adapter được duyệt; SVG/upload là phương án hoạt động                            |
| ASR/thu âm/Scratch IDE                  | Không có; dùng hội thoại chữ, đọc giọng local tùy chọn, board/lab                        |
| Xóa danh tính toàn LMS / auto retention | Export và request gỡ project text có; cần chính sách trường trước triển khai rộng        |
| Rubric tùy từng lớp/chủ đề              | Chấm rubric 4 tiêu chí 20/30/30/20 có; chưa có cấu hình override theo lớp                |
| Analytics sâu                           | Tiến độ, attempts/evidence, rubric và CSV có; chưa có dashboard trend đầy đủ theo chủ đề |
| SaaS tenant / triển lãm public          | Catalog chung deployment, sản phẩm private; không tự bật chia sẻ trẻ em                  |
| Docker Engine/HTTPS/load thực           | Compose/Caddy/syntax checks có; Docker Engine local chưa chạy, cần VPS đích              |
| Scanner antivirus ngoài                 | Hook upload có; chưa provision scanner dịch vụ                                           |

Đây là các giới hạn thật, không phải các dịch vụ đang hoạt động ẩn.

## 9. Bước tiếp theo

Nhà trường rà soát 36 tiết/câu/ảnh và chính sách dữ liệu; tạo lớp/teacher/guardian
thật và pilot nhỏ bằng simulation. Kiểm container/HTTPS/backup-restore trên VPS,
tải dự kiến và thiết bị thật. Sau đó đánh giá model local, chốt consent/retention,
thử phản hồi bằng dữ liệu mẫu trước bật flag. Mở rộng rubric theo lớp, báo cáo
theo chủ đề và học liệu lớp 1/2/3/5 qua CMS theo nhu cầu pilot.
