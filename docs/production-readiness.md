# Kiểm tra trước triển khai thực tế

Đợt bổ sung 12/10/2026: head hiện tại `0011_classes_vip_training`, có lớp,
thành tích, giá/ưu đãi và đào tạo AI Free/VIP. DB local đã backup/migrate và
đối chiếu giữ mọi hàng/cột cũ. Giữ `AI_TRAINING_ONLY=true`; cấp runtime grant
sau migrate khi deploy. Kết quả và giới hạn kiểm chứng mới tại
[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md),
[lớp/thành tích](classes-achievements.md), [giá](vip-pricing-research.md).
Các mốc kiểm thử ngày 10/10 bên dưới là lịch sử đợt vận hành trước Academy.

Cập nhật 10/10/2026. Đợt rà soát này tập trung vào vận hành và kiểm tra hồi quy
cho học sinh/admin, học liệu lớp 3–4 và quyền Free/VIP. Không thay SQL gốc,
không reset mật khẩu, cấp lại gói hay xóa dữ liệu database đang sử dụng.

## Thay đổi đã triển khai

- Bộ production có sẵn: Compose, Dockerfile dùng lock, Next standalone,
  HTTPS qua Caddy, user ứng dụng không phải root, không publish DB/API trực tiếp,
  giới hạn kích thước request và log. Cấu hình local vẫn dùng file development.
- Tách role cấu trúc `viettree_owner` với role dữ liệu `viettree_app`;
  migration chạy chủ động trước release, sau đó cấp quyền dữ liệu.
- `/ready` kiểm tra kết nối và Alembic head trực tiếp mỗi lần; chỉ cache đối
  chiếu bảng/cột thành công tối đa 60 giây trong từng worker, không cache auth.
  DB có cấu trúc đủ nhưng chưa chạy migration 0009 vẫn nhận 503.
- Cấu hình từ chối tên môi trường sai, origin rỗng/wildcard/đường dẫn và HTTPS
  không hợp lệ trong production. DB có timeout kết nối, câu lệnh và pool.
- Giới hạn đăng nhập độc lập: 120 lượt/IP/phút, 10 lượt/username/phút,
  username chuẩn hóa; IP lấy từ kết nối đã được Uvicorn xác minh proxy.
  Phù hợp nhiều học sinh dùng chung mạng; trả 429/Retry-After khi vượt ngưỡng.
- Admin có **Kiểm tra hệ thống** tại `/admin/system`: migration, quyền học
  liệu, đề rỗng/sai môn/lớp/câu nháp, quyền gợi ý VIP và thống kê auth cũ.
  Endpoint chỉ admin, chỉ đọc, no-store; không gửi thông tin tài khoản/bí mật.
- API sinh `X-Request-ID` và log cùng mã; lỗi bất ngờ trả 500 an toàn.
  Không phản chiếu exception, SQL, input hay password. API docs tắt production.
- CLI `check-system` chỉ đọc, exit 1 nếu cần xử lý; `cleanup-auth` mặc định
  dry-run, chỉ áp dụng khi có `--apply`, retention 1–365 ngày (mặc định 30).
  Công cụ không tác động lịch sử học tập, audit, users hay membership.
- CLI `bootstrap-admin` nhập password ẩn qua terminal, chỉ tạo admin đầu tiên,
  không thay tài khoản cũ. Các tài khoản tiếp theo tạo qua giao diện quản trị.
- Script backup ghi file tạm riêng, kiểm tra archive rồi mới đổi tên; không tự
  xóa backup. Quy trình restore thử dùng database mới.

## Dùng ngay trên local

Khởi động lại backend/frontend theo [run-local.md](run-local.md), đăng nhập admin,
mở **Kiểm tra hệ thống**. Không cần migration mới ngoài head hiện có
`0009_guided_hints` cho các cải thiện vận hành này.

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\backend'
../.venv/Scripts/python.exe -m app.cli check-system
../.venv/Scripts/python.exe -m app.cli cleanup-auth --retention-days 30
```

Hai lệnh trên chỉ đọc. Khi vận hành, tự đặt lịch auth cleanup với `--apply`
sau khi quyết định thời gian lưu dữ liệu; không tự dọn DB thật trong đợt này.

## Kiểm chứng và giới hạn

Kết quả đầy đủ của lần kiểm thử cuối được ghi trong
[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md). Unit/integration/browser
sử dụng database riêng `viettree-education-test`; không chạy vào DB sản xuất.
Audit npm và pip-audit của lock backend ngày 10/10/2026 không ghi nhận lỗ hổng
đã biết; đây là kết quả tại thời điểm kiểm tra, không bảo đảm mọi lỗ hổng đều có
trong cơ sở dữ liệu advisory. Docker Compose và Caddyfile đã kiểm tra cấu hình
(Caddy 2.11.7 chính thức). Đã dùng PostgreSQL 18 local để pg_dump database test
và phục hồi vào DB test mới; check-schema/readiness/check-system đạt sau phục hồi.
Máy hiện không chạy Docker Engine nên chưa xác nhận build/run container hay
VPS/HTTPS. Restore local không thay thế diễn tập phục hồi trên VPS và role đích.

Trước khi mở cho học sinh thật, thực hiện trên staging/VPS:

1. Build image, validate Caddy, import/restore vào DB đúng owner, migrate và grant;
   chạy check-schema/check-system, xác nhận không publish cổng nội bộ.
2. Kiểm tra HTTPS/cookie Secure, đăng nhập/đổi mật khẩu/thu hồi phiên, quyền
   student/admin và Free/VIP cả khi hết hạn; tạo dữ liệu thử riêng.
3. Thử đọc bài, gợi ý, lưu/tải lại/nộp bài/xem kết quả trên điện thoại và desktop.
4. Chạy backup và restore thực sự vào DB mới; có bản sao ngoài VPS, theo dõi
   health/error/dung lượng và diễn tập rollback với đúng migration head.
5. Đo tải theo số lớp/người dùng dự kiến. Cá nhân hóa hiện rebuild thống kê từ
   lịch sử sau nộp bài; chưa có benchmark chứng minh phục vụ tải lớn.
6. Giáo viên rà soát học liệu/đáp án; đơn vị vận hành hoàn thành quy trình đồng ý
   sử dụng dữ liệu trẻ em và quyền truy cập trước khi cấp tài khoản thật.

Teacher/guardian quản lý lớp, MFA, quên mật khẩu qua email, thanh toán tự động,
audio và chấm tự luận chưa được triển khai; giao diện thể hiện đúng phạm vi.

## Tham số vận hành

| Biến backend              | Mặc định | Phạm vi     |
| ------------------------- | -------- | ----------- |
| `DB_CONNECT_TIMEOUT`      | 5 giây   | 1–30        |
| `DB_STATEMENT_TIMEOUT_MS` | 30000 ms | 1000–300000 |
| `DB_POOL_SIZE`            | 5/worker | 1–50        |
| `DB_POOL_MAX_OVERFLOW`    | 5/worker | 0–50        |
| `DB_POOL_TIMEOUT`         | 5 giây   | 1–30        |
| `LOGIN_IP_LIMIT`          | 120/phút | 10–1000     |
| `LOGIN_ACCOUNT_LIMIT`     | 10/phút  | 3–30        |

Hai worker mặc định có thể dùng tối đa 20 kết nối DB, thêm kết nối cho công cụ
vận hành/migration. Điều chỉnh theo phép đo và tài nguyên PostgreSQL; env trong
Compose backend cần khai báo bổ sung nếu thay giá trị ngoài các mặc định này.
