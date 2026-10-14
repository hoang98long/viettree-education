# Rà soát học liệu, tải 50 học sinh và vận hành VPS

Ngày kiểm tra: **14/10/2026**. Mục tiêu ban đầu: **50 học sinh đồng thời**.
Kiểm thử HTTP dùng hai worker FastAPI và PostgreSQL thật trên Windows local;
không phải phép đo trên VPS của khách hàng. Database học tập hiện tại chỉ được
đọc để đối chiếu; dữ liệu mô phỏng được tạo trong database test riêng.

## 1. Học liệu Free/VIP

Ba môn lớp 1–5 có **340 bài, 1.920 câu hỏi, 280 đề luyện**. Mỗi khối có:

| Gói         | Bài học | Câu hỏi | Đề luyện |
| ----------- | ------: | ------: | -------: |
| Free        |      46 |     228 |       34 |
| VIP bổ sung |      22 |     156 |       22 |
| Tổng        |      68 |     384 |       56 |

[Báo cáo JSON](audits/content-2026-10-14.json) ghi riêng khối/môn/gói.
Đối chiếu schema nguồn và **1.920 phiên bản câu hỏi trong đề đã xuất bản**
không phát hiện cấu trúc đáp án không hợp lệ. `check-system` đạt: migration,
chính sách bài/câu/đề Free/VIP, gợi ý và đề có câu đúng môn/lớp.
Academy có đủ **180 bài**, 36 mỗi khối; `verify-ai-academy` không có lỗi
chất lượng được công cụ phát hiện. Các phép kiểm tra cấu trúc này không chứng
nhận tất cả nội dung ngữ nghĩa đều đúng.

Kiểm tra đáp án độc lập:

- Toán: **710 câu ở năm khối**, giải từ đề bài thay vì lấy đáp án chấm làm
  đáp án kiểm thử. Lớp 4 bổ sung bộ 88 câu còn thiếu; 54 câu tư duy đã có bộ
  đối chiếu riêng. Bao gồm phép tính, đơn vị, phân số, thập phân, hình học,
  thống kê, khoảng cách cây/cọc và suy luận Free/VIP.
- Lớp 3: bộ đáp án độc lập đủ **384 câu ba môn**, gồm đọc hiểu, chính tả,
  ngữ cảnh Tiếng Anh, chọn nhiều và sắp xếp.
- Lớp 4: bộ câu vận dụng mới có đối chiếu độc lập cả Tiếng Việt/Tiếng Anh.
- Lớp 5: đọc đối chiếu các bài Tiếng Việt và Tiếng Anh với ngữ liệu, lựa chọn
  và giải thích; lớp 1–2 kiểm tra ít lựa chọn, ngữ liệu được cung cấp đầy đủ,
  thời lượng ngắn và bài vận dụng nằm trong phạm vi khối.

Chưa phát hiện đáp án Toán sai trong các bộ giải độc lập. Với môn ngôn ngữ,
cần tiếp tục giáo viên đọc thử cùng học sinh để kiểm tra mức dễ hiểu thực tế;
kiểm thử tự động không đánh giá được toàn bộ sắc thái hoặc độ phù hợp của câu.
Một nhận xét biên tập: câu `Who should the group stay with?` trong học phần
`g5-should-advice` nên đổi thành câu hỏi về **children**, và nêu rõ việc ở cùng
giáo viên trong ngữ liệu nếu giữ lựa chọn có `teacher`. Đây là đề xuất cho
phiên bản học liệu mới; không ghi đè câu đã xuất bản hoặc đổi đề gắn với bài
làm cũ. Quy trình CMS tạo phiên bản mới và rà soát đề trước khi xuất bản.

## 2. Cải thiện đã thực hiện

- Bài đọc trong câu hỏi được tách thành khung **Bài đọc để tìm câu trả lời**;
  câu hỏi riêng, dễ nhìn. Đọc từng đoạn khoảng 35 tiếng cho lớp 1–2 và 55
  tiếng cho lớp 3–5; vẫn có **Xem cả phần** để đọc toàn bộ ngữ liệu.
- Giữ các dòng và dòng trắng giữa khổ thơ. Chữ phần đọc dùng màu đậm hơn.
  Không cắt ngữ liệu, không thêm tranh gợi lộ đáp án vào đề đang làm.
