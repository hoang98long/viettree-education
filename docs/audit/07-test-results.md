# 07 · Lệnh và kết quả kiểm thử · 11/11/2026

Ghi chú sau kiểm toán: theo yêu cầu dọn môi trường, container/image audit và
122 mục tạm cũng đã dọn sau xác nhận của người dùng; số liệu JSON và regression tests
trong source vẫn giữ. Hai volume Docker test đã được xóa sau phê duyệt; database ứng dụng giữ nguyên.

Windows/Python 3.13.9, Node 22.14.0/npm 10.9.2; PostgreSQL 18.
Next.js 16.4.5. Docker Engine 29.9.3; backend image Python 3.12/Linux.
Database riêng, dữ liệu giả, không gửi email/model AI/production.
Số liệu đọc máy: [test-summary.json](evidence/test-summary.json).
Log/trace/XML thô ở `.tools/audit-20261111-*`, `.tools/audit-docker-results`,
được giữ local vì trace có thể chứa cookie/fixture. Không đưa secrets vào Git.

## Baseline thực chạy, giữ nguyên FAIL

| Lệnh / phạm vi                                                       | Exit | Kết quả                                                      |
| -------------------------------------------------------------------- | ---: | ------------------------------------------------------------ |
| `python -m pip check` / venv gốc                                     |    0 | Dependency ban đầu không bị hỏng                             |
| `pytest -m "not integration" -q -rs` / backend                       |    0 | 895 passed, 9 skipped, 239 deselected                        |
| `npm run test` / frontend                                            |    0 | 93 passed / 23 files                                         |
| `npm run lint`, `npm run typecheck`, `npm run format:check`          |    0 | Baseline đạt                                                 |
| `pytest -q -rs` / Windows DB giả                                     |    1 | 28 failed, 1.161 passed; 30m41,64s                           |
| `pytest -q -rs` / Linux image + PG18 giả                             |    1 | 21 failed, 1.187 passed, 2 skipped; 32m39,19s                |
| `npm audit --json`                                                   |    1 | 1 high / 7 moderate, toàn bộ dev tree; production baseline 0 |
| `pip_audit -r backend/requirements-lock.txt --disable-pip --no-deps` |    1 | Pillow/Certifi, 41 advisory records có ID trùng              |
| `node e2e/run-audit.mjs e2e --reporter=line,json` / browser đầy đủ   |    1 | 174 passed, 5 failed, 3 skipped / 182; 17,7 phút             |

Chín unit skip là test DB thiếu marker (AUD-07), không phải lỗi Bash.
Windows full: 8 failure do `APP_ENV=test` trong khi demo fixture yêu cầu
`development`; đã sửa test context, giữ guard production. 18 failure là
assertion 68 bài trên DB có đủ pack/89 bài, đã sửa exact source/pack contracts,
không nới thành `>=`. Hai failure thật là SVG VIP lịch sử trả 200 cho Free.
Linux xác nhận 18 inventory + 2 media; một failure thiếu mount file example
trong QA image. Hai skip do không có Docker CLI trong image; 18 deploy tests
được chạy trên host với Git Bash/Docker Compose và đạt.

Năm browser failure: hai selector asset cũ `color-v3`, một operations chờ
sai response, một picture-choice chưa chờ POST lưu thành công, một GET
subjects qua Next local timeout 30s/ECONNRESET (AUD-22). Ba skip: hai HTTPS
case trên HTTP base và một case mobile trùng kiểm ba loại thiết bị đã chạy
ở desktop. Không dùng skip này như bằng chứng HTTPS đã được kiểm.

## Sau sửa: kết quả đạt và giới hạn

