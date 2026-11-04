# Giới thiệu và các mốc nâng cấp trước 04/11/2026

Các số liệu bên dưới ghi nhận từng thời điểm. Số liệu hiện tại xem [README](../README.md) và [bản nâng cấp 04/11](discovery-and-library-2026-11-04.md).

**Rà soát trước triển khai 20/10:** quản trị có báo cáo trước mở web và tải biên
bản CSV; lệnh `check-release` đối chiếu tài khoản, role DB, đủ học liệu và file
minh họa. Đã thử phục hồi DB sang bản sao riêng và kiểm thử bằng HTTPS local.
[Xem kết quả, giới hạn và các bước mở web](pre-deployment-review-2026-10-20.md).

**Nâng cấp AI Academy 19/10:** thêm 10 bài/77 hình, tổng 200 bài cho lớp 1–5.
Trò chơi chọn đúng khối; học tiếp ưu tiên bài dở; tìm không dấu và lọc bài dễ hơn.
[Hướng dẫn và cập nhật](ai-academy-upgrade-2026-10-19.md).

**Nâng cấp 17/10: học tiếp và luyện theo tình huống hằng ngày:** thêm 15 bài,
60 câu hỏi, 15 đề cho lớp 1–5. Trang chủ mở đúng bài/lượt/bước AI đang dở;
bài AI có nút tìm thẻ chưa đúng và giải thích từng thẻ, dễ đọc trên điện thoại.
[Nội dung, cách dùng và cập nhật VPS](daily-learning-and-resume.md).

**Nâng cấp 16/10: học AI và tự kiểm tra:** thêm 10 bài AI, 15 bài ba môn,
60 câu hỏi và 78 hình SVG cho lớp 1–5. Gợi ý AI theo quyền Free/VIP;
gửi lại sau lỗi mạng giữ cùng mã lượt nộp để tránh trùng.
[Nội dung, kiểm thử và cách cập nhật](learning-upgrade-2026-10-16.md).

**Bài học đã lưu và bộ Khám phá:** lưu bài theo tài khoản, đồng bộ giữa các
phiên/thiết bị; thêm 15 bài luyện ngắn, 60 câu hỏi và 15 đề cho lớp 1–5.
Admin theo dõi từng bộ học liệu; trang chủ đếm đủ lượt đã nộp vượt giới hạn
lịch sử 200 dòng. Local đã backup, migrate `0012_lesson_bookmarks` và nạp.
[Cách dùng, nội dung và cập nhật VPS](bookmarks-and-explorers.md).

**Học liệu tình huống và luyện tập:** thêm 30 bài/150 câu/30 đề cho lớp 1–5,
mỗi môn có bài Free và VIP, tranh/thẻ minh họa và gợi ý theo bước. Database
local đã nạp sau backup. Thư viện luyện tập có tìm không dấu, bài ngắn, phần
cần ôn và kết quả gần nhất/tốt nhất; admin theo dõi số học liệu bổ sung từng khối.
[Nội dung, cách dùng và nạp sang VPS](applied-learning.md).

**VPS tại Nhật 4 vCPU / RAM 8 GB / SSD 100 GB:** đã có profile `vps8gb`,
kiểm tra trước mở web `check-launch`, kiểm tra sau deploy `deploy/smoke.sh`,
sao lưu kèm SHA256 và phát hiện backup quá hạn. Đã kiểm tra HTTPS qua Caddy
local, database runtime ít quyền và mạng có độ trễ.
[Hướng dẫn triển khai gói VPS đã chọn](deploy-vps-japan.md) ·
[Báo cáo kiểm chứng](release-readiness-2026-10-15.md).

**Cập nhật 15/10/2026:** xem lại bài có đáp án đúng và lời giải chia đoạn,
minh họa ô vuông đúng tỉ lệ; sửa đếm câu đã xóa đáp án, thêm thời hạn chờ mạng
và phục hồi khi tải cấu trúc database bị gián đoạn. Ba đợt 50 học sinh với
API một worker: 2.310 request học tập không lỗi trên local.
[Chi tiết thay đổi, kiểm thử và giới hạn](review-2026-10-15.md).

