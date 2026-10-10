# API và các luồng thật

Swagger `/docs`, OpenAPI `/openapi.json` trên backend cổng 8000. Tiền tố `/api/v1`.
Pydantic validates request và response; endpoint học sinh dùng whitelist response
trước nộp. UUID không hợp lệ/extra fields đáp án → 422; không phản chiếu input.
401 → frontend về login; 403 → không có quyền; 404 → không tồn tại/không thuộc em;
409 → trạng thái, hết lượt hoặc hết giờ; 429 → rate limit; 503 → DB/schema chưa sẵn.

| Phương thức / đường dẫn | Quyền / hành vi |
| --- | --- |
| POST auth/login | JSON username/password/remember_me (tùy chọn, mặc định false), set hai cookie; trả session_expires_at; Origin allowlist |
| GET auth/me | User id, tên, roles, text_size, session_expires_at; không hash/token |
| POST auth/logout | Session bị thu hồi; CSRF header |
| GET students/me/vip/library | Student có vip.library; metadata bài VIP published đúng lớp và tiến độ của chính em |
| GET students/me/vip/mistakes?subject_code=MATH&page=1 | Student có review.mistakes; 20 câu/trang, lần chấm gần nhất từng phiên bản, không trả grading/lời giải |
| POST students/me/vip/mistakes/{answer_id}/check | Student có review.mistakes, CSRF/owner; kiểm tra đáp án tự ôn, không ghi điểm/lượt làm |
| GET students/me/vip/report?days=7 | Student có reports.personal; 7 hoặc 30 ngày, điểm/lượt/bài đọc, kỳ trước, nhịp theo ngày, snapshot kỹ năng |
| GET grades | Khung 1–5 |
| GET subjects?grade=4 | Tất cả môn, đếm chủ đề theo lớp |
| GET topics?grade=4&subject_code=MATH | Chủ đề active |
| GET lessons?topic_id=UUID | Bài published |
| GET lessons/{id} | Nội dung blocks, breadcrumb, các đề cùng chủ đề |
| POST lessons/{id}/visit | Student đúng lớp; lưu tiến độ đọc, không tự ghi hoàn thành |
| POST lessons/{id}/complete | Student đúng lớp; xác nhận đọc xong, cập nhật kế hoạch, bấm lặp không nhân đôi event |
| PUT students/me/accessibility | JSON `{ "text_size": "comfortable" }` hoặc `"large"`; lưu lựa chọn của chính học sinh |
| GET students/me/learning-plans | Tối đa 12 kế hoạch active/completed cùng lớp của chính học sinh, active trước |
| POST students/me/learning-plans | JSON `{ "subject_code": "MATH" }`; chuẩn bị kế hoạch 7 ngày hoặc trả kế hoạch active hiện có |
| GET assessments?grade=4&subject_code=MATH | Đề published, metadata/count |
| GET assessments/{id} | Metadata, không gửi câu/đáp án |
| GET students/me/dashboard | Hồ sơ/subjects/history/skills/tasks/recommendations thật |
| GET students/me/assignments | Bài được giao của chính em |
| POST students/me/assessments/{id}/assign-self | Giao source=self, idempotent dưới student lock |
| POST attempts | JSON assignment_id; kiểm tra owner/lớp/time/publication/max_attempts |
| GET attempts/{id} | Owner/admin, public content + đáp án đã lưu của em |
| PUT attempts/{id}/answers/{item_id} | JSON {answer}; owner, in_progress; validate theo loại |
| POST attempts/{id}/submit | Chấm transaction, cập nhật điểm/lịch sử/mastery/stats |
| GET attempts/{id}/result | Owner/admin, chỉ khi graded; đáp án và lời giải |
| GET students/me/history?subject_code=MATH&date=2026-10-09 | Lọc ngày Asia/Bangkok, tối đa 200 |
| GET students/me/skills | Mastery, confidence, review từ dữ liệu gốc |
| GET students/me/recommendations | Tối đa 5 đề, không ghi trùng khi reload |
| GET students/me/profile | Thông tin tối thiểu của em |
| GET admin/statistics | Đếm thật, average=null nếu chưa có |
| GET admin/students?search=...&page=1 | Tìm tên, phân trang 20 |
| PATCH admin/students/{id} | display_name/current_grade, có audit |
| GET admin/users?page=1 | Danh sách tài khoản tối thiểu, 20/trang |
| GET admin/questions?grade=4&subject_code=MATH&search=...&page=1 | Read-only, 20/trang |
| GET admin/questions/{question_version_id} | Chi tiết, grading/explanation admin-only |
| GET admin/assessments?grade=4 | Trạng thái, count items và số lượt |
| GET admin/curriculum?grade=4 | Subjects/topics/lessons/skills, read-only |

