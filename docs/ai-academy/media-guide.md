# Hướng dẫn media

1702 SVG được tạo bằng code: 8 trạng thái Mầm AI, 55 bìa chủ đề, 251 hero,
1292 minh họa nội dung/thẻ theo bài, 72 thẻ chung (24 đối tượng × 3 biến thể), 12 huy hiệu,
12 asset UI. Không gọi dịch vụ trả phí. Phong cách vector pastel, hình dễ đọc,
không dùng nhân vật có bản quyền hoặc ảnh nhận dạng học sinh.

File thật: `backend/app/academy/assets`; danh mục/mapping/hash/alt:
`backend/app/academy/data/media-manifest.json`. Mỗi bài tham chiếu cover, hero,
3 support và các thẻ tương ứng từng ví dụ. Ảnh cũ được giữ nguyên để học sinh
đang học một phiên bản cũ tiếp tục được. Phân số 3/8 được vẽ đúng, bài phép nhân có nhóm/chấm để kiểm
đếm; các tranh bối cảnh khác có thể là minh họa ký hiệu, không thay dữ kiện đề.

```powershell
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
```

Kiểm tra XML, file tồn tại, alt, hash, giới hạn 150 KB, hash trùng và mapping.
Manifest là nguồn chuẩn; không đổi file đã published dưới cùng code/hash.
Muốn thay tranh: thêm asset code mới, duyệt, tạo phiên bản bài mới.

## Upload và kiểm duyệt

Admin/teacher editor: Thư viện hình → chọn PNG/JPEG/WebP/AVIF ≤512 KB → nhập
alt, nguồn, giấy phép → upload. Backend kiểm byte ảnh/Pillow, giới hạn 8 triệu
pixel, vẽ lại pixel để bỏ metadata, resize 1280/768/256 và lưu WebP (PNG khi
codec không có). UUID object key, thư mục riêng ngoài public. SVG tùy ý và file
giả ảnh bị từ chối. Có hook `UPLOAD_SCANNER` cho hạ tầng antivirus; mặc định
chưa cấu hình scanner ngoài, không coi Pillow là antivirus.

Reviewer/admin xem và duyệt trước khi dùng. Không thu hồi media đang thuộc bài
published: ẩn/thay bài trước; khóa row tránh race với xuất bản. Ảnh chưa duyệt
chỉ staff hợp lệ xem được; học sinh chỉ xem ảnh approved sau auth.

Bundled SVG dùng một file vector cho 3 vai trò variant, không giả tạo ảnh raster.
Raster upload có 3 file resize thật; component dùng thumbnail trên thẻ và ảnh
responsive trong bài. Alt tại vị trí học giúp giải thích nội dung chứ không chỉ
ghi tên file. Không chỉ dùng màu để truyền đạt đáp án.

## Sinh hình

Tạo SVG: robot/poster/comic → queued → chạy mẫu nội bộ → review → approved.
File thực được tạo và đưa vào thư viện; không gắn nhãn đây là model sinh ảnh.
`image_generation_enabled` không thể bật trước khi có adapter raster được duyệt.
[image-generation-prompts.json](image-generation-prompts.json) chứa brief từng
asset để họa sĩ hoặc pipeline có giấy phép sử dụng sau này; không tự thực thi.
Quyền sử dụng SVG bundled ghi trong manifest: CC BY 4.0, VietTree Education.
