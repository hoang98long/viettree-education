# Quản trị tài khoản và bảo mật cá nhân

Admin mở **Quản trị tài khoản** (`/admin/accounts`). Mọi vai trò mở **Bảo mật
tài khoản** (`/account/security`) để tự đổi mật khẩu và đăng xuất phiên khác.
Nâng cấp chạy `alembic upgrade head` trước khi khởi động backend/frontend;
head mới là `0008_account_management`, không cần seed lại.

## Chức năng đã triển khai

| Thao tác | Kết quả |
| --- | --- |
| Tạo | Tên đăng nhập, tên hiển thị, email tùy chọn, một/nhiều vai trò; học sinh có lớp 1–5/cỡ chữ, mặc định Free. |
| Tìm/lọc | Tên đăng nhập/tên hiển thị/email; vai trò, trạng thái, lớp; phân trang 20 tài khoản. |
| Sửa | Thay thông tin, vai trò, lớp/cỡ chữ, trạng thái; giữ UUID và lịch sử. |
| Khóa/mở | Khóa thu hồi phiên; mở không khôi phục phiên cũ hay gia hạn VIP. |
| Đặt lại mật khẩu | Admin cấp mật khẩu tạm mới, thu hồi mọi phiên, bắt buộc người dùng đổi mật khẩu tạm. |
| Thu hồi phiên | Admin đăng xuất tài khoản khỏi mọi thiết bị; vẫn được đăng nhập lại nếu hoạt động. |
| Gói học | Liên kết tới trang cấp/gia hạn/thu hồi Free/VIP hiện có, độc lập vai trò quản trị. |
| Nhật ký | 20 thao tác gần nhất, người thực hiện, thời điểm, lý do và thay đổi. |
| Bảo mật cá nhân | Xác nhận mật khẩu hiện tại để đổi mật khẩu hoặc đăng xuất các phiên khác. |

Tên đăng nhập dài 3–80 ký tự, dùng chữ không dấu, số, chấm, gạch dưới/gạch ngang,
được chuẩn hóa chữ thường. Tên đăng nhập/email không trùng kể cả khác hoa/thường.
Email là thông tin liên hệ **chưa xác minh**, chưa dùng đăng nhập/khôi phục mật khẩu.
Học sinh không cần email riêng, ngày sinh, địa chỉ hay điện thoại. Lớp 4 hiện có
học liệu thật; các lớp khác tiếp tục dùng trạng thái đang xây dựng.

Admin nhập lại mật khẩu của mình và lý do cho mỗi thao tác trong màn hình mới.
Không đưa mật khẩu vào lý do; hệ thống không gửi email hoặc trả mật khẩu qua API.
Bàn giao mật khẩu tạm cho người dùng/người giám hộ qua kênh riêng đã thống nhất.

## Mật khẩu và phiên

Mật khẩu mới dài **15–256 ký tự**, chấp nhận Unicode/khoảng trắng, không ép chữ
hoa/số/ký hiệu. Có thể dùng cụm vài từ dễ nhớ với sự hỗ trợ của người lớn.
Chặn một số mật khẩu phổ biến, toàn khoảng trắng, mật khẩu trùng tên đăng nhập;
đổi/đặt lại phải khác mật khẩu cũ. Danh sách chặn hiện nhỏ, chưa kiểm tra mật khẩu
rò rỉ. Tài khoản cũ tiếp tục đăng nhập bằng mật khẩu đã có; không bị reset tự động.

Giao diện tạo tài khoản luôn bật yêu cầu đổi mật khẩu tạm. API hỗ trợ
`must_change_password=false` cho quy trình cấp mật khẩu đã thiết lập riêng;
admin đặt lại luôn bật cờ. Khi cờ bật, backend chỉ cho xem trạng thái đăng nhập,
thông tin bảo mật, đổi mật khẩu và đăng xuất; chặn cả học liệu lẫn API admin.

Tự đổi mật khẩu thu hồi mọi phiên cũ, thay token/CSRF cho trình duyệt hiện tại,
và cấp phiên thường 8 giờ theo cấu hình. Không giữ phiên ghi nhớ sau thao tác này.
Cache giao diện được cập nhật, tab khác kiểm tra lại; backend tiếp tục xét quyền
ở mỗi request. Khóa, đổi tên đăng nhập/vai trò thu hồi mọi phiên. Chỉ sửa tên
hiển thị, email, lớp/cỡ chữ không đăng xuất.

