# Deploy VPS tại Nhật — 4 vCPU, RAM 8 GB, SSD 100 GB

Ngày rà soát: **15/10/2026**. Dành cho gói VPS bạn đã chọn và khoảng 50 học
sinh đồng thời ban đầu. Cấu hình này có thêm dư địa so với profile RAM 2 GB;
số học sinh thực tế vẫn cần đo trên VPS và mạng Việt Nam sau khi có IP/domain.

Chọn **Ubuntu Server 24.04 LTS x86_64/amd64**. Server đặt tại Nhật không đổi
ngày học, lịch sử, VIP hoặc thành tích sang giờ Nhật. Chạy app production bằng
Docker Compose, Caddy HTTPS, FastAPI hai worker, Next standalone và PostgreSQL 18.
Phân hệ AI tiếp tục chỉ đào tạo/luyện tập nội bộ, không cần GPU hoặc model.

Cập nhật học liệu tình huống: sau khi có bộ nền tảng và backup, nạp riêng
`seed-applied-content`, rồi `verify-applied-content` qua `dc run --rm -T --no-deps backend python -m app.cli`.
Thêm 30 bài/150 câu/30 đề; xem [hướng dẫn cập nhật](applied-learning.md).

Head mới `0012_lesson_bookmarks` thêm lưu bài theo tài khoản. Bộ Khám phá dùng
`seed-supplement-content --release explorers-2026-01` sau migrate/grant, bổ sung
15 bài/60 câu/15 đề. [Quy trình cập nhật](bookmarks-and-explorers.md).

## 1. Profile dành cho VPS này

Copy `.env.production.vps8gb.example` thành `.env.production`. Wrapper
`deploy/compose.sh` đọc `VIETTREE_DEPLOY_PROFILE=vps8gb` và tự ghép
`docker-compose.production.yml` với `docker-compose.vps8gb.yml`.

| Dịch vụ      | Trần RAM runtime | Thiết lập chính                                              |
| ------------ | ---------------: | ------------------------------------------------------------ |
| PostgreSQL   |            2 GiB | shared_buffers 512 MB; work_mem 4 MB; tối đa 60 kết nối      |
| API          |          1,5 GiB | 2 worker; pool 4 + 2 mỗi worker; auth counter riêng 1/worker |
| Next.js      |            1 GiB | Node heap 512 MiB; chạy standalone                           |
| Caddy        |          256 MiB | nén gzip/zstd; HTTPS/HTTP2/HTTP3; timeout đọc request        |
| Tổng runtime |     **4,75 GiB** | Dành phần còn lại cho OS/Docker, cache và vận hành           |

