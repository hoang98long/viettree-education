# 08 · Thay đổi và rollback · 11/11/2026

Ghi chú sau audit: người dùng đã duyệt dọn môi trường không phục vụ triển khai.
Container/image/volume Docker test và 122 mục tạm đã xóa; các đoạn giữ artifact
bên dưới ghi trạng thái lịch sử trước lần dọn này. Source, backup và database
ứng dụng được giữ. Trạng thái cuối tại evidence/environment-retention.json.

Nhánh `audit/2026-11-11-system-review`, baseline `2676328`; không tạo commit
hoặc đẩy source ra dịch vụ ngoài. Không sửa `.env`, database/schema SQL gốc,
UUID/codes nội dung, phiên bản câu hỏi hay lịch sử học đang dùng.

| Batch             | File chính                                                                                       | Thay đổi / kiểm chứng                                                                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chấm điểm         | `services/grading.py`                                                                            | Số thập phân có nhóm nghìn; regression đúng/sai/precision/case/fraction                                                                               |
| AI safety/quyền   | `academy/safety.py`, `tutor.py`, `learning.py`, `access.py`                                      | Unicode/PII, false-positive, consent tie, pinned hint, NFC/trim, ảnh legacy fail-closed                                                               |
| Upload/dependency | `academy/uploads.py`, requirements lock/pyproject                                                | Allowlist decoder trước parse, Pillow 13/Certifi vá; không dùng PoC nguy hiểm                                                                         |
| Content lint      | `curriculum/quality.py`                                                                          | Cảnh báo lựa chọn số tương đương; không tự sửa đáp án/học liệu                                                                                        |
| Tiến độ nhẹ       | `services/catalog.py`, `services/learning.py`, `api/routes/catalog.py`, `api/routes/learning.py` | Tách projection metadata phục vụ visit/complete; GET giữ response cũ; live quyền/owner và lock/write giữ nguyên; 72 regression đạt                    |
| Kiểm tra release  | `services/release_readiness.py`, `content_review.py`                                             | Cảnh báo bài nguồn chưa biên tập, batch read 2 query thay N+1; không tự áp dụng DB                                                                    |
| UX                | `components/modal*`, questions/students/content-access/assessment/attempt                        | Modal dùng chung, trap bàn phím/busy/name, retry, khóa trường đang lưu                                                                                |
| CSS               | `app/globals.css`                                                                                | Tương phản muted/green/sidebar/badge và wrap tên dài ở hồ sơ 320px                                                                                    |
| Test/CI           | Tests audit, source expectations, E2E/audit runner, prepare_e2e, workflow                        | Marker DB, exact pack inventory, axe, browser smoke mandatory fixtures, audits                                                                        |
| Deploy build      | `.dockerignore`, backend Dockerfile                                                              | Loại thư mục credentials/tooling khỏi context; tách layer dependency để source đổi không cài lại toàn bộ                                              |
| Local/probe       | `next.config.ts`, `.env.example`, `scripts/load_probe.py`                                        | Default backend IPv4 tránh fallback local; metrics theo endpoint, nearest-rank percentile, thêm actual lesson/visit/skills; không tuyên bố sửa AUD-22 |
| Tài liệu          | `docs/audit/01–09`, README                                                                       | Findings, scope/evidence, limitations, hướng dẫn chạy lại                                                                                             |

Không thêm migration. Head vẫn `0012_lesson_bookmarks`. Không backfill hay
ghi lại nội dung/điểm trong DB đang dùng. Các test database/container/volume
mang prefix audit được giữ lại, chỉ dừng tiến trình do đợt này tạo sau kiểm tra.

## Cập nhật môi trường

Backend cần cài lockfile mới trong môi trường triển khai rồi build lại image.
Venv local đang chạy của người dùng không bị ép dừng hoặc ghi đè DLL. Trước
khi chạy bản mới trên máy này, dừng backend bằng terminal của bạn, rồi:

```powershell
Set-Location 'D:\01_viettree_code\viettree-education\backend'
../.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
```

Frontend chạy `npm ci`, build lại. Không cần đổi `.env` hoặc seed lại tài khoản.
Pillow 13 là thay đổi major riêng để xử lý advisory, nằm trong giới hạn
project `<14`; không nâng major framework hàng loạt. Minimatch override
11.0.1 chỉ áp trong typescript-estree; bỏ override khi upstream đã dùng bản vá.

## Rollback

Giữ image release trước và diff của nhánh audit để reviewer chọn từng batch.
Nếu UI lỗi, quay riêng batch UI về source trước rồi build lại, giữ bản vá bảo
mật. Không chạy `reset --hard`, không rollback migration hoặc khôi phục DB
đè lên lịch sử học. Không quay dependency dễ bị tấn công ra public chỉ để
khôi phục giao diện; dùng maintenance và bản vá tương thích nếu cần.

Nếu phát hiện vấn đề dữ liệu ở một deployment tương lai, dừng traffic ghi,
phục hồi backup vào DB mới, đối chiếu và duyệt chuyển kết nối. Không xóa DB
cũ. Đợt này đã thử quy trình phục hồi bằng dữ liệu giả; backup thật ngoài
VPS và quyền truy cập vận hành vẫn cần người phụ trách xác nhận.

## Kiểm tra dữ liệu và artifact cuối

[source-preservation.json](evidence/source-preservation.json) xác nhận 83/83
bảng nguồn giữ nguyên hash trước/sau. Chỉ các database giả nhận ghi fixture,
attempt và tiến độ. Backup giả, DB/container/volume audit được giữ, không
DROP/TRUNCATE/reset. Không dừng tiến trình có sẵn của người dùng.

Không áp dụng lại seed hoặc editorial vào database đang dùng trong đợt này.
Khi triển khai release sau, backup trước, preview `review-learning-content`,
review thay đổi rồi mới apply theo hướng dẫn 04/11 và check-release. Không
lấy migration rollback làm cách hoàn tác nội dung/học bạ.

Frontend final build đã bỏ override kiểm thử, manifest xác nhận API IPv4 8000. Generated next-env giữ bản gốc; chỉ dừng web3201/API8201 do audit tạo.
Không đổi server8000/8001/3000 có sẵn. New Node runner import process tường
minh để ESLint không phụ thuộc globals; không tắt rule.

[environment-retention.json](evidence/environment-retention.json): bốn runtime
container audit đã dừng; không còn container đợt này đang chạy. Database,
volume, image, backup và trace giữ nguyên. User API8000/8001 còn hoạt động
khi kiểm tra cuối; không can thiệp các tiến trình có sẵn.
