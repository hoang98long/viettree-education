# Bàn giao VietTree Education — 09/10/2026 (Asia/Bangkok)

Đã triển khai trực tiếp toàn bộ monorepo theo prompt. Luồng demo login và học sinh
làm bài đã kiểm chứng với PostgreSQL thật; không có API điểm/thống kê giả.

Trạng thái mới nhất: xem phần **Mở rộng nội dung và ngân hàng câu hỏi** cuối tài liệu.
Các checkpoint và số lượng trong phần đầu ghi nhận mốc MVP trước khi mở rộng.

| Checkpoint | Kết quả |
| --- | --- |
| 1 · Đọc SQL, mapping constraints | Hoàn thành: 34 bảng, UUID/JSONB/checks/composite FK; SQL gốc giữ nguyên |
| 2 · Cấu hình, auth, migration | Hoàn thành: FastAPI/Next, root env, session/CSRF/RBAC/rate limit, baseline + 2 bảng auth |
| 3 · Seed | Hoàn thành: admin/longnh; 12 topics, 24 lessons, 96 questions, 12 assessments, 12 skills |
| 4 · API làm bài | Hoàn thành: assignment self, exact version, start/resume/save/submit/result/history |
| 5 · Personalization | Hoàn thành: rule_v1, confidence, ôn 1/3/7 ngày, prerequisite/weak skills, rebuild statistics |
| 6 · Frontend | Hoàn thành: public/login, mọi route student/admin yêu cầu, responsive; teacher/guardian layout |
| 7 · Kiểm chứng | Pass backend/unit/integration/concurrency, frontend component/type/lint/build/format, browser desktop/mobile, smoke PostgreSQL |
| 8 · Tài liệu | README tiếng Việt, architecture/API/security/personalization, SQL kiểm chứng seed |

## Chứng cứ đã chạy

| Lệnh/kiểm chứng | Kết quả |
| --- | --- |
| `alembic upgrade head` trên DB thật/test | Pass; revision 0002_auth_sessions; không import lại DB thật |
| `python -m app.cli check-schema` | Pass, đối chiếu đủ bảng và cột |
| `python -m app.cli seed` chạy lặp | Pass; cùng số lượng, không reset password/kết quả |
| `python -m app.cli import-schema` trên DB test | Pass, dùng nguyên SQL gốc, không reset |
| `pytest -q` + TEST_DATABASE_URL riêng | **121 passed**, 1 warning deprecation từ Starlette/httpx |
| `ruff check` / `ruff format --check` | Pass sau formatter |
| `python scripts/smoke.py` trên DB thật | **SMOKE PASS** toàn luồng admin/longnh/chấm/kết quả/history/mastery/stats, rollback |
| `npm run typecheck`, `npm run lint` | Pass |
| `npm test` | **4 passed**, bốn dạng input |
| `npm run build` | Pass, Next.js 16.4.0 production build |
| `npm run format:check` | Pass |
| `npm audit` | **0 vulnerabilities** sau cập nhật toolchain |
| `npm run test:e2e` | **4 passed**: student/admin trên desktop/mobile Chrome, sau reload và route guard |
| `docker compose config --quiet` | Pass |
| SQL `database/seeds/verify.sql` | Mỗi môn 4/8/32/4; 12 đề đều 8 items; 0 câu thiếu skill |
| SQL count attempts DB thật sau smoke | **0**; lịch sử/điểm demo vẫn sạch |
| Browser với backend nối DB thật sau kiểm thử | Pass login/dashboard/logout admin và longnh, history=0; `/ready` trả ready |

Integration từ chối DB thật. Các test concurrency và browser có dữ liệu ghi thật
trong viettree-education-test; không xóa/reset cả database test. Browser lần đầu dùng
longnh, lần kiểm chứng cuối dùng học sinh test riêng do create_test_student.py tạo.

## Các phần chủ động để chờ theo prompt

Form tạo bài tập cho admin/teacher đầy đủ trường nhưng tất cả thao tác lưu/xuất bản
disabled; không có write CRUD câu hỏi. Guardian/teacher quản lý lớp/phụ huynh chưa
mở. Nội dung lớp 1/2/3/5 và bốn môn còn lại đang xây dựng. Không có AI trả phí,
upload/audio, chấm tự luận, public signup, Redis/MinIO hay leaderboard công khai.
Kế hoạch học `plan_v1` đã sử dụng các bảng learning plans gốc; chi tiết mở rộng bên dưới.

Docker daemon không chạy trong môi trường này: **chưa kiểm thử build/run container**,
chỉ cấu hình đã validate. Không tuyên bố Docker runtime pass. Local host full stack
và kết nối PostgreSQL đã được kiểm chứng. Tài liệu có hạn chế rate limit sau proxy,
rebuild toàn lịch sử, retention auth và yêu cầu consent trước khi vận hành thực tế.

Khởi động, tài khoản local DEV và lệnh kiểm chứng xem README. Không có bước deploy
Internet/commit/push tự động; toàn bộ thay đổi nguồn nằm trong workspace.

