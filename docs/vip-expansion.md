# Mở rộng VIP lớp 4

## Quyền lợi đã triển khai

| Chức năng             | Cách dùng                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| Góc học VIP           | Menu **Góc học VIP** → chọn môn hoặc chỉ xem bài chưa đọc xong; mở bài học và đề thử thách đi kèm             |
| Sổ tay ôn lỗi         | Gom câu sai/chưa trả lời trong bài đã chấm của chính em; lọc môn, phân trang, thử đáp án mới rồi xem lời giải |
| Báo cáo học tập       | Chọn 7/30 ngày gần đây, xem bài đã nộp, tỷ lệ điểm, bài đọc hoàn thành, nhịp luyện tập và kỹ năng cần ôn      |
| In / lưu PDF          | Trong báo cáo, bấm **In / lưu PDF**; trình duyệt mở hộp thoại in, chọn máy in hoặc lưu PDF                    |
| Kế hoạch theo kỹ năng | Từ Góc học VIP mở kế hoạch, chọn **Theo kỹ năng cần ôn**; tiếp tục dùng plan_v2 hiện có                       |

Tất cả chức năng mới yêu cầu tài khoản student và quyền VIP còn hiệu lực. Học sinh
Free được xem lời giới thiệu nhẹ nhàng và có đường trở lại bài miễn phí. Kết quả,
lịch sử và cây năng lực cũ vẫn xem được sau hết hạn/thu hồi VIP.

## Nội dung mới

Thêm **6 bài học, 48 câu hỏi và 6 đề thử thách**, không sửa phiên bản câu hỏi cũ:

| Môn        | Bài học mới                                                                    |
| ---------- | ------------------------------------------------------------------------------ |
| Toán       | Phân số trong một buổi làm bánh; Thiết kế luống rau: chu vi và diện tích       |
| Tiếng Việt | Thám tử đọc hiểu: tìm bằng chứng; Xưởng viết: nối ý và sửa câu                 |
| Tiếng Anh  | A trip to the market: đọc theo trình tự; Our class picnic: đọc kế hoạch và giờ |

Mỗi bài có phần khám phá, ví dụ, ghi nhớ, tự luyện và đề 8 câu. Có bốn loại câu:
chọn một, chọn nhiều, điền đáp án và sắp xếp. Bài/đề/phiên bản câu đều gắn VIP;
giới thiệu cho Free không trả nội dung đầy đủ. Nội dung tự biên soạn cho development;
giáo viên cần rà soát chuyên môn trước dùng thực tế.

Sau nạp đủ bộ seed, lớp 4 có **48 bài, 264 câu, 36 đề**, 12 chủ đề và 12 kỹ năng.
Free giữ **30 bài, 18 đề**; VIP mở thêm **18 bài, 18 đề**. Đây là số lượng bộ seed,
không bao gồm câu/đề admin tự tạo. Mỗi môn có 16 bài, 88 câu và 12 đề.

## Sổ tay ôn lỗi

- Chỉ lấy đáp án trong attempt đã `graded`, đúng chủ sở hữu và lớp hiện tại.
  Không đọc nháp, bài của học sinh khác hoặc lấy câu mới từ ngân hàng.
- Mỗi phiên bản câu chỉ xuất hiện theo lần chấm gần nhất. Nếu làm lại đúng trong
  một bài chính thức dùng phiên bản đó, câu được đưa ra khỏi sổ. Phiên bản mới
  không ghi đè lịch sử hoặc lời giải của phiên bản cũ.
- Tự ôn gọi API kiểm tra đáp án, không ghi vào attempts/answers/mastery, không đổi
  điểm hay tạo một lượt thi. Tự ôn đúng vẫn giữ câu trong sổ đến khi có lần làm bài
  chính thức đúng; màn hình giải thích rõ quy tắc này.
- Danh sách không trả đáp án đúng/lời giải sẵn; chỉ trả lời giải sau khi kiểm tra
  câu tự ôn, hoặc khi mở kết quả bài gốc đã nộp. Không che đáp án bằng CSS.
- Phân trang 20 câu; thu hồi/hết hạn VIP chặn kiểm tra tiếp ngay tại backend.

