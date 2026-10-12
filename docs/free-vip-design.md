# Thiết kế gói học miễn phí và VIP cho VietTree Education

Lớp 1–2 đã thêm bộ ba môn có quy mô/tỷ lệ Free–VIP bằng lớp 3–4: mỗi khối
68 bài/384 câu/56 đề, Free 46/228/34 và VIP 22/156/22. VIP tăng mức vận dụng
trong kiến thức của khối; gợi ý Free 1/VIP 3. Xem [nội dung và khảo sát](grades1-2-curriculum.md).
Cập nhật 12/10/2026: [AI Academy](ai-training-vip.md) có 7 bài Free / 41 bài
VIP (lớp 4: 3 / 33), lab và studio thuộc VIP. `AI_TRAINING_ONLY=true` chặn gọi
model. [Giá tham khảo và sale](vip-pricing-research.md) hiển thị tại trang gói;
admin quản lý ưu đãi có hạn. [Lớp và thành tích](classes-achievements.md) dùng
cùng tài khoản, không cộng điểm thưởng cho VIP. Migration head 0011.
Gia hạn gói đã thu hồi trả 409, cần cấp mới; replay thao tác trả quyền hiện tại.

Cập nhật lớp 3: cùng quy mô và tỷ lệ nội dung như lớp 4; 46 bài/34 đề Free,
22 bài/22 đề VIP. Mỗi bài lớp 3 có 3 gợi ý: Free xem 1 ý định hướng, VIP xem
thêm cách làm và tự kiểm tra. Tính năng `learning.guided_hints` được thêm bởi
`0009_guided_hints`; backend lọc văn bản trước khi trả JSON. Admin cấu hình
`free_hint_count` trong editor, tối thiểu 1 khi phân bổ. Bài lớp 4 cũ giữ phân
bổ trước đây. Chi tiết: [học liệu lớp 3](grade3-curriculum.md).

Trạng thái: đã triển khai Free/VIP do admin cấp, chính sách nội dung, trang giới
thiệu, thử thách và plan_v2. Migration `0003_memberships` bổ sung sáu bảng.
Thanh toán, báo cáo trong tài khoản phụ huynh và UI quản lý liên kết là giai đoạn tiếp theo.
Nội dung nâng cao hiện là bộ mẫu development cần rà soát chuyên môn trước vận hành.
Tài liệu bám theo FastAPI, Next.js và schema hiện có. Hai gói ban đầu là Free và
VIP; gói học thuộc về từng học sinh. Hiện admin cấp gói theo yêu cầu; phụ huynh xem
gói của trẻ có liên kết đã xác minh. Nâng cấp trực tuyến là phần sau. Tài khoản
giáo viên và quản trị viên giữ cơ chế quyền riêng.

Đợt mở rộng lớp 4 mới nhất: tổng 68 bài/384 câu/56 đề, gồm 46 bài/34 đề Free và
22 bài/22 đề VIP. Góc tư duy có bài Free và VIP; bảng học liệu admin theo dõi các
mạch của 3 môn, chưa chứng nhận phủ đủ chương trình. Xem [grade4-curriculum.md](grade4-curriculum.md).
Đã có Góc học VIP, sổ tay ôn lỗi/tự luyện, báo cáo 7/30 ngày và
in/lưu PDF qua trình duyệt trong tài khoản học sinh. Migration 0006 bổ sung ba
feature; hướng dẫn và giới hạn tại [vip-expansion.md](vip-expansion.md).
Admin đã có ngân hàng câu hỏi, ghép đề và giao bài; migration 0004/0005 bổ sung quyền
từng phiên bản và chống ghi đè nháp. Thiết kế cùng hướng nâng cấp tiếp tại
[authoring-design.md](authoring-design.md). Lệnh riêng `seed-demo-learners` tạo hai
Free và hai VIP 90 ngày; seed thường không tự cấp VIP.

## 1. Quyền vai trò và quyền gói học

