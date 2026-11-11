# 09 · Checklist nghiệm thu · 11/11/2026

VERIFIED = đã chạy trong phạm vi nêu; PARTIALLY VERIFIED = một phần; NOT
VERIFIED = chưa có bằng chứng tương ứng. Không phải chứng nhận production-ready.

| Điều kiện                                             | Trạng thái / chứng cứ                                                                                                                                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bảo toàn source/DB/secrets                            | VERIFIED: Git đầu sạch, nhánh riêng; 83/83 bảng nguồn khớp hash trước/sau; không đổi `.env`, không drop/reset                                                                               |
| P0 đã xác nhận                                        | Không phát hiện trong phạm vi audit; không bảo đảm không còn ngoài phạm vi                                                                                                                  |
| P1 phát hiện                                          | VERIFIED patch + regression cho cả bốn P1; cần cài lock/build/restart để áp dụng release                                                                                                    |
| Unit/integration/component                            | VERIFIED phạm vi: 992 unit, Linux 649 + 72 regression, frontend 103. Không cộng số trùng; không phải full cuối một lượt                                                                     |
| Browser                                               | PARTIALLY VERIFIED: full baseline 174/5fail/3skip; target rerun 12 pass; Windows smoke cuối 33pass/1fail AUD-22; production-mode HTTPS 34/34 + network 4/4 đạt; chưa full 182 cuối một lượt |
| Lint/type/build                                       | VERIFIED final Ruff/ESLint/typecheck/build exit 0; proxy build về 8000, next-env giữ bản gốc; format cuối ở test-summary.json                                                               |
| Session/CSRF/RBAC/owner/server grading/VIP live       | VERIFIED bằng regression trong 04/07 và 19 HTTPS protocol checks; không suy toàn bộ pentest                                                                                                 |
| Nội dung/ảnh lớp 1–5 và AI                            | VERIFIED schema/hash/inventory; PARTIALLY VERIFIED độ đúng sư phạm; chưa giáo viên duyệt toàn kho                                                                                           |
| Responsive/axe/keyboard                               | VERIFIED sáu case mẫu desktop/mobile/320/768; screen reader/thiết bị thật NOT VERIFIED                                                                                                      |
| Dependency                                            | VERIFIED audit lock sau vá exit 0; npm dev+prod 0 findings, Python 0 vulnerable package do công cụ báo                                                                                      |
| Docker/Linux/runtime                                  | VERIFIED build thật, runtime non-root/no CREATE, migration head không đổi                                                                                                                   |
| Backup/restore                                        | VERIFIED dump/restore 83 bảng dữ liệu giả local; backup ngoài VPS và diễn tập sự cố máy thật NOT VERIFIED                                                                                   |
| Tải 50 người                                          | VERIFIED kịch bản local HTTPS: 900/900 request 200, 50/50 journeys, p95 2.753,40ms; CPU hai core bão hòa, dashboard tail cần profile                                                        |
| HTTPS private CA                                      | VERIFIED HTTPX verify CA, cookie/Origin/CSRF/headers/role/logout; không đồng nghĩa domain công khai                                                                                         |
| Public DNS/TLS/VPS Nhật, WAN/soak                     | NOT VERIFIED; chưa deploy hoặc đổi DNS                                                                                                                                                      |
| Web Vitals/bố cục                                     | PARTIALLY VERIFIED: 18 navigations lab, CLS AI 0,1608–0,2089 còn cần sửa (AUD-24); INP field chưa đo                                                                                        |
| AUD-22 timeout local                                  | CÒN MỞ: một 500/30s và một pending/loading ở smoke; chưa chốt root cause; cần theo dõi staging                                                                                              |
| Demo/admin/password và release checks trên production | NOT VERIFIED môi trường thật; người vận hành cần disable demo/secret riêng/check-launch/check-release                                                                                       |
| Retention/consent/export/pháp lý                      | PARTIALLY VERIFIED code/regression; cần người phụ trách dữ liệu/pháp lý xác nhận triển khai thực tế                                                                                         |
| GDPT/độ tuổi/trải nghiệm trẻ                          | NOT VERIFIED đầy đủ bởi giáo viên và nhóm học sinh; không tự ghi đạt GDPT 2018                                                                                                              |
| GitHub Actions mới                                    | Cấu hình đã sửa và gate tương đương chạy local; chưa push/kích hoạt remote workflow                                                                                                         |

24 mục trong [02](02-risk-register.md): 18 đã sửa theo phạm vi, sáu P2 còn
mở/một phần (**08/10/11/12/22/24**). Sprint kế tiếp ở [03](03-upgrade-plan.md).
Trước mở công khai: xử lý/đánh giá rõ lỗi transport, chạy staging HTTPS/WAN,
backup ngoài máy/restore, phê duyệt nội dung và kiểm thử thủ công cần thiết.
