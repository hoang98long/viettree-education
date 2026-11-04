# Biên bản học liệu và giao diện — 04/11/2026

Phạm vi: bộ `discovery-2026-04`, hai thư viện, chọn bài luyện sau khi đọc,
bố cục gợi ý trên điện thoại và phần code được tổ chức lại.

## Kiểm thử đã chạy

| Kiểm chứng                                                           | Kết quả                                   |
| -------------------------------------------------------------------- | ----------------------------------------- |
| Backend, toàn bộ test không có marker integration                    | **881 passed**, 9 skipped, 235 deselected |
| PostgreSQL: discovery, practice library, bookmarks, library snapshot | **14 passed**, 11 deselected              |
| Frontend component                                                   | **93 passed**, 23 file                    |
| Browser: 5 khối × Free/VIP × desktop/mobile                          | **20 passed**, 3,9 phút                   |
| Browser: bố cục gợi ý desktop và điện thoại 320/390 px               | **2 passed**                              |
| Ruff check và format                                                 | Đạt, 232 file Python                      |
| ESLint, Prettier, TypeScript                                         | Đạt                                       |
| Next production build                                                | Đạt                                       |
| CLI `check-system` trên local                                        | `status: ok`                              |
| Đối chiếu bốn bộ bổ sung cũ và 200 payload AI                        | Không đổi                                 |

Đợt tích hợp chạy trên `viettree-education-test`, trình duyệt trên
`viettree-visual-browser-test`, dùng học sinh riêng từng khối/gói/thiết bị.
Không kiểm thử ghi bài làm trên database học thật. Có một cảnh báo deprecation
của Starlette TestClient/httpx; không có kiểm thử thất bại trong các vòng cuối.
Các test bị loại bằng marker không được tính là đã chạy lại.

22 ca browser gồm 20 ca học và hai ca bố cục. Các ca học mở **30 bài mới trên
cả hai loại màn hình**, hoàn tất 60 lượt luyện với **240 câu trả lời**, chấm
đúng bốn câu mỗi lượt; kiểm tra tiến độ đọc, ảnh tải được, gợi ý 1/3, bài luyện
của bài đang đọc, lọc theo bộ/môn/gói/kết quả và xóa bộ lọc. Free bị chặn khi
gọi thẳng API bài VIP. Không phát hiện tràn ngang ở các trang được kiểm tra.
Đã xem ảnh chụp thực tế, sửa nút gợi ý bị ép xuống nhiều dòng rồi kiểm tra lại.

Test nội dung xác thực schema cả 30 bài/120 câu, minh họa, ba gợi ý, độ dài bài
lớp nhỏ và một đáp án đúng duy nhất. Đáp án **40 câu Toán** được đối chiếu với
bảng đáp án viết riêng; đoạn đọc và đáp án Tiếng Việt/Tiếng Anh được rà soát
khi biên soạn. Đoạn cần đọc có trong từng câu hỏi để không phụ thuộc trí nhớ
hoặc tranh trang trí. Kiểm thử kỹ thuật không thay thế thẩm định sư phạm bởi
giáo viên hoặc thử nghiệm với học sinh.

## Dữ liệu local

Trước khi nạp, tạo backup PostgreSQL custom và kiểm tra `pg_restore --list`.
Trong transaction nạp, so sánh toàn bộ cột theo khóa chính của tất cả bản ghi
đã có: **23.933 bản ghi tại 82 bảng ứng dụng không thay đổi**. Chỉ thêm bản ghi
thuộc bộ mới; tài khoản, mật khẩu, membership, phiên, kết quả và phiên bản cũ
giữ nguyên. Chạy seed lặp trong test giữ nguyên tập phiên bản câu hỏi.

[Biên bản nạp, SHA256 và vị trí backup local](discovery-local-2026-11-04.json).
Backup nằm trong `.tools/backups`, không đưa lên Git; lần này kiểm tra mục lục
archive, chưa phục hồi lại backup mới sang một database khác.

Đối chiếu trực tiếp kho đang xuất bản sau nạp:

| Khối            | Bài học | Câu hỏi   | Đề luyện |
| --------------- | ------- | --------- | -------- |
| 1               | 89      | 474       | 77       |
| 2               | 89      | 474       | 77       |
| 3               | 89      | 474       | 77       |
| 4               | 89      | 474       | 77       |
| 5               | 89      | 474       | 77       |
| **Tổng ba môn** | **445** | **2.370** | **385**  |

AI giữ 200 bài/1.702 SVG. Không có migration; head `0012_lesson_bookmarks`.
Không thêm Redis, model AI hoặc dịch vụ nền. Các server phục vụ test ở
8001/3001 đã dừng; không dừng ứng dụng của người dùng ở 8000/3000.

## Chạy lại

Trong thư mục backend, cấu hình database test riêng và `TEST_DATABASE_URL` theo
README; tuyệt đối không trỏ test ghi vào database học thật:

```powershell
../.venv/Scripts/python.exe -m pytest -m 'not integration' -q
../.venv/Scripts/python.exe -m pytest tests/test_discovery_content.py tests/test_practice_library.py tests/test_bookmarks.py tests/test_library_snapshot.py -m integration -q
```

Frontend:

```powershell
npm test
npm run lint
npm run format:check
npm run build
npm run typecheck
```

Browser cần database test đã nạp đủ học liệu, tài khoản từ
`backend/scripts/prepare_e2e.py`, hai server trỏ cùng database đó và biến môi
trường fixture. Trong frontend: `npx playwright test e2e/discovery-learning.spec.ts`.
Helper chỉ tạo fixture trên tên database có `test`, không dùng cho production.

Đợt này không chạy lại tải 50 người dùng, Docker Engine hoặc VPS Nhật thật.
Số đo tải và phục hồi của đợt trước xem [biên bản 20/10](../pre-deployment-review-2026-10-20.md).
Trước mở công khai vẫn cần `check-launch`/`check-release`, tài khoản thật,
role DB runtime và HTTPS trên môi trường triển khai theo hướng dẫn VPS.