- Chấm điền khuyết chấp nhận cách viết số có khoảng trắng (`12 000`), khoảng
  trắng quanh dấu phân số (`3 / 8`) và dấu thập phân/chữ số 0 cuối tương
  đương khi bộ đáp án đã cho phép số thập phân (`4,750` bằng `4.75`).
- Vẫn giữ dấu Tiếng Việt, phủ định, yêu cầu chính tả và rút gọn phân số.
  Không coi `2/4` là đáp án thay cho `1/2` nếu đề chỉ chấp nhận dạng rút gọn;
  không đoán dấu chấm phân cách nghìn hoặc bỏ đơn vị sai.
- Các cải thiện tự lưu, kiểm tra request cũ, đồng hồ và rà soát học liệu
  trong admin tiếp tục được kiểm thử: [hướng dẫn](learning-reliability.md).

Không cần migration mới cho các thay đổi này. Không chạy seed để ghi đè học
liệu giáo viên đã sửa; không thay mật khẩu, gói hay lịch sử trong DB đang dùng.

## 3. Tải đồng thời

Hai nguy cơ được xử lý từ code:

1. Đăng nhập từng giữ kết nối API rồi mở kết nối thứ hai cho rate limit.
   Nay rate limit kết thúc trước khi mượn kết nối API. Worker mới cũng tự
   nạp metadata trong giao dịch ngắn này, kể cả khi đăng nhập là request đầu.
2. Nộp bài từng tính lại thống kê toàn hệ thống. Nay chỉ tổng hợp lại các
   phiên bản câu hỏi vừa chấm và ngày/môn của học sinh đó. Khóa PostgreSQL
   phối hợp giữa các lần nộp và lệnh sửa thống kê toàn bộ; hai tab nộp hai
   đề khác nhau vẫn không mất tổng ngày. Không cộng dồn số liệu mù theo retry.

Argon2 giữ nguyên độ mạnh; giới hạn hai phép xác thực mật khẩu nặng mỗi worker.
Hai worker cho tối đa bốn phép đồng thời, khoảng **256 MiB** cho vùng nhớ của
bốn phép Argon2 theo cấu hình hiện tại, chưa gồm RAM Python/DB/frontend.
Khi hàng chờ quá tải, trả 503 kèm `Retry-After`, thay vì tạo vô hạn phép xác thực.
Giới hạn chống thử mật khẩu vẫn là 120 lượt/IP/phút và 10 lượt/tài khoản/phút.

### Phép đo sau sửa

Mỗi học sinh mở danh mục/dashboard, tự giao đề, bắt đầu/resume, tải đề,
lưu hai câu, nộp, nộp lặp và xem lại kết quả: 11 request/hành trình.
Các tài khoản thuộc lớp 1–5, **25 Free / 25 VIP**. Đăng nhập được đo riêng.

| Đồng thời | Request học tập | Hoàn thành |      p95 |      p99 | Lỗi HTTP |
| --------: | --------------: | ---------: | -------: | -------: | -------: |
|        10 |             110 |      10/10 |   330 ms |   407 ms |        0 |
|        25 |             275 |      25/25 |   826 ms | 1.102 ms |        0 |
|        50 |             550 |      50/50 | 1.542 ms | 1.846 ms |        0 |

**50 lượt đăng nhập đồng thời:** 50/50 đạt; tổng 2,46 giây, p95 2,23 giây.
85 bài đã chấm và tổng thống kê ngày cùng bằng 85; không sai lệch thống kê câu.
[Dữ liệu sau sửa](audits/load-after-2026-10-14.json).

Mốc trước sửa ở 50 học sinh: p95 **2.242 ms**, p99 **3.333 ms**, 550 request
không lỗi. [Dữ liệu trước sửa](audits/load-before-2026-10-14.json).
Hai lần đo trên cùng máy, nhưng không khóa tài nguyên máy và lịch sử DB tăng
dần; đây là so sánh tham khảo, không chứng minh phần trăm tăng hiệu năng cố định.
Mốc trước sửa đăng nhập tuần tự, không dùng để so sánh tốc độ đăng nhập đồng thời.

### Ba vòng lưu đủ câu và nộp bài

