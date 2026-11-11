# 05 · Bảo mật và quyền riêng tư · 11/11/2026

Đánh giá trên code hiện hữu và dữ liệu giả trong database kiểm thử riêng.
Không tấn công production, đổi secret, gửi email/SMS hoặc đưa dữ liệu học
sinh thật ra dịch vụ ngoài. Không phải chứng nhận bảo mật hoặc xác nhận
tuân thủ pháp luật. Kết quả chạy cuối, lệnh và exit code xem
[07-test-results.md](07-test-results.md); trạng thái rủi ro tại
[02-risk-register.md](02-risk-register.md).

## Cách hiểu bằng chứng

- **VERIFIED**: hành vi đã được chạy và quan sát trong phạm vi được nêu.
  Không suy rộng từ một mẫu thành toàn bộ hệ thống an toàn.
- **PARTIALLY VERIFIED**: đã đọc đường mã hoặc chạy một phần, còn thiếu
  kiểm chứng môi trường/đối kháng/thủ công.
- **NOT VERIFIED**: chưa có phép thử tương ứng; có test trong repo chưa đủ
  để coi là đã chạy.

Kết quả sau sửa: 992 unit, Linux regression 649 và progress regression 72
đều đạt trong các phạm vi ghi tại 07. Bốn P1 (safety/consent/upload/media)
có patch và hồi quy; không coi đây là chứng nhận toàn bộ hệ thống.

## Xác thực, phiên và quyền truy cập

| Kiểm soát               | Căn cứ code/test                                                                                                                        | Đánh giá phạm vi                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Mật khẩu                | `core/security.py`: Argon2; `password_capacity` giới hạn công việc tốn bộ nhớ; không giảm tham số hash                                  | PARTIALLY VERIFIED bằng đọc mã; test account/login tại mục 07                                        |
| Phiên                   | Token ngẫu nhiên, lưu SHA-256 tại `auth_sessions`; cookie HttpOnly, SameSite=Lax, Secure theo môi trường; hết hạn được kiểm server-side | PARTIALLY VERIFIED; `test_sessions.py` kiểm deadline, logout/relogin, khóa tài khoản và thay vai trò |
| Ghi nhớ đăng nhập       | Học sinh mặc định 8 giờ, tùy chọn 7 ngày; admin/teacher bị giới hạn lại cả khi được cấp vai trò sau login                               | PARTIALLY VERIFIED; giới hạn cấu hình có validation và integration hồi quy                           |
| CSRF/CORS               | `verify_origin`, `current_user`: kiểm Origin, Sec-Fetch-Site và hash CSRF cho thao tác ghi; CORS chỉ origin cấu hình                    | PARTIALLY VERIFIED; không dựa vào ẩn nút giao diện                                                   |
| Chống dò mật khẩu       | Rate limit DB theo hash IP/account, `Retry-After`; cấu hình proxy chỉ tin IP Caddy quy định                                             | PARTIALLY VERIFIED; tải nhiều tài khoản và chính sách shared-IP cần đo ở staging                     |
| Vai trò                 | Dependency admin/student và kiểm teacher/guardian trong service; quyền đọc/ghi kiểm tại API                                             | PARTIALLY VERIFIED; cần các kết quả RBAC/IDOR trong mục 04/07                                        |
| Thu hồi và đổi mật khẩu | `services/accounts.py`: xác thực lại hành động nhạy cảm, account revision, khóa, revoke session, audit                                  | PARTIALLY VERIFIED; không có quy trình email reset/2FA được coi là đã triển khai                     |

Session/CSRF cookie chỉ là phương tiện xác thực, không chứa hồ sơ hoặc điểm.
Phản hồi người dùng chỉ cho phép các trường công khai; không trả password
hash, session hash hoặc CSRF hash. Thao tác quản trị tài khoản kiểm lại mật
khẩu và phiên; không cho quyền chỉ dựa vào role nhận từ client.

