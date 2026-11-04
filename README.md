# VietTree Education

Ứng dụng học tập cho học sinh tiểu học Việt Nam, dùng Next.js, FastAPI và
PostgreSQL. Học sinh đọc bài có minh họa, nhận gợi ý, luyện tập có tự lưu, xem
kết quả và học tiếp phần đang dở. Có Free/VIP, lớp học, giao bài, tuyên dương,
quản trị tài khoản và ngân hàng câu hỏi.

**Next.js đã nâng lên 16.4.5:** package và lockfile được ghim cùng phiên bản;
khi cập nhật máy khác, chạy `npm ci` và build lại frontend.
[Chi tiết nâng cấp và kiểm thử](docs/audits/nextjs-16.4.5-upgrade-2026-11-04.md).

**Rà soát học liệu 04/11:** đã chỉnh 232 bài cũ, cập nhật 200 phiên bản AI
Academy, bổ sung 915 hình khớp nội dung; giữ tài khoản, VIP và kết quả học.
[Các thay đổi và cách cập nhật](docs/content-editorial-review-2026-11-04.md).

**Cập nhật 04/11/2026:** thêm **30 bài / 120 câu hỏi / 30 đề luyện**, chia đều
cho lớp 1–5 và ba môn Toán, Tiếng Việt, Tiếng Anh; mỗi môn có bài Free và VIP.
Hai thư viện có bộ lọc theo bộ học liệu. Thêm ba tranh SVG; gom hàm tạo bài
trùng, tách bộ lọc dùng chung. [Nội dung, kiểm thử và cách cập nhật](docs/discovery-and-library-2026-11-04.md).

| Học liệu đang xuất bản               | Mỗi khối lớp      | Tổng lớp 1–5       |
| ------------------------------------ | ----------------- | ------------------ |
| Ba môn: bài học / câu hỏi / đề luyện | 89 / 474 / 77     | 445 / 2.370 / 385  |
| AI Academy                           | 40 bài, 11 chủ đề | 200 bài, 2.617 SVG |

Số ba môn gồm bộ nền tảng và đủ năm bộ bổ sung; chưa gồm học liệu do admin
biên soạn riêng. AI Academy ưu tiên lý thuyết, tranh và hoạt động nội bộ;
`AI_TRAINING_ONLY=true` chặn gọi mô hình. [Hướng dẫn AI Academy](docs/ai-academy/README.md).

- [Chạy local bằng hai terminal PowerShell](docs/run-local.md).
- [Deploy VPS tại Nhật: 4 vCPU / RAM 8 GB / SSD 100 GB](docs/deploy-vps-japan.md) · [hướng dẫn VPS đầy đủ](docs/deploy-vps.md).
- [Kiến trúc và cách mở rộng](docs/architecture.md) · [API](docs/api.md).
- [Kiểm tra trước mở web](docs/pre-deployment-review-2026-10-20.md) · [các mốc nâng cấp trước](docs/release-notes.md).
- [Tài khoản demo local](docs/demo-accounts.md) · [Free/VIP](docs/free-vip-design.md).

**Cỡ chữ:** nút **Cỡ chữ** hoặc **Hồ sơ của em** có ba lựa chọn, gồm **Chữ gọn hơn**
cho điện thoại; lưu riêng theo loại thiết bị trong tài khoản. [Chi tiết](docs/reading-preferences.md).
Phiên đăng nhập mặc định 8 giờ, ghi nhớ 7 ngày trên máy cá nhân; biểu tượng
VietTree về dashboard khi đang đăng nhập. [Quản lý phiên](docs/session-management.md).

Database mặc định **`viettree-education`**. Giữ nguyên SQL gốc, tài khoản,
phiên và lịch sử; migration hiện tại **`0012_lesson_bookmarks`**. Bản 04/11
không cần migration mới. Không reset, DROP hay TRUNCATE dữ liệu học tập.

## Quản trị tài khoản

Admin có **Quản trị tài khoản**: tạo/sửa, phân vai trò, khóa/mở, đặt lại mật khẩu,
thu hồi phiên và nhật ký. Mọi người dùng có **Bảo mật tài khoản** để tự đổi mật
khẩu, đăng xuất phiên khác. Mật khẩu tạm bắt buộc đổi trước khi sử dụng. Nâng cấp
chạy `alembic upgrade head` (head `0012_lesson_bookmarks`), khởi động lại server;
không cần seed/reset tài khoản. Xem [quản trị tài khoản](docs/account-management.md).

## Gói học Free / VIP

Bộ nền tảng mỗi khối 1–5 có 46 bài học và 34 đề miễn phí. VIP mở thêm 22 bài vận dụng, 22 đề thử thách mỗi khối
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

AI Academy kiểm tra quyền tại mỗi bước, không có thời gian gia hạn hoàn tất sau
hết VIP. Thu hồi chặn ngay bài/lab/xưởng VIP, giữ tiến độ, kết quả và sản phẩm
của chính em. Request cấp/gia hạn cũ lặp lại trả trạng thái hiện tại, không báo
VIP đã bị thu hồi còn hiệu lực. Gia hạn gói đã thu hồi trả 409; dùng cấp mới.
Chi tiết: [đào tạo AI Free/VIP](docs/ai-training-vip.md).

Trang **Gói học của em** đã có giá tham khảo và sale có ngày hết hạn:
30 ngày **99.000đ → 79.000đ**, 90 ngày **269.000đ → 219.000đ**,
365 ngày **899.000đ → 699.000đ**. Ưu đãi giới thiệu đến hết 12/11/2026,
giờ Việt Nam. Admin chỉnh tại `/admin/vip-pricing`; chưa có thanh toán tự động.
Xem [khảo sát giá Việt Nam và điều kiện ưu đãi](docs/vip-pricing-research.md).

