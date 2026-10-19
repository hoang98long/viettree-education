# Bàn giao VietTree Education — 09/10/2026 (Asia/Bangkok)

Đã triển khai trực tiếp toàn bộ monorepo theo prompt. Luồng demo login và học sinh
làm bài đã kiểm chứng với PostgreSQL thật; không có API điểm/thống kê giả.

Trạng thái mới nhất: [AI Academy 19/10](ai-academy-upgrade-2026-10-19.md),
[kiểm chứng AI](audits/academy-quality-2026-10-19.md). Đợt trước: [học tiếp và học liệu hằng ngày 17/10](daily-learning-and-resume.md),
[kiểm chứng](audits/daily-quality-2026-10-17.md). Đợt 16/10 xem [AI và tự kiểm tra](learning-upgrade-2026-10-16.md).
Đợt trước xem phần **Rà soát học liệu, tải 50 học sinh và VPS** cuối tài liệu;
phần VIP, phiên đăng nhập và ngân hàng câu hỏi ghi nhận các đợt trước.
Các checkpoint và số lượng trong phần đầu ghi nhận mốc MVP trước khi mở rộng.

| Checkpoint                       | Kết quả                                                                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1 · Đọc SQL, mapping constraints | Hoàn thành: 34 bảng, UUID/JSONB/checks/composite FK; SQL gốc giữ nguyên                                                        |
| 2 · Cấu hình, auth, migration    | Hoàn thành: FastAPI/Next, root env, session/CSRF/RBAC/rate limit, baseline + 2 bảng auth                                       |
| 3 · Seed                         | Hoàn thành: admin/longnh; 12 topics, 24 lessons, 96 questions, 12 assessments, 12 skills                                       |
| 4 · API làm bài                  | Hoàn thành: assignment self, exact version, start/resume/save/submit/result/history                                            |
| 5 · Personalization              | Hoàn thành: rule_v1, confidence, ôn 1/3/7 ngày, prerequisite/weak skills, rebuild statistics                                   |
| 6 · Frontend                     | Hoàn thành: public/login, mọi route student/admin yêu cầu, responsive; teacher/guardian layout                                 |
| 7 · Kiểm chứng                   | Pass backend/unit/integration/concurrency, frontend component/type/lint/build/format, browser desktop/mobile, smoke PostgreSQL |
| 8 · Tài liệu                     | README tiếng Việt, architecture/API/security/personalization, SQL kiểm chứng seed                                              |

## Chứng cứ đã chạy

| Lệnh/kiểm chứng                                | Kết quả                                                                             |
| ---------------------------------------------- | ----------------------------------------------------------------------------------- |
| `alembic upgrade head` trên DB thật/test       | Pass; revision 0002_auth_sessions; không import lại DB thật                         |
| `python -m app.cli check-schema`               | Pass, đối chiếu đủ bảng và cột                                                      |
| `python -m app.cli seed` chạy lặp              | Pass; cùng số lượng, không reset password/kết quả                                   |
| `python -m app.cli import-schema` trên DB test | Pass, dùng nguyên SQL gốc, không reset                                              |
| `pytest -q` + TEST_DATABASE_URL riêng          | **121 passed**, 1 warning deprecation từ Starlette/httpx                            |
| `ruff check` / `ruff format --check`           | Pass sau formatter                                                                  |
| `python scripts/smoke.py` trên DB thật         | **SMOKE PASS** toàn luồng admin/longnh/chấm/kết quả/history/mastery/stats, rollback |
| `npm run typecheck`, `npm run lint`            | Pass                                                                                |
| `npm test`                                     | **4 passed**, bốn dạng input                                                        |
| `npm run build`                                | Pass, Next.js 16.4.0 production build                                               |
| `npm run format:check`                         | Pass                                                                                |
| `npm audit`                                    | **0 vulnerabilities** sau cập nhật toolchain                                        |
| `npm run test:e2e`                             | **4 passed**: student/admin trên desktop/mobile Chrome, sau reload và route guard   |
| `docker compose config --quiet`                | Pass                                                                                |
| SQL `database/seeds/verify.sql`                | Mỗi môn 4/8/32/4; 12 đề đều 8 items; 0 câu thiếu skill                              |
| SQL count attempts DB thật sau smoke           | **0**; lịch sử/điểm demo vẫn sạch                                                   |
| Browser với backend nối DB thật sau kiểm thử   | Pass login/dashboard/logout admin và longnh, history=0; `/ready` trả ready          |

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

## Phiên đăng nhập và cache — 10/10/2026

- Giữ phiên thường mặc định 8 giờ; học sinh có thể chọn ghi nhớ 7 ngày trên máy
  cá nhân. Admin/teacher không được dùng phiên dài, kể cả khi thêm vai trò sau
  khi phiên ghi nhớ đã được tạo. Cấu hình qua SESSION_HOURS/REMEMBER_SESSION_DAYS.
- Logo trong giao diện ứng dụng về dashboard của vai trò hiện tại. Trang chủ có
  nút tiếp tục theo phiên; `/login` chuyển tới dashboard nếu còn phiên hợp lệ.
- Provider dùng chung trạng thái đăng nhập, cache bộ nhớ 30 giây và gộp request.
  Kiểm tra lại khi quay về tab, Back/Forward, đến hạn phiên và theo chu kỳ khi
  tab hiển thị. Đồng bộ đăng xuất giữa tab; chặn response cũ khôi phục cache.
- PostgreSQL vẫn kiểm tra phiên/tài khoản/vai trò ở mỗi API bảo vệ; giữ no-store,
  CSRF và cookie HttpOnly/SameSite/Secure. Không cần Redis hoặc migration mới.
- Login trả cả thời điểm hết hạn và cỡ chữ đã lưu, để cache không làm mất lựa
  chọn chữ lớn khi học sinh đăng nhập lại. Đăng nhập lại thay token/thu hồi phiên
  cũ cùng trình duyệt, không đăng xuất các thiết bị khác.
- **166 backend tests**, **14 component tests** pass. Browser: 8 luồng biên soạn,
  học tập và Free/VIP đạt; 6 luồng cỡ chữ/phiên đạt ở đợt kiểm chứng cuối, tổng
  14 luồng trên desktop/mobile. Backend/browser chạy tuần tự trên DB test riêng.
  TypeScript, ESLint, Prettier, Ruff check/format và production build đạt.
- Kiểm tra schema DB thật chỉ đọc, không đổi nội dung hoặc dữ liệu học tập.
  Server test tại cổng 8001/3001 đã dừng sau kiểm chứng; chạy lại ứng dụng local
  theo [run-local.md](run-local.md).

Thiết kế, TTL, cấu hình và giới hạn: [session-management.md](session-management.md).

## Mở rộng VIP lớp 4 — 10/10/2026

- Thêm sáu bài học nâng cao, 48 câu và sáu đề 8 câu cho Toán, Tiếng Việt, Tiếng Anh.
  Tổng bộ seed **48 bài, 264 câu, 36 đề**: Free 30 bài/18 đề, VIP 18 bài/18 đề.
  Nội dung mới có bốn loại câu, ví dụ và lời giải; cần giáo viên rà soát chuyên môn.
- Góc học VIP gom bài nâng cao, lọc môn/bài chưa đọc, hiển thị tiến độ và liên kết
  tới sổ tay, báo cáo, kế hoạch theo kỹ năng hiện có.
- Sổ tay lấy câu sai/chưa trả lời ở lần chấm gần nhất từng phiên bản, của chính
  học sinh và lớp hiện tại; không lấy nháp hoặc bài của người khác. Tự ôn và xem
  lời giải không ghi điểm/lượt làm/mastery; đúng ở bài chính thức sẽ đưa câu ra khỏi sổ.
- Báo cáo 7/30 ngày tổng hợp điểm/lượt đã chấm, bài đọc hoàn thành, kỳ trước,
  nhịp theo ngày và kỹ năng cần ôn có đủ bằng chứng từ toàn bộ lịch sử. Không có
  điểm hiển thị chưa có dữ liệu; không xếp hạng. In/lưu PDF qua trình duyệt trong
  tài khoản học sinh; báo cáo riêng cho guardian vẫn là bước tiếp theo.
- Migration `0006_vip_learning_tools` thêm ba feature, không thêm bảng. Mỗi API
  kiểm tra quyền VIP hiện hành, chủ sở hữu và vai trò; tự ôn vẫn yêu cầu CSRF.
  API giữ no-store; refresh gói hợp lệ giữ câu tự ôn đang nhập trên giao diện.
- Đã nâng DB local lên head 0006 và chạy `seed-vip-content` hai lần. Đối chiếu
  checksum tất cả hàng cũ trên mọi bảng trước/sau: dữ liệu cũ và SQL gốc không đổi,
  gồm mật khẩu, gói/thời hạn, phiên và lịch sử. Hai attempts, một answer và năm
  tiến độ đọc đã có vẫn giữ nguyên; không tạo dữ liệu học tập giả hoặc cấp lại VIP.
- **222 backend tests**, **14 component tests**, **6 browser journeys** đạt trên
  desktop/mobile Chrome. Browser kiểm tra Free bị chặn, VIP mở nội dung, tự ôn
  không đổi điểm, báo cáo 7/30, in, thu hồi và giữ kết quả; luồng gói/cỡ chữ vẫn đạt.
  Backend/browser chạy tuần tự trên DB test riêng. Ruff check/format, TypeScript,
  ESLint, Prettier frontend và production build đạt; warning Starlette/httpx vẫn còn.
- Đã dừng server test cổng 8001/3001. Chạy lại ứng dụng theo [run-local.md](run-local.md).

Hướng dẫn sử dụng, nạp nội dung và giới hạn: [vip-expansion.md](vip-expansion.md).

## Biên soạn bài học, minh họa và gợi ý — 10/10/2026