## Cách tính báo cáo

Khoảng 7/30 ngày gồm hôm nay, từ 00:00 ngày đầu đến thời điểm hiện tại theo
Asia/Bangkok. Kỳ trước là 7/30 ngày liền trước ngày bắt đầu; hôm nay có thể chưa
đủ ngày. Chỉ tính bài đã chấm của chính em, thuộc lớp hiện tại.

Tỷ lệ điểm = tổng điểm đạt / tổng điểm tối đa × 100; không có điểm tối đa thì hiển
thị **Chưa có dữ liệu**, không gán 0. Các đề khác nhau về độ khó nên so sánh hai kỳ
chỉ mang tính tham khảo. Ngày có hoạt động trong báo cáo là ngày có bài luyện đã
nộp, không suy ra thời gian học hoặc số lần truy cập.

Bài đọc hoàn thành tính theo thời điểm học sinh xác nhận đọc xong; không dùng để
suy ra năng lực. Kỹ năng cần ôn lấy snapshot từ toàn bộ lịch sử, ít nhất 5 câu được
chấm và mastery dưới 0,7; có hiển thị độ tin cậy. Không xếp hạng hoặc so sánh với
học sinh khác. Báo cáo được học sinh mở cùng phụ huynh; chưa thêm quyền đọc kết quả
cho guardian chưa được liên kết/xác minh, gửi email hoặc tạo PDF ở server.

## Cập nhật local

Trong PowerShell, tại `backend`:

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-vip-content
../.venv/Scripts/python.exe -m app.cli verify-seed
```

Migration `0006_vip_learning_tools` chỉ thêm ba feature vào gói VIP hiện có:
`vip.library`, `review.mistakes`, `reports.personal`. Không tạo role VIP, không cấp
VIP cho tài khoản Free, không gia hạn gói và không xóa/sửa dữ liệu học tập cũ.
Lệnh nạp mới chỉ thêm nội dung VIP, không tạo tài khoản hay reset mật khẩu.
Chạy lại không nhân đôi; xung đột phiên bản đã xuất bản làm transaction rollback.

Khởi động lại backend/frontend theo [run-local.md](run-local.md), đăng nhập bằng
tài khoản VIP đang hiệu lực. Admin vẫn cấp/gia hạn/thu hồi ở **Học sinh → Quản lý
gói học** và quản lý nhãn/quyền nội dung ở **Quyền nội dung**. Admin xem câu/đề mới
trong ngân hàng hiện có, không dùng role admin để làm bài dưới danh nghĩa trẻ.

Ở production, migration cập nhật quyền; nội dung cần được rà soát và nạp riêng,
theo luồng content-only trong [deploy-vps.md](deploy-vps.md). Không bật chế độ
development hoặc chạy seed demo để nạp trên VPS.

## API

| API                                                                               | Feature cần có                                             |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| GET `/api/v1/students/me/vip/library`                                             | `vip.library`; bài học còn kiểm tra quyền nội dung hiện có |
| GET `/api/v1/students/me/vip/mistakes?subject_code=MATH&page=1`                   | `review.mistakes`                                          |
| POST `/api/v1/students/me/vip/mistakes/{answer_id}/check` với `{ "answer": ... }` | `review.mistakes`, owner, câu đã chấm, CSRF                |
| GET `/api/v1/students/me/vip/report?days=7` hoặc `30`                             | `reports.personal`                                         |

Quyền kiểm tra tại mỗi request, kể cả tài khoản vẫn đang đăng nhập trong phiên 7
ngày. API giữ `no-store`; không cache báo cáo, đáp án hoặc trạng thái VIP dùng
chung giữa học sinh. Giao diện làm mới gói khi quay lại tab, tại hạn gói và định kỳ;
refresh hợp lệ không xóa câu trả lời tự ôn đang nhập.

Hướng mở rộng tiếp: nhắc lịch ôn có tùy chọn bật/tắt; báo cáo trong tài khoản phụ
huynh đã xác minh; dự án tự luận có giáo viên nhận xét; công cụ admin soạn bài học.
Các mục này chưa đưa vào quyền lợi đang hoạt động.
