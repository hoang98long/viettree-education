# Triển khai và vận hành AI Academy

## Local Windows

Dùng [run-local.md](../run-local.md). Nếu môi trường đã có sẵn, chỉ cập nhật
dependencies mới, migrate, seed và khởi động lại. Không ghi đè `.env` bằng file
mẫu: `CHANGE_ME_*` là placeholder, phải điền mật khẩu của chính môi trường.

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\backend'
../.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
../.venv/Scripts/python.exe -m app.cli check-system
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --no-access-log
```

Terminal frontend: `INTERNAL_API_URL=http://localhost:8000`, `PORT=3000`,
`npm run dev`. URL http://localhost:3000/ai-academy, đăng nhập người dùng hiện có.
DB local đã được nâng head 0010 và nạp học liệu trong đợt triển khai này.

## VPS / Docker

Theo toàn bộ [deploy-vps.md](../deploy-vps.md) để tạo DB roles, HTTPS, grant và
release. Production Compose `docker-compose.production.yml` có `academy_media`
volume tại `/workspace/var/ai-media`; user backend không phải root. Bundled SVG
đi trong image. Migration chạy bằng owner, seed content bằng runtime sau grant.

```bash
docker compose --env-file .env.production -f docker-compose.production.yml build
docker compose --env-file .env.production -f docker-compose.production.yml run --rm migrate
# Chạy deploy/grant-runtime.sql như hướng dẫn VPS, rồi:
docker compose --env-file .env.production -f docker-compose.production.yml run --rm backend python -m app.cli seed-ai-academy
docker compose --env-file .env.production -f docker-compose.production.yml up -d backend frontend caddy
docker compose --env-file .env.production -f docker-compose.production.yml exec -T backend python -m app.cli verify-ai-academy
```

`run migrate` cần profile operations nếu bản Compose đang dùng yêu cầu profile:
thêm `--profile operations` trước `run`. Kiểm `/health`, `/ready`, head 0010,
đăng nhập học sinh/teacher/guardian/admin và duyệt media. Không cần model server
cho simulation. `check-system` kiểm LMS; dùng thêm `verify-ai-academy` cho module.

## Tùy chọn Ollama

Mặc định `AI_PROVIDER=simulation`, model rỗng; các flag external tắt.
Muốn dùng model local: tự provision Ollama/model có giấy phép phù hợp, cấu hình
`AI_PROVIDER=ollama`, `AI_OLLAMA_URL`, `AI_OLLAMA_MODEL`, khởi động backend lại;
test model rồi admin xác nhận chính sách ở UI. Chỉ host local/ollama được chấp
nhận, không URL tùy ý. Trong container, 127.0.0.1 là chính container; phải nối
dịch vụ `ollama` trong network hoặc endpoint host có cấu hình mạng phù hợp.
Không public Ollama lên internet. Consent, quota và moderation vẫn bắt buộc.
Repo chưa tự cài/pull model, không có khóa trả phí hoặc provider cloud.

## Backup / restore

`deploy/backup.sh` tạo cặp DB dump + archive private media cùng timestamp.
Cần sao lưu cả hai, mã hóa/giới hạn quyền và giữ bản ngoài VPS theo chính sách.
Với restore, khôi phục DB **mới**, verify schema/head; phục hồi archive vào
private media volume bằng cùng release rồi kiểm 3 variants và phân quyền trước
khi chuyển traffic. Không dùng `docker compose down -v` trên deployment có dữ
liệu. Bundled SVG khôi phục bằng release code/hash manifest tương ứng.

## Troubleshooting

- 503 readiness: chạy migration bằng owner, cấp grant rồi restart backend.
- 403 teacher: kiểm global teacher + chủ lớp; CMS cần grant editor/reviewer.
- Guardian trống: kiểm verified_at, không tự suy ra liên kết theo tên.
- 409 draft: tải lại trước sửa, không lặp ghi từ tab cũ.
- 409 media: đang dùng ở published, thay hoặc ẩn bài trước thu hồi.
- Model vẫn mô phỏng: kiểm env/flag/provider/policy/consent và quota; đây là
  fallback có chủ ý. Không nhập dữ liệu thật để thử model.
- 404 ảnh upload: kiểm private volume, manifest/release và restore media.
- Thay API port khi build production: đặt INTERNAL_API_URL **lúc build**;
  không chỉ đặt lúc `next start`. Tests phải trỏ DB/port test riêng.
