# VietTree Education

Ứng dụng học tập tiếng Việt cho học sinh tiểu học: Next.js App Router + FastAPI +
PostgreSQL thật. Đăng nhập, đọc bài, lưu/resume bài làm, chấm điểm phía server,
lịch sử, năng lực và gợi ý ôn tập hoạt động end-to-end.

**Giữ nguyên** `database/viettree_education_schema.sql` với 34 bảng gốc. Không reset,
DROP hay TRUNCATE database học tập. Database mặc định có tên **`viettree-education`**,
bao gồm dấu gạch ngang. Chỉ hai bảng auth được bổ sung bằng Alembic.

## Chạy local development

Yêu cầu: Python **3.12+**, Node.js **22.12+**, npm, PostgreSQL **14+** đang chạy.
Docker Desktop/Compose là tùy chọn. Phiên triển khai đã kiểm thử trên Windows,
Python 3.13, Node 22 và PostgreSQL 18. Các lệnh PowerShell sau chạy từ root dự án.

```powershell
Copy-Item .env.example .env
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r backend/requirements-lock.txt
./.venv/Scripts/python.exe -m pip install --no-deps -e ./backend
```

Cách cài để phát triển/thay đổi dependency: `pip install -e "./backend[dev]"`.
Có thể dùng uv: `uv venv .venv` rồi `uv pip install -e "./backend[dev]"`.
Linux/macOS thay `.venv/Scripts/python.exe` bằng `.venv/bin/python`, dùng `cp` để
copy env. Không bắt buộc activate venv; lệnh trên chỉ rõ Python của dự án.

`.env` nằm tại root, được backend đọc dù chạy từ thư mục backend. Không commit file
này. `DB_PASSWORD` được ghép vào SQLAlchemy URL bằng `URL.create`, hỗ trợ ký tự đặc biệt.

| Biến | Cách sử dụng |
| --- | --- |
| DB_HOST | `localhost` khi chạy backend trên host |
| DB_PORT / DB_NAME | `5432` / `viettree-education` |
| DB_USER / DB_PASSWORD | Cấu hình local do bạn cung cấp trong `.env` |
| ALLOWED_ORIGINS | Danh sách origin chính xác, phân cách bằng dấu phẩy; mặc định `http://localhost:3000` |
| COOKIE_SECURE | `false` cho HTTP local, `true` khi triển khai HTTPS |
| SESSION_HOURS | Thời hạn tuyệt đối của phiên, mặc định 8 giờ |
| SEED_ADMIN_PASSWORD / SEED_STUDENT_PASSWORD | Chỉ dùng khi chủ động seed demo |
| INTERNAL_API_URL | Next server nối backend; mặc định `http://localhost:8000` |

Kiểm tra schema và áp dụng migration:

```powershell
Set-Location backend
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
../.venv/Scripts/python.exe -m app.cli seed
../.venv/Scripts/python.exe -m app.cli verify-seed
```

`alembic upgrade head` kiểm tra đủ bảng/cột gốc rồi thêm auth_sessions,
auth_login_limits và bảng quản lý phiên bản alembic_version. Không tạo schema học
tập khác. Thiếu bảng/cột sẽ báo lỗi và dừng. Khi schema chưa import, chạy **tùy chọn**:

```powershell
python -m app.cli import-schema
# Hoặc sử dụng psql từ root:
psql -h localhost -U postgres -d "viettree-education" -v ON_ERROR_STOP=1 -f database/viettree_education_schema.sql
```

Lệnh import đọc đúng SQL gốc, không tạo hoặc xóa database. Database phải tồn tại.
Sau import, chạy lại migration. CLI `check-schema` kiểm tra cả các cột thực tế.

Seed idempotent dùng unique codes và transaction/advisory lock: chạy lại không
nhân đôi user/role/profile/chương trình và không sửa version câu hỏi hay đề đã có.
Mật khẩu existing được giữ nguyên. Nếu code nội dung xung đột, seed rollback và
báo rõ; hãy tạo version mới qua quy trình migration nội dung đã duyệt.
Nếu username existing có vai trò khác, seed từ chối tự nâng quyền.

Chỉ khi bạn chủ động muốn đặt lại mật khẩu hai tài khoản demo:

```powershell
python -m app.cli seed --reset-demo-passwords
```

Thao tác này dùng giá trị SEED_* trong `.env` và thu hồi các phiên của hai tài khoản.
Seed bị chặn khi APP_ENV=production; ứng dụng không tự seed lúc khởi động.