Xác nhận mật khẩu giới hạn **10 lượt/phút/tài khoản**, tính cả lượt đúng/sai,
lưu PostgreSQL dùng chung giữa worker; vượt trả 429/Retry-After 60. Rate limit
đăng nhập hiện có áp dụng riêng. Không lưu/hiển thị IP, vị trí hay tên thiết bị
trong danh sách phiên; tối đa 20 dòng thời điểm, đánh dấu phiên hiện tại. Đếm theo
hạn hiệu lực thực tế của vai trò. Số bản ghi thu hồi có thể gồm phiên đã hết hạn;
thu hồi không hủy request đã xác thực và đang thực thi.

Chính sách tham khảo [OWASP Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
và [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html):
xác nhận mật khẩu cho thay đổi nhạy cảm, thay token sau đổi mật khẩu/quyền.
Không phải chứng nhận tuân thủ toàn bộ OWASP.

## Toàn vẹn và vận hành

- Không xóa tài khoản: khóa để giữ lịch sử, quan hệ và khả năng đối soát.
- Không tự khóa/đổi vai trò của mình, không loại bỏ admin hoạt động cuối cùng.
  Admin đổi mật khẩu của mình ở trang bảo mật cá nhân.
- Khóa transaction/hàng tài khoản theo thứ tự, kiểm tra lại người thực hiện;
  hai admin không thể đồng thời khóa lẫn nhau. Đăng nhập khóa hàng khi xác minh/
  cấp phiên, tránh phiên từ mật khẩu cũ sống sót sau đặt lại đồng thời.
  Khóa user dùng FOR NO KEY UPDATE để thao tác trên hồ sơ vẫn ghi được nhật ký
  tham chiếu UUID, tránh vòng chờ với khóa ngoại. Xem [PostgreSQL row locks](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-ROWS).
- Revision ngăn ghi đè khi hai người sửa. Tài khoản đã thay đổi (kể cả tự đổi
  mật khẩu/sửa hồ sơ cũ) trả 409; tải lại, rà soát rồi nhập lại thay đổi.
- Gỡ vai trò student giữ hồ sơ, membership, kết quả và quan hệ cũ; danh sách/
  thống kê học sinh hiện hành chỉ đếm người còn vai trò student. Đổi lớp không
  xóa bài làm; học liệu được lọc theo lớp hiện tại.
- Nhật ký cùng transaction, chỉ ghi trường cho phép, không password/hash,
  token/CSRF hoặc email plaintext. Không ghi bí mật/thông tin riêng tư vào lý do.
- Migration thêm account_revision (1), must_change_password (false cho tài khoản
  cũ), password_changed_at (NULL cho tài khoản cũ). Không sửa SQL gốc, mật khẩu,
  gói, phiên hoặc lịch sử cũ. Ngày đổi mật khẩu cũ chưa rõ hiển thị “—”.

Endpoint sửa hồ sơ cũ `/admin/students/{id}` giữ RBAC/CSRF, cập nhật revision,
chỉ sửa tên hiển thị/lớp, không yêu cầu xác nhận mật khẩu lần nữa. Các thao tác
nhạy cảm dùng API accounts mới. Xem danh sách endpoint trong [api.md](api.md).

## Ưu tiên phát triển tiếp

1. MFA/passkey cho admin; xác minh email, khôi phục bằng token dùng một lần và
   thông báo bảo mật sau khi cấu hình dịch vụ gửi mail.
2. Xác minh quan hệ phụ huynh–học sinh, quyền giáo viên theo lớp. Tạo vai trò
   teacher/guardian hiện chỉ cấp vai trò/layout đã có, chưa mở quản lý lớp hoặc
   truy cập kết quả con; không suy ra quan hệ từ email.
3. Nhập tài khoản hàng loạt có đối chiếu/lỗi từng hàng, bàn giao mật khẩu và
   phân quyền admin theo trách nhiệm.
4. Chính sách lưu trữ/xóa dữ liệu và giám sát theo đơn vị triển khai. VPS vẫn
   cần HTTPS, DB user riêng và backup được phục hồi thử theo [deploy-vps.md](deploy-vps.md).
