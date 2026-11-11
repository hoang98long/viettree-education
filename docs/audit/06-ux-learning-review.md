# 06 · Trải nghiệm học tập và chất lượng học liệu · 11/11/2026

Đợt này giữ nguyên phong cách, stack, mã học liệu và các phiên bản đã phát
hành. Các thay đổi tập trung vào lỗi có thể tái hiện, gợi ý đúng bài đang học,
độ rõ của thông báo và thao tác bàn phím. Không thử nghiệm với trẻ thật hoặc
đưa dữ liệu học sinh vào dịch vụ AI bên ngoài.

## Phạm vi học liệu và mức xác minh

| Hạng mục                | Kết quả và giới hạn                                                                                                                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Ba môn lớp 1–5          | 445 bài, 2.370 câu hỏi, 385 đề; gồm Free/VIP và năm bộ bổ sung. VERIFIED về inventory và schema nguồn; không đồng nghĩa mọi nội dung đã được giáo viên thẩm định.                                                                          |
| Kiểm tra Toán tự động   | 499 câu một đáp án có key dạng số literal được so bằng Fraction và cùng đơn vị dạng chữ; không phát hiện nhóm lựa chọn bằng giá trị với đáp án đúng. VERIFIED trong phạm vi parser, không bao gồm toàn bộ bài toán lời văn/quy đổi đơn vị. |
| AI Academy              | 200 bài, 1.400 bước, 600 checkpoint; 40 bài và 11 chủ đề/khối. Source có mục tiêu, độ tuổi, thời lượng, vật liệu, hướng dẫn giáo viên, hỗ trợ, mở rộng và lưu ý an toàn.                                                                   |
| Hình AI                 | 2.617 SVG, gồm hình hiện hành và hình lịch sử. Manifest kiểm đường dẫn/hash; kiểm này không chứng minh ngữ nghĩa từng tranh đều khớp bài. Các trường hợp số lượng/phân số có regression riêng.                                             |
| Gợi ý AI theo phiên bản | Đã sửa tutor lấy bản published mới nhất thay vì bản học sinh đã bắt đầu. Nay đọc version qua progress của đúng owner; giữ nguyên tiến độ và payload lịch sử. Integration/result cuối tại [07](07-test-results.md).                         |
| Chấm câu chọn AI        | Đã chuẩn hóa NFC và khoảng trắng nhất quán khi kiểm lựa chọn/chấm điểm; không bỏ dấu hoặc tự nhận đáp án ngoài bài. VERIFIED bằng unit, giữ server làm nguồn điểm.                                                                         |
| Nghe và phát âm         | PARTIALLY VERIFIED: player có giọng đọc tiếng Việt local nếu trình duyệt hỗ trợ. Kho hiện tại không phải chương trình nghe có thu âm chuẩn tiếng Anh hoặc video cho toàn bộ bài.                                                           |
| Điều kiện tiên quyết AI | 200 bài source có `prerequisites=[]`. Đã có giới hạn khối và quyền Free/VIP; chưa có đồ thị prerequisite AI đầy đủ. NOT VERIFIED về lộ trình phụ thuộc sư phạm.                                                                            |

`curriculum/quality.py` giữ kiểm schema và thêm cảnh báo số tương đương cần
giáo viên đọc lại. Không tự sửa đáp án khi hai phân số cùng giá trị: câu hỏi
về dạng tối giản có thể cố ý phân biệt cách viết. Không dùng `eval`, không
đoán dấu chấm là dấu phân cách nghìn hoặc tự quy đổi kg/g để khẳng định đúng.

Các test `test_grade4_math_review.py`, `test_grade4_extension.py` có lời giải
độc lập cho các nhóm Toán lớp 4. Kết quả thực chạy của đợt này được ghi ở 07;
không suy rộng từ test một khối sang toàn bộ lớp 1–5.

## Đọc hiểu, ngôn ngữ và hàng đợi giáo viên kiểm duyệt