- Admin có **Quản lý bài học**: lọc/tìm kiếm/phân trang, tạo bài, biên soạn theo
  khối, mục tiêu, gợi ý, câu tự suy ngẫm và minh họa. Xem trước dùng cùng thành
  phần đọc bài của học sinh; không ghi tiến độ khi xem trước.
- Nháp lưu riêng trong `lesson_drafts`; học sinh tiếp tục đọc bản đang xuất bản.
  Lưu nháp → duyệt → xuất bản. Sửa làm mất trạng thái duyệt; revision và khóa hàng
  ngăn ghi đè khi sửa đồng thời. Fingerprint kiểm tra bài/quyền/kỹ năng nguồn;
  đổi policy ở nơi khác chặn duyệt/xuất bản nháp cũ. Tạo lại nháp có xác nhận.
- Xuất bản cập nhật bài, kỹ năng và policy trong cùng transaction; lưu audit
  trước/sau và hiển thị 20 thao tác gần nhất. Admin API có RBAC/CSRF; học sinh
  không đọc được payload nháp. Mã/lớp/môn/chủ đề cố định sau khi tạo.
- 48 bài hiện có được bổ sung mục tiêu, mục lục, ba gợi ý theo chủ đề, câu hỏi
  tự suy ngẫm và minh họa SVG phân số/luống rau/đọc hiểu/đồng hồ. Nội dung mặc định
  bổ sung sau kiểm tra quyền, không ghi đè hàng bài cũ. Nội dung riêng do admin
  xuất bản thay thế các mặc định này.
- Gợi ý học tiếp tối đa ba bài cùng chủ đề, đã xuất bản, chưa đọc xong và đủ quyền.
  Ghi chú tự suy ngẫm chỉ ở trang hiện tại, không chấm/lưu server. Chuyển bài đặt
  lại trạng thái hoàn thành đúng bài mới; tiến độ và kết quả cũ giữ nguyên.
- Sửa lỗi thanh bên admin dài làm nút đăng xuất ra ngoài viewport: thanh bên
  cuộn được và menu giữ kích thước. Kiểm thử luồng biên soạn/giao bài/đăng xuất
  desktop đã chạy lại thành công sau sửa lỗi.
- **237 backend tests**, **17 component tests** đạt; **18 browser journeys** đã
  kiểm chứng trên desktop/mobile Chrome (17 đạt trong lượt toàn bộ; luồng desktop
  gặp lỗi thanh bên đã được sửa và chạy lại đạt). Gồm cả biên soạn câu/đề/giao bài,
  bài học mới, hint/reflection, VIP, kế hoạch, cỡ chữ, cookie và phiên đa tab.
  Bài học/danh sách admin không tràn ngang ở 320/768/1280 px. Đã xem minh họa desktop.
- DB local đã lên head `0007_lesson_studio`, chỉ thêm bảng nháp rỗng. Checksum
  mọi hàng đã có và SQL gốc trước/sau đều giữ nguyên. Smoke chỉ đọc xác thực
  nội dung bổ sung của 48 bài, Free bị chặn bài VIP và VIP đọc được; không tạo
  tài khoản, bài làm, điểm, tiến độ hoặc thay thời hạn gói trên DB local.
- Ruff check/format, TypeScript, ESLint, Prettier frontend và production build
  đạt. Warning deprecation Starlette/httpx vẫn còn. Test dùng database riêng;
  server test 8001/3001 đã dừng. Khởi động lại theo [run-local.md](run-local.md).

Hướng dẫn, schema/API, quy tắc sửa/xuất bản và phần chưa triển khai:
[lesson-studio.md](lesson-studio.md). Nội dung cần giáo viên rà soát trước vận hành.

## Học liệu lớp 4 và Góc tư duy — 10/10/2026

- Đối chiếu chương trình chính thức của Bộ GDĐT cho Toán, Tiếng Việt và Tiếng Anh
  lớp 4; ghi nguồn, phạm vi và phần còn thiếu trong [grade4-curriculum.md](grade4-curriculum.md).
  Nội dung tự biên soạn, chưa bao phủ toàn bộ chương trình hoặc mọi môn lớp 4.
- Thêm **20 bài, 120 câu và 20 đề luyện tập**: 16 bộ Free, 4 bộ VIP; thêm chín
  chủ đề/kỹ năng. Tổng bộ mẫu **21 chủ đề, 68 bài, 384 câu, 56 đề**. Free có
  46 bài/34 đề/228 câu; VIP có 22 bài/22 đề/156 câu.
- Bổ sung số đến lớp triệu, góc/đường thẳng, dữ liệu, khả năng qua thực nghiệm,
  tổng–hiệu, đơn vị, nhân/chia phân số; viết miêu tả/thuật việc, nói/nghe, trạng
  ngữ, văn bản thông tin; can/can't, chỉ đường và sở thích bằng tiếng Anh.
  Có mục tiêu, ví dụ, ba gợi ý, lời giải và câu hỏi tự giải thích.
- **Góc tư duy** cho học sinh có bộ lọc môn, phân trang, tiến độ của chính mình
  và quyền Free/VIP hiện hành. Bốn bài đếm khoảng, loại trừ, tìm bằng chứng và
  đọc lịch hướng dẫn kiểm tra đủ điều kiện; không dùng câu đố mơ hồ. Danh mục
  VIP bị khóa chỉ trả metadata, không trả nội dung/gợi ý/đáp án.
- Admin có bảng **Theo dõi học liệu lớp 4**, số liệu xuất bản thực tế, liên kết
  nguồn, ghi chú thiếu nội dung và bộ lọc mạch chưa có bài Free. Bảng theo mạch
  chủ đề, không chứng nhận học sinh đạt yêu cầu hoặc chương trình đã đầy đủ.
  Editor chọn nhóm bài thường/tư duy, thêm SVG biểu đồ cột và góc có kiểm tra
  dữ liệu; nháp tiếp tục tách biệt với bản học sinh đọc.
- **267 backend tests** đạt toàn bộ; sau điều chỉnh phạm vi/hoạt động chủ đề của
  bảng admin, **30 tests** cho đợt mở rộng đã chạy lại đạt. Bao gồm 120 đáp án
  kiểm tra độc lập, chấm/nộp đủ 20 đề mới, RBAC, Free/VIP, chủ sở hữu tiến độ,
  grade hiện hành, dữ liệu minh họa sai và seed lặp không sửa bài admin.
- **18 component tests**, **20 browser journeys** đạt trên desktop/mobile Chrome:
  18 luồng cũ đạt trong lượt toàn bộ; hai luồng mới sửa selector kiểm thử và chạy
  lại đạt trên production preview. Kiểm tra học bài, hint/tiến độ, khóa/mở VIP,
  bảng admin, lưu/xem trước nháp biểu đồ và giữ bản xuất bản; minh họa không gây
  tràn trang ở 320/768/1280 px. Ruff check/format, TypeScript, ESLint, Prettier
  frontend và production build đạt. Warning deprecation Starlette/httpx còn tồn tại.
- Đã chạy `seed-grade4-content` hai lần trên DB local, số lượng không tăng ở lần
  thứ hai. So sánh checksum mọi hàng cũ của mọi bảng và SQL gốc đều giữ nguyên:
  sáu tài khoản, gói/thời hạn, 22 phiên, năm attempts, một answer và tám tiến độ
  đọc vẫn nguyên trạng. Không tạo kết quả học tập giả, đặt lại mật khẩu hay cấp
  lại VIP. Không cần migration mới; head vẫn `0007_lesson_studio`.
- Smoke chỉ đọc trên DB local kiểm tra schema nội dung của cả 68 bài, quyền
  Free với 20 bài mới, bốn bài tư duy, 24 dòng bảng admin và hai VIP còn hiệu lực.
  Backend/browser dùng database test riêng và chạy tuần tự. Server test 8001/3001
  đã dừng; khởi động lại backend/frontend theo [run-local.md](run-local.md).

Ưu tiên tiếp theo: lấp các mạch còn thiếu, giáo viên rà soát/nhận xét bài viết,
nghe/phát âm có âm thanh và các môn khác. Chưa triển khai chấm tự luận hoặc audio.

## Quản trị tài khoản và bảo mật cá nhân — 10/10/2026

- Admin có trang **Quản trị tài khoản**: tạo, tìm kiếm/lọc/phân trang, sửa tên
  đăng nhập/tên hiển thị/email tùy chọn, một hoặc nhiều vai trò, trạng thái,
  lớp/cỡ chữ học sinh; liên kết gói Free/VIP. Thêm khóa/mở, đặt lại mật khẩu,
  thu hồi phiên và 20 dòng nhật ký gần nhất với chi tiết thay đổi tiếng Việt.
- Mọi vai trò có **Bảo mật tài khoản**: xác nhận mật khẩu hiện tại để đổi mật
  khẩu, xem phiên và đăng xuất phiên khác. Đổi mật khẩu thay token/CSRF, thu hồi
  các phiên cũ và cấp phiên thường mới. Cache/tab khác kiểm tra lại.
- Mật khẩu mới 15–256 ký tự, cho Unicode/khoảng trắng, chặn một số mật khẩu phổ
  biến, trùng tên đăng nhập hoặc mật khẩu cũ. Tài khoản do admin tạo/đặt lại dùng
  mật khẩu tạm phải đổi trước khi học/quản trị; backend chặn API khi cờ bật.
  Không reset hoặc ép đổi tài khoản cũ sau migration.
- Thao tác accounts có RBAC/CSRF, lý do và xác nhận mật khẩu admin, giới hạn xác
  nhận 10 lượt/phút/tài khoản dùng chung PostgreSQL. Không tự khóa/thay vai trò,
  bảo vệ admin cuối cùng. Revision/khóa transaction ngăn ghi đè, kiểm tra lại
  actor và không cho hai admin đồng thời khóa nhau. Login khóa hàng tài khoản
  để phiên từ mật khẩu cũ không sống sót sau reset đồng thời.