| Lệnh / phạm vi                                                                                                 | Exit | Kết quả / artifact                                                                |
| -------------------------------------------------------------------------------------------------------------- | ---: | --------------------------------------------------------------------------------- |
| `pytest -m "not integration" --cov=app --cov-report=json --cov-report=term -q -rs` / venv audit đúng lock mới  |    0 | **992 passed, 264 deselected**, 37,48s; coverage unit **3.662/7.095 = 51,61%**    |
| `pytest -q -rs -rf -p no:cacheprovider --junitxml=/tmp/audit-results.xml <regression-files>` / Linux           |    0 | **649 passed**, 0 fail/skip, 16m22,92s; `pytest-final.xml`                        |
| `pytest -q -rf -rs -p no:cacheprovider --junitxml=/tmp/progress-tests.xml <progress-files>` / image tối ưu mới |    0 | **72 passed**, 0 fail/skip, 7m13,23s; `progress-tests.xml`                        |
| `npm run test`                                                                                                 |    0 | **103 passed / 26 files**; `.tools/audit-20261111-frontend-final.log`             |
| Browser `audit-accessibility.spec.ts`                                                                          |    0 | **6 passed**, 57,2s; axe mẫu, 320/768, native focus/busy Escape                   |
| Browser membership/operations/picture-choices/visual-learning                                                  |    0 | **12 passed**, 1,3 phút; `browser-rerun-final.log/.json`                          |
| `node e2e/run-audit.mjs --reporter=line,json` / Windows cuối                                                   |    1 | **33 passed, 1 failed**, 3,3 phút; `smoke-first.log/.json`                        |
| `ruff check backend`, `ruff format --check backend`                                                            |    0 | All checks passed; 242 Python files formatted                                     |
| Python locked dependency audit sau vá                                                                          |    0 | Không vulnerable dependency do công cụ báo                                        |
| `npm audit --json` sau vá                                                                                      |    0 | 0 advisory, gồm dev                                                               |
| Custom `pg_dump`/restore, schema và runtime-role smoke                                                         |    0 | 83 bảng giả khớp row hash; runtime không superuser/CREATE                         |
| HTTPX qua Caddy/private CA, verify certificate bật                                                             |    0 | 19 checks đạt: cookie/CSRF/role/media/private cache/logout; `https-security.json` |
| `load_probe` HTTPS 10/25/50 qua Caddy                                                                          |    0 | Toàn bộ request 200, thống kê nhất quán; số đo bên dưới                           |
| Snapshot nguồn REPEATABLE READ READ ONLY                                                                       |    0 | **83/83 bảng không thay đổi hash**; `source-preservation.json`                    |

Không cộng các lượt trùng thành tổng test độc lập. Full suite baseline chưa
được chạy lại toàn bộ trong một lượt sau mọi patch cuối: 649 regression tập
trung covers các failure/nội dung/AI/quyền, 72 covers patch progress cuối.
Unit coverage không bao gồm số đo coverage của integration/E2E; chưa đo
baseline coverage nên không báo mức tăng.

`regression-files`: audit_academy_content, audit_release_uploads,
audit_security_grading, audit_media_access, early_primary, grade3, grade5, visual_learning,
classrooms, structure_accounts, authoring, release_readiness và academy (các tên `tests/test_*.py`; danh sách thật trong XML).
`progress-files`: audit_lesson_visits, learning, memberships, concurrency,
bookmarks, lesson_studio, resume_learning và
`test_deployment_profile.py::test_unknown_profile_fails_before_using_docker`.

### Gate qua cấu hình production local

`node e2e/run-audit.mjs --reporter=line,json` trên **Caddy HTTPS → Linux
backend/PostgreSQL**, frontend image production: **34 passed / 3,7 phút,
exit 0**, không skip. Có session, autosave/network failure simulation,
authoring, 20 editorial cases lớp 1–5 Free/VIP và sáu accessibility cases.
`node e2e/run-audit.mjs e2e/production-network.spec.ts --reporter=line,json`:
**4 passed / 15,9s, exit 0**, hai device, gồm cookie/CSRF và network latency.
Artifacts `https-browser.log/.json`, `https-network-browser.log/.json`.

Chrome dùng ngoại lệ private CA **chỉ localhost**; 19 HTTPX checks riêng
vẫn bật verify CA. Không sửa trust store hoặc tắt verify cho public domain.
34+4 là hai phạm vi riêng, không phải full 182 cuối một lượt, không xóa
kết quả Windows 33/34 hoặc tự kết luận AUD-22 đã sửa.

