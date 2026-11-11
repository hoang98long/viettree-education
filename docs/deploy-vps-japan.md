# Triển khai VPS 4 vCPU / RAM 8 GB / SSD 100 GB

Cấu hình mục tiêu cho khoảng 50 học sinh ban đầu, Ubuntu Server 24.04 LTS
amd64. Host Nhật vẫn dùng lịch học UTC+7. Chạy Docker Compose production;
không chạy dev server, stack audit, Redis hoặc mô hình AI trên VPS này.

## 1. Cấu hình sử dụng

| Dịch vụ           |     Trần RAM | Thiết lập                                               |
| ----------------- | -----------: | ------------------------------------------------------- |
| PostgreSQL 18     |        2 GiB | shared_buffers 512 MB, work_mem 4 MB, tối đa 60 kết nối |
| FastAPI           |      1,5 GiB | 2 worker, pool 4 + 2 mỗi worker, giới hạn concurrency   |
| Next.js           |        1 GiB | Standalone, Node heap runtime 512 MiB                   |
| Caddy             |      256 MiB | HTTPS, gzip/zstd, giới hạn body/log và maintenance      |
| Tổng trần runtime | **4,75 GiB** | Phần còn lại dành Linux/Docker, cache và vận hành       |

Đây là trần, không phải RAM luôn bị chiếm. PostgreSQL giới hạn file tạm
256 MB mỗi process và ngắt transaction bỏ quên sau 60 giây; câu lệnh ứng
dụng vẫn có statement/lock timeout. Không tắt fsync/synchronous_commit.
Khi maintenance tạo index lớn cần xem xét giới hạn file tạm riêng, không
tăng mặc định cho mọi kết nối.

Image backend cài 36 package runtime, không cài sáu package chỉ dùng
test/lint. Frontend build giới hạn heap Node 2 GiB, runtime dùng 512 MiB;
build hai image lần lượt. Test, tài liệu và artifact không vào build context.

Mô hình: Internet → Caddy :443 → Next :3000 hoặc API :8000 → PostgreSQL.
Chỉ Caddy publish 80/443. Có nén/cache tài nguyên công khai; API, điểm,
session và quyền VIP không đưa vào public cache. Không cần CDN giai đoạn đầu.

## 2. Chuẩn bị VPS và domain

Theo [hướng dẫn đầy đủ](deploy-vps.md) để cài Docker Engine/Compose, DNS,
firewall và chuyển source lên `/opt/viettree-education`. Bản ghi A trỏ tới
VPS; bắt đầu DNS only nếu dùng Cloudflare. Chỉ thêm AAAA khi IPv6 hoạt động.
Mở cổng SSH thực tế trước khi bật firewall, TCP 80/443, UDP 443 cho HTTP/3.

```bash
cd /opt/viettree-education
umask 077
# Chỉ copy khi chưa có .env.production; giữ env đang dùng nếu nâng cấp.
test -e .env.production || cp .env.production.vps8gb.example .env.production
chmod 600 .env.production
nano .env.production
```

Điền domain/email, release tag và ba mật khẩu riêng cho PostgreSQL admin,
owner migration và runtime app. Giữ `VIETTREE_DEPLOY_PROFILE=vps8gb`,
`AI_TRAINING_ONLY=true`. Mặc định `MAINTENANCE_MODE=true`; đặt
`MAINTENANCE_ALLOWED_IPS` là IP public của quản trị viên để thiết lập.
Không đưa `.env` local hoặc mật khẩu vào image/repository.

## 3. Build và chuyển dữ liệu

```bash
dc() { bash /opt/viettree-education/deploy/compose.sh "$@"; }
dc config --quiet
dc build backend frontend
dc pull db caddy
dc up -d db
```

Sau đó chọn **một nhánh** trong [hướng dẫn đầy đủ](deploy-vps.md):

- **Mang dữ liệu đang dùng lên VPS:** backup/dump local, tạo DB roles,
  restore, migrate và cấp `deploy/grant-runtime.sql`. Không seed demo sau
  restore. Copy cả `var/ai-media` nếu có ảnh upload riêng; SVG bundled theo image.