- Khóa user FOR NO KEY UPDATE tương thích khóa ngoại của nhật ký/phiên, tránh
  vòng chờ với thao tác khóa hồ sơ trước. Có kiểm thử đồng thời tái hiện tình
  huống hồ sơ đang khóa, thao tác sửa tài khoản đang chờ và ghi audit vẫn hoàn tất.
- Đổi lớp/gỡ vai trò học sinh giữ hồ sơ, membership, attempts/answers và tiến độ.
  Danh sách/thống kê học sinh chỉ tính người còn vai trò student. Sửa hồ sơ cũ
  tăng account_revision để màn hình mới phát hiện xung đột. Nhật ký không chứa
  password/hash, token/CSRF hoặc email plaintext; log lỗi DB chỉ tên constraint,
  không SQL/parameters. Không có API xóa tài khoản.
- **299 backend tests**, **18 component tests**, **22 browser journeys** đạt.
  Browser bao gồm tạo/sửa, mật khẩu tạm, thay token, khóa/mở, reset, tự đổi mật
  khẩu, phiên khác và các luồng biên soạn/học tập/VIP/phiên cũ trên desktop/mobile.
  Kiểm tra form không tràn trang ở 320/768/1280 px. Ruff check/format, TypeScript,
  ESLint, Prettier và production build đạt. Warning Starlette/httpx còn tồn tại.
  Sau điều chỉnh khóa user và checkbox vai trò, bộ 299 backend tests đạt lại;
  hai luồng tài khoản chạy lại đạt trên Next standalone với static assets,
  đã xem ảnh chụp giao diện điện thoại. Docker/container runtime chưa kiểm thử.
- DB local đã lên **0008_account_management**, thêm ba cột trên users, không
  thêm bảng hoặc seed tài khoản. Đối chiếu mọi cột/hàng đã có trên mọi bảng trước/
  sau và checksum SQL gốc giữ nguyên: sáu tài khoản, 23 phiên, hai membership,
  năm attempts, một answer, tám tiến độ đọc và toàn bộ học liệu vẫn nguyên trạng.
  Smoke chỉ đọc sáu hồ sơ admin mới xác nhận revision/cờ mặc định và payload an toàn.
- Kiểm thử backend/browser dùng DB test riêng và chạy tuần tự. Server kiểm thử
  8001/3001 đã dừng; khởi động backend/frontend theo [run-local.md](run-local.md).

Hướng dẫn sử dụng, chính sách và phần cần phát triển tiếp:
[account-management.md](account-management.md). Chưa có MFA, email xác minh/
khôi phục tự động, nhập hàng loạt hoặc quyền phụ huynh/giáo viên theo lớp.

## Phân hệ lớp 3 và gợi ý VIP — 10/10/2026

- Bổ sung 21 chủ đề/kỹ năng, 68 bài học, 384 câu hỏi riêng biệt và 56 đề lớp 3.
  Số lượng từng môn và tỷ lệ Free/VIP bằng bộ mẫu lớp 4: Toán 25/142/21,
  Tiếng Việt 23/130/19, Tiếng Anh 20/112/16. Free 46 bài/228 câu/34 đề;
  VIP 22 bài/156 câu/22 đề. Ngữ liệu tự biên soạn, có mục tiêu, ví dụ, ghi nhớ,
  gợi ý, tự giải thích và một số minh họa SVG. Các câu đọc kèm ngữ liệu độc lập.
- Lớp 3 tích hợp danh mục môn/chủ đề, học bài, bài tập, kế hoạch, Góc tư duy,
  công cụ VIP và quản trị hiện có. Chọn lớp mặc định theo hồ sơ; chọn bộ lọc
  không tự thay đổi lớp/quyền học. Admin lọc lớp 3 và xem bảng học liệu thực tế,
  phần còn thiếu và nguồn chương trình. Không tuyên bố hoàn thành cả chương trình.
- Gợi ý lớp 3: Free 1 định hướng, VIP 3 theo bước định hướng/cách làm/kiểm tra.
  Backend cắt văn bản VIP trước khi trả JSON, kiểm tra tính năng gói live,
  `hint_access` giải thích số gợi ý và `no-store` tránh lưu quyền/nội dung.
  Mục tiêu/ví dụ và lời giải sau nộp vẫn đầy đủ cho Free. Admin xem toàn bộ và
  cấu hình số gợi ý Free trong editor; bài cũ không có chính sách giữ cách cũ.
- Migration **0009_guided_hints** thêm `learning.guided_hints` cho gói VIP;
  không đổi membership/thời hạn hay bảng học tập. Lệnh `seed-grade3-content`
  chỉ nạp nội dung, có advisory lock/transaction/ID ổn định. Full seed development
  nạp cả hai lớp, giữ tương thích các hàm/lệnh lớp 4; verify hỗ trợ `--grade 3`
  và đếm câu riêng biệt qua các phiên bản.
- Trình soạn câu hỏi hỗ trợ các lựa chọn chỉ khác chữ hoa cho bài chính tả;
  vẫn chuẩn hóa NFC/whitespace và chặn lựa chọn trùng hệt nhau. Chấm vẫn theo
  id lựa chọn, không suy ra đáp án từ chữ hoa.
- Đã qua **377 backend tests**, gồm kiểm tra đáp án độc lập theo văn bản/phép tính
  của toàn bộ 384 câu lớp 3, schema editor, số lượng/gói, seed lặp giữ bản sửa,
  quyền theo lớp, hết hạn/thu hồi/tắt tính năng gợi ý, admin và làm/nộp/chấm bài
  thật ở cả ba môn. **19 component tests**, typecheck/lint/format và production
  build frontend đã qua. Backend/browser dùng database test riêng, chạy tuần tự.
- DB local hiện tại đã có cả hai lớp, mỗi lớp đúng 68/384/56; head mới đã áp dụng.
  Seed lớp 3 lặp hai lần: snapshot mọi hàng/cột/số lượng hiện tại trước/sau giữ
  nguyên. Đối chiếu snapshot trước đợt tài khoản xác nhận học liệu lớp 4, attempts,
  answers và tiến độ cũ giữ nguyên; SQL schema gốc không đổi. Snapshot lịch sử
  khác một số dữ liệu vận hành tài khoản/phiên/recommendations; không khôi phục
  hoặc ghi đè các dữ liệu đó.

Nguồn chương trình, giới hạn học liệu và cách nạp/vận hành:
[grade3-curriculum.md](grade3-curriculum.md). Local/VPS và README đã cập nhật.

Browser: **22 kịch bản hồi quy** và **2 kịch bản lớp 3 desktop/mobile** đã qua
trên bản production preview. Kịch bản mới kiểm tra ba môn, lớp theo hồ sơ,
bảng quản trị/editor, gợi ý Free 1 → cấp VIP 3 → thu hồi còn 1, không lộ văn bản
VIP trong JSON/DOM Free và không tràn trang ở 320/768/1280 px. Lượt đầu bộ
chọn nhãn `Lớp` của test quá chặt; sửa selector và chạy lại cả hai project lớp 3
đã qua. Đã xem ảnh bài học. Sau chỉnh bộ đếm CLI, chạy lại 79 kiểm thử liên quan
(78 qua và kiểm thử inventory qua khi sửa fixture dùng bản nháp đúng constraint).
Không chạy kiểm thử ghi trên DB thật. Server kiểm thử 8001/3001 đã dừng;
khởi động bản local theo [run-local.md](run-local.md).

## Rà soát sẵn sàng triển khai · 10/10/2026

Đã bổ sung bộ production có sẵn trong repo, tách role migration/runtime, Caddy
HTTPS/trusted proxy/body limit, Dockerfile không hot reload và user không phải
root; backup script và bootstrap admin đầu tiên không ghi đè tài khoản.
Admin có **Kiểm tra hệ thống**; CLI check-system chỉ đọc và cleanup-auth mặc định
dry-run. Readiness đối chiếu DB/head trực tiếp, cache cấu trúc 60 giây;
auth/quyền tiếp tục kiểm tra DB. Cấu hình chặt hơn, có timeout DB, mã tra cứu lỗi
và giới hạn login từng account/IP để nhiều học sinh dùng chung mạng.

| Kiểm chứng lần này                                                | Kết quả                                                                                                   |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Backend toàn bộ unit/integration/concurrency trên DB test riêng   | **402 passed**, 332.77 giây; 1 deprecation warning Starlette/httpx                                        |
| Cấu hình và phản hồi lỗi sau tinh chỉnh cuối                      | **15 passed**; không in secret cấu hình, từ chối placeholder production, mã hỗ trợ khớp log               |
| Frontend component tests                                          | **19 passed**                                                                                             |
| Playwright desktop/mobile, không skip                             | **26 passed**, 2.2 phút; accounts, authoring, lớp 3–4, Free/VIP, hints, sessions, learning, system status |
| Ruff check/format, ESLint, TypeScript, Prettier, production build | Pass                                                                                                      |
| Npm audit và pip-audit requirements-lock                          | Không ghi nhận lỗ hổng đã biết tại thời điểm kiểm tra                                                     |
| Production config riêng: docs/OpenAPI tắt, health                 | Pass bằng TestClient; không truy cập/ghi DB thật                                                          |
| Docker Compose production config --quiet                          | Pass; không in secrets; chưa build/run container                                                          |
| Caddyfile validate bằng Caddy 2.11.7 chính thức                   | Pass; checksum release đã đối chiếu; chưa chạy HTTPS/cấp chứng chỉ thật                                   |
| Backup và restore rehearsal bằng PostgreSQL 18 local              | Pass: pg_dump DB test, pg_restore vào DB test mới, schema/head/system checks đều đạt                      |
| Check-system và cleanup-auth dry-run trên DB local đang sử dụng   | Pass; head 0009, không thiếu policy/đề lỗi theo tiêu chí kiểm tra; không dọn dữ liệu                      |