## Ranh giới dữ liệu và tính toàn vẹn bài làm

`owned_attempt()` kiểm học sinh sở hữu trước đọc/ghi; admin có đường đọc,
không được ghi bài làm thay học sinh qua route student. Assignment, item
và question version được ràng buộc tại DB và service. Phụ huynh phải có
liên kết đã xác minh; giáo viên chỉ đọc/giao bài/chấm trong lớp được phép.
Các kiểm tra liên quan nằm tại `test_integration.py`, `test_classrooms.py`,
`test_academy.py` và `test_academy_management.py`; kết quả thực thi ở mục 07.

Client không được gửi điểm: request schema từ chối trường ngoài hợp đồng,
ID lựa chọn phải thuộc câu hỏi, không được trùng, ordering phải đầy đủ.
`safe_content()` whitelist nội dung trước nộp, loại grading/explanation và
các thuộc tính đánh dấu đúng/sai lồng trong option. Server chấm theo phiên
bản câu hỏi đã gắn với đề. `submit()` khóa hàng học sinh/attempt, trả kết quả
đã có nếu đã chấm, không tạo lần chấm/sự kiện trùng. Save dùng thời điểm
nhận tại server để từ chối request cũ ghi đè request mới.

**AUD-01 đã có hồi quy unit VERIFIED:** key thập phân có nhóm nghìn như
`12 000,50` chấp nhận cách viết tương đương `12000.5`. Các trường hợp sai
giá trị, khác độ chính xác, phân số chưa đúng dạng và case-sensitive vẫn
được giữ kiểm soát. Không sửa điểm/đáp án lịch sử. Integration API mới trong
`test_audit_security_grading.py` cần đối chiếu kết quả tại mục 07.

**AUD-08 còn mở:** lượt `in_progress` đã quá hạn chưa có chính sách
abandon/restart rõ; có thể chặn học lại hoặc lưu trữ đề. Không tự cấp lượt,
xóa bài làm hoặc auto-submit để né lỗi; cần quyết định nghiệp vụ và test
toàn bộ lifecycle. Đây là hạn chế chức năng, không được suy thành lỗ hổng
đọc dữ liệu học sinh khác.

## Input, upload, lỗi và log

- SQL dùng SQLAlchemy bind parameters, UUID/Pydantic validation; các query
  đọc có owner/role scope. Đọc mã không thay cho fuzzing toàn bộ endpoint.
- React hiển thị nội dung qua text; header nosniff, DENY, same-origin có ở
  backend/frontend/Caddy. Chưa tuyên bố đã kiểm mọi XSS hoặc có CSP đầy đủ.
- Upload AI giới hạn base64/raster 512 KB, 8 triệu pixel, tạo lại pixels
  để bỏ EXIF/location; file riêng và trạng thái chờ duyệt. Đợt này giới hạn
  parser plugin ngay trong `Image.open(..., formats=...)`, trước parse
  header, thay cho chỉ kiểm format sau khi đã nhận dạng. Test tại
  `test_audit_release_uploads.py`; kết quả cuối ở mục 07.
- Hook antivirus local có sẵn nhưng chưa được cấu hình thực tế; không coi
  ảnh đã qua antivirus khi hook chưa chạy. Không cho upload SVG tùy ý để
  dùng trực tiếp như hình đã được duyệt.
- Validation không phản chiếu input chứa password/bài làm. Log request có
  ID, method, status, duration; log lỗi DB chỉ loại lỗi/sqlstate/constraint,
  không nội dung SQL hoặc tham số. Trình vận hành vẫn phải giới hạn quyền
  đọc log và retention.
- Cookie và dữ liệu cá nhân dùng `no-store`; cache static/media không được
  coi là cache quyền VIP. Không cache entitlement để trì hoãn revoke.

## AI Academy: phạm vi thực tế và bảo vệ trẻ