Lớp 1–2 cần một yêu cầu ngắn mỗi lượt, tranh có ích và người lớn có thể đọc
cùng; source AI dự kiến 10 phút/bài, lớp 3–5 dự kiến 15 phút/bài. Thời lượng
này là metadata biên soạn, chưa được đo bằng thử nghiệm học sinh thực tế.
Không ép trẻ hoàn thành nhanh hơn hoặc lấy tốc độ đọc làm thước đo năng lực.

| Nội dung cần kiểm duyệt | Việc giáo viên cần xác nhận                                                                                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Toán, ưu tiên lớp 4     | Dữ kiện đủ, thứ tự phép tính, phần bằng nhau, đơn vị đáp số; hình và lời giải dùng cùng một toàn thể/đơn vị. Rà các bài nâng cao có nhiều cách diễn giải.                   |
| Tiếng Việt              | Dấu thanh, chính tả, câu hỏi đọc hiểu có bằng chứng trong đoạn; chỉ phân biệt hoa/thường khi đó là kỹ năng được hỏi. NFC không được làm mất dấu hoặc đổi nghĩa.             |
| Tiếng Anh               | Từ/câu đúng ngữ cảnh và tuổi; biến thể được chấp nhận phải có key phù hợp. Giọng đọc tiếng Việt hiện có không thay cho giáo viên/thu âm chuẩn đánh giá phát âm tiếng Anh.   |
| Câu trả lời mở và dự án | Dùng rubric và phản hồi của giáo viên khi chức năng có; không tuyên bố hệ thống đang tự chấm mọi bài viết tự do. Kiểm rubric đủ tiêu chí và trọng số.                       |
| Tranh khái niệm AI      | Xác nhận tranh thể hiện dữ kiện quan sát, không đổi theo chính mệnh đề sai cần kiểm tra; bỏ trang trí gây đếm nhầm và bổ sung mô tả có nghĩa cho ảnh.                       |
| Phân tầng Free/VIP      | Free vẫn có nội dung nền tảng và hỗ trợ theo policy; VIP thêm hỗ trợ/mở rộng. Không thay cách chấm công bằng hoặc dùng thông điệp làm trẻ thấy mình “kém” vì chưa nâng gói. |

Không có căn cứ từ đợt kiểm toán này để tuyên bố đã đối chiếu đầy đủ mọi bài
với chương trình GDPT 2018. Cần giáo viên lập bảng bài → yêu cầu cần đạt → bộ
sách/chương trình trường dùng → phiên bản/ngày duyệt trước dạy chính thức.
Đây là công việc sư phạm còn lại, không được tự đánh dấu PASS từ schema.

Source legacy và các bản patch biên tập được giữ để bảo toàn lịch sử. Đối
với database mới, cần kiểm bước cập nhật editorial thay vì suy ra rằng seed
nguồn mặc nhiên đã áp dụng mọi patch. Xem AUD-13 trong
[risk register](02-risk-register.md) và quy trình ở [08](08-changelog-and-rollback.md).
Không chạy seed sửa dữ liệu thật trong đợt kiểm toán.

## AI Academy: khung tham khảo và tiến trình đề xuất

