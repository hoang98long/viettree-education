# Kiểm thử AI Academy

Ngày thực hiện 12/10/2026. Tất cả kiểm thử ghi chạy trên PostgreSQL
`viettree-education-test`, không trên DB học tập. Tests dùng transaction rollback;
Playwright dùng user/class fixture mới, server riêng 8001/3001, một worker.

## Lệnh

Backend đã migrate/seed **database test** trước khi chạy. Settings đọc DB_NAME,
không đọc DATABASE_URL. Chỉ truyền URL test vào pytest, không in mật khẩu.

```powershell
$env:DB_NAME = 'viettree-education-test'
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
$env:TEST_DATABASE_URL = & '../.venv/Scripts/python.exe' -c "from app.core.config import settings; print(settings().database_url.render_as_string(hide_password=False))"
../.venv/Scripts/python.exe -m pytest -q
../.venv/Scripts/python.exe -m ruff check app tests scripts
../.venv/Scripts/python.exe -m ruff format --check app tests scripts
```

Frontend: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`.
Browser: tạo fixtures bằng `backend/scripts/prepare_e2e.py` (chỉ DB test), truyền
JSON output thành các env E2E_*; mật khẩu test lấy từ env riêng, không ghi vào
file JSON. Trỏ backend8001 tới DB test; `ALLOWED_ORIGINS=http://localhost:3001`.
Build frontend với INTERNAL_API_URL8001, server3001 và E2E_BASE_URL3001, rồi
`npm run test:e2e`. Không chạy browser ghi đồng thời với pytest transaction seed
trên cùng DB vì advisory/row locks. Fixture admin/test password phải là mật
khẩu của DB test, không tài khoản production.

## Phạm vi kiểm chứng

- 200 bài: content schema, 7 steps, ≥3 mục tiêu, hoạt động, 3 câu checkpoint,
  teacher/support/advanced và refs media.
- 1702 file: hash/XML/size/alt/không trùng/mapping, chỉ tiêu từng nhóm.
- Auth/IDOR/grade/staff/class/guardian; seed giữ edits; attempts/idempotence,
  no answer leak, điểm/huy hiệu một lần, resume hoạt động đã đạt.
- CMS CAS/workflow/publish/ẩn khi có draft mới, media đang dùng, SVG jobs,
  resize/upload và reject SVG tùy ý.
- Tutor disabled không network; mocked adapter enabled có consent, thu hồi,
  không gửi raw student text/ID; moderation không lưu PII bị chặn.
- Sản phẩm revision, teacher đúng lớp/trẻ còn ghi danh, tổng rubric; prompt
  phiên bản, teacher guidance, verified guardian link; export và gỡ project
  text không xóa người dùng/hàng lịch sử.
- Browser desktop/mobile: học/chấm/reload/badge/lab/tutor/privacyblock,
  autosave/nộp sản phẩm, teacher/rubric/guardian, adminclone/preview/media;
  hồi quy accounts/authoring/FreeVIP/grade3/hints/sessions/system cũ.

## Kết quả

Đợt lớp/giá/đào tạo Free/VIP tiếp theo đã nâng head 0011. Backend vòng toàn
hệ thống 476 passed; các ca Academy/lớp/membership và VIP đồng thời được kiểm
lại sau bổ sung. Browser hiện có 36 kịch bản riêng biệt đã đạt: 34 lượt đầu
và sáu ca liên quan được chạy lại thành công sau sửa. Xem chi tiết, thời gian
và cách tính các tập lặp tại [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md).
Các số bên dưới là kết quả lịch sử của đợt Academy trước chính sách này.

Lượt toàn bộ backend cuối: **468 passed**, 379,55 giây. Sau thêm kiểm tra chất
lượng và mục bài được giao: **67 kiểm thử Academy passed**, 39,45 giây (tập con
cộng một kiểm thử mới, không cộng dồn 468+67). Có một deprecation warning Starlette/httpx.
Frontend 19 component tests, lint/TypeScript và production build đã qua.
Browser: 32 kịch bản desktop/mobile đã qua, không skip (30 lượt đầu + 2 đã sửa
selector và chạy lại thành công). 26 kịch bản thuộc hồi quy LMS cũ.
Các kiểm tra triển khai được ghi bổ sung tại
[IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md).

Smoke sau thay đổi cuối: 4 trang kiểm chứng ảnh phân số đã sửa trên desktop/
mobile, mục bài được giao và Tổng quan48/48; không pageerror/5xx, ảnh hỏng
hoặc tràn trang. Đã xem ảnh thật. `verify-ai-academy` trên DB local trả quality
48/48 và issues rỗng; check-schema/check-system cũng đạt. Tất cả hàng LMS ban
đầu đối chiếu hash vẫn nguyên vẹn.

## Giới hạn

Mock HTTP xác minh adapter/policy, không chứng minh chất lượng model thật.
Không gọi paid API hoặc đưa dữ liệu trẻ tới external service. Docker config
validation không thay build/run container; HTTPS/thông lượng thực phải test
VPS đích. Chưa có kiểm thử tải diện rộng, chứng nhận accessibility hoặc audit
bảo mật độc lập. Kiểm thử browser dùng Chrome installed và responsive mobile,
không thay kiểm tra thiết bị iOS thật.

Đợt 19/10: [biên bản kiểm thử AI và tải 50 học sinh](../audits/academy-quality-2026-10-19.md).
