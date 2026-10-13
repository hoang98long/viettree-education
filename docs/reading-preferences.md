# Cỡ chữ học tập theo thiết bị

Bấm **Cỡ chữ** trên thanh đầu trang (cả khu học tập và AI Academy), hoặc mở
**Hồ sơ của em → Chữ dễ đọc cho em**. Trang hiển thị loại thiết bị đang chọn.

| Lựa chọn | Chữ thông thường | Nội dung bài học | Câu hỏi |
| --- | --- | --- | --- |
| Chữ gọn hơn | 16 px | 18 px | 20 px |
| Chữ vừa đủ lớn (mặc định) | 18 px | 20 px | 22 px |
| Chữ lớn hơn | 22 px | 24 px | 26 px |

AI Academy dùng lần lượt 18 / 20 / 23 px cho nội dung. Mức gọn giảm khoảng cách,
padding và tiêu đề; nút chính, lựa chọn cỡ chữ và ô nhập vẫn cao ít nhất 48 px.
Ô nhập tối thiểu 16 px để thuận tiện trên điện thoại. Các mức đều hỗ trợ màn hình nhỏ.

Mỗi tài khoản lưu riêng ba nhóm **điện thoại, máy tính bảng, máy tính** trên server.
Ví dụ, chọn gọn trên điện thoại và lớn trên máy tính: lần sau đăng nhập trên từng
loại thiết bị vẫn giữ lựa chọn tương ứng. Các thiết bị cùng nhóm dùng chung lựa chọn;
đây không phải cấu hình theo từng máy vật lý. Khi chưa chọn riêng, hệ thống giữ cỡ
chữ mặc định đã có của tài khoản, không tự giảm chữ trên điện thoại.

Nhận diện dùng thông tin trình duyệt, khả năng cảm ứng và kích thước màn hình;
thu nhỏ cửa sổ máy tính hoặc xoay điện thoại không đổi nhóm. Trình duyệt giả lập
thiết bị hoặc chế độ yêu cầu trang desktop có thể được nhận diện khác. Không tạo
định danh thiết bị, không lưu thông tin nhận diện vào database.

## Dữ liệu và API

Không cần migration. Dùng JSONB `student_profiles.accessibility_options` hiện có:

```json
{
  "text_size": "comfortable",
  "text_size_by_device": {
    "phone": "compact",
    "tablet": "comfortable",
    "desktop": "large"
  }
}
```

`PUT /api/v1/students/me/accessibility` nhận `text_size` (`compact`, `comfortable`,
`large`) và `device_type` (`phone`, `tablet`, `desktop`). Có `device_type` thì chỉ
cập nhật nhóm đó; bỏ trường này thì cập nhật mặc định, giữ tương thích client cũ.
Response, đăng nhập, `/auth/me` và hồ sơ trả `text_size` mặc định cùng
`text_size_by_device`; frontend chọn override của nhóm hiện tại rồi mới dùng mặc định.

Backend khóa hàng hồ sơ trước khi gộp JSONB, bảo toàn lựa chọn nhóm khác và các
tùy chọn khác khi hai thiết bị lưu đồng thời. Chỉ học sinh sửa được chính hồ sơ
của mình; giữ kiểm tra phiên, Origin và CSRF. Admin có thể chọn ba mức mặc định
trong quản trị tài khoản; chỉnh thông tin hoặc mặc định không xóa lựa chọn riêng.

Cache phiên trong bộ nhớ được cập nhật sau khi lưu thành công, không lưu token hay
thiết lập vào localStorage. Các tab nhận tín hiệu kiểm tra lại qua BroadcastChannel;
thiết bị khác nhận cấu hình khi đăng nhập, tải lại hoặc lần kiểm tra phiên kế tiếp
(30 giây khi trang đang mở). Kết quả lưu muộn không khôi phục phiên đã đăng xuất
và không ghi sang tài khoản khác. Lỗi lưu có thông báo và giữ lựa chọn đang dùng.
