# Học liệu tình huống và thư viện luyện tập

Bản cập nhật **15/10/2026**, mã học liệu `applied-2026-01`.
Đã nạp vào database local sau khi sao lưu; không cần migration mới.
Khởi động lại backend/frontend đang chạy để sử dụng giao diện mới.

## Nội dung bổ sung

Thêm **30 bài học, 150 câu hỏi, 30 đề luyện tập** cho lớp 1–5. Mỗi khối
có 6 bài: mỗi môn Toán, Tiếng Việt, Tiếng Anh thêm 1 bài Free và 1 bài VIP.
Bài Free có 4 câu; bài VIP có 6 câu. Bài có ba phần ngắn, thẻ tranh hoặc
sơ đồ/biểu đồ và lời giải cho từng câu sau khi nộp. Hình dùng SVG có sẵn,
không tải ảnh từ dịch vụ bên ngoài hoặc gọi mô hình AI.

| Lớp | Toán Free / VIP                               | Tiếng Việt Free / VIP                       | Tiếng Anh Free / VIP                      |
| --- | --------------------------------------------- | ------------------------------------------- | ----------------------------------------- |
| 1   | Giỏ quả / Chuỗi hạt lặp                       | Na chăm hoa / Hai lời dặn                   | Đồ dùng / Ghép màu và đồ vật              |
| 2   | Chia bút / Lịch buổi sáng                     | Trả bút cho bạn / Lời hẹn trả truyện        | Con vật, kích thước / Đồ chơi đổi màu     |
| 3   | Số sách trong thư viện / Đủ chỗ cho chuyến đi | Đọc thông báo / Bước trồng hạt còn thiếu    | Meet Ben / Mia's room                     |
| 4   | Chia dải ruy băng / Tổng và hiệu số cây       | Góc sách dễ tìm / Góp ý có lí do            | Anna's school day / Rainy-day plan        |
| 5   | Đong nước, số thập phân / Giá sau giảm        | Theo dõi giấy nháp / Kiểm tra lời quảng cáo | Trip to the library / Helping at the park |

Sau khi nạp cả bộ nền tảng và bộ bổ sung, mỗi khối có **74 bài, 414 câu,
62 đề**; năm khối tổng **370 bài, 2.070 câu, 310 đề**, chưa tính AI Academy
và nội dung giáo viên tự tạo. Mỗi khối gồm 49 bài Free và 25 bài VIP.
`curriculum-inventory` tiếp tục kiểm kê riêng bộ nền tảng để giữ mốc đối chiếu;
`applied-content-inventory` kiểm kê riêng phần bổ sung.