**Rà soát học liệu và tải 50 học sinh (14/10/2026):** đối chiếu 1.920 câu Free/VIP,
bổ sung kiểm tra đáp án Toán độc lập, đọc từng đoạn ngay trong câu hỏi và chấm
linh hoạt cách viết số. Đã thử 50 lượt đăng nhập đồng thời và ba vòng lưu đủ
câu/nộp bài, 2.310 request không lỗi trên local. Thống kê cập nhật theo các câu
vừa làm, có giới hạn RAM xác thực và tham số vận hành VPS. Xem
[báo cáo, số đo và giới hạn kiểm chứng](content-load-vps-review.md).

**Bài luyện tự lưu:** lưu sau khoảng 0,8 giây, giữ đáp án trên trang khi lỗi mạng,
thử lại khi có mạng; chuyển câu/nộp bài chờ lưu hết. Bài có hạn giờ hiển thị
đồng hồ theo mốc máy chủ. Admin có bảng rà soát độ dài, minh họa và phân bổ
gợi ý trong trình soạn bài. [Cách dùng và giới hạn](learning-reliability.md).

**Ba môn lớp 1–5 đã có học liệu:** mỗi khối **68 bài / 384 câu / 56 đề**:
Toán 25/142/21, Tiếng Việt 23/130/19, Tiếng Anh 20/112/16. Lớp 1–2 được
biên soạn riêng theo chương trình Việt Nam: bài 6–8 phút, minh họa đếm/thẻ
chữ, câu lệnh ngắn, lựa chọn ít, nghỉ sau 2–3 câu. Free 46 bài/34 đề;
VIP thêm 22 bài/22 đề vận dụng phù hợp khối, gợi ý 1 → 3 theo quyền.
Xem [khảo sát, nội dung và cách nạp lớp 1–2](grades1-2-curriculum.md).

**Lớp 5 mới:** 68 bài ba môn, gồm thập phân, tỉ số/phần trăm, hình học,
chuyển động, đọc hiểu/viết và Tiếng Anh theo ngữ cảnh. Có 46 bài Free/22 bài VIP,
minh họa hình học và biểu đồ quạt tròn. [Căn cứ chương trình và danh mục](grade5-curriculum.md).
Học sinh có **Thư viện bài học** (`/student/lessons`), tìm không dấu, lọc môn/gói/
tiến độ. Admin chọn khối ở đầu trang chương trình, xem tổng, thu gọn chủ đề và
biên soạn năm kiểu minh họa mới. Khởi động lại server sau cập nhật.

**AI Academy đã có đủ lớp 1–5:** mỗi khối **11 chủ đề / 40 bài**, tổng **200 bài**
và **1702 SVG** (giữ cả ảnh cho các phiên bản cũ). Học bằng tranh, mỗi lần một thẻ,
game/lab, Prompt Builder, trợ giảng an toàn, xưởng sáng tạo, sản phẩm riêng,
giao bài/chấm rubric và CMS/media theo quyền. Dùng cùng tài khoản hiện có;
mặc định học lý thuyết và bài tập nội bộ, `AI_TRAINING_ONLY=true` chặn gọi model.
Baseline mỗi khối có **5 bài Free / 35 bài VIP**, tổng 25/175; giữ quyền đã được
admin chỉnh riêng. Gợi ý mức 1 miễn phí, mức 2–3 dành cho VIP, không cần gõ mô tả.
Xem [hướng dẫn đầy đủ AI Academy](ai-academy/README.md).

**Bài học dễ đọc hơn:** mở từng phần, đọc từng đoạn; 46 tranh từ vựng/truyện,
thẻ từ và lựa chọn bài tập có hình phù hợp, tranh thay đổi theo đoạn đang đọc;
minh họa phép cộng, các hàng của số và phân số. Nội dung đọc đầy đủ vẫn có nút
**Xem cả phần**. Xem [thiết kế học bằng hình và nguồn quốc tế](visual-learning-and-ai.md).

**Deploy lên VPS:** xem [hướng dẫn riêng](deploy-vps.md) cho Ubuntu + Docker
Compose production, HTTPS, chuyển dữ liệu, tài khoản thật, backup và cập nhật.

