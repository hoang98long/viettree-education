# VietTree Education

Ứng dụng học tập tiếng Việt cho học sinh tiểu học: Next.js App Router + FastAPI +
PostgreSQL thật. Đăng nhập, đọc bài, lưu/resume bài làm, chấm điểm phía server,
lịch sử, năng lực và gợi ý ôn tập hoạt động end-to-end.

**AI Academy đã được tích hợp:** lớp 4 có **9 chủ đề / 36 tiết**, lớp 1/2/3/5
có 3 bài mẫu mỗi khối, tổng 48 bài và 315 SVG minh họa thật. Học nhiều bước,
game/lab, Prompt Builder, trợ giảng an toàn, xưởng sáng tạo, sản phẩm riêng,
giao bài/chấm rubric và CMS/media theo quyền. Dùng cùng tài khoản hiện có;
mặc định mô phỏng nội bộ, không cần dịch vụ AI trả phí.
Xem [hướng dẫn đầy đủ AI Academy](docs/ai-academy/README.md).

**Deploy lên VPS:** xem [hướng dẫn riêng](docs/deploy-vps.md) cho Ubuntu + Docker
Compose production, HTTPS, chuyển dữ liệu, tài khoản thật, backup và cập nhật.

**Kiểm tra trước triển khai:** [bản rà soát và các bước xác nhận](docs/production-readiness.md).
Admin có mục **Kiểm tra hệ thống** (`/admin/system`). Bộ production đã có trong
`docker-compose.production.yml` và `deploy/`; local tiếp tục dùng cấu hình development.
CLI `check-system` chỉ đọc, `cleanup-auth` mặc định dry-run. Head hiện tại
`0010_ai_academy`; nạp module lần đầu bằng `seed-ai-academy`.

**Chạy trên máy hiện tại:** xem [hướng dẫn local ngắn](docs/run-local.md) với hai
terminal PowerShell cho backend và frontend.

**Phiên đăng nhập:** mặc định 8 giờ; học sinh có thể chọn ghi nhớ 7 ngày trên máy
cá nhân. Biểu tượng VietTree đưa về dashboard khi đã đăng nhập; mở `/login` trong
phiên tự chuyển tiếp. Cache trạng thái giao diện 30 giây, quyền vẫn kiểm tra tại DB.
Xem [thiết kế và vận hành phiên](docs/session-management.md).

Khu vực học sinh dùng chữ mặc định 18 px, bài học 20 px, câu hỏi 22 px; các nút chính
có chiều cao tối thiểu 48 px. Tại **Hồ sơ của em → Chữ dễ đọc cho em**, chọn
**Chữ lớn hơn** để dùng chữ 22 px, bài học 24 px và câu hỏi 26 px. Lựa chọn được lưu
theo tài khoản, áp dụng trên cả điện thoại và máy tính khi đăng nhập lại.

Mục **Kế hoạch học** (`/student/learning-plan`) chuẩn bị tối đa 3 bài học chưa hoàn
thành và bài luyện tập theo chủ đề trong 7 ngày. Chọn môn rồi bấm **Chuẩn bị kế hoạch**.
Mỗi môn có một kế hoạch đang học; bấm lại sẽ mở kế hoạch đó. Dùng **Em đã đọc xong**
ở cuối bài học để lưu tiến độ đọc; nộp bài luyện tập sẽ tự cập nhật bước luyện tập.
Ngày trên kế hoạch là gợi ý, không khóa bài hay trừ điểm khi học muộn. Tiến độ đọc
không được dùng làm bằng chứng năng lực; năng lực vẫn dựa vào câu trả lời đã chấm.

**Giữ nguyên** `database/viettree_education_schema.sql` với 34 bảng gốc. Không reset,
DROP hay TRUNCATE database học tập. Database mặc định có tên **`viettree-education`**,
bao gồm dấu gạch ngang. Alembic bổ sung hai bảng auth và sáu bảng gói học, revision
`0009_guided_hints` thêm quyền gợi ý theo bước cho VIP; `0010_ai_academy`
thêm 29 bảng riêng và tái sử dụng tài khoản/lớp/media/consent. Migration tài khoản thêm vòng đời mật khẩu tạm và revision tài khoản,
giữ mật khẩu, phiên và lịch sử cũ. Bảng nháp bài học tiếp tục tách bản xuất bản.

## Quản trị tài khoản

Admin có **Quản trị tài khoản**: tạo/sửa, phân vai trò, khóa/mở, đặt lại mật khẩu,
thu hồi phiên và nhật ký. Mọi người dùng có **Bảo mật tài khoản** để tự đổi mật
khẩu, đăng xuất phiên khác. Mật khẩu tạm bắt buộc đổi trước khi sử dụng. Nâng cấp
chạy `alembic upgrade head` (head `0010_ai_academy`), khởi động lại server;
không cần seed/reset tài khoản. Xem [quản trị tài khoản](docs/account-management.md).

