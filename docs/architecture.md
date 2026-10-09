# Kiến trúc VietTree Education

Nguồn sự thật: `database/viettree_education_schema.sql`, 34 bảng gốc; database
`viettree-education`. Giữ nguyên SQL gốc. Backend dùng SQLAlchemy 2 Core với reflection
để ánh xạ **đúng toàn bộ cột, kiểu, khóa, CHECK và index** của database đã import;
không gọi `create_all`. `/ready` và `python -m app.cli check-schema` kiểm tra bảng/cột.

| Nhóm | Bảng gốc |
| --- | --- |
| Danh tính | users, user_roles, schools, student_profiles, guardian_students, classes, class_enrollments |
| Chương trình | subjects, topics, lessons, skills, skill_prerequisites, lesson_skills |
| Ngân hàng | media_assets, questions, question_versions, question_skills, lesson_questions |
| Làm bài | assessments, assessment_items, student_assignments, attempts, attempt_answers |
| Cá nhân hóa | student_skill_mastery, student_lesson_progress, student_learning_plans, learning_plan_items, learning_plan_history, student_recommendations, learning_events |
| Thống kê/quyền riêng tư | question_statistics, student_daily_statistics, audit_logs, privacy_consents |

UUID là khóa định danh. Nội dung/đáp án là JSONB object, điểm là NUMERIC, thời gian
TIMESTAMPTZ. Lớp nằm trong `grade/current_grade` (1..5), không thêm bảng grades.
`topics` unique `(subject_id, grade, code)`; `lessons` unique `(topic_id, code)`.
`question_versions` unique `(question_id, version)`, chỉ một published/question.
`assessment_items` giữ nguyên EXACT version; không sửa nội dung published khi seed lại.

Các FK ghép phải giữ: attempts `(assignment_id, student_id, assessment_id)` →
student_assignments `(id, student_id, assessment_id)`; attempt_answers
`(attempt_id, assessment_id)` → attempts và `(assessment_item_id, assessment_id,
question_version_id)` → assessment_items. API không nhận các identity này từ đáp án client.
`student_recommendations` phải có chính xác một question_version_id hoặc assessment_id.

Mọi trạng thái dùng đúng CHECK gốc: phiên `in_progress/submitted/graded/abandoned`,
bài/câu `draft/published/archived`, giao bài `assigned/in_progress/completed/cancelled/expired`,
nguồn giao `self/system/teacher/guardian`, đáp án `pending/graded/needs_review`.

Monolith FastAPI + Next.js App Router. Browser gọi `/api/v1` cùng origin, Next.js
proxy đến `INTERNAL_API_URL`; container backend dùng host.docker.internal để nối DB.
Cookie HttpOnly chứa phiên opaque, chỉ lưu SHA-256 token tại DB; CSRF token riêng,
SameSite=Lax, kiểm tra Origin và header CSRF cho thao tác ghi. Migration Alembic bổ
sung auth_sessions và auth_login_limits; baseline không import hay thay đổi bảng gốc.

Migration 0003_memberships bổ sung membership_plans/membership_plan_features,
student_memberships/membership_operations, content_access_policies và
attempt_access_grants. Gói độc lập user_roles. access.py tập trung quyết định quyền;
membership_api.py phục vụ quản lý gói, giới thiệu và chính sách nội dung. Không có
cache quyền ở session; thời hạn được tính lại mỗi request.

Đổi gói khóa theo actor/Idempotency-Key trước, rồi student_profiles; ghi membership,
operation và audit cùng transaction. Bắt đầu/lưu/nộp bài cùng khóa học sinh để tuần
tự hóa với thu hồi. Plan_v2 dùng bằng chứng mastery có sẵn, không thêm điểm giả.

Khóa hàng student_profiles tuần tự hóa bắt đầu/nộp bài và đề xuất theo học sinh;
khóa attempts bảo đảm nộp lại trả kết quả cũ. Điểm, mastery, sự kiện và tiến độ ghi
trong một transaction. Chỉ trả whitelist nội dung public trước nộp. Admin đọc đáp án
qua API riêng. Free text không tự chấm. Seed không tạo lịch sử/điểm giả.

Checkpoint: schema → cấu hình/auth → seed → API bài làm → rule_v1 → UI → kiểm thử
→ tài liệu bàn giao. Tiến độ và chứng cứ cuối cùng ở IMPLEMENTATION_STATUS.md.

## Biên soạn và giao bài

`authoring_api.py` dùng `authoring_schemas.py` và `services/authoring.py`; thao tác
ghi cùng transaction audit. Migration 0004 bổ sung policy từng phiên bản câu;
0005 thêm revision tăng đơn điệu vào câu/đề để phát hiện nháp bị sửa đồng thời.
Khóa questions trước question_versions khi biên soạn; khóa student_profiles theo
thứ tự ID rồi assessment ở chế độ chia sẻ khi giao/bắt đầu. Archive đề khóa đề
độc quyền và kiểm tra không còn lượt đang làm. Nội dung published được giữ nguyên;
phiên bản cũ đã published vẫn dùng trong đề cũ sau khi archive. UI nằm ở
`features/authoring.tsx` và `features/practice-library.tsx`.
