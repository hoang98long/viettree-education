# Chạy nhanh trên máy local hiện tại

Máy hiện có PostgreSQL, `.env`, `.venv` và frontend. Không cần Docker,
import schema hoặc seed lại mỗi lần chạy. Giữ nguyên database và tài khoản.

Sau khi cập nhật dependency, dừng backend cũ bằng Ctrl+C trong terminal
của nó rồi cài từ thư mục gốc:

```powershell
./.venv/Scripts/python.exe -m pip install -r backend/requirements-lock.txt
Set-Location frontend
npm ci
```

## 1. Terminal backend

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\backend'
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

## 2. Terminal frontend

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\frontend'
$env:INTERNAL_API_URL = 'http://127.0.0.1:8000'
$env:PORT = '3000'
npm run dev
```

Mở **http://localhost:3000**, API **http://127.0.0.1:8000/ready**.
Đăng nhập bằng tài khoản đã có; mật khẩu demo lấy từ các biến `SEED_*`
trong `.env`, nếu đã đổi thì dùng mật khẩu mới. [Tài khoản demo](demo-accounts.md).
Dừng bằng Ctrl+C ở từng terminal.

## Khi cổng 8000 không khởi động được

`WinError 10013` có thể do cổng bị chiếm hoặc Windows dành riêng. Kiểm tra:

```powershell
netstat -ano | Select-String ':8000 .*LISTENING'
netsh interface ipv4 show excludedportrange protocol=tcp
```

Nếu có PID, xem tên bằng `Get-Process -Id PID_THUC_TE`; dừng backend cũ từ
terminal của nó nếu đó là phiên của bạn. Không tắt một PID chưa xác định.
Nếu dùng cổng 8100, thay **cả hai** chỗ sau và khởi động lại frontend:

```powershell
# Terminal backend, tại backend/
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8100 --reload --no-access-log

# Terminal frontend, tại frontend/
$env:INTERNAL_API_URL = 'http://127.0.0.1:8100'
$env:PORT = '3000'
npm run dev
```

Browser vẫn mở `http://localhost:3000`; không cần đổi `ALLOWED_ORIGINS`
chỉ vì đổi cổng backend. Cổng 8100 cũng phải nằm ngoài dải bị dành riêng.
Không cần tắt firewall hoặc chạy toàn bộ ứng dụng bằng Administrator.

## Lỗi thường gặp

- `Invalid project directory ... frontend\3000`: dùng `$env:PORT='3000'`
  rồi `npm run dev`, không thêm `3000` vào cuối lệnh.
- Login 403: dùng đúng `http://localhost:3000`, cấu hình local
  `ALLOWED_ORIGINS=http://localhost:3000`, `COOKIE_SECURE=false`,
  `APP_ENV=development`; restart backend sau khi sửa.
- Login 429: đợi theo thời gian `Retry-After`, rồi thử lại.
- DB không kết nối: kiểm PostgreSQL và `DB_*`; không tạo lại/xóa DB đang dùng.

Mở admin → **Kiểm tra hệ thống** để kiểm migration, học liệu và quyền.
Học liệu máy khác: [nạp đủ năm bộ](discovery-and-library-2026-11-04.md).
Triển khai Internet dùng [hướng dẫn VPS](deploy-vps-japan.md).
