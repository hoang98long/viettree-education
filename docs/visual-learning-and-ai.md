# Học bằng hình và AI Academy lớp 1–5

Cập nhật 13/10/2026. Mục tiêu: trẻ nhìn tranh, thử một việc nhỏ và tự kiểm tra;
không phải đọc một màn hình dài hay biết nhập yêu cầu vào công cụ AI.

## Thay đổi trong ứng dụng

- Toán, Tiếng Việt, Tiếng Anh: mở từng phần bằng tiêu đề; đọc từng đoạn bằng
  **Đọc tiếp**, hoặc **Xem cả phần**. Bài đọc và dòng thơ gốc được giữ đầy đủ.
- Có 46 tranh từ vựng/truyện: con vật, trái cây, đồ dùng học tập, phương tiện,
  thời tiết, thức ăn, màu sắc và hình học. 30 tranh bổ sung sau lượt rà soát giao diện.
  Chỉ chọn tranh khi từ xuất hiện trong bài; không hiểu nhầm “cá” trong “các”.
- Tranh đi theo đoạn đang đọc; chuyển sang nội dung khác bắt đầu lại đoạn đầu.
  Thẻ từ, lựa chọn trắc nghiệm và mục sắp xếp có tranh khi nhãn cụ thể phù hợp.
  Giữ nguyên chữ, tên lựa chọn cho trình đọc màn hình và giá trị đáp án gửi backend.
  Không đoán tranh từ câu phủ định, câu dài, phép tính hoặc số lượng khác một vật.
- Minh họa phép cộng nhỏ bằng hai nhóm chấm, phân số bằng các phần bằng nhau,
  số có nhiều chữ số bằng bảng các hàng. Không suy diễn phép tính thập phân thành số nguyên.
- AI: một thẻ hình hoặc một câu checkpoint mỗi màn hình; dùng nút chạm/radio,
  **Thẻ tiếp**, **Kiểm tra lựa chọn**, rồi **Tiếp theo**. Không cần kéo thả hoặc gõ chữ.
- **Em cần gợi ý** mở gợi ý đã biên soạn; mức 1 Free, mức 2–3 VIP. Không gọi model.
  Menu công cụ, thẻ bổ sung và phần đọc dài thu gọn; lựa chọn có thể đổi và thử lại.
- Giữ cỡ chữ theo thiết bị, nút tối thiểu 48 px và hỗ trợ bàn phím.
- Hành trình AI có biểu tượng từng bước, đánh dấu bước hiện tại và bước đã xong;
  khi quay lại bước trước, gợi ý của bước cũ được đóng để tránh nhầm nội dung.

Tranh ba môn nằm trong `frontend/public/learning`; 30 tranh mở rộng được tạo bằng
SVG nguyên bản. Tạo lại chúng bằng `node scripts/generate-learning-pictures.mjs`
trong thư mục `frontend`. Không thay đổi thư viện ảnh AI có gắn lịch sử phiên bản.

## Đối chiếu nguồn quốc tế

Đã đọc mô tả và mục tiêu công khai; các gói giáo án cần đăng nhập không được
dùng làm nội dung sao chép. Học liệu và SVG VietTree được viết/vẽ mới. Đây là
thiết kế tham khảo, không phải chứng nhận hoặc bản dịch chính thức của tổ chức nào.