Chạy thêm **50 + 50 + 50 hành trình**, lưu đủ 6–8 câu của đề đã chọn:
**2.310 request, 150/150 hành trình đạt**, không lỗi HTTP. p95 từng vòng
1,20 / 1,36 / 1,22 giây. Tổng 150 bài đã chấm khớp thống kê ngày; thống kê câu
không sai lệch. Nộp lặp trả cùng kết quả, không thêm bài hoàn thành.
[Dữ liệu ba vòng](audits/load-full-answers-2026-10-14.json).

Đây là các đợt tải ngắn, không phải soak test nhiều giờ hoặc kiểm thử hàng
triệu bài lịch sử. Chưa đo tải qua Next/Caddy/HTTPS hoặc trên phần cứng VPS.
Thời gian của 50 học sinh dùng thực tế còn phụ thuộc mạng, thời gian đọc,
trình duyệt, hình ảnh và dữ liệu tăng sau thời gian vận hành.

## 4. Cấu hình VPS và cache

Compose production truyền tham số giới hạn từ `.env.production`. Điểm bắt đầu:

| Biến                                    |  Mặc định | Ý nghĩa                                          |
| --------------------------------------- | --------: | ------------------------------------------------ |
| `SERVER_WORKERS`                        |         2 | Số tiến trình API                                |
| `SERVER_LIMIT_CONCURRENCY`              |       128 | Giới hạn mỗi worker; Uvicorn trả 503 khi vượt    |
| `PASSWORD_VERIFY_CONCURRENCY`           |         2 | Số phép Argon2 mỗi worker                        |
| `DB_POOL_SIZE` / `DB_POOL_MAX_OVERFLOW` |     5 / 5 | Tối đa 10 kết nối mỗi worker                     |
| `DB_POOL_TIMEOUT`                       |    5 giây | Chờ kết nối DB có giới hạn                       |
| `DB_STATEMENT_TIMEOUT_MS`               | 30.000 ms | Giới hạn một câu SQL                             |
| `DB_LOCK_TIMEOUT_MS`                    |  5.000 ms | Giới hạn chờ khóa DB, không treo chờ hết 30 giây |
| `SERVER_GRACEFUL_TIMEOUT`               |   30 giây | Thời gian chờ request lúc dừng                   |
| `BACKEND_STOP_GRACE_PERIOD`             |       45s | Docker chờ trước khi cưỡng bức dừng              |

Ngân sách kết nối API là `workers × (pool_size + max_overflow)`, mặc định
**20**, cộng kết nối vận hành/migration/backup. Tăng worker làm tăng cả RAM
và số kết nối, không mặc nhiên làm nhanh hơn. Pool có `pre_ping` và timeout;
tham khảo [SQLAlchemy pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html).

