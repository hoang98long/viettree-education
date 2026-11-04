# Học liệu, thư viện và cấu trúc code — 04/11/2026

Bộ `discovery-2026-04` — **Khám phá cùng bạn** thêm **30 bài / 120 câu hỏi /
30 đề luyện** cho lớp 1–5: mỗi khối sáu bài, mỗi môn một Free và một VIP.
Đã sao lưu và nạp vào database local; khởi động lại backend/frontend để dùng.
Không có migration mới, head vẫn `0012_lesson_bookmarks`.

## Nội dung mới

| Lớp | Môn        | Free                      | VIP                         |
| --- | ---------- | ------------------------- | --------------------------- |
| 1   | Toán       | Đếm hạt để gieo           | Ô trống của bạn Ong         |
| 1   | Tiếng Việt | Chiếc lá bên cửa          | Chờ bạn cùng đi             |
| 1   | Tiếng Anh  | Mèo và chó: cat, dog      | Hỏi lại: có phải mèo không? |
| 2   | Toán       | Đo hai dải giấy           | Tìm số trên cánh cửa        |
| 2   | Tiếng Việt | Bình nước của Mai         | Góc đọc có chỗ trống        |
| 2   | Tiếng Anh  | Thước và tẩy của em       | Hai chiếc bút xanh          |
| 3   | Toán       | Các hàng cây nhỏ          | Bảng số còn thiếu           |
| 3   | Tiếng Việt | Tấm nhãn ở vườn trường    | Lời mời trong giờ ra chơi   |
| 3   | Tiếng Anh  | My pets can move          | Where is the rabbit?        |
| 4   | Toán       | Đọc bảng mượn sách        | Hai đội giữ sân xanh        |
| 4   | Tiếng Việt | Đọc thông báo đổi lịch    | Hai ý kiến cho góc xanh     |
| 4   | Tiếng Anh  | The weather card          | Two days, two activities    |
| 5   | Toán       | Giảm giá trong bài toán   | Xếp hộp theo từng lớp       |
| 5   | Tiếng Việt | Đọc bản tin có ngày tháng | Một đề xuất có căn cứ       |
| 5   | Tiếng Anh  | Water after a walk        | Read the trip plan          |

Bài lớp 1–2 dự kiến sáu phút, khối lớn tám phút; mỗi bài có bốn câu và ba gợi
ý. Free nhận một gợi ý định hướng trên bài được mở, VIP nhận ba mức trên cả
bài Free và VIP. Backend kiểm tra quyền lúc đọc, mở đề và lưu/nộp bài.

Toán đi từ đếm và ô trống trong 10, đo độ dài và hàng chục/đơn vị, đến nhân chia,
đọc bảng số liệu, tổng–hiệu, phần trăm và thể tích. Quy tắc dãy số được nêu rõ;
bài có đơn vị và lời giải. Đoạn đọc Tiếng Việt là văn bản tự biên soạn, ngắn
dần theo khối nhỏ, kèm lại trong từng câu hỏi. Các câu đọc hiểu lớn hơn luyện
đọc thông báo, phân biệt dữ kiện và suy đoán, tìm căn cứ cho kết luận.

