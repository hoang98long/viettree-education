# AI Academy ưu tiên đào tạo, Free và VIP

Chính sách mới 12/10/2026 thay mô tả “toàn bộ nền tảng Academy miễn phí” trước
đây. Cập nhật 19/10/2026: 200 bài/1702 SVG; tập trung lý thuyết, quan sát, câu hỏi lựa chọn/ghép/
xếp bước và bài thực hành dữ liệu mô phỏng. Không cần tài khoản model hay
API trả phí để học.

## Phân bổ quyền mặc định

| Khối        | Miễn phí                                                                                          | VIP                     |
| ----------- | ------------------------------------------------------------------------------------------------- | ----------------------- |
| Lớp 4       | AI4-01 nhận biết AI, AI4-04 dữ liệu, AI4-27 giữ thông tin riêng, AI4-37 kiểm chứng, AI4-39 căn cứ | 35 bài còn lại          |
| Lớp 1/2/3/5 | Ba bài đầu và bài số 37, 39 mỗi khối                                                              | 35 bài còn lại mỗi khối |
| Tổng        | 25 bài                                                                                            | 175 bài                 |

VIP còn có lab phân loại/bias bằng thuật toán đơn giản, Prompt Builder,
xưởng comic/poster/quiz/báo cáo từ mẫu, dự án nộp giáo viên. Free xem bìa/tên/
thời lượng và bài nhập môn; không nhận payload steps/câu hỏi của bài khóa.
Free có mức gợi ý 1, VIP tối đa 3; tất cả đều do nội dung biên soạn sẵn cung cấp.

## Server và giao diện

`ai_lessons.minimum_plan_code` mặc định VIP cho bài mới. Migration 0011 gán
đúng bảy bài miễn phí của bản cũ. Seed mới bổ sung các bài và xuất bản phiên bản
tranh cho baseline chưa sửa; giữ payload/tiến độ cũ, giữ nội dung và quyền đã
được chỉnh qua CMS. Admin có thể
đổi quyền từng bài trong editor bằng mật khẩu/lý do/revision và audit; teacher
editor không tự đổi chính sách thương mại.

Backend kiểm quyền trước start/resume/step/attempt/gợi ý, lab và lưu/nộp sản
phẩm. Progress không thay entitlement. Thu hồi VIP chặn cả bài đã mở; lịch sử,
sản phẩm đã tạo, export và thành tích riêng vẫn được giữ. Trong UI có badge
Free/VIP, khóa và đường dẫn tìm hiểu gói cùng phụ huynh. Client không tự cấp
VIP bằng chọn lớp/hoàn thành bài/giao bài.

Tranh support chỉ dùng trong bài VIP bị chặn khi không có quyền; hero/bìa/thẻ
chung dùng làm giới thiệu. Ảnh nội dung có no-store để không kéo dài cache quyền
sau thu hồi; các asset giới thiệu dùng private cache 300 giây. Dữ liệu đã tải
trước đó không thể được thu hồi khỏi trí nhớ/ảnh chụp của người học.

## Không gọi model

`AI_TRAINING_ONLY=true` mặc định. Cổng này đứng trước provider flag/consent,
nên dù DB có tutor_enabled và môi trường đặt Ollama, học vẫn dùng hướng dẫn
nội bộ. Teacher draft cũng bị giữ ở nội dung mẫu. Admin không bật được model
qua giao diện trong chế độ này; các nút vận hành model được ẩn. Không phát
triển adapter/model mới ở đợt này, giữ code cũ để không phá khả năng mở rộng.

Lab là so đặc điểm của thẻ, không model nhận dạng ảnh. Studio ghép mẫu rồi trẻ
viết/sửa, không giả vờ AI tạo sản phẩm. Đọc nội dung bằng giọng local tùy chọn
không thu âm/gửi giọng; chữ/tranh luôn dùng được.

Triển khai: `alembic upgrade head` (0012), khởi động lại backend/frontend.
DB hiện tại đã migrate, không cần reset/seed lại tài khoản. Nếu cài mới:
import SQL gốc, migrate rồi seed theo README, nạp `seed-ai-academy`. Seed chọn
Free/VIP cho bài mới và không ghi đè chính sách admin đã chỉnh.

## VIP cấp / gia hạn / thu hồi

Kiểm chứng expiry, quyền Free/VIP, CSRF/RBAC/idempotency/audit, thao tác đồng
thời, attempt VIP cũ và cấp lại sau thu hồi. Cấp/gia hạn chỉ học sinh còn hoạt
động và plan VIP đang được mở. Gia hạn gói đã thu hồi nhận 409, cần cấp kỳ mới.
Replay key cũ không thêm ngày và trả **quyền hiện tại**, không snapshot VIP cũ.
Core luyện tập giữ grace khi hết hạn tối đa 60 phút nếu hợp lệ; **thu hồi** chặn
ngay grants cũ, kể cả cấp lại. AI không áp dụng grace sau hết quyền.