Không có auth/refresh: session server-side có thời hạn tuyệt đối mặc định 8 giờ;
học sinh không có role admin/teacher chọn remember_me được 7 ngày. Hết hạn đăng nhập
lại. Cache giao diện không gia hạn phiên. Chi tiết: [quản lý phiên](session-management.md).
Không có public signup. Endpoint student yêu cầu role student, guardian không tự
đọc dữ liệu của trẻ. API biên soạn câu hỏi được mô tả ở phần mở rộng bên dưới.

Đáp án single: `{ "answer": { "option_id": "a" } }`; multiple:
`{ "answer": { "option_ids": ["a", "c"] } }`; fill blank:
`{ "answer": { "text": "ngọt" } }`; ordering:
`{ "answer": { "ordered_ids": ["b", "a", "c"] } }`.
`response_time_ms` tùy chọn, 0..86 400 000; không dùng tốc độ để đánh giá năng lực.
Không nhận is_correct/score/identity hay hint_count của client. Hint UI chưa có.

Submit không nhận grading từ client. Điểm từng item = points nếu đúng, 0 nếu sai/
bỏ trống. Điểm đúng tối đa tổng points của đề. Multiple so tập, ordering so thứ tự;
fill blank NFC/casefold/trim/gộp whitespace, **giữ dấu**. Free text grader trả None;
đề tự chấm từ chối loại chưa hỗ trợ khi bắt đầu.

Đường dẫn frontend khớp prompt; App Router catch-all dispatch theo student/admin
path, route không nhận diện hiển thị trang 404. Guards phía client bảo vệ màn hình;
mọi quyền dữ liệu còn được kiểm tra độc lập tại API, không dựa vào UI.

`lessons/{id}` trả thêm `progress_status` riêng theo người đang đăng nhập. Kế hoạch
trả `completed_count`, `items` (id/position/lesson_id/assessment_id/title/status/
due_at/completed_at). Không nhận student_id hoặc trạng thái hoàn thành kế hoạch
từ client; tiến độ được cập nhật cùng transaction xác nhận đọc/nộp bài. Chỉ bắt đầu
đọc chuyển bước sang in_progress. Không có bài học mới trả 409, môn không tồn tại
trả 404. Ngày kế hoạch tính theo Asia/Bangkok; due_at là gợi ý, không thay thế hạn
của assignment hoặc thời lượng đề.

## Free / VIP

`GET membership/plans` công khai trả quyền lợi đã phát hành. `GET students/me/membership`
trả gói hiệu lực từ DB/thời gian server; hết hạn/thu hồi trả plan_code=free và
subscription_plan_code=vip. Không nhận gói học qua API hồ sơ hoặc cookie do client đặt.

