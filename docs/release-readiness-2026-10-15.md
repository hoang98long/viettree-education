# Kiểm chứng bản triển khai VPS Nhật — 15/10/2026

Mục tiêu: **4 vCPU, RAM 8 GB, SSD 100 GB**, khoảng 50 học sinh đồng thời ban
đầu. Đã chuẩn bị profile `vps8gb` và [hướng dẫn deploy](deploy-vps-japan.md).
Đây là kiểm chứng trên Windows local/PostgreSQL thật; chưa có IP/SSH VPS Nhật
để xác nhận triển khai, chứng chỉ công khai hoặc tốc độ quốc tế.

## Thay đổi phục vụ production

- Giới hạn runtime tổng 4,75 GiB, hai API worker, pool 4 + 2 mỗi worker,
  một pool counter auth riêng/worker. Cấu hình PostgreSQL nằm trong trần 2 GiB;
  không tắt bảo đảm lưu giao dịch. Giữ project/volumes của các profile trước.
- Cache một giờ cho ảnh SVG công khai; API và dữ liệu riêng giữ chính sách cũ.
  Caddy có timeout đọc header/body và idle; publish UDP 443 cho HTTP/3 bên cạnh
  TCP HTTPS để cấu hình Docker khớp giao thức mà Caddy phục vụ.
- `check-launch` chỉ đọc, kiểm tra mode, tài khoản demo các lớp, admin đã đặt
  mật khẩu riêng và quyền DB runtime. Kiểm tra này không tự chỉnh tài khoản,
  không nằm trong `/ready` và không làm khóa ứng dụng local.
- Profile mới mặc định bảo trì: chỉ IP quản trị được cấu hình mới vào được,
  các truy cập khác nhận 503/no-store trước cả route API. Chỉ mở công khai sau
  rà soát tài khoản và `check-launch`; các profile cũ giữ mặc định như trước.
- Backup khóa chống chạy trùng, kiểm tra hết dữ liệu/trailer gzip của ảnh,
  tạo checksum cặp DB/media, đánh dấu lần thành công; helper ảnh chạy được khi
  API dừng. Smoke test kiểm tra container, HTTPS, quyền riêng tư cache,
  endpoint ẩn và backup tối đa 26 giờ. Có cấu hình xoay log cron.
- Gói image deploy có đủ ba profile/env example và SQL xác minh. Có workflow
  CI kiểm tra Python/PostgreSQL, frontend và build image trên Linux; không tự
  publish/deploy và chưa chạy Actions trong đợt local này.

Không có migration mới, không cập nhật tài khoản hoặc học liệu ở database đang
dùng. Chỉ dữ liệu tổng hợp phục vụ audit được đọc ở DB đang dùng. Các ghi thử,
thay mật khẩu/khóa demo, tạo role runtime và restore đều ở DB test riêng.

DB đang dùng hiện có **21 demo chưa có ghi nhận đổi mật khẩu**, và admin chưa
có ghi nhận đáp ứng điều kiện mở web. Đây là công việc cần thực hiện sau
restore trong chế độ bảo trì, không được đánh dấu là đã xử lý ở DB thật.

## Kiểm thử tự động

- Bộ backend không integration: **788 đạt**, 9 kiểm thử cần DB bỏ qua ở nhóm
  này; 178 integration được tách riêng. Có kiểm tra gói deploy, CRC/ảnh và
  các nhánh lỗi backup/smoke/backup quá hạn.
- **57 kiểm thử API/phiên/VIP/concurrency/phục hồi/pool/giao dịch hiện có đạt**;
  **3 kiểm thử mới** về launch và biên ngày Việt–Nhật đạt. Có giao nhau với các
  bộ kiểm thử trước; không cộng thành tổng toàn project.
- **77 kiểm thử frontend đạt**; build production, TypeScript, lint và format
  được kiểm tra trước bàn giao.
- **18/18 luồng browser HTTPS đạt**, desktop và mobile: login, cookie
  Secure/HttpOnly/SameSite, chống Origin/CSRF sai, logout, API 401/no-store,
  route vận hành ẩn, cache ảnh, Free/VIP, cấp/thu hồi VIP, bài đọc, tự lưu,
  xóa đáp án, reload, submit và lời giải.

Browser chạy với timezone `Asia/Tokyo`, frontend standalone heap 512 MiB,
backend production hai worker và DB role mới chỉ có quyền dữ liệu. Caddy là
binary thật, HTTPS dùng CA local; browser chỉ bỏ xác minh trust cho `localhost`
khi bật cờ test riêng. Không cài CA vào trust store hệ điều hành. Không coi
chứng chỉ local này là bằng chứng Let's Encrypt/domain thực đã hoạt động.