Final `npm run build` exit 0, đã kiểm routes manifest dùng
`http://127.0.0.1:8000`, không còn port test 8201. `npm run typecheck`,
`npm run lint` exit 0. Lint phát hiện thiếu import Node `process` ở runner
mới, đã thêm import tường minh và chạy lại đạt; không tắt rule. Generated
`next-env.d.ts` được trả về bản gốc sau build. `npm run format:check` và Git `diff --check` cuối exit 0;
chín báo cáo có 0 broken local links. Evidence tại `evidence/test-summary.json`.

### Lỗi local còn mở: AUD-22

Full browser có một response `/subjects` HTTP 500 sau **30.024ms**, không
`X-Request-ID`; Next log proxy ECONNRESET, backend không có 5xx tương ứng.
Probe read-only sau đó không có blocker/idle transaction; 30 truy vấn subjects
SQL p50 0,369ms/p95 0,533ms/max 6,98ms. 40 authenticated GET direct/proxy
đều 200; không chứng minh tình trạng DB tại đúng thời điểm lỗi.

Windows smoke cuối có thêm một failure desktop lớp 4 Free: sau login 200
79,68ms, dashboard/auth-me vẫn pending khi locator hết 15s; snapshot chỉ
“Đang tải”. Giữ trace tại `smoke-first-artifacts`. Đây là tín hiệu transport
chưa giải thích đầy đủ, không được gọi smoke green hoặc tăng timeout để né.
Probe thêm cùng cookie giả: 32 GET direct/proxy đều 200, max239ms; năm
hard-navigation Chrome hiện thư viện dưới5s. Dashboard request bị bỏ khi
đổi document cũng có status−1 trong flow thành công, nên riêng status−1
không chứng minh DB treo; auth/me mới pending vẫn chưa giải thích được.
API đã có timeout/retry UI; không hạ bảo mật/đổi DB để xử lý suy đoán.
Default INTERNAL_API_URL dùng IPv4 giúp tránh fallback localhost Windows
(probe kết nối mới khoảng 2.050ms), **không được coi là sửa lỗi 30s**.
Production Caddy chuyển API trực tiếp tới Linux backend; vẫn cần staging.

## Hiệu năng có đo

Workload riêng, 25 Free/25 VIP, login 50 tài khoản tuần tự; sau đó tăng
10/25/50 người, đọc dashboard/catalog/lesson/skills, ghi visit, lưu mọi đáp án,
nộp lặp và đọc kết quả. Không có think time. Backend hai worker, CPU cap 2,
RAM cap 768MiB; frontend CPU 2/RAM 768MiB, PG RAM 768MiB, Caddy 128MiB.
Host Docker báo 12 logical CPU; PG không bị giới hạn CPU riêng. Đây không
phải mô phỏng đầy đủ VPS 4-core hay mạng Nhật. CA được verify bằng HTTPX.

| Concurrent | Requests | p50 trước → sau (ms) | p95 trước → sau (ms) | RPS sau | HTTP lỗi sau |
| ---------: | -------: | -------------------: | -------------------: | ------: | -----------: |
|         10 |      180 |      207,05 → 159,83 |      712,08 → 822,62 |   32,37 |            0 |
|         25 |      445 |      619,78 → 609,83 |  1.780,81 → 1.478,01 |   34,17 |            0 |
|         50 |      900 |  1.123,34 → 1.239,79 |  3.478,12 → 2.753,40 |   33,20 |            0 |

Hai lần đo trước/sau, không lặp thống kê nhiều lần: không suy ra quan hệ
nhân quả chắc chắn hay mọi endpoint đều nhanh hơn. Tại 50 người, visit p95
3.692,27 → 2.474,08ms; dashboard vẫn khoảng **4.378,70ms**, p99 tổng sau
**4.319,45ms**, max 4.973,48ms. Còn dư địa profile, chưa đạt SLO do chủ sản
phẩm chốt. Cả hai lượt: 85 graded attempts = daily 85, question-statistics
mismatch 0. Tổng mỗi lượt 1.525 learning requests + 50 login, tất cả 200.

