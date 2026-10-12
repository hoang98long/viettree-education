# Lớp học, học sinh tự do và thành tích

Triển khai 12/10/2026, migration `0011_classes_vip_training`. Tái sử dụng
`classes`, `class_enrollments`, `student_profiles`; không tạo hệ tài khoản/lớp
khác. Các trường mới và bảng phụ không thay mật khẩu, VIP hoặc lịch sử học.

## Quản lý lớp

Admin → **Lớp và giao bài** (`/admin/classes`): tạo/sửa tên, khối, năm học,
trường và giáo viên; ghi danh/chuyển học sinh ra; đóng/mở lớp, bật/tắt thành tích.
Thông tin lớp có revision để hai người sửa đồng thời nhận 409, không ghi đè.
Lớp đang có học sinh không đổi khối/trường; chuyển học sinh trước khi đổi.
Học sinh phải đang hoạt động, có role student, cùng khối và trường nếu lớp gắn
trường. Có thể tham gia nhiều nhóm học; không tự chuyển hồ sơ sang khối khác.

**Học sinh tự do** là học sinh không có ghi danh ở lớp đang hoạt động. Tài khoản
không cần lớp để tự học; quyền nội dung vẫn do Free/VIP và khối hồ sơ quyết định.
Rời/đóng lớp không xóa tài khoản, attempts, điểm, bài nộp hoặc tuyên dương cũ.
Admin có danh sách tự do theo khối/tìm kiếm và ghi danh vào lớp phù hợp.

Teacher → `/teacher/classes`: chỉ lớp mình phụ trách, học sinh hiện đang ghi
danh, giao bài và xem/tuyên dương kết quả. Không xem danh sách tự do toàn hệ
thống hoặc lớp người khác. Thay giáo viên sẽ chuyển quyền theo DB ở request
tiếp theo. Các thao tác có auth, CSRF, validation và audit.

## Giao bài

Admin chọn cả lớp hoặc học sinh riêng (kể cả tự do). Backend hỗ trợ 1–50 người
mỗi lần giao; lớp lớn chia nhóm. Teacher chỉ giao tới học sinh lớp được phân
công. Ba loại: bài học Toán/Tiếng Việt/Tiếng Anh, bài luyện tập có chấm, bài
lý thuyết/bài tập AI Academy. Có hạn hoàn thành tùy chọn.

Giao bài không cấp VIP. Nếu người nhận chưa có quyền VIP, toàn thao tác được
từ chối, không giao một phần. Chọn học liệu miễn phí hoặc cấp gói qua chức năng
VIP rồi giao lại. Idempotency key chống thao tác lặp do mất mạng; cùng key với
payload khác trả 409. Chụp danh sách người nhận tại thời điểm giao; không tự giao
cho người ghi danh sau. Giao lại bằng thao tác mới để thêm người nhận mới.

Bài luyện tập tái sử dụng `student_assignments` và grading hiện có. Batch và
target giữ nguồn lớp/cá nhân cho cả ba loại. Học sinh → **Lớp và thành tích**
(`/student/classroom`) xem bài giao cá nhân/theo lớp, mở nội dung theo quyền.
Hạn của bài luyện tập được server thực thi; hạn bài đọc/AI là mốc nhắc học,
không chặn ôn tập. Các bài thuộc lớp không hiện sau khi người học rời lớp.
Các bài AI giao theo hai cách đều hiện thêm tại trang Hành trình AI.

## Kết quả, thứ tự và top 3

Phạm vi là **trong lớp có ghi danh**, không public bảng xếp hạng toàn nền tảng.
Học sinh khác lớp không truy cập được dù biết UUID. Học sinh thấy biệt danh
`Bạn xxxxxx` của bạn khác; admin/teacher đúng lớp xem tên thật. Tài khoản tự do
xem thành tích riêng, không bị gộp vào một bảng công khai.

Chọn kỳ **tuần này** (thứ Hai đến thứ Hai) hoặc **tháng này**, giờ Việt Nam.
Năm loại kết quả: Toán, Tiếng Việt, Tiếng Anh, câu hỏi lý thuyết AI, sản phẩm AI
đã được giáo viên chấm. Có thể lọc một bài cụ thể để so sánh cùng học liệu.
Không tính lượt đang làm, chưa chấm hoặc điểm tối đa bằng 0.
Loại học sinh đã khóa tài khoản, mất vai trò student hoặc đổi sang khối khác
khỏi bảng hiện tại; không xóa snapshot đã công bố.

1. Mỗi người/mỗi bài chỉ giữ kết quả tốt nhất trong kỳ; làm lặp không cộng điểm.
2. Điểm xếp thứ tự = trung bình điểm tốt nhất, quy về thang 100.
3. Đồng điểm: số bài có kết quả nhiều hơn, rồi thời điểm đạt sớm hơn, cuối cùng
   ID để thứ tự ổn định. Đây không phải thưởng tốc độ thao tác.
4. Không thêm hệ số hoặc điểm thưởng cho VIP. Tổng hợp nhiều bài là tham khảo;
   chọn cùng bài khi cần so sánh trực tiếp vì độ khó/số nội dung có thể khác.

AI chỉ tính checkpoint kiểu quiz; board thực hành ba mức vẫn có lịch sử nhưng
không dùng để tăng hạng bằng việc chọn mức dễ. Sản phẩm dùng rubric do người
chấm, chỉ xét bài đã review ở đúng lớp. Đọc bài có số hoàn thành riêng, không
tự biến thành điểm năng lực.

Thầy cô xem bảng rồi **Tuyên dương top 3 của kỳ**. Server chọn tối đa ba học sinh
có kết quả thật; lớp có ít người chỉ ghi nhận số người có kết quả. Snapshot
giữ hạng/biệt danh/điểm/số bài/thời gian/người công bố. Công bố lặp cùng lớp,
loại, kỳ và bài lọc trả batch cũ. Điểm live có thể thay đổi sau đó; snapshot
không tự viết lại. Tắt thành tích sẽ ẩn bảng/tuyên dương khỏi người học.

## Database mới

- `classes.edit_revision`; `class_enrollments.recognition_alias`.
- `classroom_settings`: cài đặt bảng thành tích theo lớp.
- `learning_assignment_batches` / `learning_assignment_targets`: nguồn giao
  bài và người nhận; FK về lớp/tài khoản/assignment có sẵn.
- `class_award_batches` / `class_awards`: snapshot tuyên dương top đầu.
- Ba bảng giá/ưu đãi/nguồn thị trường, xem [giá VIP](vip-pricing-research.md).
- `ai_lessons.minimum_plan_code`, xem [chính sách đào tạo AI](ai-training-vip.md).

Migration không downgrade tự động: đã có chính sách trả phí/lịch sử trẻ em thì
rollback ứng dụng tương thích hoặc restore thử vào DB mới. Backup trước release,
không `DROP`, `TRUNCATE` hoặc `docker compose down -v` để cập nhật.