Cổng bảo trì cũng đã thử bằng Caddy HTTPS thật: chặn trang và API bằng
503/no-store, IP giả trong X-Forwarded-For không vượt allowlist, mode gõ sai
vẫn giữ đóng, IP quản trị vào được và chỉ giá trị `false` mới mở công khai.
[Kết quả gate](audits/maintenance-gate-2026-10-15.json).

Một luồng browser thêm **250 ms trước mỗi request API của trang** vẫn lưu,
chuyển câu, reload và submit đúng trên cả hai thiết bị. Đó là kiểm thử độ trễ
nhân tạo, không phải phép đo tuyến từ Việt Nam sang Nhật. Test PostgreSQL đặt
`TIME ZONE Asia/Tokyo` xác nhận thời điểm 16:30 UTC vẫn thuộc ngày Việt Nam
hiện tại, dù Nhật đã sang ngày sau; lịch sử và thống kê ngày khớp.

## Tải qua HTTPS thực sự tại local

50 tài khoản tổng hợp: 25 Free/25 VIP, lớp 1–5. Client HTTPX **xác minh chứng
chỉ bằng CA local**, không dùng `verify=False`; request học tập đi qua Caddy
HTTPS tới backend production. Readiness gọi địa chỉ nội bộ vì proxy chặn nó.
Backend được đặt affinity bốn logical CPU, hai worker, pool 4 + 2 và hai phép
Argon2 mỗi worker. Không giới hạn tổng CPU/RAM cả stack bằng cgroups.

| Đợt | Đồng thời | Request học tập | Hoàn thành |      p95 |      p99 | Lỗi HTTP |
| --- | --------: | --------------: | ---------: | -------: | -------: | -------: |
| 1   |        50 |             770 |      50/50 | 1.076 ms | 1.488 ms |        0 |
| 2   |        50 |             770 |      50/50 | 1.026 ms | 1.560 ms |        0 |
| 3   |        50 |             770 |      50/50 | 1.063 ms | 1.611 ms |        0 |

50/50 đăng nhập đồng thời đạt, tổng 5,20 giây, p95 4,98 giây. 150 bài chấm,
thống kê ngày 150, không sai lệch thống kê câu. Nộp lặp không nhân đôi kết quả.
[Dữ liệu đo](audits/load-https-vps8gb-2026-10-15.json).

Không suy ra phần trăm cải thiện cố định so với những đợt trước vì số worker,
DB lịch sử và tải máy thay đổi. Caddy/Next/PG không nằm trong VM Linux 8 GB;
benchmark này không chứng minh tài nguyên VPS thực hoặc độ trễ Internet.

## Khôi phục và thư viện

Đã lấy snapshot nhất quán của **database test**, `pg_dump` custom format bằng
PostgreSQL 18; restore thật vào database test mới, kiểm tra schema/head và số
hàng **82/82 bảng**, không lệch. DB restore tạm đã được dọn, nguồn không đổi.
[Kết quả restore](audits/restore-japan-profile-2026-10-15.json).
CRC gzip, file bị cắt, path nguy hiểm và symlink của backup ảnh có kiểm thử
riêng; test Bash xác nhận backup lỗi không thay dấu lần thành công trước.

`npm audit` và `pip-audit` không phát hiện lỗ hổng đã biết trong lock tại thời
điểm kiểm tra. Đây không phải bảo đảm mọi thư viện không có lỗ hổng;
[kết quả audit](audits/security-vps8gb-2026-10-15.json) ghi phiên bản và phạm vi.

## Chưa kiểm chứng, cần thực hiện khi có VPS

Docker Engine local chưa chạy được trong phiên này, nên chưa build/run image
Linux; kiểm tra Compose/contract/Caddy/PowerShell/Bash đã thực hiện, build
Linux có trong CI chờ chạy. Chưa xác nhận quota cgroups, firewall nhà cung cấp,
Let's Encrypt, DNS và mạng từ Việt Nam, hoặc backup/restore bằng role đích trên
VPS. Chưa có soak test nhiều giờ hay dữ liệu lịch sử quy mô lớn.

Khi nhận server: triển khai đúng profile → chuyển DB/media → migration/grant →
đổi mật khẩu admin và rà soát demo → `check-launch` → backup/restore thử →
`smoke.sh --require-backup` → kiểm tra từ mạng Việt Nam. Không chạy pytest hoặc
load probe của dự án vào database production; load probe tự chặn DB không phải
test và đích mạng ngoài local.