**Tài khoản DEV, chỉ dùng local:**

| Tên đăng nhập | Mật khẩu ví dụ trong .env.example | Vai trò |
| --- | --- | --- |
| admin | Anhthuan33! | Quản trị |
| longnh | Anhthuan33! | Học sinh, lớp 4 |

Postgres local trong `.env.example` dùng user `postgres`, password `123456` đúng
cấu hình yêu cầu. Đổi toàn bộ thông tin demo và dùng DB role riêng trước khi đưa
lên Internet. Mật khẩu user lưu Argon2id; không có thông tin đăng nhập demo trong
frontend bundle, API response hay log.

Mở hai terminal (không cần Docker):

```powershell
# Terminal 1, tại backend/
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log

# Terminal 2, tại frontend/
npm ci
npm run dev
```

Mở **http://localhost:3000**. Swagger: http://localhost:8000/docs,
OpenAPI: http://localhost:8000/openapi.json, liveness `/health`, readiness `/ready`
kiểm tra kết nối DB và schema thật.

Browser luôn gọi `/api/v1` cùng origin; Next proxy đến backend. Nếu đổi cổng/host
backend, đặt `INTERNAL_API_URL` trong môi trường terminal Next hoặc
`frontend/.env.local` trước khi dev/build. Root `.env` được Compose và backend dùng;
Next không tự đọc root `.env`. Nếu đổi cổng frontend, cập nhật ALLOWED_ORIGINS.
Muốn dùng Swagger để login từ browser, thêm `http://localhost:8000` vào origins.

## Docker Compose với PostgreSQL trên host

Không có Postgres container trong compose mặc định; sử dụng DB đang có trên host.

```powershell
docker compose config --quiet
docker compose build
docker compose run --rm backend python -m alembic upgrade head
docker compose run --rm backend python -m app.cli seed
docker compose up -d
docker compose logs -f backend frontend
```

Backend container dùng `host.docker.internal`; Linux có `extra_hosts` host-gateway.
Override bằng `DOCKER_DB_HOST` nếu DB ở máy khác. DB cần lắng nghe địa chỉ phù hợp và
cho phép subnet Docker trong pg_hba.conf; không mở DB ra Internet.
Next trong container dùng `http://backend:8000`, browser vẫn dùng localhost:3000.
Cổng ứng dụng compose chỉ bind localhost. Dev có hot reload cho cả hai service.
Không tự chạy migrations/seed trong entrypoint.

`docker compose config --quiet` đã pass; build/run container chưa kiểm thử vì Docker
daemon của môi trường thực thi chưa chạy. Chạy local không phụ thuộc Docker.

## Kiểm thử và kiểm tra dữ liệu

```powershell
# backend/
../.venv/Scripts/python.exe -m ruff check app tests scripts
../.venv/Scripts/python.exe -m ruff format --check app tests scripts
../.venv/Scripts/python.exe -m pytest -q
../.venv/Scripts/python.exe scripts/smoke.py

# frontend/
npm run typecheck
npm run lint
npm test
npm run build
npm run format:check
npm audit
```

Không có TEST_DATABASE_URL: unit tests chạy; integration được ghi rõ là **skip**.
Để chạy đầy đủ, tạo **database test riêng**; tuyệt đối không trỏ tests vào DB thật:

```powershell
# Root, nếu database test CHƯA tồn tại; không chạy createdb lại nếu đã có:
createdb -h localhost -U postgres "viettree-education-test"
psql -h localhost -U postgres -d "viettree-education-test" -v ON_ERROR_STOP=1 -f database/viettree_education_schema.sql
Set-Location backend
$env:DB_NAME = 'viettree-education-test'
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed
# Tự cấu hình URL test theo tài khoản local của bạn:
$env:TEST_DATABASE_URL = 'postgresql+psycopg://postgres:123456@localhost:5432/viettree-education-test'
../.venv/Scripts/python.exe -m pytest -q
Remove-Item Env:DB_NAME
```

Integration từ chối database `viettree-education` và tên không chứa `test`. Phần lớn
tests dùng transaction + savepoint rollback. Hai tests concurrency dùng nhiều
connection và ghi user/kết quả thực **chỉ trong test DB**, không xóa/reset dữ liệu.
Mỗi test học sinh dùng user riêng để không phụ thuộc lịch sử longnh.