Không thêm migration trong đợt vận hành này, không thay SQL gốc, mật khẩu/gói học
hay lịch sử ở database hiện tại. Database phục hồi thử được giữ riêng
`viettree-restore-test-2d8276df8ae8`, không nối dịch vụ học sinh vào DB này.
Không reset/drop database test hoặc database đang sử dụng. Server kiểm thử
8001/3001 đã dừng sau kiểm thử; khởi động local theo hướng dẫn để tải code mới.

Docker Engine trên máy chưa chạy: chưa chứng minh image chạy trên Linux/VPS.
Cần kiểm tra HTTPS, role DB đích, backup/restore trên server, tải dự kiến và quy
trình dữ liệu học sinh trước mở truy cập. Chi tiết:
[production-readiness.md](production-readiness.md), [deploy-vps.md](deploy-vps.md).

## AI Academy · 12/10/2026

Đã triển khai module dùng cùng auth/FreeVIP/profile/class/guardian/media/consent,
không ứng dụng thứ hai. Migration `0010_ai_academy` thêm 29 bảng riêng, JSONB
version và FK giữ lịch sử. DB local đã backup trước, migrate/seed thành công;
hash mọi hàng cũ đối chiếu lại vẫn nguyên vẹn. Mật khẩu/gói học không đổi.

48 bài/336 bước/144 câu checkpoint: lớp 4 là 36 tiết/9 chủ đề, các khối
1/2/3/5 có khung năm và 3 mẫu mỗi khối. 10 loại hoạt động + lab 24 mẫu + Prompt
Builder, 5 dự án, 12 huy hiệu. 315 SVG file thật: 8 mascot/19 cover/48 hero/
144 minh họa/72 thẻ/12 badge/12 UI; manifest/hash/alt/mapping kiểm thành công.
AI4-12 có phiên bản 2 sửa mapping ảnh giải thích 3/8, giữ bản 1 và tiến độ đã ghim.

Player chấm/resume/ghi điểm, Free 1/VIP 3 mức gợi ý, tutor simulation và Ollama
adapter có policy/consent/quotas; xưởng sáng tạo 4 loại mẫu, nháp/nộp riêng;
teacher giao bài/CSV/rubric, guardian xác minh/chấp thuận/export/yêu cầu gỡ text;
CMS nháp/duyệt/xuất bản/ẩn/nhân bản/chủ đề mới/upload và duyệt ảnh/job SVG;
admin lớp/ghi danh/liên kết phụ huynh/quyền/chính sách/mẫu hướng dẫn/cảnh báo/yêu cầu riêng tư.

Browser chạy toàn bộ 32: 30 qua trong lượt 2,8 phút; hai teacher/guardian fail do
selector getByLabel trên textarea sau remount. Đổi sang role textbox, chọn nút
logout đầu tiên (Shell có hai nút), chạy lại cả desktop/mobile: **2 passed**,
8,6 giây, không skip. Như vậy 32 kịch bản đã qua, bao gồm 26 hồi quy LMS cũ.
Visual smoke desktop/mobile không overflow, không ảnh hỏng hoặc pageerror/5xx;
hình phân số khác dữ kiện được phát hiện và sửa bằng phiên bản mới.

19 frontend components, ESLint/TypeScript/Prettier và build production qua.
Ruff app/tests/scripts/migration 0010 qua; migrations 0001/0002/env cũ có style
khác baseline, không chỉnh lại chúng trong đợt này. Pip-audit lock với metadata
PyPI: không lỗ hổng đã biết. Compose production config --quiet, Caddy validate
và bash syntax backup qua; Docker Engine chưa chạy nên chưa run image/HTTPS.
Backup script đã mở rộng cặp dump+media archive, chưa chạy cặp này trên Docker.

Backend hồi quy toàn bộ **468 passed**, 379,55 giây; sau bổ sung chất lượng/mục
bài được giao **67 kiểm thử Academy passed**, 39,45 giây. Tập 67 là phần kiểm
lại module và một test mới, không cộng dồn vào 468. Một warning Starlette/httpx
về deprecated adapter test, không lỗi chức năng.
Admin Tổng quan có độ phủ 48/48 và cảnh báo cấu trúc/đáp án/media approved/rubric;
chỉ đọc, không tự sửa nội dung của giáo viên. Wheel được kiểm chứa 315 SVG cùng
schema và manifest. Tài liệu [AI Academy](ai-academy/README.md),
[báo cáo đầy đủ](ai-academy/completion-report.md) nêu phạm vi đã làm và còn thiếu;
không coi adapter mock là model đã chạy, hoặc simulation là nhận dạng ảnh thật.

Smoke cuối trên 4 trang xác nhận mapping 3/8 đúng trên desktop/mobile, bài được
giao hiện ở Hành trình, admin có độ phủ 48/48 và không cảnh báo chất lượng.
Server kiểm thử 8001/3001 đã dừng. Build local được trả về backend 8000;
dùng run-local để mở lại.

## Lớp, thành tích, giá và đào tạo AI Free/VIP · 12/10/2026

Đã áp dụng `0011_classes_vip_training` trên DB local sau native PostgreSQL
backup; đối chiếu hash mọi hàng/cột cũ vẫn nguyên vẹn. Head/check-schema/
check-system và verify-ai-academy đạt, chất lượng 48/48, không thiếu media.
Tám bảng mới giữ batch giao bài, snapshot tuyên dương, giá/ưu đãi/nguồn thị
trường; thêm revision lớp, biệt danh và chính sách Free/VIP từng bài AI.

- VIP: replay thao tác cũ trả quyền hiện tại, không cộng ngày hoặc báo gói đã
  thu hồi còn hiệu lực; gia hạn gói đã thu hồi cần cấp mới. Chỉ cấp/gia hạn
  học sinh còn hoạt động và plan đang mở. Thu hồi chặn nội dung và grants
  attempts cũ ngay cả khi cấp lại. Khóa/idempotency/audit giữ thao tác đồng thời.
- Admin tạo/sửa lớp, phân giáo viên, trường/năm học, ghi danh/chuyển ra/đóng
  lớp; học sinh tự do vẫn dùng được. Teacher chỉ quản lý lớp phụ trách.
  Giao bài đọc/bài chấm/AI cho cá nhân hoặc cả lớp, kiểm quyền người nhận,
  idempotency và hạn; lịch sử không bị xóa khi rời lớp.
- Thành tích năm loại: Toán, Tiếng Việt, Tiếng Anh, checkpoint AI, sản phẩm
  AI đã chấm. Trung bình thang 100 của kết quả tốt nhất mỗi bài; không cộng
  điểm từ lượt lặp/VIP. Bảng riêng theo tuần/tháng, biệt danh với học sinh,
  tuyên dương tối đa ba người có kết quả thật, snapshot không tự viết lại.
- AI Academy: giữ 48 bài/315 hình; 7 Free / 41 VIP, lớp 4 là 3 / 33. Lab,
  Prompt Builder, studio/dự án từ mẫu thuộc VIP. API kiểm quyền mỗi bước,
  giữ progress/kết quả sau thu hồi; tranh nội dung bị khóa có no-store.
  `AI_TRAINING_ONLY=true` chặn model dù cờ/consent cũ bật; hướng dẫn và soạn
  nháp dùng mẫu. Admin chỉnh Free/VIP từng bài bằng mật khẩu/lý do/revision.
- Giá tham khảo có khảo sát Monkey/OLM/Edupia và giới hạn nguồn rõ ràng.
  Đề xuất 99k/269k/899k cho 30/90/365 ngày; sale 79k/219k/699k đến hết
  12/11/2026 giờ Việt Nam. Admin chỉnh giá/ưu đãi có audit/CAS/xác nhận;
  hết hạn tự bỏ sale, nhiều ưu đãi chọn giá thấp nhất, không cộng dồn.
  Chưa tích hợp thanh toán, xem giá không cấp gói hoặc ghi doanh thu.

Kiểm chứng đợt này:

| Kiểm tra                                           | Kết quả                                                                                                        |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Backend toàn hệ thống trước bổ sung ba ca cuối     | **476 passed**, 397,10 giây                                                                                    |
| Hai ca VIP đồng thời bổ sung                       | **2 passed**, 5,20 giây                                                                                        |
| Tập Academy/lớp/membership/concurrency sau mở rộng | 97/98 qua; một assertion phân biệt bài riêng/theo lớp trong test được sửa                                      |
| Toàn bộ 10 ca lớp/giá/quyền AI sau sửa và bổ sung  | **10 passed**, 29,52 giây; có điểm Toán, rubric đúng lớp, đổi policy live và promo CAS                         |
| Frontend                                           | **19 component tests**, ESLint/TypeScript/production build đạt                                                 |
| Browser toàn hệ thống 36 desktop/mobile            | 34 qua lượt đầu; sau sửa, cả **6 ca liên quan đạt**, 33,3 giây; tổng 36 kịch bản riêng biệt đã đạt, không skip |
| Database thực tế                                   | Head 0011, schema/system/48 bài/315 SVG đạt; mọi hàng/cột cũ giữ nguyên                                        |
| Đóng gói                                           | Wheel có hai schema SQL Academy/lớp và 315 SVG; Compose production config --quiet đạt                          |

Không cộng dồn các tập kiểm thử lặp thành số kiểm thử mới. Một warning
Starlette/httpx về adapter test deprecated; không lỗi chức năng. Browser đã
phát hiện và sửa duplicate key làm danh sách lớp cũ còn hiện, đồng thời giữ
form giao bài khi roster làm mới. Kiểm thử đọc bài chờ phản hồi lưu trước
khi điều hướng. Ảnh top 3 desktop/mobile được kiểm tra; trang không tràn ngang.
Docker Engine/HTTPS trên VPS và tải thực tế vẫn cần kiểm chứng tại server đích.