Mặc định **`AI_TRAINING_ONLY=true`**, nội dung biên soạn sẵn và mô phỏng có
nhãn rõ. Không cần API mô hình trả phí, không có tool-call tự trị cho học
sinh. Bài học về AI và provider không được mô tả như mô hình thật đang chạy
khi thực tế chỉ trả nội dung nội bộ.

Provider Ollama cũ chỉ được dùng khi đồng thời đủ cấu hình, feature flag,
provider enabled/policy approved, quyền bài học và consent hợp lệ. Payload
sang provider chỉ chứa ngữ liệu/gợi ý đã duyệt, lớp và mode; không chứa
`tried`, tên, hồ sơ hoặc câu trả lời tự do của trẻ. URL provider bị giới hạn
host local/được phép, không credentials/query/path phụ; request không theo
redirect, timeout 8 giây, retry tối đa hai lượt cho lỗi kết nối/timeout.
Có quota học sinh/lớp/trường, circuit breaker và fallback nội bộ. Đây là
giới hạn số request, chưa phải hệ thống tính chi phí tiền tệ của dịch vụ
AI cloud. Đợt audit không kích hoạt provider thật.

Các thay đổi an toàn đã đưa vào code và cần đọc cùng kết quả hồi quy ở 07:

1. **AUD-02:** chuẩn NFKC, bỏ ký tự định dạng vô hình, kiểm PII và câu nguy
   hiểm tiếng Anh/Việt để giảm bỏ lọt do Unicode/biến thể trình bày.
2. **AUD-03:** phân biệt ngôn ngữ tự hại với câu học tập như “từ từ” hay
   “tự tư duy”, tránh chặn theo substring sau bỏ dấu.
3. Consent cùng timestamp ưu tiên thu hồi; không chọn bản đồng ý bằng UUID
   ngẫu nhiên khi có thu hồi đồng thời. Output được kiểm lại consent/flag
   sau provider để không phát nội dung khi quyền vừa bị thu hồi.
4. **AUD-04:** trợ giảng lấy payload phiên bản gắn với tiến độ đang học;
   công bố bản mới không âm thầm đổi gợi ý ở bài cũ.
5. Nội dung trẻ nhập được NFC/trim ở nơi phù hợp. Không bỏ dấu tiếng Việt
   hoặc hạ chữ hoa cho bài mà mục tiêu là chính tả/cách viết.

Moderation là biện pháp giảm rủi ro bằng quy tắc, **không phải bằng chứng an
toàn 100%**. Nội dung bị chặn trả lời ngắn, khuyến khích nhờ người lớn tin
cậy; ghi reason code thay cho lưu nguyên đoạn PII. Cần giáo viên/người phụ
trách tiếp tục đánh giá corpus mới, các trường hợp có ngữ cảnh và nguy cơ
false positive/false negative. Kiểm tra injection, output validation và
quota không được chỉ dựa trên lời nhắc system.

## Quyền riêng tư, consent, export và retention

Hệ thống đã có guardian link xác minh, consent theo purpose/policy version,
export dữ liệu AI đúng học sinh và quy trình yêu cầu gỡ phần nội dung dự
án. `management_api.py` kiểm `child_access()` trước export/request. Gỡ
project text sau phê duyệt không đồng nghĩa xóa sạch mọi hồ sơ học tập,
audit hoặc bản backup; phạm vi này được nói trong phản hồi API.

Các việc **NOT VERIFIED** cần đơn vị vận hành/pháp lý xác nhận trước mở web:

- Ai là bên chịu trách nhiệm dữ liệu và ai xử lý dữ liệu; mục đích, phạm vi,
  thời hạn lưu từng loại hồ sơ, log, consent, file và backup.
- Thông báo dễ hiểu cho phụ huynh/trẻ, cách xác minh người giám hộ và xử lý
  yêu cầu truy cập, sửa, gỡ hoặc rút đồng ý trong thực tế.
