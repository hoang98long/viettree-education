# Biên soạn bài học, minh họa và gợi ý học tập

## Admin

Vào **Quản lý bài học** (`/admin/lessons`). Lọc lớp, môn, trạng thái hoặc tìm theo
tên/mã. Bộ lọc **Có nháp cần xử lý** gom bài đang soạn và bài đã duyệt chờ xuất bản.
Trong **Chương trình**, liên kết **Biên soạn** mở trực tiếp từng bài.

1. Bấm **Tạo bài học**, chọn môn/chủ đề/kỹ năng trong lớp đã có chương trình.
   Nhập mã, tên, thời lượng dự kiến, thứ tự, Free/VIP và mức nội dung.
2. Soạn 3–12 phần; cần ít nhất một ví dụ. Thêm mục tiêu, tối đa năm gợi ý và ba
   câu hỏi tự suy ngẫm. Các ô nhập là văn bản thuần, không nhận HTML hoặc script.
3. Chọn minh họa phân số, luống rau, hành trình đọc hoặc đồng hồ; nhập số liệu và
   chú thích phù hợp. Không cần tải ảnh lên hoặc kết nối dịch vụ ngoài.
4. Bấm **Xem trước bài học** để đọc và thử mở gợi ý như học sinh, rồi **Lưu nháp
   bài học**. Xem trước không ghi tiến độ hoặc điểm.
5. Nhập lý do, **Duyệt bài học**, rồi **Xuất bản bài học**. Sửa sau duyệt cần lưu
   và duyệt lại. Chỉ bản được xuất bản hiển thị cho học sinh.

Mã, lớp, môn và chủ đề cố định sau khi tạo. Khi cần một bài thuộc chủ đề khác,
tạo bài mới. Admin gắn đề đã xuất bản vào bài qua trình ghép đề hiện có; trình
biên soạn bài học không tự tạo đề hoặc câu hỏi.

Mỗi thao tác có revision và audit. Hai người cùng sửa: chỉ một người lưu được,
người kia nhận 409 để tải lại; không ghi đè âm thầm. Nếu bài hoặc quyền nội dung
được đổi ở nơi khác, bản nháp cũ không được duyệt/xuất bản. **Tạo nháp từ bản hiện
tại** có xác nhận bỏ nháp cũ; nhập lý do trước khi thực hiện. Giữ bản nháp tách
riêng giúp học sinh tiếp tục đọc bài hiện tại trong lúc admin sửa.

Lịch sử gần nhất hiển thị 20 thao tác, người thực hiện và lý do. Audit giữ nội
dung trước/sau; chưa có nút khôi phục một phiên bản lịch sử hoặc xuất bản tự động.

## Học sinh

Bài học hiện có được bổ sung mục tiêu, mục lục, minh họa và ba gợi ý theo chủ đề.
Các gợi ý là nội dung giảng dạy, không được dùng làm số liệu năng lực. Khi admin
biên soạn và xuất bản hướng dẫn riêng, nội dung riêng thay thế gợi ý mặc định.

- Mục lục giúp chuyển tới phần cần đọc.
- Minh họa có chú thích và tên truy cập cho công cụ hỗ trợ đọc; hiển thị co giãn
  trên điện thoại. Phân số có các phần bằng nhau; luống rau ghi ô 1 m² và chu vi;
  đồng hồ phản ánh giờ/phút admin chọn.
- **Mở gợi ý 1/2/3** lần lượt hiển thị hướng dẫn; không trừ điểm hoặc đánh dấu
  bài đã hoàn thành.
- **Em thử giải thích nhé** có câu hỏi và ô ghi ý. Ghi chú chỉ ở trang hiện tại,
  không lưu lên server, không chấm tự luận; rời trang hoặc tải lại sẽ mất ghi chú.
- **Em có thể khám phá tiếp** gợi ý tối đa ba bài published cùng chủ đề, chưa
  đánh dấu đọc xong và có quyền truy cập. Free không được gợi ý liên kết bài VIP
  đang khóa. Đây là gợi ý theo chương trình, không phải kết luận về học lực.

Phần luyện tập, kết quả và kế hoạch học tiếp tục dùng kiểm tra quyền hiện có.
Đổi bài qua liên kết đặt lại trạng thái nút hoàn thành đúng bài mới. Xuất bản
nội dung mới giữ tiến độ đọc và lịch sử cũ; chưa theo dõi xác nhận đọc theo phiên
bản nội dung. Câu hỏi và đề đã làm vẫn giữ phiên bản đáp án riêng của chúng.

## Database và cập nhật

Migration `0007_lesson_studio` chỉ thêm bảng `lesson_drafts`: JSON payload, trạng
thái, revision, fingerprint của bài/quyền hiện tại, người và thời điểm sửa/duyệt.
Không thay SQL gốc hoặc cập nhật nội dung/tài khoản/lịch sử khi migration chạy.

```powershell
# Chạy trong thư mục backend
../.venv/Scripts/python.exe -m alembic upgrade head
../.venv/Scripts/python.exe -m app.cli check-schema
```

Khởi động lại backend/frontend theo [run-local.md](run-local.md). Không cần chạy
seed để có minh họa/gợi ý cho 48 bài hiện có: backend bổ sung nội dung mặc định
sau khi kiểm tra quyền đọc, không ghi lại hàng bài học. Trên VPS cũng chạy migration
trước khi khởi động release mới, theo [deploy-vps.md](deploy-vps.md).

Seed bảo vệ bài mẫu đã thay đổi bằng báo xung đột, không ghi đè nội dung admin
đã biên soạn. Dùng migration để cập nhật hệ thống đang vận hành. Downgrade 0007
xóa các bản nháp, giữ bài đã xuất bản và audit; sao lưu trước khi downgrade.

## API

Tất cả endpoint biên soạn yêu cầu admin; request ghi yêu cầu CSRF:

| API                                                                  | Hành vi                                                       |
| -------------------------------------------------------------------- | ------------------------------------------------------------- |
| GET `/api/v1/admin/lessons?grade=4&status=pending&search=...&page=1` | Lọc/tìm kiếm, 20 bài mỗi trang                                |
| POST `/api/v1/admin/lessons`                                         | Tạo bài chưa xuất bản và bản nháp revision 1                  |
| GET `/api/v1/admin/lessons/{id}`                                     | Payload nháp hoặc bản hiện tại, revision, xung đột và lịch sử |
| PUT `/api/v1/admin/lessons/{id}`                                     | Lưu nháp với expected_revision và source_fingerprint          |
| POST `/api/v1/admin/lessons/{id}/review`                             | Duyệt đúng revision, kiểm tra lại phạm vi/nội dung            |
| POST `/api/v1/admin/lessons/{id}/publish`                            | Cập nhật bài, kỹ năng và policy trong một transaction         |
| POST `/api/v1/admin/lessons/{id}/reset`                              | Tạo nháp từ bản hiện tại, bỏ nháp cũ, tăng revision           |

GET `/api/v1/lessons/{id}` tiếp tục kiểm tra lớp/Free/VIP/publication trước khi
trả nội dung, minh họa, gợi ý hoặc bài tiếp theo. API giữ no-store.

Hướng nâng cấp tiếp: quản lý chủ đề/kỹ năng; ảnh do giáo viên duyệt và tải lên;
lưu ghi chú theo bài; khôi phục phiên bản và nhận xét của người duyệt. Các mục
này chưa được đưa vào chức năng đang hoạt động.
