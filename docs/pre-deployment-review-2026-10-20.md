# Rà soát trước triển khai — 20/10/2026

Bản này bổ sung báo cáo trước mở web trong quản trị và lệnh `check-release`.
Đã kiểm chứng 1109 ca backend, 92 frontend unit và 133 biến thể trình duyệt.
[Biên bản tổng hợp và cách tính](audits/release-quality-2026-10-20.md).
Giữ học liệu hiện tại: 415 bài / 2250 câu / 355 đề ba môn và 200 bài AI,
1702 SVG. Không thêm migration, không đổi tài khoản, mật khẩu, VIP hay kết quả
học ở database local đang dùng. Head vẫn `0012_lesson_bookmarks`.

## Báo cáo trước mở web

Vào **Quản trị → Kiểm tra hệ thống → Trước khi mở web → Kiểm tra trước khi mở web**.
Báo cáo chạy khi quản trị yêu cầu; gồm:

- Các kiểm tra migration, quyền Free/VIP, đề và câu hỏi hiện hành.
- Tài khoản demo cần xử lý, quản trị đã đặt mật khẩu riêng và role DB runtime.
- Số bài/câu/đề đang xuất bản của đủ 15 cặp khối/môn, đối chiếu số tối thiểu của
  bộ nền tảng. Bài bổ sung và bài giáo viên tạo được tính vào số thực tế.
- Bài AI đủ phiên bản xuất bản, cấu trúc/rubric hợp lệ, ảnh tham chiếu được duyệt.
- File SVG có đủ trong bản ứng dụng, đúng hash/XML và mapping.
- Việc cần xử lý theo từng hạng mục; tải biên bản CSV cùng số thực tế/tối thiểu.

Trạng thái kiểm tra hiển thị thành danh sách co giãn, đọc được cả nhãn và kết
quả trên điện thoại; bảng số lượng chi tiết được thu gọn riêng.

API `GET /api/v1/admin/release-status` chỉ cho admin, trả `no-store`, không trả
payload, đáp án, mật khẩu hoặc danh sách học sinh. Kiểm tra chỉ đọc và không
đưa vào `/ready`; readiness tiếp tục nhẹ để phục vụ healthcheck.

CLI trong terminal backend:

```powershell
../.venv/Scripts/python.exe -m app.cli check-release
```

Lệnh trả exit code **0** khi các kiểm tra đều đạt, **1** khi còn hạng mục cần
xử lý. `check-system` và `check-launch` vẫn dùng được. `deploy/smoke.sh` dùng
`check-release` trước khi kiểm tra HTTPS và backup để tránh thông báo thành công
khi bản ứng dụng hoặc học liệu chưa đủ.

## Những gì đã đối chiếu

- Rà soát schema 1920 câu nguồn nền tảng và **2250 phiên bản câu hỏi** thuộc
  các đề đang xuất bản trong DB: không phát hiện lỗi cấu trúc.
- Backup nhất quán của DB local, phục hồi vào database test tên mới; **83 bảng**
  khớp số hàng và dấu vân tay toàn bộ dữ liệu. Đã bỏ database phục hồi tạm.
- Nguồn hiện không có ảnh Academy do người dùng tải lên. Các nhánh archive,
  CRC và lỗi backup ảnh được kiểm thử với file tổng hợp; SVG bundled được kiểm
  trực tiếp qua manifest. Cần kiểm tra backup ảnh thực sau khi có upload trên VPS.
- Tra cứu trực tuyến các dependency đang khóa bằng npm audit và pip-audit:
  không ghi nhận lỗ hổng đã biết tại thời điểm kiểm tra. Kết quả không loại trừ
  lỗ hổng chưa được công bố.
- Gói wheel Python có đủ 1702 SVG, manifest, hai schema và module chẩn đoán mới.
- CI chuẩn bị rõ bộ AI và bốn bộ học liệu bổ sung trước khi chạy toàn bộ pytest,
  tránh phụ thuộc dữ liệu còn lại từ một lần chạy local trước đó.

Các biên bản: [học liệu](audits/content-release-2026-10-20.json),
[phục hồi DB](audits/restore-full-2026-10-20.json),
[ảnh](audits/media-release-2026-10-20.json),
[dependency](audits/dependencies-release-2026-10-20.json),
[đóng gói](audits/package-release-2026-10-20.json),
[preflight](audits/preflight-release-2026-10-20.json),
[cài mới từ DB trống](audits/clean-install-release-2026-10-20.json).

