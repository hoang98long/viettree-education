# VietTree Education

Ứng dụng học tập cho học sinh lớp 1–5: Toán, Tiếng Việt, Tiếng Anh và AI
Academy. Có tài khoản Free/VIP, lớp học, giao bài và quản trị học liệu.

- [Chạy trên máy hiện tại](docs/run-local.md)
- [Triển khai VPS 4 vCPU / RAM 8 GB / SSD 100 GB](docs/deploy-vps-japan.md)
- [Cài đặt VPS đầy đủ, chuyển database và phục hồi](docs/deploy-vps.md)
- [Kiến trúc](docs/architecture.md) · [API](docs/api.md) · [Lịch sử phát triển](docs/IMPLEMENTATION_STATUS.md)

## Chức năng chính

Học sinh đọc bài có tranh, dùng gợi ý theo bước, lưu bài yêu thích, làm bài
có tự lưu và xem kết quả. Có ba cỡ chữ, lưu riêng theo loại thiết bị.
Phiên mặc định 8 giờ; tùy chọn ghi nhớ 7 ngày trên máy cá nhân.

Admin quản lý tài khoản, mật khẩu, phiên, Free/VIP, lớp, câu hỏi, bài tập và
bài học có phiên bản. Giáo viên quản lý lớp được giao; phụ huynh xem trẻ đã
liên kết và quản lý consent. VIP được kiểm quyền tại API, không cộng điểm ưu tiên.

AI Academy dùng nội dung, tranh và hoạt động mô phỏng nội bộ. Mặc định
`AI_TRAINING_ONLY=true`, không cần GPU hoặc dịch vụ mô hình AI trả phí.
Chưa có thanh toán tự động.

| Học liệu bundled            | Mỗi khối                           | Tổng lớp 1–5                 |
| --------------------------- | ---------------------------------- | ---------------------------- |
| Toán, Tiếng Việt, Tiếng Anh | 89 bài / 474 câu / 77 đề           | 445 bài / 2.370 câu / 385 đề |
| AI Academy                  | 40 bài, 11 chủ đề; 5 Free / 35 VIP | 200 bài, 2.617 SVG           |

Số ba môn bao gồm bộ nền tảng và đủ năm bộ bổ sung. Nội dung do admin biên
soạn thêm không tính trong bảng. Cần giáo viên kiểm duyệt trước khi dùng
chính thức; kiểm tra dữ liệu không thay thẩm định sư phạm.

## Chạy local development

Yêu cầu Python 3.12+, Node.js 22.12+, PostgreSQL; cấu hình hiện dùng PG18.
Máy đã cài sẵn chỉ cần [hướng dẫn ngắn](docs/run-local.md).

Cài lần đầu từ thư mục gốc, PowerShell:

```powershell
if (!(Test-Path -LiteralPath '.env')) { Copy-Item .env.example .env }
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r backend/requirements-lock.txt
./.venv/Scripts/python.exe -m pip install --no-deps -e ./backend
Set-Location frontend
npm ci
```

Điền `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` trong `.env`.
Giữ file hiện có nếu đang dùng; không commit mật khẩu. Database mặc định
`viettree-education`. Database mới phải tồn tại trước khi `import-schema`;
database đã có dữ liệu không cần import/seed lại.

```powershell
# Tại backend/, sau khi đã cấu hình PostgreSQL:
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
```

Khởi động bằng hai terminal riêng từ thư mục gốc:

```powershell
# Terminal backend
Set-Location backend
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

```powershell
# Terminal frontend
Set-Location frontend
$env:INTERNAL_API_URL = 'http://127.0.0.1:8000'
$env:PORT = '3000'
npm run dev
```

Mở **http://localhost:3000**. Backend: `/health`, `/ready`, `/docs` trên cổng
8000 khi development. Nếu gặp `WinError 10013` hoặc cổng đang dùng, xem
[cách kiểm tra và đổi sang 8100](docs/run-local.md#khi-cổng-8000-không-khởi-động-được).

Nạp học liệu lần đầu/máy khác: [năm bộ bổ sung](docs/discovery-and-library-2026-11-04.md),
[AI Academy](docs/ai-academy/deployment.md). Demo chỉ dùng development;
[danh sách tài khoản](docs/demo-accounts.md). Không seed demo sau restore dữ liệu thật.

## Triển khai production

VPS mục tiêu: **4 vCPU / RAM 8 GB / SSD 100 GB**. Dùng bốn dịch vụ:
Caddy HTTPS → Next.js standalone / FastAPI → PostgreSQL. Chỉ công khai
80/443; không public DB, API hoặc cổng Next.js.

```bash
# Trên VPS, sau khi tạo .env.production theo hướng dẫn:
dc() { bash /opt/viettree-education/deploy/compose.sh "$@"; }
dc config --quiet
dc build backend frontend
dc pull db caddy
```

Chọn `VIETTREE_DEPLOY_PROFILE=vps8gb` bằng mẫu `.env.production.vps8gb.example`.
Làm tiếp các bước tạo role, restore/migrate, cấp quyền và mở web trong
[hướng dẫn VPS](docs/deploy-vps-japan.md). Không chạy `--reload` ở production.

Image backend chỉ cài `backend/requirements-runtime-lock.txt`; lock phát triển
`requirements-lock.txt` bổ sung pytest/Ruff. Test, báo cáo và artifact tạm
không được đưa vào image. Không cần chạy stack audit trên VPS.

## Kiểm thử và vận hành

```powershell
# backend/: unit không cần DB tích hợp
../.venv/Scripts/python.exe -m pytest -m "not integration" -q
../.venv/Scripts/python.exe -m ruff check .

# frontend/
npm run test
npm run lint
npm run build
```

Integration cần database test **riêng** và `TEST_DATABASE_URL`; không trỏ vào
DB đang sử dụng. Browser smoke chạy `npm run test:audit` sau khi tạo fixture
giả bằng `scripts.prepare_e2e`; cấu hình tái hiện nằm trong `.github/workflows/verify.yml`.
Các regression bảo mật/chấm điểm vẫn giữ trong repo.

Sau triển khai: `check-launch`, `check-release`, `deploy/smoke.sh`; sao lưu
DB và ảnh upload bằng `deploy/backup.sh`, lưu bản sao ngoài VPS và thử phục
hồi. Giữ khoảng 20 GB trống; snapshot nhà cung cấp không thay backup dữ liệu.

## Cấu trúc

```text
backend/app/       API, service, học liệu, AI Academy
backend/alembic/   Migration; head 0012_lesson_bookmarks
backend/tests/    Kiểm thử nghiệp vụ, quyền và vận hành
frontend/src/     Trang, tính năng và component giao diện
database/         SQL gốc và kiểm chứng seed
deploy/           Image production, HTTPS, backup và smoke
docs/             Hướng dẫn sử dụng, kiến trúc và triển khai
```

Hướng dẫn chức năng: [tài khoản](docs/account-management.md),
[Free/VIP](docs/free-vip-design.md), [lớp/giao bài](docs/classes-achievements.md),
[biên soạn bài học](docs/lesson-studio.md), [AI Academy](docs/ai-academy/README.md).
Giấy phép: [LICENSE](LICENSE).
