# Kiểm chứng AI Academy — 19/10/2026

Phạm vi: bài AI mới lớp 1–5, danh mục/học tiếp/trò chơi, quyền Free/VIP,
hiển thị điện thoại và truy vấn danh mục. PostgreSQL test tách khỏi database
người dùng. Không gọi mô hình AI.

| Kiểm tra                                           | Kết quả                                                                               |
| -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Backend không integration                          | 869 passed; 9 kiểm thử cần DB bỏ qua; 226 integration không chọn                      |
| Integration Academy/management/visual/verification | 32 passed                                                                             |
| Frontend unit                                      | 90 passed                                                                             |
| Đóng gói và kiểm tra mã                            | Next production build, typecheck, ESLint, Ruff và format đạt                          |
| Hệ thống local                                     | `check-system` đạt, head `0012_lesson_bookmarks`; không thiếu chính sách quyền/đề lỗi |
| Playwright desktop + iPhone 13                     | 20 luồng đạt: toàn bộ 10 bài mới, Free/VIP, lọc/tìm/học tiếp/trò chơi                 |
| Media/content                                      | 200 bài hợp lệ, 1702 SVG hợp lệ; không có issue trong verify                          |
| Bảo toàn                                           | 1625 ảnh cũ, 190 payload cũ giữ nguyên; local backup và so từng hàng 82 bảng          |

Đáp án hoạt động và ba checkpoint của từng bài mới được đối chiếu bộ khóa
biên tập độc lập; kiểm tra cả lựa chọn sai và các mức số thẻ. Integration gồm
Free/VIP, gợi ý 1/3, nộp lại không trùng, hoàn thành, thu hồi VIP, hình VIP và
nạp lại giữ bài published/tiến độ. Kiểm thử giao diện đi qua cả năm khối,
tìm không dấu, trạng thái rỗng, khôi phục bước thực hành và không tràn ngang.
Hai lượt lớp 1 được kiểm lại sau tinh chỉnh xem trước lớp cao hơn: bộ lọc
“Em có thể học” trả rỗng, không gợi ý học tiếp bài vượt khối.

## Tải AI Academy với 50 học sinh

50 người dùng test riêng, 25 Free / 25 VIP, chia đều năm khối. Đăng nhập tuần
tự xong mới cho 50 học sinh cùng bắt đầu chuỗi học; số đo không bao gồm login.
Mỗi em mở home/catalog, mở bài 39 hoặc 40 theo gói, làm hoạt động/checkpoint,
mở gợi ý, nộp lại cùng mã, hoàn thành và kiểm tra thành tích.

- **800/800 yêu cầu HTTP 200**, 50/50 học sinh hoàn thành.
- **p95 791,11 ms**, p99 1118,44 ms, toàn chuỗi tải 10,26 giây.
- Đối chiếu DB: mỗi em chỉ có hai lượt chấm, một lần thưởng tổng 10 điểm và
  một tiến độ hoàn thành; gửi lại không tạo thêm điểm/lượt.
- [Kết quả JSON](academy-load-50-2026-10-19.json).

Chạy trên Windows local, API HTTP trực tiếp, PostgreSQL thật. Kết quả chưa
đại diện cho VPS Nhật, Caddy/TLS hoặc mạng Việt Nam; cần đo lại sau deploy.
Không dùng số đo này để cam kết số người dùng tối đa hay SLA.

## Giới hạn

Rà soát kỹ thuật và khóa đáp án không thay thế đánh giá của giáo viên với trẻ
thật. Chưa kiểm chứng hiệu quả học tập. Docker Engine/SSH/VPS thật không nằm
trong lần kiểm thử này. Số lượng là bộ gốc, có thể cao hơn khi giáo viên tự
biên soạn; quyền CMS riêng có thể khác mặc định 25 Free / 175 VIP.