`BACKEND_STOP_GRACE_PERIOD` phải lớn hơn `SERVER_GRACEFUL_TIMEOUT`, nên chừa
ít nhất 10–15 giây. DB được chờ dừng 60 giây, frontend 30 giây. Compose chờ
health theo thứ tự DB → API → frontend → Caddy khi khởi động;
[cơ chế chính thức](https://docs.docker.com/compose/how-tos/startup-order/).

Cache tiếp tục giới hạn đúng dữ liệu: đối chiếu cấu trúc readiness thành công
tối đa 60 giây mỗi worker; migration/kết nối kiểm tra mỗi lượt. Quyền VIP,
phiên và bài làm vẫn đọc DB, response riêng tư `no-store`. Không cần bổ sung
Redis chỉ cho mức tải đã thử; chỉ cân nhắc cache danh mục công khai sau khi
đo nút thắt và thiết kế invalidation khi admin xuất bản/đổi quyền.

Đã kiểm tra `docker compose config --quiet`, Caddyfile và cú pháp `backup.sh`.
Đã thử API với kết nối DB thực sự bị từ chối: `/health` vẫn 200,
`/ready`/đăng nhập trả 503 an toàn; readiness hồi phục khi DB kết nối lại.
Kiểm tra giữ khóa hồ sơ bằng một kết nối PostgreSQL khác cũng trả 503 khi hết
thời gian chờ; thử lại sau khi nhả khóa chỉ tạo một assignment. Log lỗi DB có
SQLSTATE để chẩn đoán mà không ghi SQL, mật khẩu hoặc câu trả lời.

Theo dõi `pg_stat_activity` phát hiện dashboard giữ khóa hồ sơ trong giao dịch
đọc/ghi gợi ý, gây chờ khi chuyển nhanh sang bài luyện. **Dashboard nay chỉ đọc**:
không khóa hồ sơ, không ghi bảng gợi ý, vẫn tính gợi ý theo dữ liệu hiện tại.
Endpoint gợi ý riêng giữ cơ chế lưu cũ. Hồi quy dùng giao dịch PostgreSQL
`READ ONLY` và giữ khóa hồ sơ bằng kết nối khác để chứng minh dashboard không
bị chặn và không phát sinh bản ghi. Giới hạn chờ khóa 5 giây bảo vệ các thao
tác ghi khi bị tranh chấp.

Kiểm tra tải lại sau sửa dashboard: **50/50 đăng nhập**, **770 request lưu đủ
câu/nộp bài thành công**, p95 học tập **1,11 giây**, p99 **1,36 giây**;
50 bài chấm khớp tổng ngày, không sai lệch thống kê câu. Tám tình huống đọc
Free/VIP desktop/mobile chạy lại đạt, ngay cả khi đang đo tải; lặp thêm ba
vòng **24/24 đạt**, không tái hiện lỗi chờ khóa trước sửa.
[Dữ liệu cấu hình cuối](audits/load-dashboard-2026-10-14.json).
Chưa xác nhận build/run Linux containers, HTTPS, reboot hay backup/restore trên
VPS thật vì Docker Engine chưa chạy và chưa có thông tin truy cập VPS.

Trước khi mở thật, làm các bước trong [deploy-vps.md](deploy-vps.md), đặc biệt
build image, migrate/grant, kiểm tra HTTPS/cookie, backup và restore sang DB
khác, thử restart và đo 50 học sinh trên staging cùng cấu hình dự kiến.
Mốc local đủ để tiếp tục triển khai thử, không phải cam kết công suất server.

## 5. Chạy lại kiểm tra

Trong `backend`, chọn **database test riêng đã import/migrate/seed**; không
trỏ load probe vào DB học tập hiện tại. Công cụ từ chối tên DB không có `test`
và đối chiếu ID tài khoản đăng nhập với DB test trước khi gửi request học tập.
Tài khoản mô phỏng chỉ nằm ở DB test; mật khẩu/phiên không xuất vào báo cáo.

```powershell
# Audit chỉ đọc; chạy với DB đang cần đối chiếu.
../.venv/Scripts/python.exe -X utf8 scripts/audit_content.py --database --output ../docs/audits/content-2026-10-14.json

# Load: backend test tại 127.0.0.1:8001, COOKIE_SECURE=false cho HTTP local.
$env:DB_NAME = 'viettree-visual-browser-test'
../.venv/Scripts/python.exe -X utf8 scripts/load_probe.py --parallel-login --levels 10 25 50 --output ../docs/audits/load-after-2026-10-14.json
../.venv/Scripts/python.exe -X utf8 scripts/load_probe.py --parallel-login --answer-all --levels 50 50 50 --output ../docs/audits/load-full-answers-2026-10-14.json
```

Load probe hiện chỉ cho endpoint nội bộ `localhost`, `127.0.0.1` hoặc `backend`;
không phải công cụ tạo tải lên domain production. Hai lượt trên tạo tài khoản,
phiên, assignment và bài làm mới ở DB test; không tự xóa dữ liệu sau khi chạy.
Tránh chạy nhiều đợt đăng nhập sát nhau vượt giới hạn IP dùng chung.

Kiểm thử trình duyệt đã đạt **25 tình huống**, một biến thể mobile bỏ qua có
chủ ý vì tình huống đó thử cả ba thiết bị trong lượt desktop. Bao gồm đọc bài
Free/VIP lớp 1/5, tự lưu/reload/mất mạng, cỡ chữ riêng theo thiết bị, admin
biên soạn/duyệt, thư viện lớp 5/cấp thu hồi VIP và học Academy đủ năm khối.
Các kiểm tra còn lại và tổng cuối được ghi tại
[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md).
