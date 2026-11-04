# Rà soát bài cũ và hình AI Academy · 04/11/2026

Đã cập nhật **232 bài ba môn** và xuất bản **200 phiên bản AI Academy** trên
database local `viettree-education`, sau sao lưu và thử phục hồi vào database
riêng. Tổng kho vẫn là 445 bài / 2.370 câu / 385 đề ba môn và 200 bài AI;
đợt này tập trung sửa chất lượng, không tăng số bài.

## Những nội dung đã chỉnh

| Khối | Bài ba môn được chỉnh | Bài AI có phiên bản mới |
| ---- | --------------------: | ----------------------: |
| 1    |                    36 |                      40 |
| 2    |                    48 |                      40 |
| 3    |                    64 |                      40 |
| 4    |                    66 |                      40 |
| 5    |                    18 |                      40 |

Ở ba môn, bổ sung hình theo ví dụ cho 219 bài thiếu minh họa, chỉnh mục tiêu
và gợi ý ở những bài còn dùng mẫu chung. Bài đổi khối lượng/thời gian lớp 4
không còn hướng dẫn tính chu vi/diện tích; đồng hồ khớp 9 giờ 30 phút. Ví dụ
phân số có hình tô đúng phần, bài vườn 8 × 5 có đủ 40 ô. Mục tiêu tiếng Anh
về sở thích không còn nói về thời tiết. Bài viết hoa nói rõ đang kiểm tra
cách viết, giữ những lựa chọn khác nhau ở chữ hoa/chữ thường.

AI Academy chỉnh lời dẫn theo chủ đề, rút gọn mục tiêu lớp 1–2 và sửa những
hoạt động chưa khớp tên bài:

- `Cat or dog?`, `Fruit picture cards`, `School things`: đúng nhóm từ,
  đồ vật và con vật; phân biệt nhãn do máy gợi ý với vật thực trong tranh.
- Thứ tự nhặt hạt → gieo hạt, nhóm hai chấm và dãy tăng thêm 2 có dữ kiện rõ.
- Bảng cây 4/6/5 có cột tương ứng; mèo trên ghế giữ nguyên vị trí khi câu
  cần kiểm tra nói sai thành dưới ghế.
- Lớp 5: phân biệt ý chính/chi tiết, cấu trúc câu chuyện, câu dựa trên mẫu
  và câu cần kiểm tra; tránh lặp cùng bài tập phân loại cho mọi tên bài.
- Giữ trọng tâm nhận biết, dùng mẫu, kiểm tra và nhờ người lớn; phần ghi
  nguồn không bị vẽ nhầm thành ổ khóa bảo mật.

138 bài AI dùng bộ hình mới, với **915 SVG bổ sung**, tổng thư viện
**2.617 SVG**. Giữ nguyên byte của 1.702 hình cũ phục vụ lịch sử. Hình mới
thể hiện nhóm vật, số lượng, âm thanh, đồ dùng, phân số, phần trăm và biểu đồ;
các khái niệm trừu tượng vẫn dùng biểu tượng hỗ trợ. Đã sửa lỗi bộ vẽ đọc
phép cộng phân số như phép cộng số nguyên. Không tạo thêm chấm trang trí
bên trong hình dùng để đếm.

## Căn cứ biên tập AI

Tham khảo [khung theo nhóm tuổi của AI4K12](https://ai4k12.org/gradeband-progression-charts/)
và [ưu tiên học AI của CSTA](https://csteachers.org/ai-priorities/): lớp nhỏ
quan sát và phân loại ví dụ cụ thể, lớp lớn giải thích và kiểm tra dữ liệu.
Tham khảo cách dùng hoạt động về dữ liệu ở
[Code.org K–5](https://studio.code.org/courses/k5-ai-data-2024/units/1?viewAs=Instructor).
Ngữ liệu và hình được biên soạn riêng; không phải chương trình được các tổ
chức này chứng nhận. `AI_TRAINING_ONLY=true` tiếp tục áp dụng.

## Bảo toàn dữ liệu

Lệnh chỉnh bài thường chỉ áp dụng khi nội dung khớp chính xác bản nguồn đã
kiểm chứng, tiêu đề không đổi và không có bản nháp giáo viên. Lưu toàn bộ
nội dung trước/sau trong nhật ký `authoring.lesson.editorial_review`, xem
tại lịch sử biên soạn bài. Không sửa câu hỏi, đáp án, đề, điểm hay quyền Free/VIP.

Bài AI xuất bản phiên bản mới và lưu bản trước. Học sinh đã bắt đầu vẫn học
phiên bản đã ghim; học sinh bắt đầu lần đầu nhận bản mới. Không reset tiến
độ để ép đổi phiên bản. `AI4-12` có một bản cũ tùy chỉnh: chỉ thay tham chiếu
hình, giữ nguyên chữ, thời lượng 35 phút và cấu hình riêng. Ba bài AI lớp 3
giữ vị trí/chủ đề lịch sử. Nội dung khác do giáo viên sửa hoặc đang có nháp
được bỏ qua. Chạy lại các lệnh không tạo thêm phiên bản của cùng đợt.

Biên bản [cập nhật local](audits/editorial-local-2026-11-04.json) đối chiếu
82 bảng: 24.173 hàng cũ giữ nguyên hoàn toàn, chỉ các trường biên tập được
phép thay đổi ở bài học; tài khoản, mật khẩu, gói, phiên và lịch sử học giữ nguyên.
Backup nằm trong `.tools/backups`, đường dẫn và SHA-256 trong biên bản.

## Cập nhật máy khác hoặc VPS

Backup DB và private media trước; triển khai cả code lẫn SVG/manifest cùng
release. Không cần migration mới ngoài head `0012_lesson_bookmarks`. Nạp
các bộ bài nền và bổ sung cần dùng trước khi chạy rà soát.

Từ thư mục `backend`, xem trước bằng:

```bash
python -m app.cli review-learning-content
```

Kiểm tra số `eligible`, `customized`, `missing`; áp dụng rồi kiểm chứng:

```bash
python -m app.cli review-learning-content --apply
python -m app.cli seed-ai-academy
python -m app.cli verify-ai-academy
python -m app.cli review-learning-content
python -m app.cli check-release
```

PowerShell local dùng `../.venv/Scripts/python.exe` thay `python`. VPS dùng
wrapper `dc` của [hướng dẫn triển khai](deploy-vps.md), ví dụ
`dc run --rm -T --no-deps backend python -m app.cli review-learning-content --apply`.
Có thể giới hạn bài ba môn bằng `--grades 1 2`; seed AI chạy cả năm khối.
Không cần tạo lại tài khoản hoặc đổi `.env`.

Trên máy local này đã áp dụng xong. Khởi động lại backend và frontend rồi
tải lại trang. Xem [biên bản kiểm thử và giới hạn](audits/editorial-quality-2026-11-04.md).