| Phương thức / đường dẫn | Quyền / hành vi |
| --- | --- |
| GET students/me/membership | Gói, trạng thái, starts_at/ends_at, features của học sinh |
| GET guardian/students | Chỉ trẻ có guardian_students.verified_at |
| GET guardian/students/{id}/membership | Guardian có liên kết đã xác minh, ngoài liên kết trả 404 |
| GET admin/students/{id}/summary | Danh tính học sinh để xác nhận thao tác |
| GET admin/students/{id}/membership | Admin xem gói hiện tại |
| GET admin/students/{id}/membership/history | 50 thao tác mới nhất |
| POST admin/students/{id}/membership/grant | Admin, CSRF, Idempotency-Key UUID; cấp mới |
| POST admin/students/{id}/membership/extend | Cùng quyền; gia hạn còn hiệu lực từ ends_at, hết hạn từ server_now |
| POST admin/students/{id}/membership/revoke | Cùng quyền; thu hồi ngay và đánh dấu revoked_at trên grants |
| GET lessons/{id}/preview | Metadata và preview.summary/goals riêng, không blocks |
| GET admin/content-access | Chính sách cấu hình và gói hiệu lực sau kiểm tra nội dung dùng chung |
| PUT admin/content/{lesson hoặc assessment}/{id}/policy | Admin, CSRF; minimum_plan_code, learning_level, preview, reason |

Cấp/gia hạn nhận `{ "duration_days": 30, "reason": "Lý do cấp gói" }`; số ngày chỉ
nhận 30/90/365, lý do 5–500 ký tự. Thu hồi chỉ nhận reason. Cùng actor/key/payload
trả snapshot lần đầu; key đã dùng với payload/đích khác trả 409. Audit cùng transaction.

Catalog thêm minimum_plan_code/learning_level/locked/lock_reason; danh sách và chi
tiết đề chỉ trả metadata. Đọc bài/làm bài vẫn kiểm tra gói độc lập. Lỗi gói là 403
với detail={code,message,required_plan}; code MEMBERSHIP_REQUIRED hoặc
MEMBERSHIP_REVOKED. Thiếu chính sách trả POLICY_NOT_READY, không trả nội dung.

POST students/me/learning-plans nhận thêm mode=basic/adaptive (mặc định basic).
Adaptive yêu cầu learning_plan.adaptive; GET trả mode/explanation và trạng thái
paused khi hết quyền, giữ các bước đã hoàn thành. Basic luôn chọn nội dung Free.

Attempt VIP có grant riêng tối đa ends_at+60 phút, không vượt thời lượng/hạn giao
bài. Hết VIP vẫn đọc/lưu/nộp chính attempt trong grant; không mở bài/attempt mới.
Result graded vẫn theo owner và không yêu cầu VIP. Thu hồi chặn grant vĩnh viễn
của attempt cũ; cấp lại VIP không khôi phục grant đã thu hồi.

## Ngân hàng câu hỏi và bài tập

Tất cả đường dẫn dưới đây có tiền tố `admin/authoring`, yêu cầu admin; mọi request
ghi yêu cầu CSRF. UUID câu hỏi là **question_version_id**, không phải questions.id.

| Phương thức / đường dẫn | Hành vi |
| --- | --- |
| GET options?grade=4 | Môn, chủ đề, kỹ năng active và bài học published |
| POST questions | Tạo câu hỏi và phiên bản nháp đầu tiên |
| GET questions/{id} | Chi tiết gồm đáp án, kỹ năng, policy và edit_revision |
| PUT questions/{id} | Sửa nháp, gửi expected_revision; xóa dấu duyệt |
| POST questions/{id}/revise | Sao chép thành phiên bản nháp mới; chỉ một nháp mỗi câu |
| POST questions/{id}/{review,publish,archive} | JSON expected_revision và reason; audit |
| POST assessments | Tạo nháp đề với 1–50 items, points, policy và preview |
| GET assessments/{id} | Chi tiết items, trạng thái duyệt và quyền hiệu lực |
| PUT assessments/{id} | Sửa nháp, gửi expected_revision; xóa dấu duyệt |
| POST assessments/{id}/clone | JSON code mới; tạo nháp đề mới |
| POST assessments/{id}/{review,publish,archive} | JSON expected_revision và reason; không archive khi có attempt đang làm |
| POST assessments/{id}/assign | JSON student_ids, available_at/due_at tùy chọn (ISO có timezone); tối đa 50 em, kiểm tra cả nhóm và dùng lại nhiệm vụ đang hoạt động cùng lịch |