Smoke cuối trang giá và đổi lớp tại 1280/390 px đạt: không pageerror/5xx/tràn
ngang, đổi lớp không lặp danh sách. Checkbox lớp/ưu đãi được chỉnh cùng hệ
style tài khoản, đúng kích thước. Build cuối đã trả về API local 8000;
server kiểm thử 8001/3001 đã dừng, server đang chạy của người dùng không bị dừng.

Tài liệu: [lớp và thành tích](classes-achievements.md),
[đào tạo AI Free/VIP](ai-training-vip.md), [khảo sát giá](vip-pricing-research.md),
[chạy local](run-local.md). Không reset/seed lại tài khoản hiện có.

## Học liệu lớp 1–2 · 12/10/2026

Đã bổ sung và nạp vào DB local hai bộ ba môn, cùng quy mô lớp 3–4:

| Môn, mỗi khối | Chủ đề | Bài học Free / VIP | Câu hỏi | Đề luyện tập |
| ------------- | -----: | -----------------: | ------: | -----------: |
| Toán          |      8 |             18 / 7 |     142 |           21 |
| Tiếng Việt    |      6 |             15 / 8 |     130 |           19 |
| Tiếng Anh     |      7 |             13 / 7 |     112 |           16 |
| Tổng          |     21 |            46 / 22 |     384 |           56 |

Hai khối thêm **136 bài / 768 câu / 112 đề**, chưa tính AI Academy. Khảo sát
phụ lục chương trình Bộ GDĐT đăng trên website trường công lập; nguồn,
phạm vi và lưu ý dự thảo tiếng Anh 2026 có trong
[thiết kế học liệu](grades1-2-curriculum.md). Ngữ liệu tự viết; bộ này bổ trợ,
không thay toàn bộ sách/chương trình năm hoặc đánh giá nghe/nói/viết mở.

Lớp 1 học khoảng 6 phút/bài, lớp 2 khoảng 8 phút; hướng dẫn làm 2–3 câu rồi
nghỉ, lưu bài để học tiếp. Đề nền tảng lớp 1 chỉ hai lựa chọn, tối đa ba ở
phần sau; lớp 2 có điền số ngắn. VIP vận dụng trong kiến thức đúng tuổi,
không yêu cầu phân số, diện tích hay bài toán hai bước. Gợi ý Free 1/VIP 3
lọc tại API và đổi ngay khi cấp/thu hồi. Bài nghe/nói thực hành cùng người
lớn, chưa có âm thanh chuẩn hoặc chấm phát âm tự động.

Thêm minh họa đếm 0–20 chấm và thẻ chữ/từ lớn 26px; admin soạn/preview được,
thẻ xuống hàng trên điện thoại. Map chương trình và kiểm tra chất lượng hỗ
trợ cả lớp 1–4; chọn khối trong hồ sơ/danh mục/giao bài vẫn kiểm quyền cũ.

Hai CLI `seed-grade1-content` / `seed-grade2-content` chỉ nạp học liệu,
giữ khóa/transaction/id ổn định, không tạo/reset tài khoản. Backup native
PostgreSQL trước nạp; đối chiếu hash sau nạp xác nhận mọi hàng/cột cũ còn
nguyên. Không cần migration mới, head vẫn `0011_classes_vip_training`.
[CSV đủ 136 bài](grades1-2-lessons.csv) đã đối chiếu mã với DB thực tế.

Kiểm chứng đợt này:

| Kiểm tra               | Kết quả                                                                                                                                                                                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend toàn hệ thống  | 626/627 qua lượt đầy đủ (905,35 giây); assertion cũ coi lớp 1 chưa có bài được chuyển sang lớp 5, ca đó và hai ca kế hoạch/gợi ý liên quan chạy lại **3 passed**. Tổng 627 ca riêng biệt đã qua, không cộng dồn lượt lặp                                |
| Học liệu mới           | 146 ca trong tập backend: cấu trúc 136 bài/768 câu, đáp án Toán độc lập, inventory, seed lặp giữ sửa đổi, quyền/gợi ý và toàn bộ 112 đề lưu/nộp/chấm                                                                                                    |
| Browser desktop/mobile | 37/40 qua lượt đầy đủ; hai assertion lớp chưa có bài cập nhật sang lớp 5 và lỗi điều hướng sau đổi mật khẩu được sửa. Cả **14 ca liên quan passed**, gồm bốn ca lớp 1–2, tài khoản, hành trình và phiên; tổng 40 kịch bản riêng biệt đã qua, không skip |
| Frontend               | 19 component tests, ESLint, TypeScript và production build qua                                                                                                                                                                                          |
| Database thực tế       | Schema/system đạt; verify-seed lớp 1/2 đúng 68 bài/384 câu/56 đề mỗi khối; dữ liệu cũ giữ nguyên                                                                                                                                                        |

Đã sửa duplicate React key khi đổi khối trong map chương trình để chỉ còn
một bảng hiện hành. Trang login chỉ chuyển hướng khi URL thực sự còn ở
`/login`, tránh trang được Next giữ lại gây chuyển về dashboard sau đổi mật
khẩu. Một warning Starlette/httpx về adapter test deprecated, không lỗi
chức năng. Các test ghi dữ liệu dùng DB test riêng.

Visual smoke thẻ từ lớp 1/2 trên 1280px và 390px đạt: chữ 26px, không
tràn ngang, pageerror hoặc HTTP 5xx; ảnh đếm và thẻ đã kiểm tra trực quan.
Wheel chứa đủ năm module học liệu mới. Build cuối trả về backend local
8000; server kiểm thử 8001/3001 đã dừng. Các server của người dùng và `.env`
không bị thay đổi. Dùng [run-local](run-local.md) để khởi động lại ứng dụng.

## Tổ chức lại kiến trúc và tài khoản theo khối · 12/10/2026

Thư mục gốc backend còn sáu file entry point/hạ tầng. Các file học liệu
`grade3_*`, `early_primary_*`, `*_curriculum` chuyển vào
`curriculum/grades/{early_primary,grade_03,grade_04}`. Builders dùng chung
tách khỏi nội dung lớp 4; registry tập trung chọn pack/map/source/inventory.
API LMS 875 dòng chia thành router auth/catalog/learning/assessments/attempts/
administration; cùng các router chức năng được đăng ký tại `api/router.py`.
Schema chia theo chức năng, seed tài khoản tách khỏi seed học liệu.
Không giữ các file tên cũ để chuyển tiếp import. Có EditorConfig và Ruff
chuẩn hóa LF; cập nhật import/tests/tài liệu/lệnh deploy.

Frontend chia các file student/admin/authoring/accounts/classrooms lớn thành
page/form/types/shared theo feature. Lesson studio tách nội dung và minh họa
thành component riêng. URL/entry point/Docker/Alembic giữ nguyên. So sánh
source hashes xác nhận toàn bộ ngữ liệu/câu hỏi giữ nguyên; OpenAPI endpoint,
request/response và validation tương đương, chỉ hai component ID nhận tên
module mới. Client sinh từ OpenAPI nên sinh lại kiểu khi cần.

Bổ sung CLI `curriculum-inventory --grade 1` kiểm kê source không cần DB;
`seed-grade-content --grade 1` nạp đầy đủ một khối, không tài khoản. Các CLI
khối cũ vẫn hoạt động. Admin xuất bảng học liệu CSV đúng bộ lọc khối/môn/mạch
thiếu Free; UTF-8 BOM, escape nội dung và chặn công thức từ text.

Đã tạo **12 tài khoản lớp 1–3**, hai Free/hai VIP 90 ngày mỗi khối; giữ nguyên
bốn tài khoản lớp 4. `seed-demo-learners --grades 1 2` chọn khối; chạy lại giữ
mật khẩu, khối, khóa, gói đã thu hồi/hết hạn. Lệnh chặn ngoài development,
collision vai trò hoặc thiếu admin/hồ sơ; cấp VIP qua service có audit.
Backup PostgreSQL trước thay đổi, hash sau tạo xác nhận mọi hàng/cột cũ
giữ nguyên. Không migration mới, head vẫn `0011_classes_vip_training`.

Backend toàn bộ **639/640** qua lượt đầy đủ, 1015,16 giây; một test đồng thời
còn import module API cũ đã sửa. Cả **4 ca account concurrency passed**,
21,08 giây sau sửa; tổng 640 ca riêng biệt đã qua, không cộng lượt lặp.
13 ca mới bảo vệ registry, seed lặp, đăng nhập/quyền theo khối, bảo toàn
tài khoản, chặn production/collision và ranh giới phụ thuộc học liệu.
Frontend **21 tests passed**, gồm hai ca CSV; lint/TypeScript/build đạt.
Wheel build ở thư mục mới có module đúng, hai SQL schema domain và 315 SVG,
không còn module gốc cũ trong gói. Schema/system DB thật đạt.

Browser toàn bộ **40 passed**, 3,5 phút, desktop/mobile, không skip; gồm tạo/
duyệt/xuất bản bài và câu, lưu/nộp/chấm, phiên/tài khoản, cấp/thu hồi VIP,
lớp/giao bài/top 3, AI Academy và xuất CSV lớp 1/2. Visual admin 1280/390px
đạt, CSV hiển thị và không tràn ngang/pageerror/5xx. Cấu hình build cuối trả
về backend local 8000; server test 8001/3001 đã dừng, không dừng server của
người dùng. Kiểm thử Docker Engine/HTTPS/tải VPS vẫn thực hiện tại server đích.

Tài liệu: [kiến trúc và cách nâng cấp](architecture.md),
[demo theo khối](demo-accounts.md), [chạy local](run-local.md), [VPS](deploy-vps.md).

