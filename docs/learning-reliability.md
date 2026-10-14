# Tự lưu bài làm và rà soát học liệu

Cập nhật 14/10/2026. Bản nâng cấp không cần migration hoặc seed lại database.
Khởi động lại backend và frontend để dùng cùng hợp đồng API mới.

## Dành cho học sinh

- Sau khi chọn hoặc ngừng gõ khoảng **0,8 giây**, bài tự lưu đáp án.
  Dòng dưới câu hỏi phân biệt chờ lưu, đang lưu, đã lưu và chưa lưu được.
- **Lưu bài**, chuyển câu và nộp bài đều chờ lưu hết đáp án mới nhất. Tự lưu
  không nộp bài và không chấm điểm trước khi học sinh xác nhận nộp.
- Khi mất mạng, lựa chọn vẫn ở trang đang mở; nút **Thử lưu lại** gửi lại phần
  chưa lưu. Khi trình duyệt báo mạng trở lại, ứng dụng cũng thử lưu phần đó.
  Lỗi không tạo vòng lặp gửi request liên tục.
- Mỗi request lưu chờ tối đa **15 giây**. Timeout không chứng minh server chưa
  ghi dữ liệu; gửi lại cùng đáp án là thao tác hợp lệ, không tạo thêm câu trả lời.
- Bấm liên kết nội bộ trong trang làm bài chờ lưu xong rồi mới chuyển trang.
  Nếu lưu thất bại, giữ trang để thử lại. Đóng hoặc tải lại tab khi còn phần
  chưa lưu kích hoạt cảnh báo chuẩn của trình duyệt.
- Đáp án chưa lưu chỉ được giữ **trong bộ nhớ của trang**, không ghi vào
  localStorage hoặc cache dùng chung. Đây không phải chế độ làm bài offline:
  chủ động đóng/reload dù cảnh báo có thể mất phần chưa lưu. Nút Back của
  trình duyệt và sự cố tắt máy không được bảo đảm khôi phục phần này.

Học sinh vẫn sửa được lựa chọn trong lúc tự lưu. Nút nộp/đổi câu thủ công chờ
hoàn tất hàng lưu; phản hồi cũ không được đánh dấu đáp án mới là đã lưu.
Khi rời trang, hủy request đang chờ và ngừng gửi các đáp án còn lại.

## Thời gian còn lại

Bài có thời hạn hiển thị đồng hồ, nhắc khi còn hai phút và dừng hiển thị tại
00:00. Mốc ban đầu lấy từ giờ máy chủ, sau đó dùng đồng hồ đơn điệu của trình
duyệt; việc chỉnh giờ thiết bị không làm nhảy bộ đếm. Reload lấy mốc mới.
Đồng hồ là thông tin hỗ trợ; backend vẫn kiểm tra hạn giao bài, thời lượng đề,
quyền Free/VIP và trạng thái bài tại mỗi lần lưu/nộp. Không tự nộp bài hoặc
gia hạn thời gian dựa trên đồng hồ giao diện.

## Dành cho admin

Trong màn hình biên soạn bài học có **Rà soát trước khi duyệt**:

- Tổng độ dài và số phần; chỉ ra câu/dòng còn dài hơn mức chia đoạn của khối
  (35 tiếng cho lớp 1–2, 55 cho lớp 3–5), gợi ý viết câu ngắn.
- Phần còn trống; trạng thái hình minh họa riêng.
- Phân bổ gợi ý Free/VIP cho bài Free; bài VIP ghi rõ toàn bộ bài yêu cầu VIP.
- Nhắc bổ sung giới thiệu riêng khi bài VIP chưa có đoạn giới thiệu.

Đếm độ dài theo khoảng trắng chỉ là gợi ý trình bày, không đánh giá ngữ nghĩa,
độ đúng hoặc chứng nhận chương trình. Không tự cắt bài đọc/dòng thơ, tự thay
quyền hoặc tự xuất bản. Quy trình lưu nháp → duyệt → xuất bản và kiểm tra
revision/fingerprint phía server vẫn bắt buộc.

## API và xử lý đồng thời

`GET /api/v1/attempts/{id}` bổ sung `server_time` (ISO 8601, UTC), bên cạnh
`deadline`. API lưu giữ nguyên `{ "answer": ... }`; không nhận điểm hoặc mốc
giờ do học sinh tự gửi để quyết định thứ tự lưu.

Frontend gom thay đổi và chỉ gửi một request lưu mỗi lần. Sau phản hồi thành
công, chỉ bỏ bản đáp án vừa được xác nhận; bản sửa mới hơn tiếp tục được lưu.
Các câu đã lưu thành công không bị gửi lại khi một câu sau thất bại.

Backend lấy giờ nhận request trước khi chờ xác thực/database. Cột `answered_at`
lưu mốc này; upsert chỉ cập nhật nếu mốc không cũ hơn đáp án hiện tại. Request
cũ xử lý muộn trả 409 thay vì ghi đè request được nhận sau. Dùng khóa bài làm
và kiểm tra quyền/thời hạn hiện có; không thay schema hoặc sửa hàng dữ liệu cũ.
Hai tab/thiết bị sửa cùng câu vẫn theo thứ tự request server nhận được, không
phải cơ chế hợp nhất hai bản sửa độc lập.

Endpoint vẫn dùng CSRF, Origin, quyền chủ bài, kiểm tra kiểu đáp án và giao dịch
commit trước khi trả thành công; không cache đáp án hoặc response bài làm.

## Kiểm thử

Rà soát tiếp ngày 14/10/2026: tách ngữ liệu khỏi tiêu đề câu hỏi, đọc từng đoạn,
giữ dòng trắng giữa khổ thơ và tăng độ đậm chữ phần đọc. API bài làm bổ sung
`grade` để chọn độ dài đoạn theo khối. Chấm điền khuyết chấp nhận cách viết số
tương đương có kiểm soát; xem [báo cáo học liệu và tải](content-load-vps-review.md).

Kiểm tra gom thao tác gõ, request chậm, đáp án mới trong lúc lưu, lỗi/retry,
request treo, hủy khi rời trang và React StrictMode. PostgreSQL thật kiểm tra
lưu lặp không tăng số hàng, request cũ không ghi đè, thời hạn, quyền chủ bài,
chấm/nộp và Free/VIP. Browser desktop/mobile kiểm tra tự lưu/reload, mạng lỗi,
chuyển trang khi còn đáp án chờ và biên soạn/duyệt bài học.