## Gói học Free / VIP

Mỗi lớp 3 hoặc 4 có 46 bài học và 34 đề miễn phí. VIP mở thêm 22 bài nâng cao, 22 đề thử thách mỗi lớp
và kế hoạch theo kỹ năng cần ôn (`plan_v2`). Cách chấm điểm và quyền
xem kết quả của chính học sinh giống nhau giữa hai gói.

- Học sinh: **Gói học của em** (`/student/membership`) và **Hồ sơ của em** hiển thị
  gói đang hiệu lực, thời hạn và quyền lợi. Bài bị khóa chỉ trả đoạn giới thiệu riêng.
- Admin: **Học sinh → Quản lý gói học** để cấp/gia hạn 30, 90 hoặc 365 ngày hoặc thu
  hồi; nhập lý do và xác nhận đúng tài khoản. Request lặp không cộng thời hạn lần hai.
- Admin: **Quyền nội dung** (`/admin/content-access`) cấu hình Free/VIP, mức nội dung
  và đoạn giới thiệu; thay đổi có audit.
- Học sinh VIP: **Kế hoạch học → Kiểu kế hoạch → Theo kỹ năng cần ôn**. Thiếu bằng
  chứng thì chọn bài nền tảng; chỉ chọn nâng cao khi kỹ năng đã vững.
- Phụ huynh: `/guardian/dashboard` xem gói của các trẻ có liên kết đã xác minh.

Hết hạn tự chuyển về quyền Free ở request tiếp theo; kết quả và tiến độ cũ được giữ.
Attempt VIP đã bắt đầu hợp lệ được hoàn tất tối đa 60 phút sau hết hạn, trong hạn
giao bài/thời lượng đề. Thu hồi VIP chặn ngay attempt đó, kể cả cấp lại VIP sau này.
Kế hoạch VIP hết quyền chuyển tạm dừng; học sinh vẫn tạo được kế hoạch cơ bản.

VIP có **Góc học VIP**, **Sổ tay ôn lỗi** với tự luyện không đổi điểm, **Báo cáo
7/30 ngày** và in/lưu PDF từ trình duyệt. Cách dùng, nội dung mới và nâng cấp:
[docs/vip-expansion.md](docs/vip-expansion.md).

VIP hiện do admin cấp, chưa tích hợp thanh toán hoặc báo cáo riêng trong tài khoản phụ huynh. Bộ nội
dung nâng cao được seed cho development; cần giáo viên rà soát trước sử dụng thực tế.
Seed thường không tự nâng cấp học sinh. Lệnh riêng `seed-demo-learners` tạo bốn
tài khoản demo theo yêu cầu, gồm hai Free và hai VIP 90 ngày.

## Ngân hàng câu hỏi, bài tập và tài khoản demo

**Lớp 3** đã có 68 bài/384 câu/56 đề, bằng quy mô lớp 4 cho từng môn: Toán
25/142/21, Tiếng Việt 23/130/19, Tiếng Anh 20/112/16. Mỗi bài lớp 3 có 1 gợi ý
định hướng cho Free, 3 gợi ý theo bước cho VIP; backend lọc gợi ý theo quyền.
Admin chọn **Lớp 3** trong quản trị học liệu và hồ sơ học sinh. Xem nội dung,
nguồn chương trình và cách nạp riêng tại [học liệu lớp 3](docs/grade3-curriculum.md).

Đợt mở rộng chương trình lớp 4 thêm **20 bài/120 câu/20 đề**: Toán, Tiếng Việt,
Tiếng Anh, có bài nền tảng Free và bài tư duy VIP. Học sinh dùng **Góc tư duy**;
admin xem **Chương trình → Lớp 4 → Theo dõi học liệu**. Thêm SVG góc/biểu đồ và
nhóm bài tư duy trong editor. Căn cứ chương trình, giới hạn và cách nạp riêng:
[docs/grade4-curriculum.md](docs/grade4-curriculum.md).

Admin có **Quản lý bài học**: tạo/biên soạn, xem trước, lưu nháp, duyệt và xuất bản;
kiểm tra revision tránh ghi đè, lưu lịch sử thao tác. Học sinh có mục tiêu, mục lục,
minh họa SVG, gợi ý từng bước, câu hỏi tự suy ngẫm và gợi ý bài tiếp theo có kiểm tra
quyền. Chi tiết: [docs/lesson-studio.md](docs/lesson-studio.md).

Admin vào **Ngân hàng câu hỏi → Tạo câu hỏi** để soạn bốn loại câu, đặt đáp án/lời
giải và xem trước. Lưu nháp, duyệt nội dung rồi xuất bản. Câu đã xuất bản được
sửa qua phiên bản mới; đề và bài làm cũ vẫn dùng đáp án cũ.

