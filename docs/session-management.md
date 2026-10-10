# Phiên đăng nhập và cache

## Phương án đã triển khai

| Trường hợp                                                  | Thời hạn mặc định       | Hành vi                                                                 |
| ----------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------- |
| Đăng nhập thường                                            | 8 giờ từ lúc đăng nhập  | Tải lại trang hoặc mở lại trình duyệt trong hạn không cần nhập mật khẩu |
| Học sinh chọn ghi nhớ trên máy cá nhân                      | 7 ngày từ lúc đăng nhập | Cookie tồn tại qua lần đóng/mở trình duyệt                              |
| Admin, giáo viên hoặc học sinh có thêm các vai trò này      | 8 giờ                   | Backend không cấp phiên dài dù client gửi `remember_me=true`            |
| Đăng xuất, tài khoản bị khóa, phiên bị thu hồi hoặc hết hạn | Mất quyền truy cập      | Backend từ chối ngay request tiếp theo                                  |

8 giờ phù hợp một ngày học/làm việc; 7 ngày là lựa chọn thêm cho học sinh dùng máy
cá nhân. Checkbox ghi nhớ mặc định bỏ chọn. Không dùng tùy chọn này trên máy chung.
Đây là thời hạn tuyệt đối: đọc bài hoặc kiểm tra phiên không kéo dài thời hạn.
Hiện chưa có thời hạn theo thời gian không hoạt động; có thể bổ sung riêng cho
admin khi cần, cùng quy trình quản lý thiết bị và thu hồi mọi phiên.

Thời hạn được quyết định ở backend, lưu trong `auth_sessions.expires_at`. Cookie
`viettree_session` và `viettree_csrf` có `Max-Age`/`Expires` cùng thời hạn. Token phiên
ngẫu nhiên, cookie phiên HttpOnly; database chỉ lưu hash. HTTPS production bật
Secure. Mỗi request bảo vệ kiểm tra phiên, trạng thái tài khoản và vai trò trong DB;
cache giao diện không cấp quyền. Đăng nhập lại tạo token mới và thu hồi token cũ
trên cùng trình duyệt; phiên ở thiết bị khác vẫn giữ nguyên.
Nếu học sinh được cấp thêm role admin/teacher trong khi còn phiên ghi nhớ, backend
cũng giới hạn phiên đang có theo thời hạn thường tính từ lúc tạo phiên.

Không cần migration: dùng bảng `auth_sessions` hiện có. Các phiên cũ giữ thời hạn
đã lưu trong DB. Thay cấu hình quyết định thời hạn cookie cho lần đăng nhập mới;
riêng phiên admin/teacher luôn bị giới hạn theo `SESSION_HOURS` hiện hành tính từ
lúc tạo, nên giảm cấu hình có thể làm phiên đặc quyền đang có hết hạn sớm hơn.

## Điều hướng khi đã đăng nhập

- Biểu tượng VietTree trong giao diện học tập/quản trị đưa về dashboard của vai trò
  hiện tại, thay vì đưa về trang giới thiệu với nút đăng nhập.
- Trang giới thiệu `/` có nút vào góc học tập/trang quản trị theo phiên hiện có.
- Mở `/login` khi phiên hợp lệ tự chuyển tới dashboard; không hiện form đăng nhập.
- Tải lại trang, mở tab mới hoặc mở lại trình duyệt đều kiểm tra cookie với backend.
- Hết phiên ở trang bảo vệ thì chuyển về đăng nhập. Lỗi mạng/503 hiển thị nút thử lại,
  không giả định người dùng đã đăng xuất.

## Cache được dùng

`SessionProvider` tại layout gốc dùng chung kết quả `/auth/me` cho toàn bộ giao diện:

- Cache trạng thái trong bộ nhớ của từng tab, TTL **30 giây**; gộp các yêu cầu đang
  chạy để tránh gọi lặp khi nhiều thành phần cần thông tin người dùng.
- Kiểm tra lại khi chuyển trang sau TTL, khi quay về tab, khi trang được khôi phục
  bằng Back/Forward và định kỳ 30 giây khi tab đang hiển thị.
- Khi tới thời điểm hết hạn do API trả về, kiểm tra lại với backend. Đồng hồ client
  chỉ dùng để lên lịch, không quyết định phiên hợp lệ.
- Đăng nhập/đăng xuất xóa hoặc thay trạng thái; `BroadcastChannel` đồng bộ các tab
  cùng origin bằng tín hiệu `refresh`/`logout`, không gửi token hay dữ liệu người dùng.
  Trình duyệt không hỗ trợ BroadcastChannel vẫn kiểm tra khi quay về tab/đến chu kỳ.
- Request cũ trả về sau khi đổi tài khoản hoặc đăng xuất không được khôi phục cache.
- API bảo vệ trả 401 sẽ xóa trạng thái giao diện ngay. Thu hồi ngoài trình duyệt được
  phát hiện qua request bảo vệ tiếp theo hoặc lần kiểm tra phiên, thường trong 30 giây
  với tab đang mở. Tab ẩn kiểm tra khi quay lại.

Không lưu token hay thông tin tài khoản vào localStorage/sessionStorage. API vẫn
trả `Cache-Control: no-store`; không cache dùng chung ở CDN, Next server hoặc Redis.
PostgreSQL là nguồn xác thực duy nhất và đã có khóa chính/index cho tra cứu phiên.
Chỉ cân nhắc Redis khi đo tải cho thấy cần, kèm cơ chế đồng bộ thu hồi giữa worker;
không dùng TTL Redis để làm chậm việc khóa tài khoản/thu hồi quyền.

## Cấu hình và sử dụng

Trong `.env` ở thư mục gốc:

```dotenv
SESSION_HOURS=8
REMEMBER_SESSION_DAYS=7
```

`SESSION_HOURS` cho phép 1–24 giờ, `REMEMBER_SESSION_DAYS` cho phép 1–30 ngày.
Khởi động lại backend sau khi đổi; khi dùng Compose production, khai báo các biến
này trong `environment` của service backend nếu muốn thay giá trị mặc định.
Giao diện đăng nhập ghi rõ các giá trị **mặc định** 8 giờ/7 ngày.

API `POST /api/v1/auth/login` nhận thêm `remember_me` (không truyền tương đương
`false`). Login và `GET /api/v1/auth/me` trả `session_expires_at` theo ISO 8601 kèm
múi giờ, không trả token trong JSON. Cookie và CSRF vẫn dùng cơ chế hiện có.

Sau cập nhật code, khởi động lại backend và frontend theo
[hướng dẫn local](run-local.md). Đăng xuất rồi đăng nhập lại để thử tùy chọn ghi nhớ.

## Kiểm chứng

- Backend: thời hạn DB/cookie, phiên thường/ghi nhớ, giới hạn cho vai trò đặc quyền,
  hết hạn dù còn cookie, thu hồi, tài khoản bị khóa, đổi token khi đăng nhập lại.
- Component: gộp request, TTL, lỗi mạng, kiểm tra khi quay về tab, hết hạn, đồng bộ
  đăng xuất và chống kết quả cũ khôi phục phiên.
- Browser: học sinh/admin bấm logo, truy cập trang chủ và `/login`, reload, mở tab
  mới, đăng xuất đồng bộ; kiểm tra trên desktop và mobile, database test riêng.

Nguyên tắc hết hạn ở server và không cache dữ liệu phiên nhạy cảm tham khảo
[OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
Thời hạn 8 giờ/7 ngày và cache 30 giây là lựa chọn cho VietTree, không phải thông số
bắt buộc của tài liệu tham khảo.