UNESCO mô tả 12 năng lực trong bốn chiều: tư duy lấy con người làm trung tâm,
đạo đức, kỹ thuật/ứng dụng và thiết kế hệ thống; tiến trình Understand →
Apply → Create. Đây là tài liệu để người biên soạn chọn mục tiêu phù hợp,
không phải yêu cầu trẻ lớp 1 phải học toàn bộ khung.
[Nguồn UNESCO](https://www.unesco.org/en/articles/ai-competency-framework-students).

UNICEF Guidance on AI and Children v3.0 đưa ra 10 yêu cầu, bao gồm an toàn,
quyền riêng tư, công bằng, minh bạch, hòa nhập và lợi ích của trẻ. Áp dụng
vào sản phẩm này bằng dữ liệu giả, giải thích mô phỏng, quyền truy cập theo
vai trò và nhờ người lớn khi gặp nội dung không phù hợp; không coi checklist
là chứng nhận đã đáp ứng đầy đủ quyền trẻ em.
[Nguồn UNICEF](https://www.unicef.org/innocenti/reports/policy-guidance-ai-children).

Bảng dưới là **đề xuất biên soạn của dự án cho sprint sau**, không sao chép
giáo trình quốc tế, không phải tính năng khóa lộ trình đã được triển khai:

| Nhóm lớp | Tiến trình cụ thể                                                                                                                                                 | Cách trẻ thể hiện điều đã hiểu                                                                                             |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1–2      | Quan sát máy giúp việc gì → ghép tranh/từ/âm thanh mẫu → xếp hai nhóm → thấy nhãn sai → giữ thông tin riêng. Mỗi lượt bắt đầu với hai thẻ, người lớn đọc nếu cần. | Chỉ tranh, chọn hoặc sửa một nhãn, nói một câu ngắn. Checkpoint dùng ba câu dạng tranh và không yêu cầu gõ thông tin thật. |
| 3        | Mẫu và nhãn → ví dụ học khác ví dụ thử → nhóm thiếu mẫu có thể đoán sai → kiểm tra câu ngắn → mini poster/câu chuyện.                                             | Nêu chi tiết làm căn cứ, thử thêm mẫu chưa thấy, nói khi nào cần hỏi lại.                                                  |
| 4–5      | Chất lượng dữ liệu/thiên lệch → nhận dạng và ngôn ngữ qua mô phỏng → kiểm chứng số liệu/câu trả lời → quyền riêng tư/nguồn → mini project có tiêu chí và thử lại. | So hai cách làm, nêu giới hạn kết luận, ghi nguồn hỗ trợ, cải tiến sản phẩm sau góp ý.                                     |

Khung bài ưu tiên: khởi động bằng tranh → một ý ngắn → ví dụ → thao tác →
phản hồi → ba checkpoint → tổng kết một phút/thử thách tùy chọn. Source AI
đã có bảy bước/bài; cần thử với học sinh để biết bước nào vẫn quá dài hoặc
khó hiểu. Tách rõ tiến độ hoàn thành khỏi minh chứng thành thạo; không gán
nhãn cố định “học yếu” dựa trên vài lần chọn sai.

`AI_TRAINING_ONLY=true` tiếp tục là mặc định. Lab nearest-neighbour và SVG
template được mô tả là mô phỏng, không được trình bày như nhận dạng bằng mô
hình thật. Adapter mô hình còn giữ để tương thích nhưng không mở gọi mô
hình, tool hoặc dịch vụ trả phí trong đợt này.

Các nhóm prompt injection, rò thông tin, xử lý output và tiêu thụ tài nguyên
trong [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
được dùng làm gợi ý kiểm soát kỹ thuật; không thay cho kiểm duyệt sư phạm.
Xem thêm [05 · Bảo mật/quyền riêng tư](05-security-privacy-review.md).

## Những cải tiến UX đã thực hiện

| Phát hiện                                                            | Thay đổi                                                                                                                                                                                   | Mức xác minh tại phần việc UX                                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Modal chỉ có `aria-modal`, Tab/Escape/focus chưa được quản lý đầy đủ | `components/modal.tsx` dùng `<dialog>`/`showModal()`, thêm trap Tab/Shift+Tab tại ranh giới, xử lý cancel, giữ nền inert và trả focus; áp dụng modal nộp bài, câu hỏi, học sinh và policy. | VERIFIED ở 7 component tests và browser mẫu quản trị/nộp bài trên desktop/mobile; không suy ra đã kiểm mọi modal/trình duyệt. |
| Modal câu hỏi thiếu tên khi loading/lỗi                              | Đưa heading có ID ra ngoài nhánh dữ liệu, giữ accessible name ngay lúc mở.                                                                                                                 | VERIFIED về component contract và luồng mở dialog quản trị trên browser; screen reader thật chưa kiểm.                        |
| Lỗi mạng danh sách bài giao bị nói là “không tìm thấy”               | `student/assessment.tsx` hiển thị lỗi API và nút thử lại; chỉ nói missing khi request thành công nhưng không có bài.                                                                       | VERIFIED component test, gồm phân biệt error/missing; không bỏ owner check.                                                   |
| Có thể sửa tiếp trường trong khi request lưu đang chạy               | Fieldset disabled, `aria-busy`, chặn đóng bằng Escape khi busy; lỗi giữ dữ liệu vừa nhập và mở lại trường.                                                                                 | VERIFIED component test với deferred request/rejection.                                                                       |
| Chữ metadata, nút xanh, nhãn sidebar/badge khó đọc                   | `--muted` đổi từ `#6d8179` sang `#566f63`, `--green` thành `#1f704f`; chỉnh màu sidebar/badge. Contrast muted trên trắng/paper/light-green khoảng 5,46/5,14/4,89:1.                        | VERIFIED phép tính màu và axe ở trạng thái render mẫu; không chứng nhận WCAG AA toàn web.                                     |
| Tên/tài khoản dài làm hồ sơ tràn ngang trên điện thoại               | Cho nội dung tên/tài khoản xuống dòng, giữ bố cục trong viewport 320px.                                                                                                                    | VERIFIED trong browser mẫu 320/768px; chưa suy ra mọi chuỗi nhập và mọi thiết bị.                                             |

Các lựa chọn có sẵn tiếp tục được giữ: ba cỡ chữ lưu theo phone/tablet/desktop,
skip link, `lang=vi`, focus-visible, reduced-motion, nút lên/xuống thay cho
bắt buộc kéo thả, tự lưu và retry khi lỗi mạng. Có code không đồng nghĩa đã
kiểm mọi tổ hợp thiết bị/trình duyệt; trạng thái cuối xem 07 và
[09 · Acceptance](09-acceptance-checklist.md).

## Kết quả thực chạy cho UX và luồng học

| Phạm vi                       | Kết quả thực tế                                                                                   | Giới hạn                                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Frontend component            | **103 passed / 26 file**                                                                          | Kiểm logic/component trong jsdom, không thay browser hoặc screen reader.                                                  |
| `audit-accessibility.spec.ts` | **6 passed**, ba kịch bản trên desktop/mobile; 57,2 giây                                          | Axe trên trang mẫu, bố cục 320/768px, Tab/Shift+Tab, Escape và trả focus; xác nhận Escape không đóng dialog khi đang nộp. |
| Full browser baseline         | **174 passed / 5 failed / 3 skipped**, tổng 182                                                   | Giữ nguyên kết quả thất bại ban đầu; không gọi toàn bộ suite đã xanh.                                                     |
| Rerun mục tiêu sau sửa        | **12 passed** cho membership, operations, picture-choices và visual-learning, trên desktop/mobile | Chạy lại nhóm liên quan với dữ liệu giả; không thay thế một lượt full suite sau thay đổi.                                 |

Axe không phát hiện violation thuộc các nhóm tag đã chọn trên trang đăng nhập,
dashboard/thư viện/hồ sơ học sinh, AI Academy và các trang quản trị mẫu.
Đây là VERIFIED trong những trạng thái đã quét, không phải chứng nhận WCAG 2.2
AA hay bằng chứng mọi menu/form/nội dung động đều tiếp cận được. Các log
`audit-20261111-frontend-final.log`, `audit-20261111-a11y-final.log` và
`audit-20261111-browser-rerun-final.log` được tổng hợp tại
[07 · Kết quả kiểm thử](07-test-results.md).

Browser thật từng phát hiện dialog có một nút vẫn Tab ra ngoài khi chỉ dựa
vào native `showModal()`. Đã thêm xử lý ranh giới rõ ràng và xác minh lại;
không coi native dialog tự đủ để đạt yêu cầu. Lỗi thao tác kiểm tra hệ thống
được sửa bằng cách chờ đúng response do UI yêu cầu, không dùng response của
GET thứ hai để suy ra UI đã tải xong. Lượt membership lỗi từng ghi nhận proxy
HTTP500 sau khoảng 30 giây; lượt mục tiêu đã đạt nhưng không suy ra nguyên
nhân transport đã được loại bỏ trong mọi tình huống. Chi tiết còn theo dõi ở
[02 · Risk register](02-risk-register.md) và [07](07-test-results.md).

Đã xem trực tiếp hai ảnh mẫu `visual-ai-grade1-mobile.png` và
`picture-choice-desktop.png`: bố cục rõ, tranh và các lựa chọn đọc được trong
hai mẫu này. Không suy rộng việc xem hai ảnh thành duyệt toàn bộ 2.617 SVG
hoặc đánh giá mọi bài đều dễ hiểu đối với trẻ.

## Kiểm tra thủ công còn cần trước khi mở rộng sử dụng

- Mở rộng kiểm bàn phím ngoài hai luồng mẫu đã đạt: mọi modal, widget động,
  dialog lồng nhau và trường hợp element mở đã biến mất; kiểm thêm trên các
  trình duyệt/thiết bị thật được hỗ trợ.
- Screen reader thật: heading/landmark, tên dialog cả loading/error, thứ tự
  đọc câu hỏi, thông báo tự lưu/chấm/lỗi và công thức/phân số.
- Điện thoại/tablet thật, đặc biệt Safari/iOS: portrait/landscape, phóng to chữ,
  bàn phím ảo, kết nối chậm và mục tiêu chạm; bộ giả lập viewport 320/768px đã
  đạt không thay cho kiểm tra thiết bị thật.
- Kiểm tra lại alt thẻ AI: một số thẻ bổ sung ở `academy/player.tsx` vẫn dựng
  lời thay thế từ mã asset; cần mô tả cảnh có nghĩa và kiểm với người dùng.
- Chuẩn bị audio có transcript và phát lại trước khi quảng bá chương trình
  nghe tiếng Anh đầy đủ; kiểm khả năng không có giọng local.
- Thử với nhóm nhỏ có giáo viên/phụ huynh: trẻ hiểu yêu cầu mà không phải đọc
  quá nhiều, biết sửa lỗi và biết xin giúp đỡ. Không suy ra usability từ axe.

Động lực học tập giữ hướng ghi nhận tiến bộ, lời nhắc tích cực và có thể nghỉ.
AI Academy không có bảng xếp hạng công khai. Tuyên dương lớp của LMS cần tiếp
tục giới hạn đúng phạm vi, tối thiểu dữ liệu hiển thị và được nhà trường xem
xét cách dùng; không mở thành bảng thành tích trẻ em công khai hoặc gây áp lực
phải mua VIP/duy trì thời gian màn hình.

Chưa thực hiện screen reader thực, Safari/iOS thật hoặc thử nghiệm sư phạm
với trẻ. Các mục này là NOT VERIFIED cho tới khi có bằng chứng riêng, kể cả
khi automated accessibility scan và bộ test khác đều đạt.

## Đo giao diện cuối đợt

Caddy HTTPS/Linux smoke **34/34**, production-network **4/4** đạt.
Đo lab 18 navigations phát hiện CLS AI Academy **0,1608–0,2089**,
ghi AUD-24 để ổn định shell/skeleton theo kích thước nội dung. Đây không
phải field Web Vitals. LCP/TTFB và bundle có phạm vi cụ thể tại
[07](07-test-results.md) và [evidence](evidence/web-vitals-lab.json).
INP/thiết bị thật/giáo viên vẫn chưa kiểm, không tự nhận UX toàn diện.