| Nguồn | Điều đối chiếu | Cách áp dụng |
| --- | --- | --- |
| [Day of AI: Grade 1 – Learning from Patterns](https://dayofai.org/units/grade-1-learning-from-patterns) | Lứa 6–7, học qua ví dụ, quy luật và dự đoán; con người cung cấp thông tin | Lớp 1 xem hai thẻ, tìm điểm giống/khác, phát hiện máy có thể nhầm |
| [Day of AI: Grade 2 – Data All Around Us](https://dayofai.org/units/grade-2-data-all-around-us) | Lứa 7–8, thu thập/sắp xếp dữ liệu, ví dụ và sáng tạo | Lớp 2 xếp bộ sưu tập, sửa nhãn, thử tranh mới và kể ba sự kiện |
| [AI4K12: Grade Band Progression Charts](https://ai4k12.org/gradeband-progression-charts/) | Khung dự thảo K–2 và 3–5, năm ý lớn: cảm nhận, biểu diễn/lập luận, học, tương tác và tác động xã hội | Chia mức theo khối; nối quan sát, nhóm dữ liệu, lời nhắc rõ, kiểm chứng và an toàn |
| [Raspberry Pi Foundation: Discovering AI (8–12)](https://experience-ai.org/en/lessons/36) | Dữ liệu, quy luật, dự đoán, nhiệm vụ và câu kiểm tra cuối bài | Lớp 3–5 tập nhận đầu vào/đầu ra, kiểm tra nhãn/dự đoán và giải thích giới hạn |

Các mô-đun Experience AI 11–14 không được đưa nguyên mức độ vào lớp 1–2.
Chương trình trong app hiện là lý thuyết, hoạt động theo quy tắc và dữ liệu mẫu;
không huấn luyện mô hình hay gửi dữ liệu trẻ ra dịch vụ ngoài.

## Quy mô và mức theo khối

| Khối | Chủ đề / bài | Free / VIP baseline | Thời lượng gợi ý | Mức học |
| --- | --- | --- | --- | --- |
| 1 | 9 / 36 | 3 / 33 | 10 phút/bài | Hai thẻ, tranh và câu ngắn; người lớn hỗ trợ đọc |
| 2 | 9 / 36 | 3 / 33 | 10 phút/bài | Nhãn, phân loại, thử lại, kể theo thứ tự |
| 3 | 9 / 36 | 3 / 33 | 15 phút/bài | Quy tắc, dữ liệu, lời nhắc, tự đối chiếu |
| 4 | 9 / 36 | 3 / 33 | 15 phút/bài | Giữ 36 nội dung đã có, trình bày ngắn và nhiều tranh hơn |
| 5 | 9 / 36 | 3 / 33 | 15 phút/bài | Chất lượng nhãn, nhiều tình huống, mẫu học/mẫu thử, tiêu chí và giới hạn |

Tổng **180 bài / 1260 bước / 540 câu checkpoint**. Chín nhóm: AI quanh em,
dữ liệu, giao tiếp, Toán, Tiếng Việt, Tiếng Anh, sáng tạo, an toàn, dự án.
Lớp 4 giữ phân bổ 3/3/4/4/4/4/4/4/6 bài; các khối khác có bốn bài/nhóm.
Không đổi ID ba bài mẫu cũ để giữ các tham chiếu, giao bài và tiến độ.
[Danh sách đầy đủ 180 bài](ai-academy/lessons.csv).

Lớp 5 tăng độ khó ở phép tính thập phân/phân số/tỉ lệ và cách kiểm tra dữ liệu.
Ví dụ dùng nhãn sai, mẫu có nhiều nền/tư thế, tách A1/A2 để tránh thử lại đúng
mẫu đã học, hoặc kiểm tra 4/5 là 80%. Các lớp nhỏ dùng mẫu cụ thể, không dùng
thuật ngữ kỹ thuật thay cho trải nghiệm.

## Nạp dữ liệu và bảo toàn

Không cần migration mới. Trong `backend`:

```powershell
../.venv/Scripts/python.exe -m app.cli seed-ai-academy
../.venv/Scripts/python.exe -m app.cli verify-ai-academy
```

Khởi động lại backend và frontend. Seed thêm bài/ảnh mới; baseline cũ nguyên vẹn
được xuất bản thành phiên bản tranh mới. Kiểm fingerprint, metadata, revision,
người tạo/duyệt và lịch sử phiên bản trước khi nâng cấp. Bài giáo viên sửa, nháp,
vị trí/quyền sửa riêng được giữ. Khi vị trí mới bị trùng, thêm ở vị trí trống.

Payload và ảnh của phiên bản cũ được giữ; học sinh đang học vẫn dùng phiên bản
đã bắt đầu. Bài mở mới dùng phiên bản mới. Không reset kết quả, huy hiệu, điểm,
lớp, gói hoặc mật khẩu. Tổng thư viện **1547 SVG**, gồm **1232 ảnh mới** và
315 ảnh cũ, có manifest/hash/alt; cộng thêm 46 tranh dùng trong ba môn.

Minh họa màu đỏ cho thẻ cặp/bút/táo và số lượng “Two cats” được đối chiếu với
nội dung; sửa tranh theo phiên bản mới, không ghi đè ảnh đang gắn với lịch sử.
Ảnh VIP của phiên bản đã lưu trữ vẫn kiểm tra quyền VIP, không trở thành ảnh miễn phí.

Học sinh chỉ mở lớp hiện tại hoặc lớp dưới; quyền bài VIP và gợi ý được kiểm tra
tại backend. Checkpoint không gửi đáp án/giải thích chấm vào payload trước khi làm.
Số lượng Free/VIP trên là baseline; giữ cấu hình admin đã sửa riêng.

Nhà trường nên rà soát thời lượng, độ đọc và tổ chức hoạt động với trẻ trước khi
coi đây là kế hoạch dạy chính thức; 36 bài nhỏ không tương đương 36 tiết 35–45 phút.
