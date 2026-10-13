# Định hướng mở rộng VietTree Education

## Đã triển khai trong vòng này

Code đã chia theo module API/schema/nghiệp vụ/học liệu; frontend tách theo
feature/trang/form. Registry học liệu dùng chung cho CLI và admin; CLI nạp
đầy đủ từng khối và kiểm kê source không cần DB. Admin xuất bảng học liệu
CSV theo bộ lọc. Có 20 tài khoản thử Free/VIP cho lớp 1–5, gồm bốn tài khoản lớp 5 mới;
những tài khoản cũ giữ mật khẩu và gói. Xem [kiến trúc](architecture.md)
và [demo theo khối](demo-accounts.md).

Ba môn lớp 1–5 đã có mỗi khối 68 bài/384 câu/56 đề. Lớp và giao bài cá nhân/
cả lớp, kết quả và tuyên dương top 3 đã triển khai; không còn là đề xuất.

Chữ học sinh 18 px, bài học 20 px, câu hỏi 22 px; chế độ chữ lớn lưu theo tài khoản.
Kế hoạch học 7 ngày theo môn có tối đa 3 bài mới và bài luyện tập, theo dõi tiến độ
đọc và bài đã nộp. Kế hoạch dùng dữ liệu chương trình đang xuất bản, cùng lớp và
còn lượt luyện tập. Không gán điểm hoặc năng lực từ thao tác xác nhận đọc.

Lớp 5 đã có bộ ba môn theo chương trình Việt Nam, 46 bài Free và 22 bài VIP.
Thư viện bài học tìm không dấu, lọc tiến độ/gói/môn; admin có tổng học liệu và
biên soạn thêm tam giác, hình thang, hình tròn, hình hộp, biểu đồ quạt tròn.
Xem [nội dung và phạm vi lớp 5](grade5-curriculum.md).

## Các chức năng đề xuất tiếp theo

Quản trị tài khoản đã có tạo/sửa, vai trò, khóa/mở, mật khẩu tạm, thu hồi phiên,
nhật ký và bảo mật cá nhân. Ưu tiên tiếp cho vận hành: MFA admin, xác minh email/
khôi phục bằng token, nhập hàng loạt và quyền theo lớp/quan hệ phụ huynh đã xác minh.
Chính sách và giới hạn: [account-management.md](account-management.md).

Admin đã có trình biên soạn bài học theo khối, nháp riêng, duyệt/xuất bản và audit.
Các bài hiện có thêm minh họa, mục tiêu, gợi ý từng bước và bài học tiếp theo.
Hướng dẫn và phần mở rộng chưa triển khai: [lesson-studio.md](lesson-studio.md).

VIP đã mở thêm Góc học VIP, sổ tay câu sai với tự ôn không đổi điểm và báo cáo
7/30 ngày có thể in. Bộ lớp 4 hiện có 68 bài/384 câu/56 đề, gồm 22 bài/22 đề VIP.
Chi tiết sử dụng và hướng mở rộng: [vip-expansion.md](vip-expansion.md).

Thiết kế gói học Free/VIP, quyền nội dung và tính năng nâng cao được tách thành
[free-vip-design.md](free-vip-design.md). Phần admin cấp/gia hạn/thu hồi, kiểm tra quyền,
22 bài/22 đề nâng cao, plan_v2 và xem gói qua liên kết phụ huynh đã triển khai; VIP vẫn
giữ nguyên vai trò student và không thay thế quyền quản trị hoặc liên kết phụ huynh.

| Ưu tiên | Chức năng                              | Giá trị và tiêu chí nghiệm thu                                                                                                                                                    |
| ------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1       | Báo cáo phụ huynh theo tuần            | Chỉ phụ huynh có liên kết đã xác minh được xem; tách tiến độ đọc và bằng chứng kỹ năng, báo thiếu dữ liệu khi cần. Không tự gửi thông báo trước khi có cấu hình và chấp thuận.    |
| 2       | MFA admin và khôi phục tài khoản       | Xác thực bổ sung, mã dự phòng và quy trình khôi phục có xác minh; rate limit/audit, thu hồi phiên phù hợp. Không dùng mật khẩu demo cho vận hành thật.                            |
| 3       | Tự điều chỉnh bước kế hoạch            | plan_v2 theo kỹ năng đã có. Tiếp tục thay bước bị đóng/hết lượt mà giữ lịch sử thay đổi và các bước đã hoàn thành.                                                                |
| 4 | Tăng độ phủ học liệu lớp 1–5 | Bộ lớp 5 đã có 68 bài. Tiếp tục tăng số văn bản đọc, bài viết mở, đo/vẽ, mô hình khối và thực hành dữ liệu; có giáo viên rà soát theo kế hoạch năm học. |
| 5       | Đọc hướng dẫn bằng âm thanh            | Nút nghe/dừng, không tự phát; dùng âm thanh đã được rà soát cho tiếng Việt/tiếng Anh. Bài kiểm tra đọc hiểu cần quy tắc riêng để âm thanh không làm thay phần cần đánh giá.       |

## Thứ tự thực hiện đề nghị

Đợt lớp 4 có thêm Góc tư duy, bảng học liệu admin, góc và biểu đồ SVG. Trước khi
mở thêm khối lớp, bổ sung các mảng lớp 4 còn thiếu đã ghi trong
[grade4-curriculum.md](grade4-curriculum.md), đặc biệt nghe/nói có âm thanh và
bài viết được giáo viên nhận xét. Bảng hiện tại theo mạch, chưa đánh giá đạt yêu cầu.

Giao bài theo lớp đã có; ưu tiên báo cáo phụ huynh từ dữ liệu thật và bảo mật
quản trị khi triển khai. Sau khi có đủ lịch sử mới cải tiến
quy tắc kế hoạch cá nhân. Mở rộng nội dung có thể thực hiện song song với việc rà
soát chuyên môn của giáo viên.

Các dòng đề xuất là chức năng chưa triển khai. Admin đã có ngân hàng câu hỏi,
ghép đề và giao bài hàng loạt; học sinh đã có thư viện luyện tập. Thiết kế chi tiết
và các bước nâng cấp admin/người dùng nằm tại [authoring-design.md](authoring-design.md).
Mọi chức năng mới tiếp tục dùng schema hiện có,
quyền phía API và kiểm thử trên database test riêng.