**Gói VPS tiết kiệm 3 cores / RAM 2 GB / SSD 50 GB:** đã có profile `small`,
giới hạn RAM dịch vụ, một worker, pool DB nhỏ và dùng image build trên máy khác.
Giữ đầy đủ Free/VIP và học liệu; không cần migration mới.
[Hướng dẫn cho gói VPS này](deploy-small-vps.md).

**Kiểm tra trước triển khai:** [bản rà soát và các bước xác nhận](production-readiness.md).
Admin có mục **Kiểm tra hệ thống** (`/admin/system`). Bộ production đã có trong
`docker-compose.production.yml` và `deploy/`; local tiếp tục dùng cấu hình development.
CLI `check-system` chỉ đọc, `cleanup-auth` mặc định dry-run. Head hiện tại
`0012_lesson_bookmarks`; nạp AI lần đầu bằng `seed-ai-academy`.

**Chạy trên máy hiện tại:** xem [hướng dẫn local ngắn](run-local.md) với hai
terminal PowerShell cho backend và frontend.

**Phiên đăng nhập:** mặc định 8 giờ; học sinh có thể chọn ghi nhớ 7 ngày trên máy
cá nhân. Biểu tượng VietTree đưa về dashboard khi đã đăng nhập; mở `/login` trong
phiên tự chuyển tiếp. Cache trạng thái giao diện 30 giây, quyền vẫn kiểm tra tại DB.
Xem [thiết kế và vận hành phiên](session-management.md).

Khu vực học sinh dùng chữ mặc định 18 px, bài học 20 px, câu hỏi 22 px; các nút chính
có chiều cao tối thiểu 48 px. Bấm **Cỡ chữ** hoặc vào **Hồ sơ của em → Chữ dễ đọc cho em**:
chọn **Chữ gọn hơn** (16 px, bài học 18 px, câu hỏi 20 px) cho màn hình điện thoại,
**Chữ vừa đủ lớn** hoặc **Chữ lớn hơn** (22/24/26 px). Giao diện điều chỉnh khoảng
cách theo cỡ chữ. Lựa chọn lưu trong tài khoản, riêng cho **điện thoại / máy tính bảng /
máy tính**, dùng cả trong AI Academy và giữ sau đăng nhập lại. Thiết bị chưa chọn
riêng dùng cỡ chữ mặc định cũ. Xem [cấu hình cỡ chữ](reading-preferences.md).

Mục **Kế hoạch học** (`/student/learning-plan`) chuẩn bị tối đa 3 bài học chưa hoàn
thành và bài luyện tập theo chủ đề trong 7 ngày. Chọn môn rồi bấm **Chuẩn bị kế hoạch**.
Mỗi môn có một kế hoạch đang học; bấm lại sẽ mở kế hoạch đó. Dùng **Em đã đọc xong**
ở cuối bài học để lưu tiến độ đọc; nộp bài luyện tập sẽ tự cập nhật bước luyện tập.
Ngày trên kế hoạch là gợi ý, không khóa bài hay trừ điểm khi học muộn. Tiến độ đọc
không được dùng làm bằng chứng năng lực; năng lực vẫn dựa vào câu trả lời đã chấm.

**Giữ nguyên** `database/viettree_education_schema.sql` với 34 bảng gốc. Không reset,
DROP hay TRUNCATE database học tập. Database mặc định có tên **`viettree-education`**,
bao gồm dấu gạch ngang. Alembic bổ sung hai bảng auth và sáu bảng gói học, revision
`0009_guided_hints` thêm quyền gợi ý theo bước cho VIP; `0010_ai_academy`
thêm 29 bảng riêng và tái sử dụng tài khoản/lớp/media/consent. `0011_classes_vip_training`
thêm 8 bảng quản lý giao bài, tuyên dương và giá VIP, cùng chính sách đào tạo AI.
`0012_lesson_bookmarks` thêm bảng lưu bài theo tài khoản.
Migration tài khoản thêm vòng đời mật khẩu tạm và revision tài khoản,
giữ mật khẩu, phiên và lịch sử cũ. Bảng nháp bài học tiếp tục tách bản xuất bản.
