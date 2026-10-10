# Ngân hàng câu hỏi và bài tập lớp 4

## Phạm vi đã triển khai

Trình biên soạn bài học, minh họa và gợi ý đã có ở **Quản lý bài học**. Luồng nháp
riêng, kiểm tra revision, duyệt/xuất bản và giới hạn tại [lesson-studio.md](lesson-studio.md).

Admin có thể biên soạn câu hỏi, xem trước, duyệt, xuất bản và lưu trữ; ghép đề từ
câu hỏi đã xuất bản và giao bài cho học sinh. Học sinh tìm đề trong **Thư viện
luyện tập**, làm bài và xem kết quả theo quyền Free/VIP hiện có.

Quyền biên soạn thuộc vai trò admin, độc lập với gói VIP. Teacher chưa có quyền
biên soạn hoặc giao bài cho lớp; bước mở rộng này cần kiểm tra quan hệ phụ trách lớp.

## Nội dung bổ sung

Mỗi môn có thêm hai bài miễn phí và hai bài nâng cao, mỗi bài kèm sáu câu hỏi và
một đề. Nội dung gồm giải thích, ví dụ, hướng dẫn luyện tập và lời giải từng câu.

| Môn | Miễn phí | VIP |
| --- | --- | --- |
| Toán | Làm tròn số; chu vi và diện tích | Dữ kiện trong bài toán nhiều bước; bài toán tổng và phân số |
| Tiếng Việt | Vai trò của từ; dùng từ chính xác | Đọc hiểu có bằng chứng; liên kết đoạn văn |
| Tiếng Anh | Giờ giấc và hoạt động; thời tiết | Kế hoạch cuối tuần; dự án trong lớp |

Tổng seed lớp 4: **42 bài, 216 câu hỏi, 30 đề**, gồm **30 bài/18 đề Free** và
**12 bài/12 đề VIP**. Mỗi môn có 14 bài, 72 câu và 10 đề. Đề cũ có tám câu, đề
bổ sung có sáu câu. Không tạo điểm hoặc lịch sử học giả. Đây là nội dung demo
tự biên soạn; giáo viên cần rà soát tính phù hợp chương trình và chuyên môn trước
khi dùng chính thức.

## Biên soạn câu hỏi

Đi tới `/admin/questions/new`. Nhập mã duy nhất, môn, chủ đề, kỹ năng, độ khó,
gói, nội dung và lời giải. Bốn loại hỗ trợ: chọn một đáp án, chọn nhiều đáp án,
điền khuyết và sắp xếp. Xem trước dùng đúng thành phần làm bài của học sinh.

Luồng: **Nháp → Duyệt nội dung → Xuất bản → Lưu trữ**. Nháp được sửa; sửa sẽ
xóa dấu duyệt. Duyệt/xuất bản/lưu trữ cần lý do 5–500 ký tự và ghi audit.
Backend kiểm tra đáp án thuộc lựa chọn, lựa chọn không trùng, thứ tự đầy đủ,
đáp án điền khuyết không rỗng và kỹ năng đúng môn/lớp.

Câu đã xuất bản giữ nguyên nội dung và đáp án. **Tạo phiên bản mới** sao chép
sang nháp có số phiên bản tăng. Khi xuất bản phiên bản mới, phiên bản trước
chuyển lưu trữ; đề cũ vẫn tham chiếu phiên bản trước và chấm theo đáp án cũ.
Không xóa cứng dữ liệu đang được lịch sử tham chiếu.

Hai người cùng sửa hoặc duyệt nháp được phát hiện qua `edit_revision`. Request
ghi gửi `expected_revision`; nếu khác revision hiện tại, API trả 409. Revision
tăng sau mỗi lần lưu/duyệt/xuất bản/lưu trữ. Giao diện cần tải lại khi có xung đột.

## Tạo và giao bài tập

Đi tới `/admin/assessments/new`. Chọn môn/chủ đề, bài học đi kèm nếu cần, loại
luyện tập/bài được giao/thử thách/kiểm tra, Free/VIP, mức nội dung và giới thiệu.
Tìm và thêm 1–50 câu đã xuất bản; sắp thứ tự, đặt điểm từng câu, thời lượng và
số lượt tối đa. Duyệt rồi xuất bản tương tự câu hỏi. Đề đã xuất bản được sao
chép thành nháp mới để sửa; lịch sử vẫn dùng đề cũ.