Khi bàn giao, frontend dev ở http://localhost:3000 và backend ở
http://localhost:8000 đang chạy, kết nối lại database thật `viettree-education`.

## Mở rộng cho học sinh tiểu học — 09/10/2026

- Tăng cỡ chữ học sinh, kể cả các breakpoint điện thoại: nội dung chung 18 px,
  bài học 20 px, câu hỏi 22 px, nhãn phụ 15–16 px; nút chính tối thiểu 48 px.
  Chế độ chữ lớn dùng 22/24/26 px, lưu trong student_profiles.accessibility_options.
- Trang Kế hoạch học: tối đa 3 bài mới cùng lớp và bài luyện tập đi kèm, lịch 7 ngày
  theo Asia/Bangkok. Tái sử dụng kế hoạch active của môn, không tạo trùng khi bấm lại.
- Xác nhận đọc xong lưu student_lesson_progress, cập nhật learning_plan_items và
  learning_plan_history. Submit cập nhật bước luyện tập trong transaction chấm.
  Đủ bước thì kế hoạch hoàn thành; đọc bài không tự tăng mastery hoặc tạo điểm.
- Không thêm migration, không thay SQL gốc. Sửa ngoại lệ .gitignore để mã nguồn
  frontend/src/lib không bị quy tắc Python lib/ bỏ qua.
- Đề xuất phát triển và tiêu chí nghiệm thu được ghi tại roadmap.md.

Chứng cứ vòng mở rộng: 5 integration test mới đã pass, 6 browser test đã pass trên
desktop/mobile Chrome, gồm reload/đăng nhập lại, tạo kế hoạch lặp và lưu tiến độ.
Chế độ chữ lớn không gây tràn ngang trang kế hoạch ở 320/768/1280 px. Chỉ database
test được dùng cho kiểm thử browser ghi dữ liệu.

Kiểm tra tổng thể sau mở rộng: **126 backend tests**, **4 component tests**, typecheck,
eslint, ruff và production build đều pass. Một warning deprecation Starlette/httpx
từ thư viện vẫn còn. Frontend format check pass. Đã nối lại backend với DB thật và
kiểm tra login/xem dashboard/kế hoạch/hồ sơ/logout; dashboard không tràn ngang ở
320/390/768/1280 px cho cả hai cỡ chữ. Kiểm tra giao diện trên DB thật không lập kế
hoạch, đánh dấu đọc hoặc tạo bài làm.

## Triển khai Free / VIP — 09/10/2026

- Migration 0003_memberships đã áp dụng trên database thật và test: 6 bảng bổ sung,
  giữ nguyên 34 bảng/SQL gốc. Gói độc lập vai trò; thời hạn kiểm tra từng request.
- 24 bài/12 đề hiện có vẫn Free. Thêm 6 bài nâng cao, 48 câu và 6 thử thách riêng
  (mỗi môn 2 bộ); tổng 30 bài/144 câu/18 đề. Bộ mới là nội dung mẫu development,
  cần giáo viên rà soát chuyên môn trước vận hành; không tự cấp VIP cho demo.
- Admin cấp/gia hạn/thu hồi 30/90/365 ngày, CSRF, Idempotency-Key, khóa DB và audit;
  cấu hình policy/preview nội dung. Không mở CRUD câu hỏi bị giữ chờ trong prompt.
- API bảo vệ đọc bài/tiến độ/giao bài/bắt đầu/lưu/nộp và lọc gợi ý/kế hoạch. Free
  chỉ xem preview riêng; dùng chung câu hỏi VIP khiến đề yêu cầu VIP.
- Attempt VIP có khoảng hoàn tất tối đa 60 phút sau hết hạn, giới hạn bởi due_at
  và thời lượng. Thu hồi chặn ngay và vĩnh viễn grant đó; kết quả đã nộp giữ nguyên.
- Plan_v2 ưu tiên prerequisite/weak/review; advanced chỉ khi đủ bằng chứng vững.
  Hết quyền chuyển paused, giữ tiến độ; kế hoạch cơ bản tiếp tục hoạt động.
- Guardian xem gói của trẻ có verified_at; chưa có UI tạo/xác minh liên kết,
  báo cáo/PDF hoặc thanh toán trực tuyến.

Đã đối chiếu checksum từng hàng cũ trước/sau migration+seed trên DB thật: toàn bộ
users/password/roles/profile, nội dung cũ, tiến độ đọc và lịch sử giữ nguyên. DB
thật vẫn 0 attempts, 1 dòng tiến độ đọc; seed không tạo điểm hoặc kế hoạch giả.
SQL gốc giữ nguyên checksum. Không reset/xóa database.

Kiểm thử browser Free → cấp/gia hạn VIP trong phiên → đọc/làm/nộp nâng cao →
plan_v2 → thu hồi → giữ kết quả đã pass trên desktop/mobile Chrome, cùng 6 luồng
cũ. Preview không tràn ngang ở 320/768/1280 px. Frontend typecheck/lint/format,
production build và 4 component tests pass.