## Lớp 5 và thư viện bài học · 13/10/2026

Bổ sung pack `curriculum/grades/grade_05` cho Toán, Tiếng Việt, Tiếng Anh:
**68 bài / 384 câu / 56 đề**, gồm 46 bài/34 đề Free và 22 bài/22 đề VIP.
Toán 9 chủ đề, 25 bài/142 câu/21 đề; Tiếng Việt 6 chủ đề, 23/130/19;
Tiếng Anh 7 chủ đề, 20/112/16. Tổng năm khối 340 bài/1920 câu/280 đề,
chưa tính AI Academy hoặc học liệu do giáo viên tạo. Registry giữ expected
theo từng pack; không ép số chủ đề Toán lớp 5 bằng các khối trước.

Đối chiếu phần lớp 5 trong chương trình Toán/Ngữ văn/Tiếng Anh, cùng văn bản
sửa đổi 17/2025; nguồn và phạm vi ở [học liệu lớp 5](grade5-curriculum.md).
Ngữ liệu gốc do VietTree tự viết: truyện 312/330 tiếng tính cả nhan đề,
miêu tả khoảng 220–230, thơ 123, giải thích 230; Tiếng Anh 62–69 từ mỗi bài.
Toán dùng phép tính decimal/fraction chính xác; chấp nhận phẩy/chấm trong
câu điền thập phân. Nghe/nói và văn mở cần người hướng dẫn, chưa có audio hay
chấm tự luận. Không khẳng định đã phủ đầy đủ kế hoạch năm học.

Học sinh có **Thư viện bài học** (`/student/lessons`): tìm tên/chủ đề không dấu,
lọc môn/gói/tiến độ/bài tư duy, phân trang 12 bài, trạng thái và quyền hiện hành.
API chỉ trả metadata bài đã xuất bản, môn/chủ đề hoạt động và tiến độ của chính
học sinh, đúng khối hồ sơ; không trả nội dung VIP, gợi ý hay đáp án qua danh mục.
Tiến độ và quyền dùng `no-store`; mở bài vẫn kiểm quyền ở backend.

Admin chọn khối ở đầu trang chương trình, xem tổng theo bộ lọc, mở/thu gọn
chủ đề và xuất CSV. Editor/preview hỗ trợ thêm tam giác, hình thang, hình tròn,
hộp chữ nhật và biểu đồ quạt tròn. Hình thang có thể đảo độ dài hai đáy;
biểu đồ có tổng 100%, chú giải chữ, xử lý nhóm 0%/100%. Số đo có thêm chữ
20/24 px để đọc trên điện thoại; backend từ chối số đo/nhãn/tổng không hợp lệ.

Nạp grade 5 hai lần trên DB local sau pg_dump; lần hai không tăng số lượng.
Tạo `free5_01`, `free5_02`, `vip5_01`, `vip5_02`; VIP mới 90 ngày. Chạy lại giữ
mật khẩu/hồ sơ/gói. So sánh hash xác nhận mọi hàng/cột cũ của DB thật còn nguyên;
hash toàn bộ nội dung/câu hỏi/gợi ý/đáp án lớp 1–4 không đổi. Head vẫn
`0011_classes_vip_training`; không cần schema migration mới. `check-system`
trên DB local đạt, không thiếu quyền hoặc có đề lỗi. Wheel chứa đủ bảy module
grade 5 và cả SQL schema domain.

Backend lượt đầy đủ cuối **725/725 passed**, 1162,29 giây, không skip. Bao gồm
ba ca kiểm thời điểm giao dịch và cập nhật assertion cũ về lớp 5. Bộ mới kiểm
schema 68 bài/384 câu, đáp án Toán độc lập, độ dài
ngữ liệu, toàn bộ 56 đề lưu/đọc lại/nộp/chấm, seed lặp, tìm kiếm/phân trang,
quyền riêng tư, nháp/chủ đề đóng, gợi ý/cấp/thu hồi VIP. Kiểm thêm Góc học VIP
và kế hoạch theo kỹ năng cho lớp 5. Ruff lint/format đạt.

Frontend **25 component tests passed**, ESLint, TypeScript và production build
đạt. Danh mục CSV, hướng dẫn local/VPS, kiến trúc, demo và roadmap cập nhật.
README dùng tham chiếu biến môi trường cho mật khẩu demo.

Lượt browser ban đầu phát hiện hai lỗi không ổn định: duyệt câu trả 200 nhưng
refresh chưa thấy đã duyệt; đăng nhập trả 200 nhưng mở bài ngay có thể nhận 401.
Kiểm thử ASGI/PostgreSQL độc lập tái hiện phiên chưa commit tại thời điểm gửi
HTTP. Sửa dependency database dùng chung `scope="function"` trên LMS, auth,
AI Academy và lớp học; commit/rollback trước phản hồi. Tăng mức FastAPI tối
thiểu lên 0.121 (lock đang là 0.143.0). Có ba ca bảo vệ scope mọi route, commit
trước phản hồi và lỗi commit trả 503/rollback, không báo thành công giả.

Browser cuối trên DB riêng mới **42/42 passed**, 3,8 phút, không skip; gồm cả
hai luồng đã lỗi. DB `viettree-grade5-browser-test` được import SQL gốc,
migrate head, nạp năm khối và AI Academy, kiểm tra hệ thống đạt. Backend
pytest chạy trên `viettree-education-test`; hai bộ ghi tách DB.

Đã xem hình và thư viện trên desktop/mobile; số đo chữ lớn và chú giải biểu
đồ đọc được, kiểm tra tràn ngang đạt. Build cuối trả về backend local 8000;
server kiểm thử 8001/3001 đã dừng. Không sửa `.env` hoặc dừng server người dùng.
Cache `backend/build` cũ được lưu lại trong `.tools` rồi đóng wheel sạch;
so khớp mọi file Python với source, không còn module gốc cũ đi kèm.

## Cỡ chữ theo thiết bị · 13/10/2026

Thêm **Chữ gọn hơn**: giao diện 16 px, bài học 18 px, câu hỏi 20 px;
giữ hai mức vừa/lớn. Cân chỉnh padding, khoảng cách, tiêu đề và lựa chọn trên
màn hình nhỏ; nút chính vẫn tối thiểu 48 px. Có lối tắt **Cỡ chữ** trên LMS
và AI Academy; AI dùng 18/20/23 px. Sửa thứ tự ưu tiên CSS để câu hỏi dùng đúng
cỡ chữ ở cả ba mức, tránh bị quy tắc tiêu đề ghi đè.

Lưu `text_size_by_device` trong JSONB hồ sơ hiện có: điện thoại, máy tính bảng,
máy tính; thiết bị chưa chọn dùng mặc định cũ. Không cần migration hoặc ghi lại
dữ liệu thật. Khóa hàng trước khi gộp để hai thiết bị lưu đồng thời không làm mất
lựa chọn khác. Admin hỗ trợ mức mặc định gọn và giữ các lựa chọn riêng khi sửa
tài khoản. Đăng nhập, phiên, dashboard và hồ sơ trả cùng cấu hình.

Cache phiên cập nhật ngay sau lưu; BroadcastChannel báo các tab kiểm tra lại,
không gửi dữ liệu tài khoản. Kết quả cũ không ghi đè lần lưu mới, không khôi phục
phiên đã thoát hoặc ghi sang tài khoản khác. Nhận diện điện thoại/máy tính bảng
giữ ổn định khi xoay màn hình và thu nhỏ cửa sổ; không lưu định danh thiết bị.

Kiểm thử tập trung trên database riêng: **20 backend / 41 frontend passed**;
**11 browser passed**, bao gồm điện thoại, máy tính, máy tính bảng, ba cỡ câu hỏi,
màn hình 320–1280 px, AI, lỗi mạng, reload/đăng nhập lại, đổi tài khoản, đồng bộ tab,
quản trị tài khoản và phiên. Một lượt mobile bỏ qua ca đa thiết bị trùng lặp;
ca đó đã chạy cả ba nhóm bằng ba browser context trong lượt desktop.
Ruff, ESLint, TypeScript, Prettier và production build đạt.

Chi tiết sử dụng và API: [cỡ chữ học tập](reading-preferences.md).

## Học bằng hình và đủ AI lớp 1–5 · 13/10/2026

Bài học ba môn mở từng phần, đọc từng đoạn và có lựa chọn xem đầy đủ; giữ toàn bộ
ngữ liệu gốc và dòng thơ. Bổ sung 16 SVG từ vựng/truyện, hình phép cộng nhỏ, phân
số có phần bằng nhau và bảng các hàng của số. Chỉ minh họa dữ kiện phù hợp,
không hiểu nhầm số âm/thập phân hoặc từ “cá” trong “các”.

AI Academy có **180 bài / 1260 bước / 540 checkpoint**, mỗi khối 1–5 đủ **36 bài /
9 chủ đề**, baseline **3 Free / 33 VIP**. Lớp 1–2 khoảng 10 phút, hai thẻ;
lớp 3–5 khoảng 15 phút, lớp 5 tăng chất lượng dữ liệu, mẫu học/mẫu thử, tiêu chí,
thập phân/phân số/tỉ lệ và kiểm chứng. Tham khảo mục tiêu công khai Day of AI,
AI4K12 và Discovering AI 8–12; nội dung/ảnh tự biên soạn, không sao chép giáo án.

Giao diện mỗi lần một thẻ/câu, nút chạm thay dropdown/kéo thả, gợi ý không cần
gõ mô tả; gợi ý 1 Free, 2–3 VIP từ học liệu nội bộ. Menu công cụ và phần đọc
dài thu gọn; cập nhật đáp án bỏ trạng thái đạt cũ. Giữ font theo thiết bị.

