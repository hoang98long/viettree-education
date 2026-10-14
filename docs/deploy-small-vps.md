# Triển khai gói VPS 3 cores / RAM 2 GB / SSD 50 GB

Ngày cập nhật: **14/10/2026**. Cấu hình theo gói trong ảnh: **3 cores, RAM gốc
2 GB, SSD 50 GB**. Không tính 1 GB tặng thêm vào yêu cầu tối thiểu vì phần đó
phụ thuộc đăng ký 12 tháng. Nếu được cấp 3 GB, dùng cùng profile để có thêm dư địa.

Đã chuẩn bị profile `small`, quy trình build trên máy khác và kiểm thử ứng dụng
với một worker/pool nhỏ. Chưa chạy Docker Linux hoặc đo tổng RAM trên VPS này;
chưa có SSH server đích và Docker Engine trên máy local chưa hoạt động. Các mức
giới hạn là cấu hình triển khai, chưa phải số RAM thực tế đã đo trong container.

## 1. Các điều chỉnh

| Dịch vụ                         | Giới hạn RAM | Cấu hình                                                               |
| ------------------------------- | -----------: | ---------------------------------------------------------------------- |
| PostgreSQL                      |      512 MiB | shared buffers 64 MB, work_mem 2 MB, tối đa 30 kết nối, giảm song song |
| Backend                         |      448 MiB | 1 worker; tối đa 96 request/connection theo Uvicorn; pool API 4 + 2    |
| Frontend                        |      384 MiB | Next standalone; V8 old-space tối đa 192 MiB                           |
| Caddy                           |       96 MiB | Go memory target 64 MiB, một logical processor cho Go                  |
| Migration, chỉ chạy khi bảo trì |      256 MiB | Dừng ứng dụng trước migration theo hướng dẫn chung                     |

Bốn dịch vụ chạy thường xuyên có tổng **giới hạn 1.440 MiB**. Phần còn lại dành
cho hệ điều hành, Docker và tác vụ vận hành; kiểm tra `free -m` trên máy thật
vì nhà cung cấp có thể tính GB khác GiB. Các quota CPU là trần từng dịch vụ,
không phải số cores được đặt riêng; hệ điều hành vẫn chia sẻ ba cores của host.

- API chờ kết nối DB bằng limiter riêng, không chiếm hết thread xử lý request
  trong lúc đợi pool nhỏ. Commit/rollback có slot riêng và kết thúc trước response.
- Rate limit dùng **một kết nối DB riêng mỗi worker**; tổng API + auth counter
  tối đa **7 kết nối** trong profile này, cộng readiness/backup/migration.
- Hash khi tạo/đổi/đặt lại mật khẩu và xác thực đăng nhập dùng chung **một slot
  Argon2**. Giữ nguyên độ mạnh mật khẩu; không giảm memory cost của thuật toán.
- `/ready` nạp metadata trước khi Caddy mở website. Profile cho khởi động tối đa
  60 giây trước khi tính lỗi healthcheck; tránh dồn nạp schema vào lượt login đầu.
- Log mỗi dịch vụ giới hạn 5 MB × 2 file. PostgreSQL giữ mặc định an toàn của
  `fsync` và commit; `max_wal_size` là mục tiêu mềm, không phải giới hạn ổ đĩa cứng.
- Giữ đủ bài lớp 1–5, AI lý thuyết, Free/VIP, lớp, admin và kết quả. Không thêm
  Redis/model AI hoặc dịch vụ mới vào VPS. Không cần migration/schema mới.

Profile giữ **project name và volumes của deployment hiện có**. `build` bị loại
khỏi backend/frontend; VPS chỉ chạy image đã build, không build frontend trên VPS.
Compose cần **2.24.4 trở lên** để dùng `!reset`.
[Cơ chế merge](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/).

## 2. Chuẩn bị VPS

Chọn **Ubuntu Server 24.04 LTS x86_64**, SSH/root hoặc sudo và môi trường cho phép
Docker/cgroups. Nếu loại ảo hóa không hỗ trợ Docker hoặc swap, cần xác nhận lại
với nhà cung cấp trước khi cài. Thực hiện DNS, SSH/firewall và Docker ở mục 1–3
của [hướng dẫn VPS chung](deploy-vps.md).

Kiểm tra tài nguyên:

```bash
uname -m
free -m
df -h /
docker compose version
docker info
swapon --show
```

Có thể thêm **2 GB swap** làm đệm khi cập nhật/backup. Ví dụ dưới chỉ tạo khi
chưa có swap và chưa có `/swapfile`; không ghi đè cấu hình swap đang tồn tại:

