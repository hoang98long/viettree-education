# Chạy nhanh trên máy local hiện tại

Máy Windows hiện có `.env`, `.venv`, `frontend/node_modules` và PostgreSQL 18
đang chạy. Dùng PowerShell; không cần Docker hoặc cài lại các thư viện.

## 1. Mở backend — terminal thứ nhất

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\backend'
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
../.venv/Scripts/python.exe -m app.cli check-system
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

Giữ terminal này mở. Migration cập nhật cấu trúc nếu cần, giữ dữ liệu học tập.
Không cần import schema hoặc seed lại mỗi lần chạy.

Nâng cấp lớp 3 lần đầu: trước khi mở backend, chạy thêm
`../.venv/Scripts/python.exe -m app.cli seed-grade3-content`.
Head hiện tại `0010_ai_academy`, bao gồm gợi ý VIP từ 0009. Admin tạo/chỉnh hồ sơ học sinh
**Lớp 3**, rồi chọn lớp 3 trong học liệu. Mỗi bài lớp 3: Free 1 gợi ý, VIP 3;
xem [học liệu lớp 3](grade3-curriculum.md). Không đổi tài khoản lớp 4 tự động.

AI Academy trên máy hiện tại đã được migrate và nạp 48 bài/315 hình. Với máy
khác hoặc lần nâng cấp đầu, cài thêm dependencies và nạp module trước khi chạy:

```powershell
../.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
```

Đăng nhập → **AI Academy** (`/ai-academy`); admin `/admin/ai-academy`.
Mặc định mô phỏng, không cần khóa AI. Chi tiết [AI Academy](ai-academy/README.md).
Giữ `.env` hiện có; file `.env.example` dùng placeholder, không chép đè mật khẩu.

## 2. Mở frontend — terminal thứ hai

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\frontend'
$env:INTERNAL_API_URL = 'http://localhost:8000'
$env:PORT = '3000'
npm run dev
```

Giữ terminal này mở. Truy cập **http://localhost:3000**.
Đặt cổng qua biến `PORT` để tránh lỗi truyền tham số qua npm/PowerShell.

## 3. Đăng nhập và kiểm tra

Admin mở **Kiểm tra hệ thống** để xem migration, quyền Free/VIP, đề và phiên cũ;
bấm **Kiểm tra lại** để cập nhật số liệu. Chỉ đọc, không tự dọn dữ liệu.
Xem [kiểm tra trước triển khai](production-readiness.md) cho bảo trì/backup.

Admin mở **Quản trị tài khoản** để tạo/sửa, khóa/mở, đặt lại mật khẩu hoặc thu hồi
phiên. Mọi tài khoản mở **Bảo mật tài khoản** để tự đổi mật khẩu. Tài khoản mới
dùng mật khẩu tạm được dẫn tới trang đổi mật khẩu trước khi sử dụng. Đợt này cần
migration `0008_account_management` (đã bao gồm trong lệnh bước 1), không cần seed lại tài khoản.
Chi tiết: [quản trị tài khoản](account-management.md).

Nội dung lớp 4 mới: mở **Góc tư duy** ở tài khoản học sinh; admin xem
**Chương trình → Lớp 4 → Theo dõi học liệu**. Nạp riêng nếu DB chưa có đợt mở rộng:

```powershell
# Chạy trong backend, một lần; không đổi tài khoản hay tiến độ cũ.
../.venv/Scripts/python.exe -m app.cli seed-grade4-content
```

Khởi động lại hai server sau khi cập nhật code. Xem [học liệu lớp 4](grade4-curriculum.md).

| Tài khoản              | Mục đích                                          |
| ---------------------- | ------------------------------------------------- |
| `admin`                | Quản trị, ngân hàng câu hỏi, tạo bài tập, cấp VIP |
| `longnh`               | Học sinh lớp 4                                    |
| `free4_01`, `free4_02` | Học sinh gói Free                                 |
| `vip4_01`, `vip4_02`   | Học sinh demo VIP; gói có thể hết hạn             |

Mật khẩu demo lấy từ `.env` ở thư mục gốc: `SEED_ADMIN_PASSWORD` cho admin,
`SEED_STUDENT_PASSWORD` cho học sinh. Nếu đã đổi mật khẩu, dùng mật khẩu mới.
Admin có thể cấp/gia hạn VIP tại **Học sinh → Quản lý gói học**.

Phiên thường mặc định **8 giờ**. Học sinh có thể chọn **Ghi nhớ đăng nhập trên máy
cá nhân** để giữ phiên **7 ngày**. Trong phiên, bấm biểu tượng VietTree sẽ về
dashboard; mở `/login` tự chuyển tiếp. Xem [quản lý phiên](session-management.md).

Học sinh VIP mở menu **Góc học VIP** để tìm bài nâng cao, ôn câu sai và xem/in báo
cáo 7/30 ngày. Chi tiết: [mở rộng VIP](vip-expansion.md).

Kiểm tra backend và kết nối database tại **http://localhost:8000/ready**.
Tài liệu API: **http://localhost:8000/docs**.
Dừng hệ thống bằng **Ctrl+C** ở cả hai terminal.

## Khi gặp lỗi

Sau nâng cấp bài học, chạy `../.venv/Scripts/python.exe -m alembic upgrade head`
trong `backend`, rồi khởi động lại hai server. Admin dùng **Quản lý bài học**;
học sinh mở bài để xem minh họa và gợi ý. [Hướng dẫn](lesson-studio.md).

- **`Invalid project directory ... frontend\3000`:** chạy lại đúng lệnh
  `npm run dev` ở trên; không thêm `3000` vào cuối lệnh.
- **Cổng 8000/3000 đang dùng:** kiểm tra terminal cũ; nếu ứng dụng đã chạy thì mở
  trang web luôn. Muốn khởi động lại, dừng phiên cũ bằng Ctrl+C rồi chạy lại.
- **Không kết nối database:** kiểm tra service `postgresql-x64-18` và các biến
  `DB_*` trong `.env`; database hiện tại là `viettree-education`.
- **Đăng nhập lỗi 403:** dùng đúng `http://localhost:3000`, đặt
  `ALLOWED_ORIGINS=http://localhost:3000`, `COOKIE_SECURE=false`,
  `APP_ENV=development` trong `.env`, rồi khởi động lại backend.
- **Đăng nhập lỗi 429:** đợi khoảng một phút rồi thử lại.

Nếu chuyển sang máy khác hoặc thiếu thư viện, xem phần
[Chạy local development trong README](../README.md#chạy-local-development).