`scripts/smoke.py` dùng FastAPI TestClient nối PostgreSQL thật: admin → longnh → ba
môn → Toán → lưu đáp án → nộp → nộp lặp → kết quả → history → mastery → admin stats.
Mặc định rollback cuối phiên để longnh không có điểm demo giả. `--persist` ghi lượt
làm thật khi bạn chủ động yêu cầu. Rate limit vẫn được ghi độc lập. Chạy smoke cần
cài nhóm dependency dev.

Browser E2E với Chrome trên máy (hoặc cài Chrome qua Playwright nếu chưa có):

```powershell
# Backend terminal riêng, dùng DB test rồi chạy uvicorn như trên:
$env:DB_NAME = 'viettree-education-test'

# Frontend terminal, server Next đang chạy:
$env:E2E_STUDENT_PASSWORD = $env:SEED_STUDENT_PASSWORD
$env:E2E_ADMIN_PASSWORD = $env:SEED_ADMIN_PASSWORD
# Nếu SEED_* chưa có trong terminal, đặt bằng giá trị trong .env local.
npm run test:e2e
```

E2E ghi lịch sử vào test DB, có thể dùng hết 5 lượt của đề sau nhiều lần chạy. Không
reset DB thật để chạy lại; dùng test DB mới hoặc dữ liệu test chuyên dụng. Ảnh desktop/
mobile và trace khi fail nằm ở frontend/test-results (gitignored).

Để chạy lặp không hết lượt, tại terminal backend đã đặt DB_NAME=test:
`python scripts/create_test_student.py` tạo một học sinh test mới và chỉ in username.
Đặt username đó vào `E2E_STUDENT_USERNAME` ở terminal frontend; password vẫn từ
SEED_STUDENT_PASSWORD. Script từ chối database thật và không xóa học sinh cũ.

SQL đối chiếu seed: `database/seeds/verify.sql`. Kết quả mặc định mỗi môn: 4 chủ đề,
8 bài học, 32 published questions, 4 published assessments, mỗi đề 8 câu.
Tổng: **12 chủ đề, 24 bài học, 96 câu hỏi, 12 đề**, 12 kỹ năng; câu hỏi được gắn
lesson_questions, lesson_skills và question_skills đúng phiên bản.

## Phạm vi tính năng

Đã triển khai:

- Session server-side có thu hồi, cookie HttpOnly, CSRF/Origin, giới hạn login 10
  requests/phút/IP backend dùng chung giữa worker; login/logout/me và RBAC thật.
- Khung lớp 1–5, giữ toàn bộ môn trong schema; nội dung thực lớp 4 cho ba môn chính.
- Lesson blocks an toàn, tự luyện tập, assignment self idempotent, resume draft.
- Single choice, multiple choice, fill blank giữ dấu Việt, ordering; điểm theo item.
- Transaction nộp bài, khóa hàng, nộp lại trả kết quả cũ; giới hạn lượt/thời gian/IDOR.
- Lịch sử và dashboard DB thật, mastery/confidence/review/recommendations rule_v1;
  rebuild mastery và question/daily statistics: `python -m app.cli rebuild`.
- Admin dashboard, danh sách/tìm kiếm/phân trang học sinh và câu hỏi, sửa hồ sơ tối
  thiểu có audit; chương trình, chi tiết đáp án admin-only, đề/lượt làm, analytics.
- Responsive desktop/tablet/mobile, keyboard controls, reduced motion, loading/
  empty/error/retry; trang 403/404, chuyển login khi hết phiên.

Được để chờ mở rộng theo phạm vi prompt:

- Tạo/sửa/xóa/duyệt/xuất bản câu hỏi từ UI/API: **chỉ scaffold**, mọi nút ghi disabled.
- Teacher/guardian có RBAC và layout; chưa quản lý lớp hoặc xem dữ liệu học sinh.
  Quyền guardian_students phải được xác minh trước khi mở tính năng phụ huynh.
- Lớp 1/2/3/5 và bốn môn khác: khung chương trình, trạng thái Đang xây dựng.
- Không có public signup, editor, upload/media/audio, auto-grader tự luận, AI/ML,
  email, thông báo, Redis/MinIO hay dịch vụ trả phí. Bài luyện viết là hướng dẫn tại
  lesson, không có quy trình nộp tự luận/giáo viên chấm trong MVP.
- Chưa lập learning_plan_items tự động; lộ trình MVP thể hiện qua bài học, tiến độ và
  gợi ý. Các bảng kế hoạch gốc được ánh xạ và giữ nguyên cho giai đoạn tiếp theo.