Giữ nguyên user_roles: student, guardian, teacher, admin. Gói Free/VIP được lưu
riêng, không thêm role vip hoặc đổi role student thành vip. Học sinh VIP vẫn chỉ
đọc hồ sơ, bài làm và kết quả của mình. VIP không cấp quyền đọc đáp án trước nộp,
quản lý lớp, sửa câu hỏi hoặc cấp VIP cho người khác.

Một thao tác được phép khi đồng thời thỏa mãn: tài khoản hoạt động, vai trò phù
hợp, đúng chủ sở hữu/liên kết đã xác minh, nội dung được xuất bản và phù hợp lớp,
gói học có quyền tương ứng; thao tác làm bài còn phải thỏa hạn giao bài và số lượt.
Các kiểm tra phục vụ học và kiểm tra quản trị có chính sách riêng.

Kiểm tra quyền trên từng request và từ chối khi thiếu chính sách rõ ràng phù hợp
với [hướng dẫn phân quyền của OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
Các lựa chọn về gói, thời hạn và trải nghiệm trong tài liệu này là đề xuất sản phẩm.

## 2. Ma trận sản phẩm

| Khả năng                                        | Free                                            | VIP                                                              | Tình trạng hiện tại                                            |
| ----------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------- |
| Bài học nền tảng được đánh dấu miễn phí         | Có                                              | Có                                                               | 46 bài/34 đề Free, gồm bộ cũ và phần mở rộng                   |
| Luyện tập đi kèm bài miễn phí, chấm và lời giải | Có                                              | Có                                                               | Đã có                                                          |
| Lịch sử, kết quả và cây năng lực của chính em   | Có                                              | Có                                                               | Đã có; tiếp tục xem khi hết VIP                                |
| Kế hoạch học theo thứ tự chương trình           | Tối đa 3 bài mới/kế hoạch, từng môn             | Có                                                               | Đã có plan_v1                                                  |
| Cỡ chữ, hỗ trợ đọc và giao diện điện thoại      | Đầy đủ                                          | Đầy đủ                                                           | Đã có tùy chọn cỡ chữ; các hỗ trợ mới dùng chung               |
| Bài học nâng cao và luyện tập VIP               | Xem giới thiệu, không mở nội dung đầy đủ        | Có                                                               | 22 bài/156 câu VIP development, cần rà soát chuyên môn         |
| Thử thách theo chủ đề, đề tổng hợp nâng cao     | Không                                           | Có                                                               | 22 đề thử thách theo chủ đề; đề tổng hợp là phần sau           |
| Kế hoạch cá nhân theo kỹ năng cần ôn            | Không; vẫn có gợi ý luyện tập cơ bản            | Có; phối hợp nền tảng, ôn và nâng cao                            | Đã triển khai plan_v2                                          |
| Góc học VIP, lọc môn và bài chưa đọc            | Không                                           | Có                                                               | Đã triển khai                                                  |
| Sổ tay ôn lỗi và tự luyện không đổi điểm        | Không                                           | Có                                                               | Câu sai gần nhất của chính em, lọc môn/phân trang              |
| Báo cáo cá nhân 7/30 ngày và in/lưu PDF         | Không                                           | Có                                                               | Trong tài khoản học sinh, xem cùng phụ huynh                   |
| Báo cáo phụ huynh                               | Tiến độ và kết quả cơ bản của trẻ được liên kết | Thêm xu hướng theo tuần, kỹ năng cần ôn, hướng dẫn hỗ trợ và PDF | Báo cáo là giai đoạn sau; hiện chỉ xem gói của trẻ đã liên kết |

Không giới hạn thêm số bài Free được đọc mỗi ngày. Số lượt làm từng đề vẫn theo
assessments.max_attempts cho cả hai gói. VIP có thêm đề/biến thể mới, không được
vượt giới hạn đề cũ hoặc cộng điểm khác học sinh Free. Cách tính mastery, confidence
và lời giải cho đề đã làm phải giống nhau giữa hai gói.

Không đưa tính năng chưa triển khai vào danh sách quyền lợi đang bán. Giai đoạn
đầu chỉ mở VIP khi đã có nội dung nâng cao được duyệt và kiểm tra quyền hoàn chỉnh.

## 3. Nội dung miễn phí và nâng cao

Mỗi bài học và đề luyện có hai thuộc tính độc lập:

- learning_level: basic (nền tảng), reinforcement (củng cố), advanced (nâng cao).
- minimum_plan_code: free hoặc vip.

Độ khó của câu hỏi không tự quyết định gói học. Một câu khó có thể nằm trong đề
Free; một bài VIP có thể nhắc lại kiến thức nền tảng trước khi dạy phần nâng cao.
Nội dung VIP vẫn thuộc lớp của học sinh; không tự mở lớp khác bằng việc trả phí.

Đề xuất giữ 24 bài học và 12 đề hiện có là Free khi chuyển sang mô hình mới. Phần
VIP bắt đầu với 6 bài mới và đề đi kèm, mỗi môn 2 bài, sau khi rà soát chuyên môn:

| Môn        | Ví dụ nội dung VIP lớp 4                                          |
| ---------- | ----------------------------------------------------------------- |
| Toán       | Giải bài toán nhiều bước; giải thích và so sánh cách giải phân số |
| Tiếng Việt | Đọc hiểu suy luận; lựa chọn chi tiết và cách diễn đạt phù hợp     |
| Tiếng Anh  | Đọc đoạn hội thoại dài hơn; lựa chọn câu theo ngữ cảnh            |

Các chủ đề trên đã có nội dung mẫu trong advanced_curriculum.py, được xuất bản khi
chủ động seed development. Rà soát chương trình/đáp án trước vận hành. Dùng version/câu hỏi mới; không sửa version published
đang được tham chiếu trong bài làm. Không mở CRUD câu hỏi bị giữ chờ trong prompt gốc.

Một đề có nội dung VIP phải mang chính sách VIP. Kiểm tra cả quan hệ lesson_id,
assessment_items và các đường lấy câu hỏi; không để đề Free chứa nguyên bộ câu
của bài VIP do gắn nhãn thiếu. Việc đổi nhãn có audit và áp dụng ở request tiếp
theo, gồm bài đang làm; attempt từng được bắt đầu dưới quyền VIP giữ quy tắc grant
ở mục 5. Attempt Free đổi sang VIP cần gói phù hợp để tiếp tục. Kết quả đã nộp giữ nguyên.

## 4. Trải nghiệm giao diện

Trang danh sách có bộ lọc Tất cả / Miễn phí / Nâng cao và nhãn rõ ràng trên từng
thẻ: Miễn phí, VIP, Nâng cao. Phân biệt nội dung bị giới hạn gói với nội dung lớp
đang xây dựng. Không hiển thị nội dung nháp cho học sinh.

Khi mở bài VIP bằng tài khoản Free, trang giới thiệu hiển thị tên, mục tiêu học,
thời lượng và một đoạn xem trước được biên tập riêng. Không trả toàn bộ bài học
rồi che bằng CSS. Trang có hai lựa chọn: Học bài miễn phí và Xem gói học cùng phụ
huynh. Giữ lời nhắn nhẹ nhàng: “Bài này nằm trong gói VIP. Em vẫn có thể học các
bài miễn phí bên dưới.”

Tại Hồ sơ của em, mục Gói học hiển thị Free hoặc VIP, ngày hết hạn và quyền lợi
đang hoạt động. Thông tin tài chính nằm trong luồng dành cho phụ huynh/người lớn;
không đặt bước nhập thanh toán trong màn hình làm bài của trẻ.

Luồng phụ huynh: chọn trẻ đã liên kết và xác minh → so sánh quyền lợi → chọn thời
hạn → xác nhận/nâng cấp → xem trạng thái. Nâng cấp cho một trẻ không tự cấp VIP
cho các trẻ còn lại. Luồng phụ huynh cần được xây cùng kiểm tra guardian_students.

Trang admin quản lý gói theo học sinh: tìm tên/tài khoản, xem thời hạn, cấp, gia hạn,
thu hồi, lịch sử thay đổi. Các thao tác nhập thời hạn và lý do, có xác nhận đích
đến và audit. Admin có thể xem trước nội dung qua endpoint quản trị; không nộp
bài hoặc thay đổi điểm dưới danh nghĩa học sinh.

## 5. Thời hạn, gia hạn và hết VIP

Giai đoạn đầu đề xuất các kỳ 30, 90, 365 ngày; chưa xác định giá bán hoặc cổng thanh
toán. Không tự gia hạn khi chưa xây dựng quy trình tương ứng. Lưu thời gian UTC,
hiển thị Asia/Bangkok cùng giờ kết thúc để tránh nhầm ngày hết hạn.

VIP có hiệu lực khi status=active và starts_at <= server_now < ends_at. Không có
bản ghi thì Free. Hết hạn được tính tại thời điểm request, không phụ thuộc cron.
Trạng thái hiển thị: free, active, expired, revoked. Không nhận is_vip, plan_code
hoặc ngày hết hạn từ request chỉnh hồ sơ của học sinh.

Gia hạn khi còn VIP: ends_at mới = ends_at hiện tại + số ngày cấp. Gia hạn khi đã
hết hạn hoặc cấp mới: starts_at = server_now, ends_at = server_now + số ngày cấp.
Thao tác lặp cùng Idempotency-Key trả lại kết quả lần đầu, không cộng ngày lần hai.
Khóa student_profiles trước khi cập nhật membership và bản ghi thao tác; audit
được ghi cùng transaction. Không thu hồi gói do người dùng chỉ tắt tự gia hạn.

Khi hết VIP:

- Giữ toàn bộ lịch sử, điểm, cây năng lực và kết quả đã nộp, gồm kết quả đề VIP.
- Chặn bắt đầu đề VIP mới, đọc bài VIP đầy đủ và tạo kế hoạch nâng cao mới.
- Bài VIP đã bắt đầu hợp lệ được hoàn tất trong tối đa 60 phút sau khi gói hết
  hạn; không vượt hạn assignment hoặc thời lượng đề. Ngoại lệ này chỉ dành cho
  chính attempt đã bắt đầu, không cho mở bài hay đề mới.
- Kế hoạch nâng cao cũ vẫn xem được tiến độ và chuyển paused; gợi ý chuyển sang
  kế hoạch cơ bản, giữ các bước đã hoàn thành. Không tự tính bước bị khóa là xong.
- Thu hồi do quản trị viên có hiệu lực ngay với quyền VIP, không áp dụng khoảng
  hoàn tất trên; vẫn giữ kết quả đã nộp theo quyền chủ sở hữu hiện có.

Kết quả cũ chỉ chứa câu và lời giải thuộc bài làm của chính em; không mở toàn bộ
ngân hàng VIP hay phiên bản câu hỏi mới. Gói trả phí không thay thế kiểm tra owner,
trạng thái tài khoản, xuất bản nội dung hoặc cửa sổ làm bài.

## 6. Thiết kế dữ liệu bổ sung

Schema gốc hiện không có bảng gói học. Đề xuất migration Alembic bổ sung, giữ nguyên
database/viettree_education_schema.sql và các khóa ngoại ghép của bài làm:

| Bảng đề xuất             | Trường và ràng buộc chính                                                                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| membership_plans         | code PK (free/vip), name, is_active, created_at; khai báo gói                                                                                                                                                                      |
| membership_plan_features | plan_code FK, feature_code, composite PK; danh sách quyền đã được phát hành của gói                                                                                                                                                |
| student_memberships      | student_id PK/FK student_profiles, plan_code FK, starts_at, ends_at, status active/revoked, source admin/payment, granted_by/revoked_by FK users, revoked_at, revoke_reason, updated_at; CHECK ends_at > starts_at                 |
| membership_operations    | id UUID PK, student_id FK, actor_user_id FK, idempotency_key UNIQUE theo actor, operation grant/extend/revoke, request_fingerprint, response_snapshot JSONB, created_at; bảo đảm yêu cầu lặp không cộng ngày hoặc thao tác lần hai |
| content_access_policies  | id UUID PK, lesson_id FK nullable, assessment_id FK nullable, minimum_plan_code FK, learning_level, preview JSONB, updated_by FK users; CHECK đúng một target khác NULL, unique riêng theo lesson_id và assessment_id              |
| attempt_access_grants    | attempt_id PK/FK attempts, membership_student_id FK student_memberships, allowed_until TIMESTAMPTZ, granted_at, revoked_at; CHECK allowed_until > granted_at; dùng cho hoàn tất attempt khi VIP hết hạn                            |

Membership là trạng thái hiện tại; membership_operations và audit_logs lưu lịch
sử cấp/gia hạn/thu hồi. Không xóa lịch sử để đổi gói. Request fingerprint ngăn cùng
idempotency key nhưng khác nội dung/đích đến. Khi cấp grant, backend lấy học sinh
từ attempt và đối chiếu membership_student_id, không nhận chủ sở hữu từ client.
Thu hồi gói đồng thời ghi revoked_at trên các grant của học sinh để việc cấp VIP
mới sau đó không khôi phục grant đã thu hồi. Các thao tác cùng khóa hồ sơ học sinh.

Danh sách feature_code cố định trong backend:

| Mã                                                                                                    | Gói                                           |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| learning.basic, practice.basic, results.own, skills.own, learning_plan.basic, accessibility.text_size | Free và VIP                                   |
| learning.advanced, practice.advanced, practice.challenge                                              | VIP, khi nội dung/tính năng đã phát hành      |
| learning_plan.adaptive                                                                                | VIP, khi plan_v2 đã phát hành                 |
| guardian_report.basic                                                                                 | Free và VIP, khi luồng phụ huynh đã phát hành |
| guardian_report.detailed, guardian_report.export                                                      | VIP, khi báo cáo đã phát hành                 |

Quyền báo cáo được tính từ gói của trẻ, kết hợp role guardian và verified_at của
liên kết guardian_students. Mua gói không tự xác minh quan hệ với trẻ.

Migration khởi tạo hai gói và gắn chính sách Free tường minh cho các bài/đề hiện
có. Nội dung mới thiếu chính sách không được phục vụ đầy đủ cho học sinh; admin
thấy lỗi cấu hình để bổ sung. Cập nhật db.validate/db.load để phản chiếu các bảng
mới sau migration. Downgrade chỉ xử lý bảng bổ sung, không sửa bảng học tập gốc.
Tắt tính năng phân gói và chuyển phiên bản ứng dụng tương thích trước downgrade.
Seed bổ sung chính sách còn thiếu cho nội dung đã xác định gói; chạy lại seed
không ghi đè nhãn Free/VIP do quản trị viên đã chỉnh và lưu audit.

## 7. Kiểm tra quyền và điểm tích hợp

Tập trung logic trong backend/app/services/access.py; các điểm dự kiến:

- resolve_membership: tính gói đang hiệu lực bằng thời gian server và trạng thái DB.
- require_feature: kiểm tra role, quan hệ với trẻ và feature của gói đang hoạt động.
- authorize_content: kiểm tra owner khi liên quan, trạng thái published, lớp và
  chính sách bài học/đề; admin preview dùng luồng riêng.
- authorize_attempt: kiểm tra owner, trạng thái và grant của attempt; không gọi
  require_vip đơn thuần trên result của bài đã nộp.
- visible_catalog / eligible_learning_content: tách metadata được giới thiệu khỏi
  nội dung đủ quyền để đưa vào gợi ý, kế hoạch và làm bài.

Danh sách và trang khóa chỉ trả metadata đã duyệt cùng locked/reason/required_plan.
Endpoint trả nội dung đầy đủ vẫn độc lập chặn tài khoản không đủ quyền. Media của
bài VIP, nếu được bổ sung, đi qua quyền truy cập hoặc URL có thời hạn; không đặt
file đầy đủ công khai rồi chỉ khóa trang bài học.

Các đường hiện có cần áp dụng: lessons list/detail/visit/complete, assessments
list/detail/assign-self, attempts start/read/save/submit, recommendations, dashboard,
learning-plans list/create và luồng quản trị xem trước. Các API nội bộ hiện trả
content hoặc grading phải giữ phân quyền quản trị. Teacher giao đề VIP không
tự bỏ qua điều kiện gói; UI phải kiểm tra đối tượng có quyền trước khi giao.

Gợi ý và kế hoạch Free chọn bài đủ quyền, không đặt bài bị khóa thành nhiệm vụ
bắt buộc. VIP mở thêm tập nội dung được xét; không mặc định đẩy trẻ sang bài khó.
Plan_v2 chọn bài nền tảng khi confidence còn thấp; ưu tiên prerequisite và kỹ năng
cần ôn khi có đủ bằng chứng. Kế hoạch cơ bản vẫn dùng được nếu gói hết hạn.

## 8. API đề xuất

Tất cả đường dẫn có prefix /api/v1. Các API trong bảng đã hoạt động:

| Endpoint                                                | Quyền và hành vi                                                             |
| ------------------------------------------------------- | ---------------------------------------------------------------------------- |
| GET /membership/plans                                   | Danh sách gói và quyền lợi đã phát hành; không quảng cáo phần chưa hoạt động |
| GET /students/me/membership                             | Gói hiện tại, trạng thái, ngày kết thúc, features của chính học sinh         |
| GET /guardian/students/{id}/membership                  | Guardian có liên kết verified_at; gói của trẻ                                |
| GET /admin/students/{id}/membership                     | Admin xem gói                                                                |
| GET /admin/students/{id}/membership/history             | Admin xem lịch sử thao tác                                                   |
| GET /guardian/students                                  | Danh sách trẻ có liên kết đã xác minh                                        |
| GET /admin/content-access                               | Danh sách chính sách và gói hiệu lực của bài/đề                              |
| PUT /admin/content/{lesson hoặc assessment}/{id}/policy | Admin, CSRF, lý do; cấu hình chính sách và audit                             |
| POST /admin/students/{id}/membership/grant              | Admin, CSRF, Idempotency-Key; cấp mới theo duration_days cho phép và lý do   |
| POST /admin/students/{id}/membership/extend             | Admin, CSRF, Idempotency-Key; gia hạn, không tự đổi vai trò                  |
| POST /admin/students/{id}/membership/revoke             | Admin, CSRF, Idempotency-Key; thu hồi, bắt buộc lý do                        |
| GET /lessons/{id}/preview                               | Metadata và đoạn giới thiệu được duyệt, không lấy nguyên blocks              |

GET membership ví dụ: plan_code=vip, status=active, starts_at/ends_at dạng ISO UTC,
features=[learning.basic, learning.advanced, ...]. Admin/teacher không có hồ sơ
học sinh không tự được tạo membership học sinh; UI theo role chỉ hiện phần phù hợp.
plan_code là gói có hiệu lực hiện tại: hết hạn/thu hồi thì free; thêm
subscription_plan_code=vip để thể hiện gói trước đó, status=expired/revoked và
features chỉ còn các quyền Free. Không dùng tên gói đã mua để suy ra quyền còn hiệu lực.

Đọc membership từ DB tại mỗi request ở giai đoạn đầu; giữ response học tập
Cache-Control: no-store. UI cập nhật gói sau thao tác, khi quay lại trang và khi
tới ends_at; backend vẫn kiểm tra độc lập nếu giao diện hiển thị trạng thái cũ.

Lỗi: 401 khi chưa đăng nhập; 404 cho tài nguyên riêng không thuộc chủ sở hữu/
liên kết; 403 với code MEMBERSHIP_REQUIRED cho bài published được giới thiệu nhưng
chưa đủ gói; 409 cho thao tác thay đổi mâu thuẫn hoặc key lặp khác payload; 422
cho input không hợp lệ. UI phân biệt lỗi gói với lỗi CSRF và sai vai trò, không
đưa nút nâng cấp cho mọi lỗi 403. Không dùng 402 làm cơ chế xác nhận trả tiền.
Chuẩn hóa detail dạng {code, message, required_plan} cho lỗi gói; cập nhật ApiError
trong frontend/src/lib/api.ts để nhận mã lỗi và vẫn hỗ trợ detail chuỗi của API cũ.

## 9. Triển khai theo giai đoạn

Giai đoạn 1: Free/VIP do admin cấp theo thời hạn, gắn nhãn nội dung, API kiểm tra
quyền, trang gói và giới thiệu bài bị khóa. Duyệt và bổ sung bộ bài nâng cao mới.
Mọi chức năng hiện có tiếp tục miễn phí theo cấu hình chuyển đổi.

Giai đoạn 2: kế hoạch cá nhân plan_v2 và thử thách nâng cao; xây luồng phụ huynh,
xác minh liên kết, báo cáo và PDF. Chỉ thêm feature vào quyền lợi sau khi nghiệm thu.

Giai đoạn 3: thanh toán dành cho người lớn, sau khi chọn nhà cung cấp và chính sách
giá. Bổ sung orders và payment_events riêng, giá/đích học sinh được xác định phía
server. Xác thực webhook, đối chiếu đơn/số tiền/trạng thái; event xử lý lặp không
cấp VIP lần hai. Trang redirect từ thanh toán không tự cấp quyền. Tiền tệ/chu kỳ
và hoàn tiền được thiết kế riêng khi chốt mô hình kinh doanh.

## 10. Tiêu chí nghiệm thu

| Tình huống                                             | Kết quả bắt buộc                                                                 |
| ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Free gọi trực tiếp API bài VIP hoặc đoán UUID          | Không có blocks/câu hỏi/đáp án ngoài quyền; không chỉ chặn UI                    |
| Free đổi localStorage, cookie phụ hoặc gửi is_vip=true | Không làm thay đổi quyền từ server                                               |
| VIP vào trang admin hoặc bài làm học sinh khác         | Vẫn bị chặn bởi role/owner                                                       |
| VIP vừa cấp/gia hạn/thu hồi trong phiên hiện tại       | Quyền có hiệu lực ở request tiếp theo, không cần đăng nhập lại                   |
| Hết hạn đúng ends_at                                   | Không mở bài VIP mới; vẫn xem kết quả của mình                                   |
| Hết hạn giữa attempt                                   | Chỉ attempt được cấp grant tiếp tục trong allowed_until; không kéo dài cửa sổ đề |
| Thu hồi trong attempt                                  | Quyền VIP bị chặn ngay; dữ liệu đã lưu và kết quả cũ được giữ                    |
| Hai request cấp/gia hạn cùng Idempotency-Key           | Một thay đổi, một lần cộng thời hạn; key khác payload trả 409                    |
| Guardian chưa verified hoặc chọn trẻ ngoài liên kết    | Không xem báo cáo hoặc thao tác nâng cấp cho trẻ đó                              |
| Không có chính sách nội dung hoặc thiếu migration      | Không lộ nội dung; báo lỗi cấu hình phù hợp cho người vận hành                   |
| Kế hoạch/gợi ý Free và VIP hết hạn                     | Không đưa bài bị khóa thành bước bắt buộc; giữ tiến độ cũ                        |
| Chuyển đổi dữ liệu hiện tại                            | 24 bài/12 đề vẫn Free, điểm/lịch sử không thay đổi; SQL gốc giữ nguyên           |

Kiểm thử backend cho role/owner/gói/biên thời gian/idempotency, browser cho thẻ khóa,
nâng cấp, hết hạn, màn hình chữ lớn và điện thoại. Tất cả kiểm thử ghi dữ liệu chạy
trên database test riêng. Chứng cứ chạy thực tế được ghi tại
[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md).