Đây là giới hạn trên, không phải dung lượng luôn được cấp/đo tiêu thụ. API có
tối đa **14 kết nối thường dùng** gồm 12 pool API + 2 counter auth; thêm kết nối
cho readiness và công cụ quản trị. Không bật `fsync=off` hay bỏ đồng bộ giao dịch.
`effective_cache_size` là gợi ý cho planner, không phải vùng RAM cấp riêng.
[Giới hạn Docker](https://docs.docker.com/engine/containers/resource_constraints/),
[bộ nhớ PostgreSQL](https://www.postgresql.org/docs/18/runtime-config-resource.html).

Profile `small` cũ vẫn có thể sử dụng cho máy 2 GB. Khi chuyển profile, giữ
project name `viettree`, DB_NAME và các volumes. Không chạy `down -v` hoặc
`volume prune`. Cập nhật cấu hình PostgreSQL cần recreate container DB; làm
trong cửa sổ bảo trì, sau backup.

## 2. Cài đặt lần đầu

Dùng [hướng dẫn đầy đủ](deploy-vps.md), với các lựa chọn dưới đây:

1. Trỏ bản ghi **A** của domain về IPv4 VPS. Chỉ thêm AAAA khi IPv6 hoạt động.
   Bắt đầu bằng DNS trực tiếp/DNS only nếu dùng Cloudflare.
2. Cài Docker Engine và Compose theo mục 2–3. Mở đúng cổng SSH trước khi bật
   firewall; mở **TCP 80/443**, **UDP 443** cho HTTP/3 cả ở VPS và firewall nhà
   cung cấp. Chỉ Caddy publish cổng; DB/API/Next nằm trong mạng Docker.
3. Đặt múi giờ **hệ điều hành** theo Việt Nam để lịch cron dễ quản lý:

   ```bash
   timedatectl set-timezone Asia/Ho_Chi_Minh
   timedatectl status
   ```

   Kiểm tra NTP đang đồng bộ. Containers của profile dùng UTC; ứng dụng tính
   ngày học và hiển thị theo UTC+7, tương đương giờ Việt Nam hiện tại.

4. Đưa source lên `/opt/viettree-education` theo mục 4, hoặc dùng bộ image build
   ngoài VPS ở phần tiếp theo. Không chuyển `.env` local vào container.
5. Dùng đúng mẫu env mới:

   ```bash
   cd /opt/viettree-education
   umask 077
   cp .env.production.vps8gb.example .env.production
   chmod 600 .env.production
   nano .env.production
   ```

   Thay DOMAIN, ACME_EMAIL, RELEASE và **ba mật khẩu DB khác nhau**, đủ mạnh.
   Giữ `VIETTREE_DEPLOY_PROFILE=vps8gb`, `COOKIE_SECURE` do Compose cấp,
   `AI_TRAINING_ONLY=true`. Mật khẩu trong env phải khớp các DB role đã tạo.
   Mặc định `MAINTENANCE_MODE=true`: chỉ IP trong `MAINTENANCE_ALLOWED_IPS`
   truy cập được. Đặt allowlist thành IP public/CIDR của máy quản trị đang dùng
   để đăng nhập/đổi mật khẩu; IP khác nhận 503/no-store, kể cả API. Khi IP mạng
   thay đổi, cập nhật allowlist qua SSH rồi recreate Caddy. Cấu hình này tin IP
   kết nối trực tiếp, vì vậy giữ DNS only trong lần triển khai đầu.

6. Dùng wrapper cho **mọi lệnh** trong hướng dẫn chung:

   ```bash
   dc() { bash /opt/viettree-education/deploy/compose.sh "$@"; }
   dc config --quiet
   dc build backend frontend
   dc pull db caddy
   dc up -d db
   ```

7. Theo mục **6–9 của hướng dẫn chung**: tạo owner/runtime roles; **restore DB
   hiện tại hoặc khởi tạo mới**, chạy migration, cấp `deploy/grant-runtime.sql`,
   đặt mật khẩu quản trị rồi khởi động web. Giữ head của release, hiện là
   `0012_lesson_bookmarks`. Không seed demo sau restore.

   Khi chuyển từ local, dump chỉ chứa database. Copy cả thư mục **`var/ai-media`**
   nếu đã upload ảnh riêng, theo phần Academy trong hướng dẫn chung; không chỉ
   chuyển dump rồi bỏ mất ảnh. Hình bundled đi cùng image.

8. Xác nhận trước khi mở cho học sinh:

   ```bash
   dc up -d --no-build --pull never backend frontend caddy
   dc exec -T backend python -m app.cli check-launch
   # Chỉ tiếp tục sau khi check-launch đạt và đã rà soát tài khoản:
   # sửa .env.production: MAINTENANCE_MODE=false
   dc up -d --no-deps caddy
   bash deploy/backup.sh
   bash deploy/smoke.sh --require-backup
   docker stats --no-stream
   df -h
   ```

`check-launch` **chỉ đọc**, kiểm tra hệ thống và thêm các điều kiện mở web:
production mode; có admin hoạt động đã đặt mật khẩu riêng; tài khoản demo lớp
1–5/`longnh` đang hoạt động nhưng chưa có ghi nhận đổi mật khẩu; DB runtime
không có quyền superuser, tạo role/database/schema hoặc sở hữu bảng public.
Không tự khóa, đổi mật khẩu hay thu hồi VIP. Dùng quản trị tài khoản để đổi mật
khẩu/khóa đúng các tài khoản cần xử lý; admin legacy cần đổi mật khẩu qua trang
bảo mật để có ghi nhận, không chỉnh cột bằng SQL cho qua kiểm tra.

Smoke test kiểm tra container running/healthy/OOM, `check-launch`, HTTPS,
chuyển hướng HTTP, API chưa đăng nhập trả 401/no-store, ảnh tĩnh có cache và
endpoint vận hành không công khai. Không tạo tài khoản hay bài làm.
Restart count được in để theo dõi; script không tự restart hoặc sửa DB.

Đối chiếu chỉ đọc DB local hiện tại: **21 tài khoản demo** chưa có ghi nhận đổi
mật khẩu; admin cũng chưa có ghi nhận đáp ứng kiểm tra mở web. Không khóa hoặc
đổi mật khẩu local trong đợt này. Sau restore, dùng chế độ bảo trì và allowlist
để rà soát/khóa demo hoặc đặt mật khẩu riêng; đổi mật khẩu admin tại
`/account/security`, rồi chạy lại `check-launch`. Không tắt bảo trì chỉ để bỏ
qua kiểm tra. Các tài khoản demo đã chuyển thành tài khoản thật có thể giữ
lịch sử/VIP và đổi mật khẩu qua chức năng quản trị.

### Build ở máy khác hoặc CI

VPS 8 GB có thể build, nhưng để giảm cạnh tranh CPU/RAM khi đang có lớp học,
có thể build trên máy khác bằng Docker Engine Linux đang chạy:

```powershell
Set-Location 'D:\01_viettree_code\viettree-education'
./deploy/build-images.ps1 -Release '2026-10-15-vps8gb-v1'
```

Helper tạo image Linux amd64, archive cấu hình có đủ **ba profile**, mẫu env,
SQL gốc và `database/seeds/verify.sql`, cùng SHA256. Gói không chứa env thật,
DB dump hoặc ảnh upload riêng. Upload hai archive và hai checksum; xác minh
`sha256sum -c`, `docker load` rồi giải nén cấu hình theo mục 3–4 của
[hướng dẫn image ngoài VPS](deploy-small-vps.md). Chọn mẫu **vps8gb**, bỏ lệnh
build trên server và dùng `--no-build --pull never` khi chạy app. Pull db/caddy
riêng vì chúng không nằm trong archive image ứng dụng.

Workflow `.github/workflows/verify.yml` kiểm tra backend trên PostgreSQL test,
frontend và build hai image trên Linux sau khi repository được push lên GitHub.
Workflow không publish image hoặc tự deploy. Chưa coi việc thêm workflow là đã
chạy thành công CI; cần xem kết quả Actions ở repository khi push.

## 3. Tốc độ từ Việt Nam tới Nhật

Đã thêm cache **1 giờ** cho SVG công khai `/learning/*`, giữ nén của Caddy và
cache dài theo tên hash của bundle Next. Đổi nội dung ảnh cùng tên có thể cần
tối đa một giờ để trình duyệt tải lại; dùng tên mới nếu cần cập nhật tức thì.
Ảnh này không chứa dữ liệu cá nhân. HTML/API/kết quả/VIP và ảnh upload riêng
không được chuyển sang public cache.

Hiện dùng DNS trực tiếp là đủ để triển khai ban đầu. Khi muốn thêm CDN sau này,
chỉ cache nội dung công khai; cấu hình trusted proxy/IP/rate limit và thử lại
trước khi bật proxy Cloudflare. Không bật “Cache Everything” cho `/api/*`,
đăng nhập, trang admin hoặc bài làm. Cache không thay thế kiểm tra quyền phía
server. [Hành vi cache Cloudflare](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/),
[trusted proxies Caddy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy).

Vị trí Nhật không cho biết chắc độ trễ: phụ thuộc ISP, tuyến quốc tế, giờ cao
điểm và mạng điện thoại. Đo từ **máy ở Việt Nam**, cả Wi-Fi và 4G/5G, sau khi
domain chạy HTTPS:

```powershell
curl.exe -o NUL -sS -w "DNS=%{time_namelookup}s TLS=%{time_appconnect}s TTFB=%{time_starttransfer}s TOTAL=%{time_total}s\n" https://TEN_MIEN_THAT/health
curl.exe -o NUL -sS -w "TTFB=%{time_starttransfer}s TOTAL=%{time_total}s\n" https://TEN_MIEN_THAT/login
```

Đây là đo thời gian HTTP, không tương đương ping. Thử thêm đăng nhập, ảnh,
tự lưu, tải lại và nộp một bài thử riêng. Đã có kiểm thử local thêm 250 ms cho
request trình duyệt; độ trễ đó là mô phỏng, không phải ước lượng tuyến Việt–Nhật.

## 4. Sao lưu và vận hành

Script backup mới khóa chống hai lần chạy trùng, dump DB, đọc hết từng file ảnh
và kiểm tra CRC gzip, tạo SHA256 cho cặp dump/media. File `latest.success`
chỉ cập nhật sau khi cả cặp hoàn thành. Nếu backup lỗi, dấu thành công cũ được
giữ; không xóa bản trước. Helper sao lưu ảnh vẫn chạy được khi API dừng bảo trì.
Chọn các cặp có `.sha256`, kiểm tra trước khi dùng:

```bash
cd /var/backups/viettree
sha256sum -c TEN_BAN_SAO_LUU.sha256
```

Đặt lịch backup 02:15 giờ Việt Nam như mục 11 của hướng dẫn chung. Snapshot
duy nhất của nhà cung cấp là một điểm phục hồi bổ sung; vẫn giữ dump/media ở
kho hoặc máy khác với VPS và thử restore. Giữ env/password trong kho riêng có
quyền truy cập hạn chế. Duy trì khoảng **20 GB trống** cho image, WAL và backup;
đây là ngưỡng vận hành ban đầu, cần chỉnh theo kích thước DB thực tế.

Có thể kiểm tra mỗi giờ, bao gồm sau backup, với log đã xoay:

```bash
install -m 644 deploy/viettree-logrotate /etc/logrotate.d/viettree
logrotate -d /etc/logrotate.d/viettree
# Thêm dòng này trong /etc/cron.d/viettree-backup cùng PATH/SHELL của hướng dẫn chung:
# 45 * * * * root bash /opt/viettree-education/deploy/smoke.sh --require-backup >> /var/log/viettree-smoke.log 2>&1
```

`--require-backup` từ chối nếu dấu sao lưu thành công quá **26 giờ**, checksum
sai hoặc không có backup. Nếu cron của máy không được giám sát thì log không
tự gửi cảnh báo; dùng công cụ giám sát của nhà cung cấp hoặc kiểm tra định kỳ.
Không tự xóa backup hay thay cấu hình SSH bằng script này.

## 5. Phạm vi đã kiểm chứng và bước cuối trên VPS

Đọc [báo cáo kiểm chứng](release-readiness-2026-10-15.md) để phân biệt kiểm thử
local với VPS thật. Sau khi có server, cần chạy bộ image Linux và `smoke.sh`
trên VPS, kiểm tra chứng chỉ công khai, firewall nhà cung cấp, backup/restore
với role đích và tốc độ từ mạng Việt Nam trước khi phát tài khoản học sinh.
