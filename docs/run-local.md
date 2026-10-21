# Chạy nhanh trên máy local hiện tại

Cập nhật 20/10: **Quản trị → Kiểm tra hệ thống → Trước khi mở web**, có tải biên
bản CSV; CLI `check-release` kiểm tài khoản, học liệu và ảnh trước mở công khai.
[Biên bản và hướng dẫn cập nhật](pre-deployment-review-2026-10-20.md).

AI Academy cập nhật 19/10: 200 bài, 11 chủ đề/khối, trò chơi đúng lớp và tìm/học tiếp.
Local hiện tại đã backup/nạp; khởi động lại hai server. Máy khác/VPS backup, build
và chạy `seed-ai-academy` theo [hướng dẫn](ai-academy-upgrade-2026-10-19.md).
Không có migration mới.

Máy Windows hiện có `.env`, `.venv`, `frontend/node_modules` và PostgreSQL 18
đang chạy. Dùng PowerShell; không cần Docker hoặc cài lại các thư viện.

**Bản hiện tại 17/10:** đã backup và nạp bộ `daily-2026-03`, thêm 15 bài/60 câu/
15 đề. Có đủ bốn bộ bổ sung thì mỗi khối đạt **83 bài/450 câu/71 đề** ở ba môn.
Trang chủ học tiếp đúng bài/lượt/bước AI, phản hồi bài AI dễ xem lại hơn.
Head vẫn `0012_lesson_bookmarks`; khởi động lại hai server.
[Nội dung và lệnh nạp trên máy khác](daily-learning-and-resume.md).
Các số 68/384/56, 74/414/62 và 77/426/65 ở phần cũ ghi nhận các mốc trước.

Bản nâng cấp 14/10 bổ sung tự lưu bài luyện, đồng hồ thời hạn và rà soát học liệu.
Không cần migration hoặc seed lại; khởi động lại cả hai server theo hướng dẫn
dưới đây. [Cách dùng tự lưu](learning-reliability.md).

Bản 15/10 cải thiện xem lại đáp án/lời giải, hình minh họa, bộ đếm câu đã làm
và xử lý lỗi mạng/database; cũng chỉ cần khởi động lại server, không seed lại.
[Báo cáo kiểm thử](review-2026-10-15.md).

Bộ tình huống mới đã nạp trên máy này: thêm 30 bài/150 câu/30 đề cho lớp 1–5.
Khởi động lại hai server để dùng thư viện luyện tập mới (tìm không dấu, chọn bài
ngắn và ôn thêm). Các số 68/384/56 bên dưới là bộ nền tảng; có bộ bổ sung thì
mỗi khối thành 74/414/62. Máy khác nạp bằng `app.cli seed-applied-content` sau
khi có bộ nền tảng. [Hướng dẫn và quyền Free/VIP](applied-learning.md).

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

**Lớp 1–2 trên máy này đã có học liệu**. Đăng nhập học sinh có hồ sơ khối 1/2,
hoặc admin tạo/chỉnh hồ sơ tại Quản trị tài khoản. Mỗi khối 68 bài/384 câu/56
đề; bài ngắn 6–8 phút, Free 1/VIP 3 gợi ý. Với máy chưa nạp, chạy một lần:

```powershell
../.venv/Scripts/python.exe -m app.cli seed-grade1-content
../.venv/Scripts/python.exe -m app.cli seed-grade2-content
```

Không đổi khối hay mật khẩu tài khoản hiện có tự động. Chi tiết
[khảo sát và học liệu lớp 1–2](grades1-2-curriculum.md).

Nâng cấp lớp 3 lần đầu: trước khi mở backend, chạy thêm
`../.venv/Scripts/python.exe -m app.cli seed-grade3-content`.
Head hiện tại `0012_lesson_bookmarks`, bao gồm lớp/thành tích/giá, gợi ý VIP và lưu bài. Admin tạo/chỉnh hồ sơ học sinh
**Lớp 3**, rồi chọn lớp 3 trong học liệu. Mỗi bài lớp 3: Free 1 gợi ý, VIP 3;
xem [học liệu lớp 3](grade3-curriculum.md). Không đổi tài khoản lớp 4 tự động.

Đợt 16/10 có thêm bộ ôn tập `review-2026-02` (15 bài/60 câu/15 đề),
10 bài AI và sửa quyền gợi ý/gửi lại sau lỗi mạng.
[Nội dung và lệnh cập nhật](learning-upgrade-2026-10-16.md).