```bash
if [ ! -e /swapfile ] && [ -z "$(swapon --show --noheadings)" ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  printf '/swapfile none swap sw 0 0\n' >> /etc/fstab
fi
swapon --show
```

Swap chậm hơn RAM; nếu dùng swap liên tục thì giảm tải và kiểm tra lại bộ nhớ.
[Docker về RAM/swap](https://docs.docker.com/engine/containers/resource_constraints/).
Giữ ít nhất khoảng **10 GB trống** trên ổ 50 GB cho cập nhật, WAL và backup tạm.

## 3. Build và đóng gói trên máy Windows khác

Máy build cần Docker Desktop chạy **Linux containers**, đủ RAM/dung lượng cho
build Next.js. Máy hiện tại có thể dùng khi Docker Engine được bật. Không dùng
output `.next` đã build trên Windows để thay image Linux.

Tại thư mục project:

```powershell
./deploy/build-images.ps1 -Release '2026-10-14-small-v1'
```

Helper build hai image **linux/amd64** tuần tự, kiểm tra platform, xuất Docker
archive bằng `docker image save`, SHA256 và gói cấu hình triển khai. Không chạy
deploy qua SSH; không đóng gói `.env.production` hoặc database học sinh.

Kết quả tại `.artifacts/2026-10-14-small-v1/`:

- `viettree-2026-10-14-small-v1-linux-amd64.tar` và `.sha256`.
- `viettree-2026-10-14-small-v1-deployment.tar.gz` và `.sha256`.
- `release.json` mô tả tên image/platform/checksum.

Upload vào thư mục staging trên VPS do bạn tạo, ví dụ `/root/viettree-upload`:

```powershell
scp .artifacts/2026-10-14-small-v1/* root@VPS_IP:/root/viettree-upload/
```

Không ghi đè release artifact có sẵn; mỗi lần cập nhật dùng tag mới. Gói cấu
hình đã có các env **example**, Compose, wrapper, SQL gốc và script deploy nên
không cần upload toàn bộ source hoặc `node_modules`.

## 4. Load image và chọn profile trên VPS

Sau upload, trên VPS:

```bash
cd /root/viettree-upload
sha256sum -c viettree-2026-10-14-small-v1-linux-amd64.tar.sha256
sha256sum -c viettree-2026-10-14-small-v1-deployment.tar.gz.sha256
docker image load --input viettree-2026-10-14-small-v1-linux-amd64.tar
mkdir -p /opt/viettree-education
tar -xzf viettree-2026-10-14-small-v1-deployment.tar.gz -C /opt/viettree-education
cd /opt/viettree-education
```

Lần đầu tạo env:

```bash
umask 077
cp .env.production.small.example .env.production
chmod 600 .env.production
nano .env.production
```

Thay domain/email và **ba mật khẩu DB** bằng giá trị riêng; giữ
`VIETTREE_DEPLOY_PROFILE=small`, `RELEASE=2026-10-14-small-v1` trùng image đã load.
Khi cập nhật, giữ env thật; không copy example đè lên env đang sử dụng.

Mọi lệnh Compose của profile này dùng wrapper:

```bash
dc() { bash /opt/viettree-education/deploy/compose.sh "$@"; }
dc config --quiet
dc pull db caddy
dc run --rm --no-deps caddy caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
dc up -d db
```

Wrapper đọc đúng một biến chọn profile trong env, không `source`/chạy nội dung
file mật khẩu như shell. Nếu chọn profile sai, dừng với lỗi thay vì dùng cấu hình
khác. Chạy `dc config` không có `--quiet` có thể hiện secret, không đưa output đó
vào chat hoặc log công khai.

Thực hiện **mục 6–9 của hướng dẫn chung** để tạo DB roles, import/restore,
migrate, cấp runtime grant và tạo admin. Dùng hàm `dc` ở trên thay hàm Compose
trong hướng dẫn chung; image đã load nên **bỏ bước `dc build`**. Không seed demo
lên DB học sinh. Với DB đã có dữ liệu, backup và dùng nhánh restore/cập nhật,
không import SQL gốc lặp lại tùy tiện.

Khởi động sau khi schema/grant sẵn sàng:

```bash
dc up -d --no-build --pull never backend frontend caddy
dc ps
dc exec -T backend python -m app.cli check-system
dc exec -T backend python -m app.cli verify-ai-academy
docker stats --no-stream
```

Nếu thiếu image/tag, sửa hoặc load lại image; không build trên VPS để xử lý.
Kiểm tra HTTPS và các luồng ở mục 10 của hướng dẫn chung.

## 5. Backup, cập nhật và dung lượng

`deploy/backup.sh` đã dùng cùng wrapper, nên cron cũng chọn đúng profile `small`:

```bash
bash deploy/backup.sh
```

Script tạo cặp DB dump + media và kiểm tra đọc archive trước khi báo thành công;
không tự xóa bản backup. Chuyển bản sao ra máy khác hoặc kho backup độc lập,
kiểm tra restore. Trên ổ 50 GB chỉ giữ số bản local phù hợp dung lượng; xóa bản
cũ sau khi đã xác minh bản sao ngoài VPS. Snapshot nhà cung cấp là lớp bổ sung.

Cập nhật: build/export trên máy khác → upload/verify/load → backup → dừng
Caddy/frontend/backend → migration/grant nếu release yêu cầu → đổi `RELEASE`
trong env → `dc up -d --no-build --pull never backend frontend caddy` → kiểm thử.
Giữ image release cũ để rollback code khi schema tương thích. Không dùng
`docker compose down -v`, `docker system prune --volumes` hoặc xóa volume DB.

Theo dõi `df -h`, `free -m`, `docker stats`, health và log 503/429. Chưa bật
audio/video hoặc lưu file lớn đại trà. Khi chỉ có 2 GB RAM, cập nhật và các
tác vụ nhập/xuất hàng loạt nên làm trong khung bảo trì.

## 6. Kết quả kiểm chứng và giới hạn

Load dùng PostgreSQL thật, một worker, password slot=1, pool API 4+2/timeout
10 giây và chỉ cho **backend** chạy trên ba logical CPU của máy Windows local.
Sau `/ready`, **50/50 đăng nhập đồng thời đạt** (p95 khoảng 4,06 giây).

| Học sinh đồng thời | Request lưu đủ câu/nộp/xem kết quả | Hoàn thành |      p95 |
| -----------------: | ---------------------------------: | ---------: | -------: |
|                 10 |                                154 |      10/10 |   338 ms |
|                 25 |                                385 |      25/25 |   837 ms |
|                 50 |                                770 |      50/50 | 1.543 ms |

Không lỗi HTTP; 85 bài đã chấm khớp tổng ngày, thống kê câu không lệch.
[Báo cáo raw](audits/load-small-vps-2026-10-14.json).
Backend riêng có working set đỉnh khoảng **174 MiB** trong cửa sổ lấy mẫu của
lượt thử; đây không phải tổng RAM cả VPS hoặc số đo dưới Linux cgroups.
[Cấu hình và quan sát bộ nhớ](audits/small-vps-observation-2026-10-14.json).

Kiểm tra phát hiện pool nhỏ làm các thread chờ DB chiếm hết thread endpoint;
đã chuyển chờ kết nối ra limiter riêng, dùng slot riêng cho commit và auth guard.
Hồi quy dùng **pool một kết nối, một thread endpoint, sáu request đồng thời**
đạt; commit/rollback trước response, DB mất kết nối, quyền và deadline tiếp tục
được kiểm tra. Profile merge giữ nguyên volumes/cổng private, không có build
trên VPS; cú pháp Bash/PowerShell được kiểm tra.

Kiểm tra: **754 unit không cần DB đạt**, 76 ca tài khoản/vận hành đạt, 43 ca
API/giao dịch/quyền/tải đạt sau thay đổi xử lý pool, 4 ca hồi quy pool/commit
đạt, 29 ca readiness/vận hành đạt và 2 ca contract deployment đạt. Các lượt
có phần trùng nhau, không cộng số ca để suy ra tổng duy nhất.
Frontend standalone chạy với `--max-old-space-size=192` đã đạt **14 tình huống
Chrome desktop/mobile**: đọc Free/VIP, tự lưu/mất mạng, tranh, thư viện lớp 5 và
cấp/thu hồi VIP. Không sửa nội dung bài hoặc bỏ chức năng để giảm tài nguyên.

Chưa đo PostgreSQL với shared buffers mới, tổng RAM/disk/CPU trên VPS, build
image Linux, áp dụng quota container hoặc tải 50 người qua Caddy/HTTPS. Cần
chạy thử trên VPS theo đúng profile trước khi mở rộng sử dụng. Mục tiêu vẫn
là 50 người, nhưng các số đo local không bảo đảm cùng độ trễ trên VPS thực tế.

Nguồn cấu hình PostgreSQL:
[Resource Consumption](https://www.postgresql.org/docs/18/runtime-config-resource.html).
