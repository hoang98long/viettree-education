# Database và migration

Head hiện tại `0011_classes_vip_training`: thêm chính sách Free/VIP trên
`ai_lessons`, cài đặt lớp, giao bài và tuyên dương. Xem
[database lớp và thành tích](../classes-achievements.md). Các bảng Academy
ở migration 0010 dưới đây được giữ nguyên dữ liệu.

Giữ nguyên `database/viettree_education_schema.sql` (34 bảng gốc).
`backend/alembic/versions/0010_ai_academy.py` sau `0009_guided_hints` chạy DDL
additive ở `backend/app/academy/schema.sql`. Không DROP/TRUNCATE/reset dữ liệu.

| Nhóm           | Bảng mới                                                                                              |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| Chương trình   | ai_programs, ai_grades, ai_units, ai_lessons, ai_lesson_versions                                      |
| Quyền          | ai_staff_roles                                                                                        |
| Media          | ai_media_assets, ai_media_variants, ai_media_usages                                                   |
| Giao bài / học | ai_assignments, ai_assignment_targets, ai_attempts, ai_progress, ai_competency_progress               |
| Sản phẩm       | ai_projects, ai_project_submissions, ai_rubric_scores                                                 |
| Ghi nhận       | ai_badges, ai_student_badges, ai_rewards_ledger                                                       |
| AI / an toàn   | ai_prompt_templates, ai_provider_configs, ai_feature_flags, ai_generation_jobs, ai_moderation_reviews |
| Vận hành       | ai_content_approvals, ai_audit_logs, ai_events, ai_usage_windows                                      |

29 bảng, FK tới users/student_profiles/classes/media_assets. Tái sử dụng
guardian_students, class_enrollments, privacy_consents; không tạo bảng thay thế.
Steps/activities/quiz/options ở JSONB phiên bản; submissions chứa artifact JSONB
giới hạn 11 trường. Không lưu raw chat, audio, webcam hoặc nội dung bị chặn.

## Nạp và nâng cấp

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
../.venv/Scripts/python.exe -m app.cli check-schema
```

Seed UUID ổn định theo code, advisory lock và on-conflict; không sửa bản đã được
giáo viên biên soạn, không đổi người dùng/mật khẩu/gói/tiến độ. Lệnh chỉ thêm
chương trình, bài, media, mẫu và chính sách mặc định. Khi thay đổi học liệu đã
seed, lưu **phiên bản mới qua CMS**, không mong seed ghi đè. Không chạy file
schema.sql trực tiếp lần hai.

## Rollback

Downgrade 0010 chỉ cho phép khi **tất cả bảng Academy rỗng**; có dữ liệu sẽ từ
chối để tránh mất lịch sử. Chọn rollback ứng dụng tương thích DB hoặc khôi phục
backup vào DB mới để kiểm chứng; không xóa bảng Academy để ép downgrade.
Media upload cần backup cùng DB. Bundled SVG nằm trong release source.

`verify-ai-academy` trả `quality.baseline_published/baseline_required` và issues
cho bài bị ẩn/chưa published, cấu trúc không hợp lệ, media chưa approved hoặc
rubric sai. Đây là báo cáo chỉ đọc; có issues cần nhà trường xem xét, không có
auto repair hoặc tự ghi đè phiên bản biên soạn.

Trên DB local hiện tại đã backup trước migration, chạy head 0010 + seed và đối
chiếu hash của từng hàng trong các bảng cũ: tất cả hàng ban đầu giữ nguyên.
Các hàng mới ở media_assets là phần mở rộng hợp lệ. Không đặt bản backup chứa
dữ liệu riêng lên git hoặc thư mục public.