- Chính sách lưu trữ và truy cập khi VPS đặt ở Nhật; hợp đồng với nhà cung
  cấp, vị trí backup và quy trình sự cố phải được người phụ trách đối chiếu
  với yêu cầu pháp luật Việt Nam hiện hành.
- Khả năng phục hồi, tiêu hủy dữ liệu theo chính sách đã duyệt và kiểm soát
  quyền người vận hành; không tự đặt retention pháp lý từ code.

Không có kết luận “tuân thủ đầy đủ” chỉ dựa vào việc có consent checkbox,
export endpoint hoặc backup script. Báo cáo này không cung cấp tư vấn pháp lý.

## Secrets và dependency

Không sao chép `.env` thật vào báo cáo, commit hoặc fixture. Biến mẫu chỉ
là placeholder. CI dùng mật khẩu giả cho DB tạm và không dùng tài khoản
production. Kiểm tra dependency chỉ gửi tên/phiên bản package đến cơ sở dữ
liệu advisory, không gửi hồ sơ học sinh hoặc database.

Đã vá lock backend Pillow **13.0.0**, Certifi **2026.10.19**, giới hạn
decoder trước parse; audit Python lock cuối exit 0, không advisory do công
cụ báo. Scoped minimatch **11.0.1** và Zod **4.6.7**; npm audit cuối exit 0,
0 findings toàn bộ dev/production. Không nâng major framework hàng loạt.
Pillow major được test trong venv audit đúng lock và Linux image; venv người
dùng chưa bị ghi đè khi các tiến trình cũ đang chạy (cách cập nhật ở 08).

Quét 3.246 tracked files ở thời điểm kiểm kê không thấy high-confidence
private-key/AWS/GitHub-token theo pattern đã dùng, `.env` không tracked.
Không phải quét entropy/lịch sử Git hoàn chỉnh; chưa kiểm backup/IAM VPS.

## Quyền media và HTTPS đã xác minh

`academy/access.py` trước sửa có thể mở SVG VIP cũ thiếu usage. Đã kiểm usage
published/archived; draft Free không mở VIP. Fallback prefix ổn định `AIx-nn`
tra owner lesson và quyền DB; asset không thuộc bài hợp lệ fail-closed.
Shared asset có usage Free hợp lệ vẫn đọc được; không suy Free từ tên file.
23 SQL-backed unit, hai integration và HTTPX Free 403/no-store đã đạt.

[HTTPS evidence](evidence/https-security.json): 19 checks qua production Caddy
local, HTTPX verify private CA bật; login Secure/HttpOnly/SameSite=Lax,
anonymous 401, cross-Origin/thiếu CSRF 403, student-admin 403, docs/openapi
và public ready 404, HSTS/nosniff/frame headers, logout rồi reuse 401.
Đây là private TLS local; chưa xác minh public certificate/DNS của người dùng.
Các regression session/RBAC/owner/đổi mật khẩu đã chạy, không chỉ đọc mã;
những hàng PARTIALLY VERIFIED ở trên vẫn giới hạn vì không pentest toàn bộ
endpoint hoặc đánh giá thực tế mạng trường học/shared-IP.

## Nguồn tham chiếu và kết luận có giới hạn

[OWASP ASVS](https://asvs.owasp.org/) phiên bản 5.0.0 được dùng để định hướng
auth/session/access control, validation, crypto và vận hành.
[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
được dùng để đối chiếu injection, dữ liệu nhạy cảm, output và giới hạn dùng
provider. Không chấm đạt một level ASVS hoặc công bố chứng nhận từ checklist.

Các lỗi đã xác nhận và sửa có regression, nhưng trạng thái phát hành còn
phụ thuộc full suite, browser, dependency audit và nghiệm thu staging ở
[09-acceptance-checklist.md](09-acceptance-checklist.md). Chưa pentest toàn
bộ, chưa kiểm VPS thật, chưa chứng nhận pháp lý và chưa vận hành mô hình AI
thật với học sinh.