## Cấu trúc và tài liệu

```text
frontend/src/app/         Public + student/admin/teacher/guardian routes
frontend/src/features/    Giao diện học tập và quản trị
frontend/src/lib/         API client và TypeScript contracts
frontend/e2e/             Browser tests desktop/mobile
backend/app/api.py        REST routes và RBAC
backend/app/core/          Cấu hình, session, CSRF, Argon2id
backend/app/db.py          SQLAlchemy reflection/kiểm tra schema
backend/app/services/      Làm bài và graders
backend/app/personalization/  rule_v1 và rebuild thống kê
backend/app/curriculum.py  Nội dung tự biên soạn
backend/app/seed.py        Seed an toàn, idempotent
backend/alembic/           Baseline + migration auth có rollback
backend/tests/            Unit, integration, concurrency
backend/scripts/smoke.py  Smoke transaction mặc định rollback
database/                 SQL gốc và SQL đối chiếu seed
docs/                     Kiến trúc, API, RBAC, personalization, trạng thái
```

Xem `docs/architecture.md`, `docs/api.md`, `docs/security.md`,
`docs/personalization.md`, `docs/IMPLEMENTATION_STATUS.md`.
Rollback chỉ migration bổ sung: `alembic downgrade 0001_baseline` sẽ xóa hai bảng
auth và làm mọi phiên hết hiệu lực; đây là thao tác chủ động của người vận hành,
không chạy tự động. Baseline downgrade không thay đổi bảng gốc.

## Vận hành và xử lý lỗi

- **Không nối được DB:** kiểm tra service, DB_HOST, cổng 5432, tên database có `-`,
  credentials và pg_hba.conf. `check-schema` và `/ready` tách lỗi hạ tầng khỏi UI.
- **Thiếu schema:** import SQL gốc nếu cần, rồi migration. Không dùng create_all hoặc
  schema thay thế; không xóa bảng cũ để hết lỗi.
- **CORS/403 CSRF:** mở localhost:3000 đúng ALLOWED_ORIGINS, không trộn localhost với
  127.0.0.1. Gửi X-CSRF-Token từ cookie viettree_csrf cho request ghi. Đăng nhập lại
  nếu cookie cũ. SameSite=Lax và Origin được kiểm tra cả login.
- **429 login:** đợi một phút. Khi proxy qua Next, nhiều browser cùng được nhìn như
  IP của proxy; production cần reverse proxy đáng tin và thiết kế rate limit theo
  client IP thực trước khi phục vụ nhiều người. Không tin X-Forwarded-For tùy ý.
- **Seed conflict:** seed giữ account/version/assessment cũ; kiểm tra code được báo,
  không chỉnh published version đang được tham chiếu bởi lịch sử.
- **Docker chưa chạy:** mở Docker Desktop; compose mặc định không chạy DB mới.
- **Đổi URL backend cho build production:** INTERNAL_API_URL của rewrite được chốt
  khi build; build lại khi đổi địa chỉ backend. `npm start` dùng build đã tạo.

Trước production: đặt APP_ENV=production, COOKIE_SECURE=true, HTTPS origins, mật khẩu
DB mạnh và DB role ít quyền; backend từ chối cấu hình production không đạt các điều
kiện này. Tắt seed demo, tách secrets khỏi image và không public Swagger nếu không
cần. Thiết lập HTTPS/reverse proxy, backup `pg_dump` mã hóa + diễn tập restore,
giám sát, chính sách giữ/xóa dữ liệu do đơn vị vận hành xác định, và cơ chế đồng ý
phụ huynh thích hợp. Demo không thay thế quy trình consent. Không có leaderboard
công khai hoặc chia sẻ kết quả giữa học sinh. Chỉ log method/status/duration và
loại lỗi; request validation không phản chiếu password/đáp án. Nội dung JSON được
React render thành text, không render HTML tùy ý.

Quy mô MVP: reflection lúc kết nối đầu, rebuild toàn thống kê sau mỗi submission
được tuần tự hóa bằng advisory lock để không mất cập nhật; phù hợp triển khai nhỏ.
Khi dữ liệu lớn cần incremental aggregates/job kiểm chứng, retention auth tables,
thêm pagination lịch sử (hiện tối đa 200 bản ghi), rà soát nội dung chuyên môn và
phát triển quy trình giáo viên. Không công bố đây là đánh giá năng lực chuẩn hóa.
