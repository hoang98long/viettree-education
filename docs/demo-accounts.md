# Tài khoản thử nghiệm theo khối lớp

Máy local có **20 tài khoản thử lớp 1–5**: thêm 12 học sinh lớp 1–3 và bốn
học sinh lớp 5, giữ nguyên bốn tài khoản lớp 4.
Mỗi khối có hai Free và hai VIP. VIP mới được cấp 90 ngày, có audit theo cơ chế
quản trị gói hiện hành; không tạo điểm/thành tích hoặc lịch sử giả.

| Khối | Free                   | VIP                  |
| ---- | ---------------------- | -------------------- |
| 1    | `free1_01`, `free1_02` | `vip1_01`, `vip1_02` |
| 2    | `free2_01`, `free2_02` | `vip2_01`, `vip2_02` |
| 3    | `free3_01`, `free3_02` | `vip3_01`, `vip3_02` |
| 4    | `free4_01`, `free4_02` | `vip4_01`, `vip4_02` |
| 5    | `free5_01`, `free5_02` | `vip5_01`, `vip5_02` |

Mật khẩu tài khoản mới là **`SEED_STUDENT_PASSWORD` trong `.env` ở thư mục gốc**.
Không ghi mật khẩu thật vào Git/tài liệu/nhật ký. Tài khoản đã đổi mật khẩu dùng
mật khẩu mới; chạy lại lệnh không đặt lại hoặc nâng quyền. Tên `vip` chỉ là
nhãn lúc tạo: xem **Gói học của em** hoặc admin để biết thời hạn hiện tại.

```powershell
# Trong backend; mặc định năm khối, không reset dữ liệu cũ.
../.venv/Scripts/python.exe -m app.cli seed-demo-learners
# Chỉ tạo/kiểm tra khối cần dùng.
../.venv/Scripts/python.exe -m app.cli seed-demo-learners --grades 1 2
```

Lệnh cần `APP_ENV=development`, `SEED_STUDENT_PASSWORD` và admin đang hoạt động
để ghi audit cấp VIP. Output chỉ có username/khối/created/gói, không có mật
khẩu. Tài khoản cũ giữ mật khẩu, khối, trạng thái khóa, phiên và gói đã hết hạn/
thu hồi; không tự cấp lại VIP. Collision vai trò hoặc thiếu hồ sơ dừng transaction.
Học sinh mới ở trạng thái tự do, admin gán lớp khi cần.

Production tạo học sinh thật qua **Quản trị tài khoản**, chọn khối 1–5, mật
khẩu tạm và buộc đổi; cấp VIP qua quản trị. Không dùng tài khoản demo cho học
sinh thật. Xem [quản trị tài khoản](account-management.md).
