# 03 · Kế hoạch nâng cấp có ưu tiên · 11/11/2026

Giữ stack/API/schema/lịch sử. Không thêm hàng loạt chức năng chỉ vì có trong
checklist. Batch và rollback ở [08](08-changelog-and-rollback.md).

| Giai đoạn         | Công việc / trạng thái                                                       | Phụ thuộc, độ khó, rủi ro                                | Điều kiện chấp nhận                                                                                     |
| ----------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Now               | ĐÃ LÀM: baseline, inventory, nhánh riêng, DB giả và đối chiếu nguồn          | Nhỏ; chỉ đọc nguồn, không clone PII                      | 83/83 bảng nguồn khớp hash; lệnh/exit thật ở 07                                                         |
| Now               | ĐÃ LÀM: chấm số, AI safety/consent/version, media VIP/upload/dependency      | Vừa; chạm quyền/chấm nên cần regression                  | Bốn P1 có patch/test; Linux/HTTPS âm tính đạt                                                           |
| Now               | ĐÃ LÀM: shared modal, contrast, retry và form đang lưu                       | Vừa; focus cần browser thật                              | Component và sáu case axe/keyboard mẫu đạt                                                              |
| Now               | ĐÃ LÀM: content lint/readiness, exact pack tests, CI browser                 | Vừa; không tự sửa DB thật/không nới assertion            | Query budget, exact IDs và mandatory fixtures; remote CI chưa chạy                                      |
| Now               | ĐÃ LÀM: preview/visit nhẹ, tải 10/25/50, Linux/image/restore/private TLS     | Vừa; test DB/ports/limits riêng                          | Không lỗi HTTP/đếm trùng; latency/CPU/RAM thật ở 07                                                     |
| Next · sprint 1   | Staging VPS Nhật, theo dõi AUD-22, backup ngoài máy và restore drill         | Cần VPS/domain/quyền; vừa, rủi ro vận hành               | HTTPS công khai, Caddy API direct, cookie/CSRF/role; không 5xx/reset bất thường; đo WAN/soak            |
| Next · sprint 1   | Giáo viên duyệt học liệu, ưu tiên lớp 4 và tranh AI lớp 1–2                  | Nguồn chương trình chính thức và giáo viên; công sức lớn | Người/ngày/version duyệt, bảng yêu cầu cần đạt; giải quyết đa nghĩa, thử nhóm nhỏ                       |
| Next · sprint 1   | Chốt abandon/restart attempt hết hạn                                         | Quyết định nghiệp vụ; vừa, tác động lịch sử              | Không reset điểm/attempt; rõ lượt/version/mastery, idempotency/đồng thời                                |
| Next · sprint 1   | Screen reader, điện thoại thật, bàn phím ảo/zoom                             | Thiết bị/người kiểm; vừa                                 | NVDA/VoiceOver đọc đúng heading/dialog/trạng thái/công thức; không chỉ axe                              |
| Next · sprint 1   | Ổn định bố cục AI Academy khi tải (AUD-24)                                   | Cần skeleton giữ kích thước và layout review; vừa        | Đo lại lab hai viewport, không flash nội dung sai quyền, không đổi focus; sau đó field CLS trên staging |
| Next · theo số đo | Profile dashboard/lesson, cân nhắc CPU/pool/cache                            | Cần số liệu staging; vừa, rủi ro cache stale             | Không cache VIP/owner; SLO thống nhất, double-submit/statistics vẫn đúng                                |
| Later             | Prerequisite AI theo tuổi, audio chuẩn/transcript, metrics/alerts, retention | Nội dung và quy trình vận hành                           | Graph không vòng, gợi ý giải thích được, tối thiểu dữ liệu và có budget                                 |
| Later             | Thanh toán/reset email/SMS/model AI thật                                     | Yêu cầu/phê duyệt riêng                                  | Sandbox, consent, hạn mức/output/fallback; không tự bật dịch vụ thật                                    |

Chưa deploy/đổi DNS/push workflow. Phần chưa có điều kiện xác minh ghi
NOT VERIFIED ở [09](09-acceptance-checklist.md). Người vận hành chốt SLO
và lịch mở web sau khi giải quyết các mục còn lại ở [02](02-risk-register.md).