Thư viện có **1547 SVG**: 315 cũ, 1232 bổ sung; đối chiếu số lượng và màu sắc với
nhãn. Màu đỏ có phiên bản sửa riêng, giữ ảnh và payload cũ. Ảnh thuộc bài VIP
vẫn khóa khi phiên bản được lưu trữ. Giáo viên sửa/nháp/vị trí/quyền riêng được
giữ; giữ tiến độ trỏ phiên bản đã bắt đầu. Không cần migration mới.

Đã pg_dump trước khi nạp trên database hiện tại, seed chạy lặp không tăng số lượng.
Kiểm hash mọi hàng cũ ngoài các cột AI được chủ động nâng cấp: không có thay đổi
ngoài dự kiến, không reset tài khoản/gói/kết quả. Đủ 180 baseline published,
1547 ảnh hợp lệ; `verify-ai-academy` và `check-system` đạt.

Kiểm thử tập trung: **214 backend** cho AI, hình, gợi ý, phiên bản/quyền riêng tư,
snapshot thư viện và giao dịch; **81 kiểm tra lớp 5** đã đạt, rồi kiểm lại các ca
thư viện sau sửa. **48 frontend** đạt. Lượt browser liên quan **21 passed**, gồm
năm khối trên desktop/mobile, Free/VIP, lưu/resume, CMS, giáo viên/phụ huynh,
ba môn, font và thư viện; một ca đa thiết bị trùng mobile được bỏ qua vì đã
thử cả ba nhóm trong lượt desktop. Hai ca browser bổ sung xác nhận minh họa màu đỏ
đạt trên desktop/mobile; hồi quy backend xác nhận ảnh VIP của bản lưu trữ vẫn
trả 403 cho tài khoản Free. Ruff, ESLint, TypeScript, Prettier và production build đạt.

Sửa lỗi tiến độ lúc chuyển nhanh sang thư viện: count/page dùng một snapshot SQL,
và phản hồi lưu thành công phát tín hiệu làm mới thư viện. Có hồi quy bằng hai
connection PostgreSQL chứng minh không lệch count với danh sách.

Tài liệu: [thiết kế và nguồn quốc tế](visual-learning-and-ai.md),
[danh sách 180 bài](ai-academy/lessons.csv).

## Rà soát tranh và thao tác học · 13/10/2026

Bổ sung 30 SVG nguyên bản cho đồ dùng, phương tiện, thời tiết, thức ăn, màu và
hình học; ba môn có tổng 46 tranh. Thẻ từ, đáp án trắc nghiệm và mục sắp xếp
hiển thị hình khi nhãn cụ thể phù hợp; giữ nguyên chữ và giá trị đáp án gửi backend.
Không suy đoán tranh từ câu phủ định, phép tính hoặc nhãn có số lượng khác một vật.
Bút mực và bút chì có tranh riêng, tránh lẫn nghĩa trong thẻ từ.

Tranh chỉ theo đoạn đang đọc; chuyển bài/bước mới đặt lại đoạn đầu. Hành trình
AI có biểu tượng, bước đang học và dấu hoàn thành; quay lại đóng gợi ý cũ,
khóa đổi bước trong lúc lưu/lấy gợi ý. Đổi tên nút giọng đọc thành “Nghe bài”;
giữ cờ bật/tắt và điều kiện giọng trên thiết bị đã có.

Đối chiếu lại mô tả công khai Day of AI, AI4K12 và Discovering AI. Đọc kiểm tra
database hiện tại: đủ 180 bài, mỗi lớp 36 bài, 1547 ảnh AI hợp lệ và không có
lỗi chất lượng tham chiếu. Lượt bổ sung giao diện không cần migration hoặc seed
lại dữ liệu bài học. Học liệu giáo viên và lịch sử phiên bản không bị ghi lại.

Kiểm thử: **54 frontend passed**; **4 backend** cho độ phủ năm khối và độ đúng
của tranh; **12 browser AI/quan sát đã đạt**, thêm **2 browser thẻ từ/đáp án**
đạt sau kiểm tra cuối. Browser chạy Chrome desktop và mô phỏng mobile; thêm
kiểm tra chiều rộng 320/390/768/1280 px, lưu/reload, chuyển bước và đóng gợi ý.
ESLint, TypeScript, Prettier và production build đạt. Tài liệu chi tiết:
[học bằng hình](visual-learning-and-ai.md).

## Tự lưu và rà soát học liệu · 14/10/2026

Bài luyện tự lưu sau 0,8 giây; một request mỗi lần, giữ bản sửa mới khi phản hồi
cũ đến muộn, chờ lưu hết trước đổi câu/nộp hoặc chuyển bằng liên kết nội bộ.
Lỗi mạng giữ đáp án trên trang, có retry thủ công/online; request treo dừng sau
15 giây. Cảnh báo đóng/reload khi chưa lưu; không lưu đáp án trong localStorage.
Không bảo đảm khôi phục phần chưa lưu nếu đóng trang/tắt máy hoặc dùng Back.

Backend nhận mốc request trước xác thực/DB, conditional upsert theo answered_at
chặn request cũ xử lý muộn. Giữ khóa chủ bài, quyền Free/VIP, CSRF, thời hạn và
chấm điểm trên server. GET attempt bổ sung server_time; đồng hồ giao diện dùng
mốc server, nhắc hai phút, không tự nộp hoặc thay đổi hạn làm bài.

Admin có rà soát độ dài/câu dài, phần trống, hình và gợi ý/giới thiệu VIP trước
khi duyệt. Chỉ gợi ý biên soạn, giữ validation/revision và quy trình xuất bản.
Không thêm migration, không seed hoặc sửa dữ liệu học tập hiện tại.

Kiểm thử: **66 frontend passed**. Lượt backend ban đầu có **36 ca đạt**, sau đó
chốt **6 ca đạt** cho clock/API, request cũ, nộp/chấm, quyền chủ bài, thời hạn
và dependency transaction. Lượt browser cuối **10 passed** trên desktop/mobile,
gồm lỗi mạng, response chậm, chuyển trang, lưu/reload, kết quả, admin/CMS và tranh.
`check-system` trên DB hiện tại đạt, head giữ 0011_classes_vip_training. Ruff,
ESLint, TypeScript, Prettier và production build đạt.

Chi tiết: [tự lưu bài và rà soát học liệu](learning-reliability.md).

## Rà soát học liệu, tải 50 học sinh và VPS · 14/10/2026

Đối chiếu nguồn và 1.920 phiên bản câu hỏi trong đề xuất bản: không lỗi cấu
trúc đáp án. Bộ giải độc lập bao phủ 710 câu Toán năm khối, đủ ba môn lớp 3
và các câu vận dụng lớp 4; bổ sung bộ 88 câu Toán lớp 4. Môn ngôn ngữ có
đọc đối chiếu và một lưu ý biên tập Tiếng Anh lớp 5 trong báo cáo chi tiết;
không coi kiểm tra schema là chứng nhận mọi câu đều chính xác.

Tách ngữ liệu khỏi câu hỏi, đọc từng đoạn, giữ dòng trắng giữa khổ thơ và tăng
độ đậm chữ đọc. Chấm điền khuyết chấp nhận cách viết số tương đương có kiểm
soát, vẫn giữ dấu Tiếng Việt và yêu cầu rút gọn phân số. Dashboard chỉ đọc,
không giữ khóa hồ sơ/ghi gợi ý khi chuyển trang; gợi ý vẫn dựa trên kết quả.

Rate limit hoàn tất trước kết nối API; worker mới tự nạp metadata khi đăng
nhập đầu tiên. Giới hạn Argon2, số worker/concurrency/kết nối và chờ khóa DB.
Thống kê nộp bài chỉ tổng hợp câu vừa chấm và ngày/môn của học sinh; khóa
phối hợp với lệnh rebuild toàn bộ, cùng câu và hai tab của một học sinh.
Không thêm migration hoặc sửa dữ liệu DB học tập đang dùng.

Chứng cứ kiểm thử:

| Phạm vi                                                    | Kết quả                                                                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Toàn bộ backend trước các bổ sung cuối                     | 926 ca đã chạy: 925 đạt; một test gọi login bằng chữ ký cũ đã cập nhật và chạy lại đạt (`--lf`, cùng 4 ca account concurrency) |
| Toàn bộ không cần DB sau bổ sung giới hạn                  | 750 passed; 9 ca cần DB bỏ qua trong lượt này, 171 integration không chọn; các ca DB đã được chạy riêng/toàn bộ                |
| Sửa dashboard/điền khuyết/API/quyền/tải/vận hành liên quan | 37 passed sau thay đổi cuối, gồm DB mất kết nối, khóa hồ sơ, dashboard READ ONLY, nộp đồng thời và toàn bộ integration API     |
| Frontend component                                         | 68 passed                                                                                                                      |
| Browser tổng hợp                                           | 25 passed; một biến thể mobile bỏ qua có chủ ý vì desktop đã kiểm tra ba thiết bị trong cùng ca                                |
| Đọc câu hỏi sau sửa dashboard                              | 8/8 desktop/mobile Free/VIP đạt khi đồng thời chạy tải 50 học sinh                                                             |
| Lặp kiểm tra chuyển nhanh/đọc/lưu sau sửa dashboard        | 24/24 đạt trong ba vòng, không còn lỗi chờ khóa đã tái hiện trước đó                                                           |
| Load ba vòng lưu đủ câu                                    | 2.310 request, 150/150 hành trình; không lỗi, không lệch tổng/statistics                                                       |
| Load sau sửa dashboard                                     | 50/50 đăng nhập; 770/770 request học tập, p95 1,11 giây; 50 bài khớp tổng ngày                                                 |
| DB hiện tại chỉ đọc                                        | check-system và verify-ai-academy đạt, head 0011_classes_vip_training, đủ 180 bài AI                                           |

