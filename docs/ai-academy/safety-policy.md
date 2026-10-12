# An toàn, riêng tư và vận hành

Học sinh học bằng tranh, dữ liệu mẫu và tình huống hư cấu. Mầm AI là nhân vật
minh họa; AI có thể sai và không có cảm xúc thật. Không camera, microphone,
thu âm hay gallery công khai. Không thu thập PII trong các câu trả lời lựa chọn.

## Trợ giảng

Chỉ 6 chế độ học sinh: ExplainConcept, GiveHint, AskSocraticQuestion,
ReviewStudentDraft, PracticeEnglish, BrainstormStory. Hai chế độ staff là
GenerateTeacherDraft/GenerateImagePrompt. Không có chat mở truy cập internet.
GiveHint yêu cầu học sinh đã thử; Free mức 1, VIP mức 2–3. ReviewStudentDraft
hiện trả checklist đối chiếu bài, không gửi nguyên văn nháp tới model hoặc tự
chấm văn bằng AI. PracticeEnglish là hội thoại chữ, không nhận diện giọng nói.

Lời tự viết được kiểm mẫu PII/email/URL/số điện thoại/tên-trường, nội dung nguy
hiểm và prompt injection. Bị chặn: chỉ lưu reason_code, không lưu raw input.
Output provider kiểm lại; sai cấu trúc/không phù hợp/timeout trả hướng dẫn nội bộ.
Các regex là lớp phòng vệ hạn chế, có thể chặn nhầm hoặc bỏ sót; chưa thay thế
kiểm duyệt chuyên môn và đánh giá an toàn mô hình trước production.

Ollama chỉ nhận ngữ liệu đã duyệt, mode, grade và hint mẫu. Không gửi tên, ID,
profile, lớp, địa chỉ hoặc raw bài làm của trẻ. Không ghi request body/provider
prompt vào logs. Flags đọc DB; quyền/consent kiểm lại sau response.

Để có gọi mô hình phải đồng thời: env cấu hình; tutor flag; provider enabled;
policy approved; chấp thuận `ai-academy-v1` còn hiệu lực của guardian đã xác minh
hoặc bản ghi có thẩm quyền từ nhà trường. Thu hồi liên kết/consent ngăn gọi tiếp.
Consent không bắt buộc cho mô phỏng/ngữ liệu nội bộ.

Quota persisted theo ngày UTC: 20 lượt/người, 300/lớp, 2.000/trường hoặc phạm vi
deployment khi chưa có trường. Không dùng ID thuần trong usage key. Tutor
10 request/phút/người, circuit breaker từng worker. Sinh SVG 10 request/phút.

## Dữ liệu và thời hạn

Tiến độ/attempt/sản phẩm riêng tư, chỉ chính học sinh, guardian đã xác minh và
teacher đang phụ trách theo phạm vi. CSV tránh formula injection. Audit không
chứa mật khẩu; uploads ngoài public, có auth. Khi xem lớp, chỉ trẻ còn ghi danh.

Chính sách vận hành đề xuất cần nhà trường chốt trước mở thật: events/usage
90 ngày, cảnh báo đã xử lý 180 ngày, audit 365 ngày; bài làm/điểm giữ trong năm
học và thời gian giải quyết khiếu nại. **Chưa có job tự xóa các dữ liệu này**:
không tự áp dụng retention vào dữ liệu học tập hiện tại. `cleanup-auth` cũ chỉ
dọn auth hết hạn theo lệnh chủ động, không dọn Academy.

Export JSON theo quyền có trong portfolio/guardian. Yêu cầu gỡ **nội dung tự viết
của sản phẩm** được admin xác nhận mật khẩu và xét duyệt: artifact rỗng, gỡ
feedback, tăng revision; vẫn giữ hàng bài nộp, điểm, tiến độ, users và audit.
Chưa phải xóa danh tính/toàn bộ hồ sơ LMS; yêu cầu đó xử lý theo quy trình nhà
trường, backup/retention đã thống nhất. File export là dữ liệu riêng, không chia
sẻ qua public gallery.

Không tuyên bố chứng nhận pháp lý hay đảm bảo mô hình không sai. Cần đánh giá
điều khoản model, bảo vệ dữ liệu trẻ em, tải và phản hồi giáo viên trước mở thật.