Vào **Tạo bài tập** để chọn câu đã xuất bản, sắp thứ tự, đặt điểm, thời gian,
Free/VIP; duyệt/xuất bản và giao cho tối đa 50 học sinh. Học sinh dùng **Thư viện
luyện tập** để tìm theo môn, gói, loại và từ khóa. Nội dung VIP được bảo vệ tại API.

Sau migration và seed, tạo thêm tài khoản bằng `python -m app.cli seed-demo-learners`
trong backend (chỉ development):

| Tài khoản          | Gói                           |
| ------------------ | ----------------------------- |
| free4_01, free4_02 | Free, lớp 4                   |
| vip4_01, vip4_02   | VIP 90 ngày từ lúc tạo, lớp 4 |

Mật khẩu là `SEED_STUDENT_PASSWORD` trong `.env`. Chạy lại không đổi mật khẩu hoặc
gia hạn/cấp lại VIP. Thiết kế, luồng sử dụng và đề xuất nâng cấp tiếp:
[docs/authoring-design.md](docs/authoring-design.md).

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

| Biến                                        | Cách sử dụng                                                                          |
| ------------------------------------------- | ------------------------------------------------------------------------------------- |
| DB_HOST                                     | `localhost` khi chạy backend trên host                                                |
| DB_PORT / DB_NAME                           | `5432` / `viettree-education`                                                         |
| DB_USER / DB_PASSWORD                       | Cấu hình local do bạn cung cấp trong `.env`                                           |
| ALLOWED_ORIGINS                             | Danh sách origin chính xác, phân cách bằng dấu phẩy; mặc định `http://localhost:3000` |
| COOKIE_SECURE                               | `false` cho HTTP local, `true` khi triển khai HTTPS                                   |
| SESSION_HOURS                               | Thời hạn tuyệt đối của phiên, mặc định 8 giờ                                          |
| REMEMBER_SESSION_DAYS                       | Phiên ghi nhớ cho học sinh không có role admin/teacher, mặc định 7 ngày               |
| SEED_ADMIN_PASSWORD / SEED_STUDENT_PASSWORD | Chỉ dùng khi chủ động seed demo                                                       |
| INTERNAL_API_URL                            | Next server nối backend; mặc định `http://localhost:8000`                             |

Kiểm tra schema và áp dụng migration:

```powershell
Set-Location backend
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
../.venv/Scripts/python.exe -m app.cli seed
../.venv/Scripts/python.exe -m app.cli verify-seed
../.venv/Scripts/python.exe -m app.cli verify-seed --grade 3
```

`alembic upgrade head` kiểm tra đủ bảng/cột gốc rồi thêm auth_sessions,
auth_login_limits, sáu bảng gói học và bảng quản lý phiên bản alembic_version. Không tạo schema học
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