- **Cài mới hoàn toàn:** tạo roles, import SQL/migrate, nạp nội dung nền
  tảng và đủ năm pack/AI, tạo admin production. Không dùng mật khẩu demo.

Head hiện tại `0012_lesson_bookmarks`. Không import schema/restore đè lên
database đã vận hành. Với release cập nhật, backup trước; xem preview
`review-learning-content` và kiểm thay đổi trước khi apply học liệu.

Có thể build ngoài VPS bằng `deploy/build-images.ps1`, chuyển image archive
và checksum rồi `docker load`. Trên VPS dùng `--no-build --pull never` cho
app và pull db/caddy riêng. Hạn chế build lúc học sinh đang sử dụng.

## 4. Mở web

```bash
dc up -d --no-build --pull never backend frontend caddy
dc exec -T backend python -m app.cli check-launch
dc exec -T backend python -m app.cli check-release
```

Hai check chỉ đọc. Đổi mật khẩu admin, khóa hoặc đổi mật khẩu các tài khoản
demo còn hoạt động qua giao diện, kiểm quyền DB runtime và nội dung còn cảnh
báo. Khi đạt, sửa `.env.production` thành `MAINTENANCE_MODE=false`, rồi:

```bash
dc up -d --no-deps caddy
bash deploy/backup.sh
bash deploy/smoke.sh --require-backup
docker stats --no-stream
df -h
```

Kiểm HTTPS, login/logout, cấp/thu hồi VIP, đọc/làm/nộp bài, AI Academy và
upload trước khi phát tài khoản. API đi trực tiếp qua Caddy, không vòng
qua Next proxy. Đo thêm từ Wi-Fi/4G ở Việt Nam nếu server đặt tại Nhật:

```powershell
curl.exe -o NUL -sS -w "TTFB=%{time_starttransfer}s TOTAL=%{time_total}s\n" https://TEN_MIEN_THAT/login
```

Tải local trước đây 50 người không lỗi HTTP, p95 khoảng 2,75 giây; dashboard
còn tail cao. Đây không phải cam kết hiệu năng VPS hoặc mạng Việt–Nhật.

## 5. Vận hành gọn

- Sao lưu DB và ảnh upload mỗi ngày bằng `deploy/backup.sh`; kiểm checksum,
  copy ra ngoài VPS và định kỳ restore vào DB khác. Snapshot duy nhất của
  nhà cung cấp chỉ là phương án bổ sung.
- Giữ ít nhất khoảng 20 GB trống cho WAL, image và backup. Theo dõi `df -h`,
  `docker stats --no-stream`, restart/OOM và `deploy/smoke.sh --require-backup`.
- Docker log xoay 3 × 10 MB mỗi dịch vụ. Cài `deploy/viettree-logrotate`
  cho log cron theo hướng dẫn đầy đủ. Không cài hệ log nặng cùng VPS giai đoạn đầu.
- Đặt lịch backup/smoke theo [hướng dẫn cron](deploy-vps.md); marker backup
  quá 26 giờ hoặc checksum lỗi phải được xử lý, không bỏ qua.
- Khi nâng cấp: backup → build/load release → maintenance → migrate/grant
  nếu cần → up app → check-launch/check-release/smoke → mở lại.
- Giữ project name `viettree` và volume dữ liệu khi đổi release. Không dùng
  `docker compose down -v`, `volume prune` hoặc `system prune --volumes`.

## 6. Trạng thái chuẩn bị

Đã kiểm local: chấm điểm/quyền, Linux image, HTTPS smoke, restore dữ liệu giả
và tải 50 người. Docker audit đã được dọn khỏi luồng triển khai; regression
tests vẫn ở repo/CI. Chưa deploy VPS thật, chưa đo WAN hoặc chạy dài ngày.

Cần theo dõi thêm timeout ở proxy Windows local, giảm dịch chuyển bố cục
trang AI, duyệt sư phạm với giáo viên và chốt vòng đời bài làm hết hạn.
Các việc này không làm phát sinh thêm dịch vụ nền trên VPS.

Nguồn cấu hình: [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/),
[PostgreSQL 18 resource consumption](https://www.postgresql.org/docs/18/runtime-config-resource.html).