`GET admin/questions` bổ sung bộ lọc `status`, `question_type`, `minimum_plan_code`,
`topic_id`; search tìm mã hoặc nội dung. `GET admin/assessments` có metadata quyền.

Input câu hỏi gồm code, grade, subject_id, topic_id, skill_ids, question_type,
difficulty, content={prompt,options}, grading, explanation (chuỗi), minimum_plan_code.
Grading: single dùng correct_option_id; multiple dùng correct_option_ids; fill_blank
dùng accepted_answers/case_sensitive; ordering dùng ordered_ids. Các trường dư bị từ chối.
Input đề gồm code/grade/subject_id/topic_id/title/assessment_type, lesson_id tùy chọn,
description, time_limit_seconds, max_attempts, minimum_plan_code, learning_level,
preview và items=[{question_version_id,points}]. Swagger có schema đầy đủ.

409 cho revision cũ, mã trùng, sửa nội dung đã xuất bản hoặc thiếu bước duyệt;
422 cho đáp án/cấu trúc sai, đề Free chứa câu VIP, thời gian không hợp lệ; 403 khi
giao cho học sinh sai lớp/gói. Lỗi không trả đáp án nội bộ cho học sinh.
Nội dung đã xuất bản giữ nguyên; đề cũ tiếp tục dùng phiên bản câu từng được xuất
bản dù phiên bản đó chuyển archived. Luồng và giới hạn:
[authoring-design.md](authoring-design.md).

## Biên soạn bài học

Admin có GET/POST `admin/lessons`, GET/PUT `admin/lessons/{id}` và POST
`admin/lessons/{id}/{review,publish,reset}`. Danh sách lọc grade/subject_code/status
(`pending` để xem nháp cần xử lý)/search/page; chi tiết trả payload, revision,
source_fingerprint, source_changed và lịch sử. Request ghi yêu cầu CSRF.
PUT kiểm tra expected_revision và source_fingerprint; action kiểm tra revision
và reason. Nháp tách khỏi bài đang xuất bản; publish cập nhật bài/kỹ năng/policy
atomic. Mỗi lần lưu làm mất trạng thái đã duyệt; revision hoặc nguồn cũ trả 409.

GET `lessons/{id}` bổ sung content.goals/hints/reflection/illustration và
next_lessons có kiểm tra quyền, không trả nháp cho học sinh. Giới hạn và schema:
[lesson-studio.md](lesson-studio.md), Swagger.

## Mở rộng lớp 4

- `GET /api/v1/students/me/thinking?subject_code=MATH&page=1`: chỉ student, lớp lấy
  từ hồ sơ, mỗi trang 20 bài tư duy đã xuất bản ở môn/chủ đề đang hoạt động.
  Trả `grade`, `items`, `total`, `page`; item gồm `id`, `title`, `subject_code`,
  `subject_name`, `estimated_minutes`, `progress_status` của chính học sinh và
  chính sách truy cập. Danh mục không trả lesson content, hints hoặc đáp án.
  Nội dung được mở bằng endpoint bài học có kiểm tra quyền trực tiếp.
- `GET /api/v1/admin/curriculum-map`: chỉ admin, bảng biên tập của 3 môn lớp 4.
  Trả `grade`, `rows`; mỗi mạch có nguồn tham khảo, ghi chú bổ sung, chủ đề hoạt
  động hay chưa, số bài Free/VIP/chưa có chính sách, câu hỏi riêng biệt đang hoạt
  động có phiên bản xuất bản và đề xuất bản. Không tính bản nháp. Bảng không là
  tỷ lệ hoàn thành hay chứng nhận đạt chương trình.
- Lesson studio hỗ trợ `content.category = core | thinking` (mặc định `core` khi
  thiếu). SVG thêm `angles` với `angle` 1–180 và `bars` với `labels`/`values` cùng
  độ dài 1–6, nhãn 1–18 ký tự, giá trị 0–100, `tick` 1–20. Metadata lưu trong
  JSONB hiện có; quy trình duyệt/xuất bản, revision và CSRF giữ nguyên.