| Tên đăng nhập | Mật khẩu ví dụ trong .env.example | Vai trò         |
| ------------- | --------------------------------- | --------------- |
| admin         | Anhthuan33!                       | Quản trị        |
| longnh        | Anhthuan33!                       | Học sinh, lớp 4 |

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
tests dùng transaction + savepoint rollback. Các tests concurrency dùng nhiều
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
$env:DB_NAME = 'viettree-education-test'
$env:E2E_STUDENT_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_VIP_STUDENT_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_VIP_MOBILE_STUDENT_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_AUTHORING_STUDENT_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_VIP_TOOLS_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_VIP_TOOLS_MOBILE_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_LESSON_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_LESSON_MOBILE_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_CURRICULUM_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_CURRICULUM_MOBILE_USERNAME = & '../.venv/Scripts/python.exe' '../backend/scripts/create_test_student.py'
$env:E2E_STUDENT_PASSWORD = $env:SEED_STUDENT_PASSWORD
$env:E2E_ADMIN_PASSWORD = $env:SEED_ADMIN_PASSWORD
# Nếu SEED_* chưa có trong terminal, đặt bằng giá trị trong .env local.
npm run test:e2e
```

E2E ghi lịch sử vào test DB, có thể dùng hết 5 lượt của đề sau nhiều lần chạy. Không
reset DB thật để chạy lại; dùng test DB mới hoặc dữ liệu test chuyên dụng. Ảnh desktop/
mobile và trace khi fail nằm ở frontend/test-results (gitignored).
Chạy pytest và browser E2E tuần tự khi dùng chung một test DB để tránh khóa giữa
transaction rollback dài của pytest và request ghi của browser. Helper E2E tôn
trọng Retry-After khi nhiều lượt đăng nhập dùng chung IP proxy.

Để chạy lặp không hết lượt, tại terminal backend đã đặt DB_NAME=test:
`python scripts/create_test_student.py` tạo một học sinh test mới và chỉ in username.
Đặt username đó vào `E2E_STUDENT_USERNAME` ở terminal frontend; password vẫn từ
SEED_STUDENT_PASSWORD. Script từ chối database thật và không xóa học sinh cũ.

SQL đối chiếu seed: `database/seeds/verify.sql`. Mỗi bộ mẫu lớp 3 hoặc lớp 4: Toán có
25 bài/142 câu/21 đề; Tiếng Việt 23/130/19; Tiếng Anh 20/112/16. Đề có 6 hoặc 8 câu.
Tổng mỗi lớp: **21 chủ đề, 68 bài học, 384 câu hỏi, 56 đề**, 21 kỹ năng; hai lớp có 136 bài/768 câu/112 đề. Câu hỏi được gắn
lesson_questions, lesson_skills và question_skills đúng phiên bản.

## Phạm vi tính năng

Đã triển khai:

- Session server-side có thu hồi, cookie HttpOnly, CSRF/Origin, giới hạn login 10
  requests/phút/IP backend dùng chung giữa worker; login/logout/me và RBAC thật.
- Khung lớp 1–5, giữ toàn bộ môn trong schema; nội dung thực lớp 3 và 4 cho ba môn chính.
- Lesson blocks an toàn, tự luyện tập, assignment self idempotent, resume draft.
- Single choice, multiple choice, fill blank giữ dấu Việt, ordering; điểm theo item.
- Transaction nộp bài, khóa hàng, nộp lại trả kết quả cũ; giới hạn lượt/thời gian/IDOR.
- Lịch sử và dashboard DB thật, mastery/confidence/review/recommendations rule_v1;
  rebuild mastery và question/daily statistics: `python -m app.cli rebuild`.
- Admin dashboard, danh sách/tìm kiếm/phân trang học sinh và câu hỏi, sửa hồ sơ tối
  thiểu có audit; chương trình, chi tiết đáp án admin-only, đề/lượt làm, analytics.
- Admin biên soạn câu hỏi và ghép đề, nháp/duyệt/xuất bản/lưu trữ, tạo phiên bản
  và sao chép đề; chống ghi đè bằng revision, giao bài hàng loạt theo lớp/gói.
- Thư viện luyện tập học sinh lọc theo môn, Free/VIP, loại đề và từ khóa.
- Responsive desktop/tablet/mobile, keyboard controls, reduced motion, loading/
  empty/error/retry; trang 403/404, chuyển login khi hết phiên.

Được để chờ mở rộng theo phạm vi prompt:

- Teacher có RBAC/layout; quản lý lớp và giao bài chưa mở. Guardian chỉ xem gói
  học của trẻ có guardian_students.verified_at; báo cáo trong tài khoản guardian chưa mở.
  Học sinh VIP đã có báo cáo riêng và in/lưu PDF từ trình duyệt.
- Lớp 1/2/5 và bốn môn khác: khung chương trình, trạng thái Đang xây dựng.
- Chưa có public signup, upload/media/audio, auto-grader tự luận, AI/ML,
  email, thông báo, Redis/MinIO hay dịch vụ trả phí. Bài luyện viết là hướng dẫn tại
  lesson, không có quy trình nộp tự luận/giáo viên chấm trong MVP.
- Kế hoạch cơ bản `plan_v1` và kế hoạch VIP `plan_v2` đã hoạt động. Gợi ý luyện tập
  `rule_v1` vẫn hoạt động độc lập và chỉ chọn đề đủ quyền gói hiện tại.
  Khi nội dung hoặc lượt làm bài thay đổi sau lúc lập kế hoạch, quy tắc truy cập
  và giới hạn lượt vẫn được API thực thi; kế hoạch chưa tự thay thế bước bị đóng.

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
backend/alembic/           Baseline + migrations auth/Free-VIP
backend/tests/            Unit, integration, concurrency
backend/scripts/smoke.py  Smoke transaction mặc định rollback
database/                 SQL gốc và SQL đối chiếu seed
docs/                     Kiến trúc, API, RBAC, personalization, trạng thái
```

Xem `docs/architecture.md`, `docs/api.md`, `docs/security.md`,
`docs/personalization.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/roadmap.md`.
Thiết kế gói học miễn phí/VIP: [docs/free-vip-design.md](docs/free-vip-design.md)
(thiết kế và trạng thái triển khai; thanh toán và báo cáo trong tài khoản phụ huynh là giai đoạn sau).
Downgrade từ head về `0002_auth_sessions` sẽ xóa dữ liệu sáu bảng gói học. Cần
backup và chuyển về phiên bản ứng dụng tương thích trước; không downgrade tự động.
Downgrade về `0001_baseline` còn xóa auth và làm mọi phiên hết hiệu lực. Baseline
downgrade không thay đổi bảng học tập gốc.

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
