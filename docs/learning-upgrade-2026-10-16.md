# Học AI và tự kiểm tra — 16/10/2026

Thêm **10 bài AI**, **15 bài ba môn / 60 câu hỏi / 15 đề luyện tập** cho
lớp 1–5. Bài mới có tranh/thẻ, câu ngắn, lời giải và gợi ý.
Không thêm bảng; Alembic head vẫn là `0012_lesson_bookmarks`.

## AI: thử nghiệm và kiểm chứng

Mỗi khối thêm chủ đề thứ 10, hai bài; số 37 Free, số 38 VIP.

| Khối | Bài Free                      | Bài VIP                        |
| ---- | ----------------------------- | ------------------------------ |
| 1    | Đếm lại cùng robot            | Hai màu của quả táo            |
| 2    | Đọc lại lời chỉ dẫn           | Nhãn nào cần sửa?              |
| 3    | Thử bằng thẻ chưa gặp         | Không đoán quả chỉ từ màu      |
| 4    | Hai cách kiểm tra phép tính   | Bộ mẫu đồ dùng công bằng hơn   |
| 5    | Bốn trên năm chưa phải tất cả | Điểm tổng có che một nhóm lỗi? |

Tổng Academy **190 bài / 1330 bước / 570 câu checkpoint**, mỗi khối
38 bài, mặc định 4 Free / 34 VIP. Quyền admin chỉnh riêng vẫn được giữ.
Lớp 1 dùng hai thẻ; lớp 2 dùng hai hoặc ba; lớp 3–5 tối đa bốn thẻ ở bài mới,
có thể chọn ít thẻ hơn. Checkpoint có ba câu, hiển thị từng câu.
Thư viện có **1625 SVG**, thêm 78 hình, giữ hình/phiên bản cũ.

Học liệu do VietTree biên soạn, tham khảo cách chia độ tuổi của
[AI4K12](https://ai4k12.org/gradeband-progression-charts/) và hoạt động phân loại,
dữ liệu, dự đoán lớp 3–5 của [Code.org](https://code.org/en-US/artificial-intelligence).
AI4K12 là khung đang lấy ý kiến, không phải chứng nhận cho VietTree.
Ứng dụng chuyển thành hoạt động thẻ mẫu có sẵn, **không gọi model**,
không cần GPU, webcam, thu âm hoặc nhập thông tin riêng.

## Ba môn: đọc kỹ, thử lại, tự kiểm tra

Bộ `review-2026-02`: mỗi khối ba bài, mỗi bài bốn câu và một đề riêng.

| Khối | Toán                  | Tiếng Việt             | Tiếng Anh, tự chọn    |
| ---- | --------------------- | ---------------------- | --------------------- |
| 1    | Đếm lại cho chắc      | Bút của Hà             | Hello, little pencil! |
| 2    | Nhớ một chục khi cộng | Chiếc cốc dùng lại     | A cat or a dog?       |
| 3    | Chia đều rồi thử lại  | Giỏ sách lớp em        | May I come in?        |
| 4    | Cùng một chiếc bánh   | Tấm bảng nhắc tưới cây | A rainy day           |
| 5    | Giảm giá rồi kiểm tra | Đọc bảng tin cho đúng  | Ask the way politely  |

Tiếng Việt Free ở cả năm khối; Toán lớp 1–2 Free, lớp 3–5 VIP;
Tiếng Anh của bộ mới là VIP. Tổng thêm **7 Free / 8 VIP**.
Free nhận gợi ý đầu, VIP đủ ba. Văn bản đọc hiểu được đặt trong từng câu hỏi;
hội thoại tiếng Anh có nghĩa tiếng Việt, chỉ dẫn cần thiết có ngay trong đề.
Phép tính và độ đọc tăng dần theo khối, dựa trên các mạch đã có trong registry.
Không tự nhận bao phủ toàn bộ sách giáo khoa. Xem
[chương trình tổng thể Bộ GDĐT](https://moet.gov.vn/content/tintuc/Lists/News/Attachments/8421/chuong-trinh-tong-the-ctgdpt-2018.pdf)
và nguồn môn/khối trong trang quản trị Chương trình học.

Sau khi nạp baseline và ba bộ applied/explorers/review: mỗi khối có
**80 bài / 438 câu / 68 đề**, toàn bộ **400 bài / 2190 câu / 340 đề** ở ba môn,
chưa tính Academy hoặc bài giáo viên tạo. Các bộ bổ sung được nạp riêng.

## Quyền và độ ổn định

- API bắt đầu bài AI trả `hint_limit` theo quyền hiện tại. Giao diện dừng ở
  mức được dùng; API gợi ý kiểm tra lại quyền mỗi lần, kể cả sau thu hồi VIP.
- Dữ liệu trả cho học sinh bỏ `standard`/`advanced`, vốn dùng làm gợi ý mức 2–3.
  Chỉ API gợi ý có kiểm tra quyền mới trả các nội dung này.
- Nộp lại cùng lựa chọn sau lỗi mạng giữ cùng mã idempotency; đổi câu trả lời
  hoặc mức bài tạo mã mới. Tránh ghi trùng khi server lưu nhưng phản hồi bị mất.
- Builder học liệu ngắn dùng chung; nội dung explorers đã xuất bản được so sánh
  không đổi sau khi tách builder. Admin theo dõi bộ review riêng từng khối.
- Tranh phép cộng không có chấm trang trí gây đếm nhầm; màu táo/bút mới khớp
  nhãn. Không ghi lại file hình cũ.

## Cập nhật môi trường khác

Sao lưu database trước. Trong thư mục backend:

```powershell
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
../.venv/Scripts/python.exe -m app.cli seed-supplement-content --release review-2026-02
../.venv/Scripts/python.exe -m app.cli verify-supplement-content --release review-2026-02
```

VPS dùng các lệnh `python -m app.cli ...` tương ứng trong container backend,
build lại image để có code/SVG mới, khởi động lại backend/frontend theo
[hướng dẫn VPS Nhật](deploy-vps-japan.md). Giữ `AI_TRAINING_ONLY=true`.
Không cần seed tài khoản để cập nhật bài.

[Kết quả kiểm thử và kiểm tra bảo toàn dữ liệu](audits/verification-quality-2026-10-16.md).