Tiếng Anh có nghĩa từ mẫu, ngữ cảnh quen thuộc và ít lựa chọn ở lớp nhỏ. Trong
bộ bổ trợ này, lớp 1–2 ưu tiên làm quen từ/câu, có người lớn đọc cùng; lớp 3–5
luyện hiểu câu và giao tiếp đơn giản. Đây là lựa chọn biên soạn của ứng dụng.
[Hướng dẫn năm học 2026–2027](https://xaydungchinhsach.chinhphu.vn/cong-van-so-5208-bgddt-gdpt-huong-dan-thuc-hien-nhiem-vu-giao-duc-pho-thong-nam-hoc-2026-2027-119260808110247193.htm)
yêu cầu triển khai ngoại ngữ phù hợp điều kiện và đối tượng học sinh. Chính
phủ có [mục tiêu tiếng Anh bắt buộc từ lớp 1 trên toàn quốc vào năm 2030](https://en.baochinhphu.vn/english-to-become-compulsory-language-from-grade-1-nationwide-by-2030-111251031143422078.htm).
Các mạch nội dung kế thừa registry môn/khối của dự án và [Chương trình tổng thể
GDPT 2018](https://moet.gov.vn/content/tintuc/Lists/News/Attachments/8421/chuong-trinh-tong-the-ctgdpt-2018.pdf).
Đây là học liệu bổ trợ, chưa phải đánh giá bao phủ toàn bộ một bộ sách giáo khoa.

Thêm ba tranh SVG gốc: chiếc lá, giày và bình nước tại `frontend/public/learning`.
Tranh chỉ gắn với từ cụ thể; không suy đoán từ câu dài/phủ định. Các bài tiếp
tục dùng hình đếm, hàng cây, biểu đồ, thẻ và hình hộp có sẵn. Ảnh trang trí có
nhãn chữ đi kèm; câu hỏi vẫn đủ dữ kiện khi không xem ảnh.

## Giao diện và cách dùng

Vào **Thư viện bài học** hoặc **Thư viện luyện tập** → **Chọn thêm bộ lọc** →
**Bộ bài học** → **Khám phá cùng bạn**. Có thể kết hợp môn, Free/VIP, tìm không
dấu, tiến độ hoặc kết quả. Đổi bộ sẽ về trang đầu; **Xóa bộ lọc** trở về toàn bộ
thư viện. Lựa chọn **Tất cả bộ bài** gồm cả học liệu nền tảng và nội dung admin
biên soạn. Các bộ đã đăng ký nhưng chưa nạp có thể trả danh sách trống.

Bộ lọc dùng cùng một component ở hai thư viện; metadata chỉ gồm mã/tên.
Không cấp quyền đọc bài, không trả đáp án và không chuyển khối của học sinh.
Danh sách và tổng số vẫn lấy trong cùng snapshot SQL, tối đa 12 mục/trang.

Trong bài học, bài luyện gắn trực tiếp với bài đang đọc được đưa lên đầu.
Hiển thị tối đa ba lựa chọn, có **Xem thêm bài luyện tập** để mở thư viện.
Khối gợi ý Free/VIP tự xuống hàng trên màn hình hẹp để nút không bị ép thành
một cột chữ dài.

Sau nền tảng và đủ năm bộ applied/explorers/review/daily/discovery: mỗi khối
**89 bài / 474 câu / 77 đề**, tổng **445 bài / 2.370 câu / 385 đề** ba môn.
AI Academy giữ nguyên **200 bài / 1.702 SVG**, gồm ảnh cho phiên bản cũ.
Không tính nội dung admin tự tạo. AI tiếp tục chế độ đào tạo nội bộ.

## Tổ chức code và dọn tệp

- Nội dung mới ở `backend/app/curriculum/supplements/discovery/`: `pack.py`
  điều phối, ba file môn học chứa nội dung, `__init__.py` giữ mã/tên và tham số
  mặc định cho hàm tạo bài.
- Bỏ ba wrapper `builders.py` bị trùng trong `daily`, `review`, `explorers`;
  tham số từng bộ chuyển về package, cả ba dùng `supplements/builders.py`.
  Builder `applied` có hành vi khác nên vẫn giữ riêng.
- Tách tìm kiếm không dấu và kiểm tra bộ học liệu vào
  `services/library_filters.py`; service luyện tập không còn import chi tiết
  nội bộ của service bài học. Router, schema và service vẫn tách theo trách nhiệm.
- `frontend/src/features/lessons/release-filter.tsx` dùng chung hai thư viện.
- Rút gọn README và hướng dẫn local; phần giới thiệu và các mốc cũ được giữ tại
  [release-notes.md](release-notes.md), không xóa tài liệu vận hành.

Đã đối chiếu payload của bốn bộ bổ sung cũ và 200 bài AI trước/sau refactor:
không đổi. Không xóa migration, SQL gốc, media phiên bản cũ hoặc bản backup.
Đối chiếu local sau nạp giữ nguyên **23.933 bản ghi tại 82 bảng ứng dụng**;
chỉ thêm bản ghi thuộc bộ mới. Xem [biên bản nạp và SHA256 backup](audits/discovery-local-2026-11-04.json).

## Cập nhật máy khác và VPS

Sao lưu trước khi nâng cấp, lấy source mới và build lại frontend/backend.
Máy hiện tại đã nạp, chỉ cần khởi động lại hai terminal theo [run-local.md](run-local.md).
Máy khác đã có nền tảng và các bộ trước, chạy trong thư mục `backend`:

```powershell
../.venv/Scripts/python.exe -m app.cli seed-supplement-content --release discovery-2026-04
../.venv/Scripts/python.exe -m app.cli verify-supplement-content --release discovery-2026-04
../.venv/Scripts/python.exe -m app.cli check-system
```

Máy đã có nền tảng nhưng chưa có đủ các bộ bổ sung, dùng vòng lặp sau thay cho
lệnh nạp riêng một bộ; có thể chạy lại với các bộ đã nạp:

```powershell
$contentReleases = @('applied-2026-01', 'explorers-2026-01', 'review-2026-02', 'daily-2026-03', 'discovery-2026-04')
foreach ($contentRelease in $contentReleases) {
  ../.venv/Scripts/python.exe -m app.cli seed-supplement-content --release $contentRelease
  if ($LASTEXITCODE -ne 0) { throw 'Không nạp được bộ học liệu; dừng để kiểm tra' }
  ../.venv/Scripts/python.exe -m app.cli verify-supplement-content --release $contentRelease
  if ($LASTEXITCODE -ne 0) { throw 'Kiểm chứng học liệu chưa đạt; dừng để kiểm tra' }
}
```

VPS dùng hàm `dc` trong [hướng dẫn deploy](deploy-vps.md):

```bash
dc run --rm -T --no-deps backend python -m app.cli seed-supplement-content --release discovery-2026-04
dc run --rm -T --no-deps backend python -m app.cli verify-supplement-content --release discovery-2026-04
dc up -d backend frontend caddy
```

Đây là seed cộng thêm, chạy lặp không tạo bản câu hỏi mới hoặc sửa bài đã xuất
bản. Không seed lại tài khoản, reset mật khẩu hay đổi cấu hình môi trường local.
Máy mới hoàn toàn cần import schema/migrate, nạp nền tảng và các bộ trước theo
hướng dẫn triển khai. CI đã bổ sung bộ mới vào bước chuẩn bị học liệu.

Chi tiết kiểm chứng ở [biên bản chất lượng 04/11](audits/discovery-quality-2026-11-04.md).
