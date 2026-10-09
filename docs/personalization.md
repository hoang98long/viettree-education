# Cá nhân hóa rule_v1

Nguồn gốc là attempts graded + attempt_answers graded + question_skills đúng
question_version_id. Không seed điểm/mastery. Dữ liệu ít hiển thị “Cần luyện tập
thêm để đánh giá” (<5 câu). Mastery không phải kết luận chuẩn hóa về học sinh.

Replay theo graded_at, attempt id, assessment_item_id để kết quả cố định. Mỗi
bằng chứng có y=1 nếu đúng, 0 nếu sai/bỏ trống; alpha=min(0.5,(0.15+0.05*difficulty)*weight).
Câu đầu mastery=y; câu sau mastery=(1-alpha)*mastery_old+alpha*y.
Recent_accuracy dùng EWMA alpha=0.3. Confidence=min(1,n/20), counts là số bằng chứng
ở từng skill, correct_count đếm câu đúng. Một câu nhiều skill đóng góp vào từng
skill theo weight cho EWMA; confidence vẫn đếm số câu, không phải số điểm.
Hint_usage_rate là trung bình tỷ lệ câu có hint; MVP chưa cung cấp hint nên bằng 0.

Lịch ôn là heuristic: mastery<0.5 → 1 ngày; <0.8 → 3 ngày; còn lại → 7 ngày.
Ngày tính từ graded_at, timezone lưu UTC, UI/nhóm daily dùng Asia/Bangkok. Đây là
quy tắc khởi đầu, chưa được tuyên bố kiểm chứng tâm lý/học thuật.

Gợi ý chỉ chọn đề published cùng lớp, còn lượt. Sau 2 lần làm cùng đề trong 24 giờ
thì tạm tránh đề đó. Ưu tiên prerequisite chưa vững của skill yếu (có ít nhất 5
bằng chứng), rồi kỹ năng không bị prerequisite chặn, đến hạn ôn, mastery thấp.
Người mới có warmup và không có mastery giả. Với skill yếu ở phân số, bài phép
tính được ưu tiên nếu nền tảng chưa được luyện vững; lý do “Ôn kỹ năng nền tảng…”.

Tối đa 5 gợi ý/lần; khóa student_profiles tuần tự hóa insert/update. Dùng lại bản
ghi pending/shown/accepted của cùng assessment; reload không sinh trùng vô hạn.
Chỉ điền assessment_id, question_version_id=NULL để đúng CHECK NUM_NONNULLS=1.
Nộp đề đánh dấu gợi ý tương ứng completed. Mỗi lần học sau có thể tạo gợi ý mới
hợp lý. Hạn gợi ý 1 ngày được làm mới khi engine lựa chọn lại.

Submit cập nhật tất cả dưới transaction và khóa student/attempt; nộp lại trả kết
quả cũ trước khi update/sự kiện. Rebuild mastery replay lịch sử thay vì cộng lại
count, nên không nhân đôi. `python -m app.cli rebuild` có thể tính lại mọi học sinh,
question_statistics và student_daily_statistics. Không xóa dữ liệu gốc hoặc tự
động ghi event mới khi rebuild.

Thống kê toàn hệ thống được tuần tự hóa bằng advisory lock trước snapshot/upsert
để hai học sinh nộp đồng thời không ghi tổng thiếu. Active_seconds giữ 0 trong MVP
vì không có dữ liệu theo dõi thời gian đáng tin; không giả lập engagement.
Counts gồm đáp án bỏ trống trong question stats như một cơ hội luyện tập sai,
nhưng questions_answered daily chỉ gồm câu học sinh thực sự trả lời.

MVP rebuild toàn lịch sử mỗi nộp, ưu tiên đúng và đơn giản; cần incremental update
và kiểm tra reconciliation khi dữ liệu lớn. Không xử lý xóa/sửa lịch sử gốc trong
API MVP; rebuild upsert dựa trên lịch sử append-only, không phải công cụ dọn dữ liệu.
Không lưu nhãn kỳ thị, dữ liệu nhạy cảm hay suy luận ngoài kết quả bài làm.

## Kế hoạch và quyền gói học

Gợi ý rule_v1 lọc đề theo quyền Free/VIP hiện tại trước khi chọn tối đa 5 đề.
Kế hoạch cơ bản plan_v1 vẫn chỉ chọn tối đa 3 bài Free chưa hoàn thành, đúng lớp.

Plan_v2 (mode=adaptive) yêu cầu feature learning_plan.adaptive. Chỉ dùng mastery
khi có ít nhất 5 bằng chứng; ưu tiên prerequisite cần ôn, rồi kỹ năng yếu hoặc đến
hạn ôn. Bài nâng cao chỉ được xét khi có bằng chứng, mastery >= 0.8 và confidence
>= 0.25 cho mọi kỹ năng được liên kết. Thiếu dữ liệu chọn bài nền tảng theo thứ tự
chương trình. Thực hiện theo quy tắc, không suy luận ngoài dữ liệu câu trả lời.

Bài luyện đi kèm ưu tiên đúng lesson_id rồi đề cùng chủ đề, có quyền và còn lượt.
Mỗi môn có một kế hoạch active; đổi kiểu sẽ archive kế hoạch trước và giữ lịch sử.
Khi hết/thu hồi quyền adaptive, GET chuyển kế hoạch active sang paused, giữ tiến độ;
cấp lại cho phép tạo kế hoạch adaptive mới, không tự khôi phục kế hoạch paused.
Kế hoạch chưa tự thay bước sau khi đề bị đóng/hết lượt. Cách chấm/mastery không đổi
theo gói. Bộ câu nâng cao dùng version riêng, không sửa bằng chứng lịch sử.