Đã xác định lỗi chờ khóa khi rời dashboard bằng `pg_stat_activity`; giữ
profile lock và ghi gợi ý ở GET dashboard đã được bỏ. SQLSTATE được ghi vào
log an toàn; giới hạn chờ khóa trả 503 để thử lại thay vì chờ 30 giây.
Ruff, ESLint, TypeScript, Prettier và build production đạt. Compose/Caddyfile/
backup script kiểm tra cấu hình/cú pháp đạt. Phép đo dùng hai worker, PostgreSQL
thật trên máy Windows 12 logical CPU, dữ liệu/tài khoản mô phỏng ở DB test.

Chưa build/run container Linux, xác nhận HTTPS/reboot/backup trên VPS thật;
Docker Engine local chưa chạy và chưa có thông tin truy cập VPS. Chưa soak
test nhiều giờ hoặc benchmark lịch sử hàng triệu bài. Các số đo là mốc local
để triển khai staging, không cam kết công suất VPS.

Chi tiết, số đo trước/sau và cách chạy lại:
[content-load-vps-review.md](content-load-vps-review.md).

## Profile VPS tiết kiệm · 14/10/2026

Theo ngân sách gói 3 cores / RAM gốc 2 GB / SSD 50 GB, bổ sung
`docker-compose.small-vps.yml` và `.env.production.small.example`. Bốn dịch vụ
có giới hạn RAM tổng 1.440 MiB, backend một worker, hash/verify chung một slot,
pool API 4+2 và một kết nối riêng cho auth counter. PostgreSQL giảm bộ nhớ/số
kết nối/song song; Next standalone giới hạn V8 heap 192 MiB; log quay vòng.
Giữ dữ liệu, quyền, cấp VIP và toàn bộ học liệu. Không có migration mới.

Phát hiện thread chờ pool chiếm hết thread endpoint khi chỉ có một worker;
đã dùng limiter riêng cho chờ kết nối, commit/rollback và auth guard. Giữ
commit trước response, cleanup có shield khi request bị hủy. Readiness nạp
metadata trước khi proxy nhận người dùng. Hồi quy pool một kết nối / thread
endpoint một / sáu request đạt.

`deploy/compose.sh` chọn profile từ env mà không chạy file secret như shell;
backup dùng cùng wrapper và giữ project/volumes cũ. Helper PowerShell build
Linux amd64 trên máy khác, export image cùng gói cấu hình và SHA256. Profile
nhỏ loại bỏ build trên VPS. Đã kiểm tra cú pháp helper/wrapper, archive cấu
hình và contract Compose; chưa build image vì Engine local chưa chạy.

Kiểm thử: **754 unit đạt**, **76 tài khoản/vận hành**, **43 API/giao dịch/tải**,
**4 pool/commit**, **29 readiness/vận hành**, **2 deployment contract** đạt;
các nhóm có trùng nhau. **14 browser đạt** với frontend standalone/heap 192 MiB
và backend một worker. Thử tải 10/25/50 học sinh trên DB test: 50/50 login,
770 request ở mức 50 không lỗi, p95 khoảng 1,54 giây; thống kê khớp. Backend
được giới hạn affinity ba logical CPU trên Windows, working set đỉnh lấy mẫu
khoảng 174 MiB; chưa áp dụng cgroups hoặc đo tổng RAM cả stack.

Hướng dẫn, lệnh build/upload/load/backup và giới hạn kiểm chứng:
[deploy-small-vps.md](deploy-small-vps.md). Chưa triển khai/đo trên VPS thật.

## Rà soát tiếp ngày 15/10/2026

Kết quả học tập có đáp án đúng theo khóa chấm chính thức, giữ ngữ liệu riêng
và chia lời giải theo khối lớp. Hình luống rau dùng ô vuông đúng tỉ lệ; bộ
minh họa tránh diễn giải ngày/phân số âm/hỗn số thành phần tô màu dương.
Bộ đếm và bài nộp mới loại các câu đã xóa hết nội dung, vẫn giữ thao tác xóa
trong tự lưu. API frontend có timeout gồm tải JSON, giữ hủy request và không
tự lặp lệnh ghi. Metadata DB chỉ đưa vào sử dụng sau khi phản chiếu thành công.

764 kiểm thử backend, 77 frontend và 14 browser đạt; nhóm tập trung
API/giao dịch/phục hồi/định dạng đáp án 53 đạt (có giao nhau với nhóm backend).
Ba đợt 50 học sinh, 2.310 request học tập không lỗi, p95 1,55–1,69 giây trên
local với API một worker, ba logical CPU; 150 bài chấm khớp thống kê.
DB đang dùng chỉ đọc để kiểm tra: 1.920 câu trong đề xuất bản hợp lệ về schema,
`check-system` đạt. Không có migration mới hoặc ghi đè học liệu đã xuất bản.
[Báo cáo và giới hạn](review-2026-10-15.md).

## Bản triển khai VPS Nhật: 4 vCPU / RAM 8 GB / SSD 100 GB

Profile `vps8gb` giới hạn runtime tổng 4,75 GiB, hai worker, tối đa 14 kết nối
API/counter và PostgreSQL trong 2 GiB. Cache SVG công khai một giờ; Caddy có
timeout đọc và UDP 443 cho HTTP/3. Profile mới mở đầu bằng bảo trì/allowlist IP;
`check-launch` rà soát admin/demo/quyền DB trước khi công khai. DB local còn
21 demo chưa ghi nhận đổi mật khẩu, admin cần xử lý theo hướng dẫn sau restore;
không đổi hoặc khóa tài khoản trên DB local trong đợt này.

Backup có khóa chống trùng, kiểm tra payload/trailer gzip, SHA256 và dấu lần
thành công; `smoke.sh --require-backup` kiểm tra container/HTTPS/cache và backup
quá 26 giờ. Có cấu hình xoay log, helper build đóng gói đủ ba profile và workflow
CI chờ chạy trên GitHub. Thêm quy tắc LF cho script/config Linux khi làm ở Windows.

788 kiểm thử không integration, 77 frontend, 18 browser HTTPS đạt; các nhóm API
hiện có 57 đạt, biên ngày Nhật/Việt và launch mới 3 đạt. Gate bảo trì kiểm tra
thực tế trên Caddy local, gồm thử giả IP. Tải qua HTTPS local ba lần 50 học sinh:
2.310 request không lỗi, 150 bài khớp thống kê, p95 1,03–1,08 giây. Restore thật
database test đối chiếu 82 bảng không lệch. npm/pip audit không có advisory
được phát hiện tại thời điểm kiểm tra; chưa scan OS của image Linux.

Chưa có VPS/SSH; chưa build/run image Linux vì Docker Engine local không chạy
được. Không coi profile/cấu hình hoặc CA HTTPS local là xác nhận quota VPS,
Let's Encrypt hay tuyến mạng Việt–Nhật. Xem
[deploy-vps-japan.md](deploy-vps-japan.md),
[báo cáo và bằng chứng](release-readiness-2026-10-15.md).

## Học liệu tình huống và thư viện luyện tập — 15/10/2026

Thêm 30 bài, 150 câu hỏi và 30 đề cho lớp 1–5, chia đều ba môn và Free/VIP.
Mỗi bài có hình/thẻ minh họa, ba phần ngắn, gợi ý phân quyền 1/3 và lời giải
từng câu. Bộ bổ sung có inventory/seed/verify riêng, giữ mốc kiểm kê bộ nền
tảng. Database local đã nạp sau backup: 81 bảng/20.860 dòng dữ liệu cũ giữ nguyên.

Thư viện luyện tập dùng API phân trang 12 bài, tìm không dấu, lọc môn/gói/loại
đề/số câu/kết quả, nút chọn nhanh trên điện thoại; kết quả gần nhất quyết định
bài cần ôn dưới 80%, điểm tốt nhất giữ riêng. Khối và lịch sử lấy theo học sinh
đăng nhập; response không chứa đáp án và không cache. Admin xem được số học
liệu bổ sung đã xuất bản từng khối.

799 backend không integration, 21 kiểm thử nội dung/API liên quan (gồm 10
integration PostgreSQL), 80 frontend, 6 browser mới và 2 browser hồi quy đạt.
Type/lint/format/build đạt. Không đo lại sức tải VPS trong đợt này. Xem
[nội dung, triển khai và giới hạn](applied-learning.md),
[bằng chứng nạp local](audits/applied-local-2026-10-15.json).

## Lưu bài và bộ Khám phá — 15/10/2026

Migration `0012_lesson_bookmarks` thêm lưu bài theo tài khoản, khóa chính ghép
và khóa ngoại. Thư viện/bài học có lưu/bỏ lưu, danh sách riêng và đồng bộ khi
đăng nhập thiết bị khác; không mở khóa nội dung VIP. Bộ lọc thu gọn trên điện
thoại; bỏ thẻ cuối trang tự trở về trang còn bài. Sửa bộ đếm dashboard dùng
toàn bộ lượt đã chấm, thay vì tối đa 200 dòng lịch sử.

Thêm 15 bài/60 câu/15 đề cho lớp 1–5, gồm 7 Free/8 VIP, mỗi bài bốn câu và gợi
ý 1/3 theo gói. Chung cơ chế release inventory/seed/verify cho hai bộ bổ sung;
admin theo dõi từng bộ. Đã backup, migrate và nạp local, giữ nguyên 81 bảng và
21.910 dòng có trước đợt này. Bản thơ nháp chưa có lượt học được biên tập qua
bài thay thế, giữ nguyên bốn phiên bản câu hỏi cũ.

810 backend không integration; 45 kiểm thử nội dung/API liên quan (gồm 23
integration); 83 frontend; 12 browser desktop/mobile đạt. Các nhóm backend có
22 ca trùng nhau. Type/lint/format/build đạt; không đo lại VPS trong đợt này.
[Hướng dẫn, danh mục và kiểm chứng](bookmarks-and-explorers.md).