AI Academy có 190 bài cho lớp 1–5 và 1625 hình trong thư viện. Với máy
khác hoặc lần nâng cấp đầu, cài thêm dependencies và nạp module trước khi chạy:

```powershell
../.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
```

Đăng nhập → **AI Academy** (`/ai-academy`); admin `/admin/ai-academy`.
Mặc định `AI_TRAINING_ONLY=true`: học lý thuyết và bài tập, không gọi model.
Lớp 4 có 3 bài Free / 33 bài VIP; lab và xưởng sáng tạo thuộc VIP.
Chi tiết [AI Academy](ai-academy/README.md).
Giữ `.env` hiện có; file `.env.example` dùng placeholder, không chép đè mật khẩu.

Lớp 5: máy hiện tại đã nạp bộ ba môn. Máy khác nạp riêng nếu chưa có:

```powershell
../.venv/Scripts/python.exe -m app.cli seed-grade-content --grade 5
../.venv/Scripts/python.exe -m app.cli verify-seed --grade 5
```

Dùng `free5_01` hoặc `vip5_01` với mật khẩu học sinh cấu hình; xem
[danh sách tài khoản](demo-accounts.md). Học sinh mở **Thư viện bài học** để tìm
và lọc; admin chọn **Chương trình → Lớp học liệu → Lớp 5**.
[Căn cứ và danh mục lớp 5](grade5-curriculum.md). Không cần migration mới cho đợt này.
Đã sửa thời điểm commit để phiên đăng nhập và thao tác duyệt/nộp hoàn tất trước
khi trả thành công. Cần khởi động lại backend để nhận sửa lỗi này.

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

Admin mở **Lớp và giao bài** (`/admin/classes`) để tạo lớp, ghi danh học sinh
hoặc giao bài riêng cho học sinh tự do. Giáo viên dùng `/teacher/classes`;
học sinh dùng **Lớp và thành tích** để xem bài giao/kết quả/top 3 trong lớp.
Xem [hướng dẫn lớp và thành tích](classes-achievements.md).

**Giá VIP và ưu đãi** (`/admin/vip-pricing`) quản lý giá tham khảo và sale có
ngày hết hạn, hiển thị tại **Gói học của em**. Chưa có thanh toán tự động;
cấp/thu hồi vẫn qua quản lý gói. Xem [bảng giá và khảo sát](vip-pricing-research.md).

Phiên thường mặc định **8 giờ**. Học sinh có thể chọn **Ghi nhớ đăng nhập trên máy
cá nhân** để giữ phiên **7 ngày**. Trong phiên, bấm biểu tượng VietTree sẽ về
dashboard; mở `/login` tự chuyển tiếp. Xem [quản lý phiên](session-management.md).

Bấm **Cỡ chữ → Chữ gọn hơn** để dùng giao diện gọn cho điện thoại. Có ba mức chữ;
lựa chọn tự lưu theo tài khoản và nhóm điện thoại / máy tính bảng / máy tính,
dùng cả trong AI Academy. Khởi động lại hai server để nhận cập nhật này; không cần
migration. Xem [cấu hình cỡ chữ](reading-preferences.md).

Học sinh VIP mở menu **Góc học VIP** để tìm bài nâng cao, ôn câu sai và xem/in báo
cáo 7/30 ngày. Chi tiết: [mở rộng VIP](vip-expansion.md).

Kiểm tra backend và kết nối database tại **http://localhost:8000/ready**.
Tài liệu API: **http://localhost:8000/docs**.
Dừng hệ thống bằng **Ctrl+C** ở cả hai terminal.

## Khi gặp lỗi

Tài khoản thử đủ các khối: xem [danh sách Free/VIP lớp 1–5](demo-accounts.md).
Sau refactor chỉ khởi động lại hai server, không cần migration/reset mới.
Admin có **Chương trình → Xuất học liệu CSV** để tải bảng theo bộ lọc.

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
- **API báo dữ liệu tạm bận (503):** thử lại sau vài giây; backend đã giới hạn
  chờ khóa DB. Sau cập nhật 14/10, khởi động lại cả hai server để dùng dashboard
  chỉ đọc, bài đọc trong đề và chấm số mới. Không cần migration mới.

Nếu chuyển sang máy khác hoặc thiếu thư viện, xem phần
[Chạy local development trong README](../README.md#chạy-local-development).