## Trạng thái local và điều kiện mở công khai

DB local có đủ số lượng học liệu, AI và SVG. Bốn điều kiện production hiện còn
được báo cần xử lý: đang chạy development; **21 tài khoản demo** chưa khóa/đổi
mật khẩu qua quản trị; chưa có admin đáp ứng dấu mốc đặt mật khẩu riêng; kết nối
DB local đang dùng quyền quản trị. Các tài khoản này được giữ để bạn tiếp tục
dùng thử local.

Trên bản sao test riêng, đã xử lý các điều kiện đó, dùng backend production
hai worker/pool 4+2, role runtime ít quyền, Next standalone với heap 512 MiB,
Caddy HTTPS thật và kiểm thử theo múi giờ Nhật. `check-release` đạt toàn bộ.
Chứng chỉ là CA local, chưa phải chứng chỉ tên miền công khai; không cài CA vào
trust store của Windows. Chỉ browser test trên localhost được bỏ xác minh trust;
probe HTTPS dùng đúng CA để xác minh chứng chỉ.

Docker Engine trên máy hiện tại chưa chạy, nên không xác nhận build/chạy toàn
bộ Compose Linux trong đợt này. Workflow có bước build hai image trên Linux,
nhưng chưa có kết quả chạy GitHub Actions hoặc VPS/SSH thật trong phiên này.

## Cập nhật lên VPS

1. Backup DB và thư mục upload, kiểm tra checksum trước khi thay release.
2. Cập nhật source/image, chạy migration nếu server còn ở head cũ. Đợt này
   không yêu cầu nạp lại học liệu trên máy đã đủ bộ 19/10.
3. Giữ chế độ bảo trì, dùng đúng profile `vps8gb`. Sau restore, xử lý demo và
   admin qua quản trị tài khoản, cấp role DB runtime theo hướng dẫn VPS.
4. Khởi động bản mới và chạy:

   ```bash
   dc run --rm -T --no-deps backend python -m app.cli check-release
   bash deploy/backup.sh
   bash deploy/smoke.sh --require-backup
   ```

5. Dùng tên miền thật để thử Free/VIP, lưu/nộp bài, học tiếp, gợi ý và quản trị
   trên điện thoại; sau đó tắt bảo trì để mở công khai. Đo lại tải và độ trễ từ
   Việt Nam đến VPS Nhật; số đo local không phải cam kết dung lượng/SLA.

Hàm `dc` và thứ tự build/migrate/grant có trong
[hướng dẫn VPS](deploy-vps.md) và [profile VPS Nhật](deploy-vps-japan.md).
Local chỉ cần khởi động lại backend/frontend để thấy báo cáo mới.

## Đo tải qua HTTPS local

Cả hai đợt dùng Caddy với chứng chỉ được probe xác minh bằng CA local, backend
production hai worker/pool 4+2, giới hạn tiến trình API vào bốn CPU. Đây là host
Windows local với PostgreSQL thật, không phải máy VPS Nhật hoặc phép đo mạng quốc tế.

| Tải                                | Kết quả                                                         | Độ trễ p95 |
| ---------------------------------- | --------------------------------------------------------------- | ---------- |
| 50 đăng nhập đồng thời             | 50/50 thành công, không lỗi HTTP                                | 8398,06 ms |
| 50 học sinh luyện ba môn           | 750/750 HTTP 200; 50 lượt đã chấm; không lệch thống kê          | 2632,17 ms |
| 50 học sinh học AI, 25 Free/25 VIP | 800/800 HTTP 200; đủ tiến độ, không trùng điểm/lượt khi gửi lại | 2570,06 ms |

Độ trễ đăng nhập đỉnh cao hơn do hàng đợi xác minh mật khẩu hai luồng/worker. Các
request học đo riêng sau login; bài luyện gồm lưu đủ đáp án, học tiếp, nộp lại
và đối chiếu kết quả DB. Có lưu lượng browser kiểm thử cùng host; số đo là
kiểm tra chức năng khi có tải, chưa phải benchmark/SLA.

[Kết quả ba môn](audits/core-https-load-50-2026-10-20.json) ·
[Kết quả AI](audits/academy-https-load-50-2026-10-20.json).