Backend: **146 tests pass**, gồm boundary hết hạn/grace, owner/role/guardian,
policy thiếu/dùng chung câu, giữ nhãn sau seed, plan_v2 dùng bằng chứng thật và
gia hạn đồng thời (key giống/khác). Ruff check/format pass. Warning deprecation
Starlette/httpx của thư viện vẫn còn.

Smoke chỉ đọc trên DB thật pass: revision 0003_memberships, /ready, đăng nhập
Free và admin, chặn nội dung VIP, preview riêng, 48 chính sách (12 VIP), dashboard
và history. Không tạo bài làm/điểm/kế hoạch hoặc thay gói trên DB thật.

## Mở rộng nội dung và ngân hàng câu hỏi — 09/10/2026

- Bổ sung 12 bài lớp 4, 72 câu và 12 đề: sáu bài Free và sáu bài VIP, đều có
  giải thích/ví dụ/lời giải. Tổng **42 bài, 216 câu, 30 đề** cho Toán, Tiếng Việt
  và Tiếng Anh; Free 30 bài/18 đề, VIP 12 bài/12 đề.
- Đã áp dụng migration `0004_question_authoring` và `0005_authoring_revisions`
  trên DB thật/test. Thêm policy theo phiên bản câu và revision chống ghi đè.
  SQL gốc giữ nguyên; chỉ bổ sung schema bằng migration.
- Admin biên soạn bốn loại câu, xem trước, lưu nháp, duyệt, xuất bản, lưu trữ,
  tạo phiên bản mới. Đề cũ giữ phiên bản câu/đáp án cũ, kể cả khi có phiên bản mới.
- Admin ghép 1–50 câu đã xuất bản, sắp thứ tự/điểm/thời gian/gói, duyệt/xuất bản,
  sao chép đề và giao cho tối đa 50 học sinh. Kiểm tra toàn bộ nhóm cùng transaction;
  lặp cùng lịch dùng lại nhiệm vụ đang hoạt động. Tìm học sinh theo tên hoặc tài khoản.
- Học sinh có thư viện lọc môn/Free/VIP/loại/từ khóa. Mở từ nhiệm vụ dùng đúng
  assignment, tuân thủ lịch mở/hạn nộp và cập nhật hoàn thành sau nộp bài.
- Đã tạo thực tế `free4_01`, `free4_02`, `vip4_01`, `vip4_02` ở lớp 4, hai VIP
  thời hạn 90 ngày. Mật khẩu dùng SEED_STUDENT_PASSWORD local. Lệnh tạo riêng chỉ
  development; chạy lại giữ nguyên mật khẩu/gói/thời hạn.
- Đối chiếu checksum mọi trường/hàng đã có trước migration và seed: tài khoản,
  mật khẩu, vai trò, nội dung, tiến độ và lịch sử cũ không đổi. DB thật vẫn 0 attempts,
  một tiến độ đọc; không seed điểm hay kế hoạch giả. Seed và tạo demo đã chạy lặp.

Thiết kế và bước nâng cấp tiếp: [authoring-design.md](authoring-design.md).
Teacher quản lý lớp, trình soạn bài học, nhập CSV, báo cáo phụ huynh và thanh toán
vẫn là đề xuất; nội dung demo cần giáo viên rà soát chuyên môn.

Kiểm chứng cuối đợt:

- **155 backend tests pass**, gồm bốn loại câu, đáp án không hợp lệ, revision cũ,
  sửa sau duyệt, giữ đáp án phiên bản cũ trong lượt đang làm/đề cũ, câu VIP độc lập,
  giao bài atomic/idempotent, clone và chặn archive khi có lượt đang làm.
- **10 browser journeys pass** trên desktop/mobile Chrome, gồm admin tạo câu →
  duyệt/xuất bản → ghép đề → giao bài → học sinh tìm trong thư viện → mở đúng
  nhiệm vụ → nộp/kết quả → nhiệm vụ completed; các luồng Free/VIP và chữ lớn vẫn pass.
- TypeScript, ESLint, Prettier, **4 component tests**, production build; Ruff
  check/format app/tests và hai migration mới đều pass. Đã xem ảnh admin mobile;
  trình ghép/giao bài không tràn ngang.
- Smoke trên DB thật: `/ready`, admin/longnh và bốn tài khoản mới đăng nhập được,
  Free bị chặn bài VIP, VIP mở được; 72 policy bài/đề và head 0005. Đăng nhập cập
  nhật thời điểm truy cập và phiên auth theo thiết kế; không tạo bài làm/điểm/
  kế hoạch hoặc sửa nội dung. Đối chiếu toàn bộ hàng cũ đã pass ngay sau migration
  và seed, trước bước đăng nhập smoke.
- Backend và browser chạy tuần tự trên DB test trong lượt kiểm chứng cuối để
  tránh tranh chấp với transaction rollback của pytest. Warning deprecation
  Starlette/httpx vẫn còn; runtime Docker chưa kiểm thử vì chưa có daemon.

Ứng dụng local được đưa về backend DB thật tại http://localhost:8000 và frontend
development tại http://localhost:3000 sau kiểm thử.
