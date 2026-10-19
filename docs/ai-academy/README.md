# VietTree AI Academy

Module học AI tiểu học trong VietTree Education, dùng cùng đăng nhập, phiên,
quyền Free/VIP, hồ sơ, lớp học và phụ huynh đã xác minh. Không cần khóa AI trả phí.

## Quy mô học liệu

| Nội dung                         |                            Số lượng seed |
| -------------------------------- | ---------------------------------------: |
| Lớp 1–5                          |                   11 chủ đề, 40 bài/khối |
| Tổng bài / bước / câu checkpoint |                         200 / 1400 / 600 |
| Kiểu hoạt động                   | 10; thêm lab phân loại và Prompt Builder |
| Dự án theo khối                  |   5; mỗi học sinh lưu một sản phẩm/dự án |
| Huy hiệu                         |        12, ghi nhận số bài đã hoàn thành |
| File SVG nguyên bản              |    1702, gồm ảnh mới và ảnh phiên bản cũ |

Từng bài có mục tiêu, tình huống, kiến thức, hoạt động, checkpoint, vận dụng,
hướng dẫn giáo viên, hỗ trợ và thử thách. Đây là chương trình làm quen AI tích
hợp Toán/Tiếng Việt/Tiếng Anh; không thay bộ học liệu ba môn lớp 1–5 hiện có.
Học liệu cần giáo viên nhà trường rà soát trước khi đưa vào dạy chính thức.

## Màn hình dùng được

- Học sinh: `/ai-academy`, `/ai-academy/grades/4`, bài học nhiều bước,
  `/games`, `/lab`, `/creative-studio`, `/ai-tutor`, `/projects`, `/portfolio`.
  Các đường dẫn viết ngắn dùng tiền tố `/ai-academy`.
- Giáo viên: `/teacher/ai-academy` giao bài, báo cáo/CSV, chấm rubric và góp ý;
  `/teacher/ai-academy/content` cho người được cấp quyền biên soạn/kiểm duyệt.
- Phụ huynh: `/guardian/ai-academy` theo dõi đúng trẻ đã xác minh, chấp thuận/
  thu hồi trợ giảng mô hình, xuất dữ liệu và yêu cầu gỡ nội dung sản phẩm.
- Admin: `/admin/ai-academy` bài học có phiên bản, thư viện/duyệt ảnh,
  chủ đề mới, lớp/ghi danh/quyền/phụ huynh, báo cáo, hàng đợi SVG,
  mẫu hướng dẫn có phiên bản, cảnh báo và yêu cầu riêng tư.

Baseline cập nhật 19/10/2026: mỗi khối **5 bài Free / 35 bài VIP**,
toàn module **25 Free / 175 VIP**. Giữ quyền admin đã chỉnh riêng.
Free có gợi ý mức 1 trong bài được mở;
VIP có mức 2–3, lab/Prompt Builder và studio/dự án từ mẫu. Server kiểm tra quyền
tại mỗi bước; không gửi nội dung bài VIP rồi chỉ che trong browser.
Xem [chính sách đào tạo AI](../ai-training-vip.md) và
[giá VIP tham khảo](../vip-pricing-research.md). Chưa có thanh toán tự động.

Học từng thẻ bằng nút chạm, checkpoint từng câu; **Em cần gợi ý** không yêu cầu
nhập chữ. Menu công cụ và giải thích dài thu gọn để trẻ tập trung. Lớp 1–2 có
bài khoảng 10 phút; lớp 1 hai thẻ, lớp 2 có hai hoặc ba thẻ; lớp 3–5 khoảng 15 phút. Có thể chia thời gian theo trẻ.
Xem [đối chiếu quốc tế và thiết kế](../visual-learning-and-ai.md),
[danh sách 200 bài](lessons.csv).

## Chạy nhanh

Trong terminal backend, dùng môi trường và PostgreSQL đã cấu hình:

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
```

Head là `0012_lesson_bookmarks`. Khởi động backend/frontend theo
[run-local.md](../run-local.md), đăng nhập bằng tài khoản hiện có. Seed không đổi
mật khẩu, VIP, lớp hoặc lịch sử. Không tạo bài làm/điểm demo giả.

## Tài liệu

[Khảo sát](architecture-audit.md), [kiến trúc](architecture.md),
[database](database.md), [chương trình](curriculum.md), [media](media-guide.md),
[an toàn](safety-policy.md), [giáo viên](teacher-guide.md),
[triển khai](deployment.md), [kiểm thử](testing.md),
[prompt minh họa](image-generation-prompts.json).

[Báo cáo đối chiếu prompt, kiểm chứng và phần còn thiếu](completion-report.md).

## Phạm vi còn cần tích hợp

Đợt hiện tại ưu tiên đào tạo: `AI_TRAINING_ONLY=true` chặn provider trước
flag/consent và giữ trợ giảng/soạn nháp ở mẫu nội bộ. Admin không bật model
qua UI trong chế độ này; học lý thuyết, bài tập và studio vẫn dùng được.

Ollama có adapter thật và kiểm thử HTTP bằng mock; chưa có model cài/chạy để
kiểm chứng chất lượng phản hồi thật. Sinh ảnh bitmap bằng model chưa có adapter
được duyệt; nút bật trả lỗi rõ ràng, dùng SVG/mẫu nội bộ và upload raster thay thế.
Giọng nói chỉ đọc bằng giọng local có sẵn khi bật, không ASR/thu âm/webcam.
Không có IDE Scratch, gallery công khai, tenant SaaS độc lập hoặc rubric tùy biến
theo từng lớp. Rubric sản phẩm hiện cố định 20/30/30/20. Mỗi kiểu game dùng board
chọn/ghép/xếp thẻ chung; lab là thuật toán so đặc điểm, không nhận dạng pixel.
Docker/HTTPS thật phải được kiểm tra trên server đích; xem báo cáo kiểm thử.

**19/10:** tìm bài không dấu, lọc bài, học tiếp đúng bài dở và trò chơi đúng khối.
Thêm 10 bài/77 SVG; [chi tiết nâng cấp](../ai-academy-upgrade-2026-10-19.md).
