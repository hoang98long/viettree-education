# Định hướng mở rộng VietTree Education

## Đã triển khai trong vòng này

Chữ học sinh 18 px, bài học 20 px, câu hỏi 22 px; chế độ chữ lớn lưu theo tài khoản.
Kế hoạch học 7 ngày theo môn có tối đa 3 bài mới và bài luyện tập, theo dõi tiến độ
đọc và bài đã nộp. Kế hoạch dùng dữ liệu chương trình đang xuất bản, cùng lớp và
còn lượt luyện tập. Không gán điểm hoặc năng lực từ thao tác xác nhận đọc.

## Các chức năng đề xuất tiếp theo

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

| Ưu tiên | Chức năng | Giá trị và tiêu chí nghiệm thu |
| --- | --- | --- |
| 1 | Giáo viên giao bài cho lớp | Giáo viên chỉ xem lớp mình phụ trách; chọn đề đã xuất bản, giờ mở/hạn nộp; giao lặp không tạo trùng. Học sinh thấy bài trong Nhiệm vụ hôm nay; giáo viên xem ai chưa bắt đầu/đang làm/đã nộp. |
| 2 | Báo cáo phụ huynh theo tuần | Chỉ phụ huynh có liên kết và quyền phù hợp mới xem dữ liệu trẻ; tổng hợp bài đã đọc, bài đã nộp, kỹ năng cần ôn và gợi ý hỗ trợ. Tách rõ tiến độ học khỏi độ vững kỹ năng; chưa có dữ liệu thì báo chưa đủ để đánh giá. |
| 3 | Tự điều chỉnh bước kế hoạch | plan_v2 theo kỹ năng đã có. Tiếp tục thay bước bị đóng/hết lượt mà giữ lịch sử thay đổi và các bước đã hoàn thành. |
| 4 | Nội dung lớp 1–3 và lớp 5 | Ưu tiên lớp 1–2 với câu ngắn, hình minh họa và hướng dẫn từng bước; giáo viên rà soát nội dung, đáp án và độ khó trước khi xuất bản. Giữ trạng thái đang xây dựng cho phần chưa có nội dung. |
| 5 | Đọc hướng dẫn bằng âm thanh | Nút nghe/dừng, không tự phát; dùng âm thanh đã được rà soát cho tiếng Việt/tiếng Anh. Bài kiểm tra đọc hiểu cần quy tắc riêng để âm thanh không làm thay phần cần đánh giá. |

## Thứ tự thực hiện đề nghị

Đợt lớp 4 có thêm Góc tư duy, bảng học liệu admin, góc và biểu đồ SVG. Trước khi
mở thêm khối lớp, bổ sung các mảng lớp 4 còn thiếu đã ghi trong
[grade4-curriculum.md](grade4-curriculum.md), đặc biệt nghe/nói có âm thanh và
bài viết được giáo viên nhận xét. Bảng hiện tại theo mạch, chưa đánh giá đạt yêu cầu.

Hoàn thiện giao bài cho lớp trước để giáo viên đưa hệ thống vào hoạt động hằng ngày.
Tiếp đó làm báo cáo phụ huynh từ dữ liệu thật; sau khi có đủ lịch sử mới cải tiến
quy tắc kế hoạch cá nhân. Mở rộng nội dung có thể thực hiện song song với việc rà
soát chuyên môn của giáo viên.

Các dòng đề xuất là chức năng chưa triển khai. Admin đã có ngân hàng câu hỏi,
ghép đề và giao bài hàng loạt; học sinh đã có thư viện luyện tập. Thiết kế chi tiết
và các bước nâng cấp admin/người dùng nằm tại [authoring-design.md](authoring-design.md).
Mọi chức năng mới tiếp tục dùng schema hiện có,
quyền phía API và kiểm thử trên database test riêng.