Đề Free chứa câu hoặc bài học VIP sẽ bị từ chối khi duyệt/xuất bản. Backend
kiểm tra chính sách từng phiên bản câu hỏi, bao gồm câu độc lập trong ngân hàng.
Thiếu chính sách không làm nội dung trở thành miễn phí. Câu hỏi/đáp án nội bộ
chỉ được trả cho admin; học sinh nhận câu qua lượt làm và lời giải sau khi nộp.

Sau xuất bản, tìm và chọn tối đa 50 học sinh, đặt giờ mở/hạn nộp. Backend kiểm
tra tài khoản hoạt động, lớp, gói và thời gian. Nếu một học sinh không hợp lệ,
toàn bộ lần giao không ghi dữ liệu. Giao lại cùng đề, người giao và lịch mở/hạn
nộp sẽ dùng lại nhiệm vụ đang hoạt động. Thay lịch của nhiệm vụ đang hoạt động
trả 409; chưa có chức năng chỉnh lịch hàng loạt. Giao bài chưa ghi nhận việc học
sinh đã bắt đầu hoặc hoàn thành.

Học sinh thấy bài trong nhiệm vụ và thư viện; thư viện lọc theo môn, Free/VIP,
loại đề và từ khóa. Đề VIP bị khóa chỉ hiện giới thiệu đã cấu hình. Giới hạn
lượt, thời gian và quyền gói tiếp tục được kiểm tra khi bắt đầu/lưu/nộp.
Không lưu trữ đề khi có học sinh đang làm.

## Database và tài khoản demo

- `0004_question_authoring`: thêm `question_version_access_policies`, backfill
  quyền từng phiên bản từ chính sách bài/đề đang tham chiếu.
- `0005_authoring_revisions`: thêm `edit_revision` vào `question_versions` và
  `assessments`. Không sửa file SQL gốc hoặc xóa bảng học tập.
- Dùng lại `question_versions`, `question_skills`, `assessment_items`,
  `student_assignments` và `audit_logs` hiện có.

Chạy `python -m alembic upgrade head`, `python -m app.cli seed`, rồi
`python -m app.cli seed-demo-learners` trong backend. Lệnh demo chỉ chạy ngoài
production và cần `SEED_STUDENT_PASSWORD`; không tự chạy khi khởi động ứng dụng.

| Tên đăng nhập | Gói ban đầu | Lớp |
| --- | --- | --- |
| free4_01 | Free | 4 |
| free4_02 | Free | 4 |
| vip4_01 | VIP 90 ngày từ lúc tạo | 4 |
| vip4_02 | VIP 90 ngày từ lúc tạo | 4 |

Mật khẩu lấy từ `SEED_STUDENT_PASSWORD` trong `.env` local. Chạy lại không đặt
lại mật khẩu, không tự gia hạn hoặc cấp lại VIP đã hết hạn/thu hồi, không đổi
gói hay vai trò tài khoản đã có.

## Các bước nâng cấp đề xuất

| Ưu tiên | Admin | Học sinh / phụ huynh | Điều kiện nghiệm thu |
| --- | --- | --- | --- |
| 1 | Khôi phục phiên bản bài học và nhận xét duyệt | Trình soạn theo khối, minh họa/gợi ý và nháp riêng đã có | Bổ sung nút khôi phục, nhận xét và tiến độ đọc theo phiên bản |
| 2 | Nhập CSV câu hỏi có màn hình kiểm tra lỗi và xem trước | Ngân hàng nội dung phong phú hơn | Không ghi từng phần khi file lỗi; không sửa câu đã xuất bản |
| 3 | Giáo viên giao bài theo lớp, quản lý lịch và theo dõi chưa nộp | Nhiệm vụ theo lớp, nhắc hạn trong ứng dụng | Kiểm tra quan hệ giáo viên–lớp ở API, giao lặp không trùng |
| 4 | Phân tích câu quá dễ/khó từ tỷ lệ đúng và số lượt | Sổ câu cần ôn, luyện lại kỹ năng yếu | Dữ liệu đủ mẫu, phân biệt thiếu bằng chứng với yếu kỹ năng |
| 5 | Báo cáo tuần và xác minh liên kết phụ huynh | Phụ huynh theo dõi tiến độ và hỗ trợ con | Chỉ người có liên kết xác minh; không chia sẻ kết quả giữa học sinh |
| 6 | Quy trình thanh toán và đối soát | Người lớn mua/gia hạn VIP | Webhook xác thực, thao tác lặp không cấp VIP hai lần |

Các dòng trong bảng này là đề xuất, chưa được quảng cáo như chức năng đã phát hành.
