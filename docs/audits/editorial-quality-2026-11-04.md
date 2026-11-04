# Kiểm chứng biên tập học liệu · 04/11/2026

## Phạm vi và kết quả

Rà soát nguồn của 445 bài ba môn, 2.370 câu hỏi và 200 bài AI Academy,
gồm Free/VIP lớp 1–5. Áp dụng 232 bản chỉnh hỗ trợ bài cũ và 200 phiên bản
AI trên local. Xem [nội dung/cách cập nhật](../content-editorial-review-2026-11-04.md)
và [đối chiếu dữ liệu local](editorial-local-2026-11-04.json).
[Kiểm chứng gói triển khai và hash hình](editorial-release-2026-11-04.json)
được thực hiện sau khi đóng gói bản cuối.

| Kiểm tra                                                | Kết quả                                                |
| ------------------------------------------------------- | ------------------------------------------------------ |
| Backend ngoài nhóm integration                          | 895 passed, 9 skipped, 239 deselected                  |
| Hồi quy biên tập sau sửa guard xuất bản                 | 14 passed                                              |
| Integration biên tập và học trực quan, PostgreSQL riêng | 11 passed                                              |
| Frontend component                                      | 93 passed, 23 file                                     |
| Trình duyệt production Next.js 16.4.5                   | 20 passed, desktop/mobile                              |
| Python lint/format, frontend lint/typecheck/format      | Đạt                                                    |
| Production frontend build                               | Đạt; bản build cuối dùng API local 8000                |
| SVG                                                     | 2.617 file khớp manifest; 1.702 file cũ không đổi byte |
| Gói backend                                             | Wheel chứa catalog biên tập, baseline AI và hình SVG   |
| Cập nhật lại lần hai                                    | Không thay đổi hàng dữ liệu, không thêm phiên bản      |

Integration chạy trên bản phục hồi từ backup trước biên tập, trong transaction
rollback. Database trình duyệt riêng có 20 học sinh mới, chia năm khối, hai
gói và hai thiết bị; đã dừng server test và xóa riêng database thử nghiệm.
Không xóa hoặc reset dữ liệu trên `viettree-education`.

Trình duyệt kiểm tra mở bài ba môn và hình minh họa, gợi ý, thực hành AI,
checkpoint đạt 100%, hoàn thành bài, ảnh tải được và không tràn ngang. Mỗi
kịch bản còn gọi mở cả 40 bài của khối để kiểm quyền Free/VIP và không lộ
đáp án trong payload trước chấm: 800 lần gọi, gồm yêu cầu bị chặn theo gói.
Đã xem ảnh chụp hoạt động lớp nhỏ và phân số trên điện thoại, cùng các bảng
hình theo năm khối. Đây là mẫu kiểm tra giao diện, không phải thao tác toàn
bộ 1.400 bước qua UI.

## Các lỗi và bất hợp lý được xử lý

- Gợi ý đổi đơn vị nói nhầm chu vi/diện tích; mục tiêu sở thích nói thời tiết.
- Hình đếm có lượng không khớp mẫu hoặc thêm chấm trang trí gây đếm nhầm.
- Bài từ vựng trái cây/đồ dùng dùng nhóm con vật; bài trình tự chỉ phân loại vật.
- Bộ vẽ đọc “Ai ...?” thành AI; từ “nguồn” thành ổ khóa; âm thanh thành con chim.
- Hình lấy số trong mệnh đề cần kiểm tra thay vì mẫu quan sát; hình vị trí
  thay đổi theo chính câu sai.
- Regex phép cộng nhận một phần của phép cộng phân số như số nguyên.
- Chạy lại bản cập nhật chỉ đổi media có thể cố tạo lại cùng UUID phiên bản.
  Đã chặn phiên bản release tồn tại và bản cập nhật không tạo khác biệt.

Đã kiểm thêm lựa chọn số tương đương trong câu hỏi một đáp án, theo cùng
đơn vị: không phát hiện trường hợp đáp án đúng trùng giá trị. 12 cảnh báo
trùng khi bỏ qua hoa/thường là bài kiểm tra viết hoa có chủ ý; giữ nguyên
đáp án và làm rõ lời hướng dẫn. Không sửa lịch sử `question_versions`.

## Bảo toàn và giới hạn

Backup custom-format được kiểm `pg_restore --list`; backup trước biên tập
đã được phục hồi thật vào database riêng. Khi xuất bản local, kiểm từng hàng
trên 82 bảng trong cùng transaction: 24.173 hàng cũ giữ nguyên hoàn toàn;
chỉ `content/updated_at` của 232 bài thường, `revision/updated_at` của 200 bài
AI và trạng thái xuất bản của 200 phiên bản AI cũ thay đổi. Payload cũ giữ
nguyên; bản mới và tham chiếu media được thêm vào. Không đổi tài khoản,
mật khẩu, gói, phiên, bài làm, điểm hoặc tiến độ.

Kiểm tra cấu trúc/hash không thay cho thẩm định sư phạm từng câu. Kiểm số
tương đương chưa bao phủ mọi cách diễn đạt lời văn hoặc quy đổi đơn vị.
Một số tranh khái niệm vẫn là biểu tượng. Cần giáo viên thử bài theo độ tuổi
và ghi nhận phản hồi trong lớp trước dạy chính thức. Chín test bị bỏ qua do
thiếu Bash/Docker Compose CLI trên môi trường kiểm thử; không được tính là passed. Có cảnh báo chuyển
đổi `httpx` của Starlette, chưa làm hỏng kiểm thử hiện tại.

Không triển khai lên VPS thật hoặc đo tải mạng Việt Nam–Nhật trong đợt
biên tập này. Không đổi migration; head vẫn `0012_lesson_bookmarks`.
