# API và các luồng thật

Swagger `/docs`, OpenAPI `/openapi.json` trên backend cổng 8000. Tiền tố `/api/v1`.
Pydantic validates request và response; endpoint học sinh dùng whitelist response
trước nộp. UUID không hợp lệ/extra fields đáp án → 422; không phản chiếu input.
401 → frontend về login; 403 → không có quyền; 404 → không tồn tại/không thuộc em;
409 → trạng thái, hết lượt hoặc hết giờ; 429 → rate limit; 503 → DB/schema chưa sẵn.

| Phương thức / đường dẫn | Quyền / hành vi |
| --- | --- |
| POST auth/login | JSON username/password, set hai cookie; Origin allowlist |
| GET auth/me | User id, tên, roles; không hash/token |
| POST auth/logout | Session bị thu hồi; CSRF header |
| GET grades | Khung 1–5 |
| GET subjects?grade=4 | Tất cả môn, đếm chủ đề theo lớp |
| GET topics?grade=4&subject_code=MATH | Chủ đề active |
| GET lessons?topic_id=UUID | Bài published |
| GET lessons/{id} | Nội dung blocks, breadcrumb, các đề cùng chủ đề |
| POST lessons/{id}/visit | Student đúng lớp; lưu tiến độ đọc, không tự ghi hoàn thành |
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

Không có auth/refresh: dùng session server-side thời hạn tuyệt đối 8 giờ; hết hạn
đăng nhập lại. Không có write API câu hỏi hay public signup. Endpoint student yêu
cầu role student, guardian không tự đọc dữ liệu của trẻ.

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