Login sau: p50 109,96ms/p95 136,86ms, 50/50 thành công trong 5,74s;
**không đo 50 lần Argon2 đồng thời**. CPU backend sampled peak **205,7%**
ở cap hai core, RAM khoảng **263,50MiB**; DB khoảng 198,50MiB, frontend
35,21MiB, Caddy 42,74MiB. Sample khoảng 1–3s, không phải tuyệt đối max.
Frontend không tải page trong API workload này, nên RAM đó không đại diện
SSR burst. Evidence: [load](evidence/https-load.json), [trước](evidence/https-load-before.json),
[tài nguyên](evidence/resources.json), [trước](evidence/resources-before.json).

Preview editorial được đo query budget **464 → 2 SELECT**, một lần local
268,6 → 49,2ms; không phải WAN benchmark. POST visit/complete dùng projection
nhẹ, query budget visit/first complete/repeat 12/13/12 gồm ba auth queries;
không dựng related assessments/hints/body/bookmarks, quyền live giữ nguyên.

### Web Vitals lab và bundle

[web-vitals-lab.json](evidence/web-vitals-lab.json): 18 navigations Chrome
qua Caddy HTTPS/Linux, ba lượt mỗi path/viewport, không throttle CPU/mạng,
settle 1,5s. Bảng là median ba lượt; không phải Core Web Vitals field.
Route `/login` trong sáu mẫu đã có session nên chuyển về dashboard; không
dùng chúng làm số đo trang login ẩn danh.

| Viewport | Trang                | TTFB ms | LCP ms |    CLS |
| -------- | -------------------- | ------: | -----: | -----: |
| 390px    | `/student/dashboard` |   10.90 |    216 | 0.0444 |
| 390px    | `/ai-academy`        |   11.40 |    196 | 0.2089 |
| 1365px   | `/student/dashboard` |   14.20 |    228 | 0.0960 |
| 1365px   | `/ai-academy`        |    5.70 |    208 | 0.1608 |

CLS AI Academy 0,1608–0,2089 là điểm cần cải thiện (AUD-24); không suy từ
LCP nhanh trên localhost thành UX tốt trên mạng di động. Không đo INP
đại diện/field. Tổng 33 JS chunks đã emit ở test build: 1.215.203 bytes raw,
377.135 bytes gzip từng file; đây là toàn bộ chunks, không phải initial
payload mỗi route, không dùng để so baseline chưa đo.

## Chạy lại an toàn

Tạo database **mới** riêng, cấu hình `DB_NAME` và `TEST_DATABASE_URL` trỏ DB
đó, `APP_ENV=development` cho synthetic fixture; passwords ngẫu nhiên trong
env. Không dùng `viettree-education`, không DROP/TRUNCATE/reset hay copy PII.
Theo job backend trong `.github/workflows/verify.yml` để import/migrate/seed
đủ năm pack/AI; các bước chỉ dành DB test mới. Trong `backend`:

```bash
python -m pytest -q -rs
ruff check .
ruff format --check .
```

Coverage cần venv audit riêng có `requirements-lock.txt`, `pytest-cov`;
không dùng `--system-site-packages` (đã gặp package Anaconda không đúng).
Trong `frontend`, với backend/web test đang chạy, `E2E_FIXTURE_FILE` là JSON
từ `python -m scripts.prepare_e2e`, `E2E_BASE_URL` và passwords fixture:

```bash
npm ci
npm run test
npm run lint
npm run build
npm run typecheck
node e2e/run-audit.mjs --reporter=line
node e2e/run-audit.mjs e2e --reporter=line,json
```

CI Linux dùng `E2E_BROWSER_CHANNEL=chromium`; runner kiểm đủ fixture và cấm
`test.only`. Local private CA chỉ được bỏ trust trong browser với localhost;
public domain phải verify certificate bình thường. Không in passwords ra log.
Venv người dùng chưa bị thay package trong khi backend cũ đang chạy: dừng
backend bằng terminal của bạn, cài lock mới rồi restart; xem [08](08-changelog-and-rollback.md).

## Giới hạn

Starlette cảnh báo chuyển httpx vẫn còn. Chưa remote GitHub Actions, chưa
pentest toàn bộ, screen reader/iOS thật, giáo viên duyệt toàn kho, test dài
ngày/traffic lịch sử lớn, public DNS/TLS/VPS Nhật, backup ngoài máy hoặc INP
field của người dùng. Không dùng các PASS local để tuyên bố production-ready.