VIP có **Góc học VIP**, **Sổ tay ôn lỗi** với tự luyện không đổi điểm, **Báo cáo
7/30 ngày** và in/lưu PDF từ trình duyệt. Cách dùng, nội dung mới và nâng cấp:
[docs/vip-expansion.md](docs/vip-expansion.md).

VIP hiện do admin cấp, chưa tích hợp thanh toán hoặc báo cáo riêng trong tài khoản phụ huynh. Bộ nội
dung nâng cao được seed cho development; cần giáo viên rà soát trước sử dụng thực tế.
Seed thường không tự nâng cấp học sinh. Lệnh riêng `seed-demo-learners` tạo
hai Free và hai VIP 90 ngày mỗi khối 1–5; `--grades` chọn khối. Chạy lại giữ
nguyên mật khẩu, hồ sơ và gói cũ.

## Lớp học, giao bài và thành tích

Admin mở **Lớp và giao bài** (`/admin/classes`) để tạo/sửa lớp, phân giáo viên,
ghi danh hoặc chuyển học sinh ra. Học sinh tự do vẫn tự học và nhận bài riêng.
Giáo viên mở `/teacher/classes` để giao bài cá nhân/cả lớp, xem kết quả và
tuyên dương top 3; chỉ được quản lý lớp mình phụ trách.

Học sinh mở **Lớp và thành tích** (`/student/classroom`) để xem bài được giao,
kết quả theo Toán/Tiếng Việt/Tiếng Anh/AI/sản phẩm AI. Xếp thứ tự theo kết quả
tốt nhất mỗi bài, trung bình thang 100; VIP không cộng điểm thưởng. Bảng riêng
trong lớp dùng biệt danh, có tuần/tháng và snapshot tuyên dương top 3.
Xem [thiết kế và cách sử dụng](docs/classes-achievements.md).

## Ngân hàng câu hỏi, bài tập và tài khoản demo

**Lớp 1 và 2** có quy mô từng môn bằng lớp 3–4, nội dung phù hợp trẻ mới học.
Máy hiện tại đã nạp sau backup. Máy khác dùng `seed-grade1-content` và
`seed-grade2-content`; lệnh chỉ thêm học liệu, không tạo/reset tài khoản hoặc
cấp VIP. Admin tạo học sinh với khối đúng; danh mục mặc định theo hồ sơ.
Kho năm khối có tổng **340 bài / 1920 câu / 280 đề**, tách học liệu AI Academy.

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

| Khối | Free               | VIP 90 ngày khi tạo mới |
| ---- | ------------------ | ----------------------- |
| 1    | free1_01, free1_02 | vip1_01, vip1_02        |
| 2    | free2_01, free2_02 | vip2_01, vip2_02        |
| 3    | free3_01, free3_02 | vip3_01, vip3_02        |
| 4    | free4_01, free4_02 | vip4_01, vip4_02        |

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

Lệnh `seed` trên dành cho nền tảng/demo local. Để có số lượng học liệu hiện tại
trong bảng đầu README, [nạp đủ năm bộ bổ sung](docs/discovery-and-library-2026-11-04.md#cập-nhật-máy-khác-và-vps)
sau khi nền tảng đã có; các lệnh bổ sung không tạo/reset tài khoản.

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

| Tên đăng nhập | Mật khẩu ví dụ trong .env.example    | Vai trò         |
| ------------- | ------------------------------------ | --------------- |
| admin         | `SEED_ADMIN_PASSWORD` trong `.env`   | Quản trị        |
| longnh        | `SEED_STUDENT_PASSWORD` trong `.env` | Học sinh, lớp 4 |

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
- Học liệu ba môn chính lớp 1–5; các môn khác giữ khung trong schema.
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
- Thư viện bài học tìm không dấu, lọc môn/gói/tiến độ; minh họa hình học lớp 5.
- Responsive desktop/tablet/mobile, keyboard controls, reduced motion, loading/
  empty/error/retry; trang 403/404, chuyển login khi hết phiên.

Các phần còn tiếp tục mở rộng:

- Báo cáo học tập riêng trong tài khoản guardian cần mở rộng; chỉ truy cập trẻ
  có liên kết đã xác minh. Teacher đã quản lý lớp/giao bài; học sinh VIP có báo
  cáo riêng và in/lưu PDF.
- Bốn môn khác ngoài Toán/Tiếng Việt/Tiếng Anh mới có khung chương trình.
- Chưa có public signup, audio học bài, chấm tự động bài văn, email/thông báo
  hay thanh toán tự động. Bài văn LMS là hướng dẫn để thực hành với người lớn.
  AI Academy đã có media, bài thực hành và giáo viên chấm rubric sản phẩm;
  mặc định `AI_TRAINING_ONLY=true`, học lý thuyết/bài tập nội bộ.
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
backend/app/api/routes/   REST routes và RBAC theo chức năng
backend/app/schemas/      Request/response contracts theo chức năng
backend/app/core/          Cấu hình, session, CSRF, Argon2id
backend/app/db.py          SQLAlchemy reflection/kiểm tra schema
backend/app/services/      Làm bài và graders
backend/app/personalization/  rule_v1 và rebuild thống kê
backend/app/curriculum/   Học liệu theo khối/môn, registry và seed nội dung
backend/app/fixtures/     Tài khoản demo và seed development riêng
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