Nội dung bám các chủ đề đã có trong bản đồ chương trình của từng khối.
Đối chiếu [Chương trình tổng thể của Bộ GD&ĐT](https://moet.gov.vn/content/vanban/Lists/VBPQ/Attachments/1483/vbhn-chuong-trinh-tong-the.pdf)
và các nguồn môn học trong [lớp 1–2](grades1-2-curriculum.md),
[lớp 3](grade3-curriculum.md), [lớp 4](grade4-curriculum.md),
[lớp 5](grade5-curriculum.md). Đây là bài bổ trợ, không phải một bộ sách giáo khoa
hoặc tuyên bố đã bao phủ toàn bộ chương trình.

Tiếng Anh lớp 1–2 dùng thẻ có nghĩa tiếng Việt, thao tác chọn và gợi ý đọc cùng
người lớn. Đây là giai đoạn làm quen tự chọn; không thay thế luyện nghe/nói.
[Hướng dẫn Ngoại ngữ 1 tiểu học của Bộ GD&ĐT](https://xaydungchinhsach.chinhphu.vn/huong-dan-to-chuc-day-hoc-cac-mon-ngoai-ngu-1-cap-tieu-hoc-119230810082407558.htm).

## Quyền học và gợi ý

- Free được học ba bài bổ sung miễn phí của khối, mỗi bài mở một gợi ý đầu.
- VIP học cả sáu bài, mở tuần tự đủ ba gợi ý ở cả bài Free và VIP.
- Backend lọc gợi ý trước khi gửi dữ liệu; bài/đề VIP tiếp tục kiểm tra quyền
  khi đọc, tự giao và bắt đầu làm bài. Danh mục hiển thị bài bị khóa không cấp
  quyền truy cập nội dung. Cấp/thu hồi VIP có hiệu lực khi tải lại danh mục.

## Thư viện luyện tập mới

Học sinh mở **Thư viện luyện tập** (`/student/practice`):

- Tìm tên bài/chủ đề có hoặc không dấu; nhập từ khóa rồi bấm **Tìm bài**.
- Ba nút nhanh: **Bài ngắn** (tối đa 6 câu), **Chưa nộp**, **Ôn thêm**.
  Bấm lại nút đang chọn để bỏ lọc. Các điều kiện đang chọn được kết hợp với nhau.
- **Chọn thêm bộ lọc** mở môn, gói, kết quả gần nhất, tối đa 4/6/8 câu và loại đề.
- Mỗi trang tối đa 12 bài; đổi bộ lọc trở về trang đầu. Có xóa lọc, làm mới,
  điểm tốt nhất, điểm gần nhất và liên kết về bài học/gợi ý.

“Ôn thêm” là bài có **lần nộp đã chấm gần nhất dưới 80% số điểm tối đa**.
Đạt từ 80% được ghi riêng; đây là chỉ báo chọn bài ôn, không phải kết luận về
năng lực toàn môn. Điểm tốt nhất vẫn giữ khi lần mới có điểm thấp hơn.
Bài đang làm hoặc nộp nhưng chưa chấm không tính là điểm 0. “Chưa nộp” ở
đây nghĩa là chưa có lần nộp đã chấm với số điểm tối đa lớn hơn 0.

Dữ liệu chỉ thuộc học sinh hiện tại và khối trong hồ sơ trên server. API dùng
`Cache-Control: no-store`, không trả nội dung câu hỏi, đáp án hoặc lời giải.
Phân trang và thống kê đọc trong cùng một truy vấn để tránh lệch khi có lần
nộp mới; lượt làm của học sinh khác không ảnh hưởng kết quả.

Admin mở **Chương trình**, chọn khối để xem số bài/câu/đề bổ sung đã xuất bản
so với 6/30/6 dự kiến. Bảng môn/chủ đề và CSV tự cộng thêm học liệu mới.

## Nạp sang máy khác hoặc VPS

Máy local hiện tại đã nạp. Với máy khác, sao lưu DB và nạp bộ nền tảng của các
khối trước; từ thư mục `backend` chạy:

```powershell
../.venv/Scripts/python.exe -m app.cli applied-content-inventory
../.venv/Scripts/python.exe -m app.cli seed-applied-content
../.venv/Scripts/python.exe -m app.cli verify-applied-content
```

Chỉ nạp một số khối: `seed-applied-content --grades 1 2` và kiểm tra bằng
`verify-applied-content --grades 1 2`. Lệnh inventory chỉ đọc source, không cần DB.

VPS dùng wrapper đã cấu hình, khi đang bảo trì sau backup:

```bash
dc run --rm -T --no-deps backend python -m app.cli seed-applied-content
dc run --rm -T --no-deps backend python -m app.cli verify-applied-content
```

Lệnh nạp dùng một transaction cho các khối được chọn và khóa phối hợp với
các lệnh seed khác. Chỉ thêm mã học liệu mới, không gọi seed tài khoản,
không đổi mật khẩu, gói, phiên đăng nhập, lịch sử hoặc câu hỏi đã xuất bản.
Chạy lại giữ nguyên bản bài học giáo viên đã chỉnh. Nếu câu hỏi phiên bản 1
hoặc cấu trúc đề đã khác source, lệnh báo xung đột và rollback; dùng ngân hàng
câu hỏi/biên tập bài học để quản lí phiên bản thay vì sửa trực tiếp dữ liệu SQL.

## Kiểm chứng đợt cập nhật

- 799 kiểm thử backend không integration đạt, 9 bài kiểm tra cần DB bị bỏ qua
  trong lượt này; 21 kiểm thử học liệu/API liên quan đạt, gồm 10 integration
  thực trên PostgreSQL riêng. Có kiểm tra đáp án Toán giải độc lập, schema,
  quyền/gợi ý cả năm khối, tìm không dấu, phân trang và cách tính kết quả cá nhân.
- Luồng trình duyệt desktop/mobile: Free lớp 1 đọc/gợi ý/làm/nộp/ôn,
  VIP lớp 5 xem biểu đồ/gợi ý, admin kiểm kê đủ năm khối; kiểm tra không tràn
  ngang ở 320/390/768/1280 px. Cả 6 kịch bản mới đạt, cùng 2 kịch bản hồi quy
  lớp 5 (thư viện, tiến độ và cấp/thu hồi VIP). 80 kiểm thử frontend đạt;
  typecheck, lint, format và build production đạt.
- Nạp local có backup custom và `pg_restore --list`; so sánh dữ liệu cũ của
  **81 bảng, 20.860 dòng** trước/sau trong transaction: giữ nguyên, chỉ thêm
  học liệu. [Bằng chứng nạp local](audits/applied-local-2026-10-15.json).

Đợt này không đo lại sức tải VPS hoặc chạy thử mạng Việt–Nhật. Các phép đo
HTTPS/50 người dùng thuộc [đợt chuẩn bị VPS trước](release-readiness-2026-10-15.md).
