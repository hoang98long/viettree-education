# Giá VIP tham khảo tại Việt Nam · 12/10/2026

Đây là khảo sát giá công khai để **đề xuất** gói tự học VietTree, không phải khảo
sát đầy đủ mọi đơn vị hoặc xác nhận checkout. Giao diện **Gói học của em** có
bảng này, nguồn tham khảo và ưu đãi đang hiệu lực. Chưa có cổng thanh toán;
giá không tự ghi nhận doanh thu hoặc cấp gói cho học sinh.

## Mốc giá quan sát

| Đơn vị / sản phẩm |                       Mốc giá công khai | Phạm vi và giới hạn                                                                                 |
| ----------------- | --------------------------------------: | --------------------------------------------------------------------------------------------------- |
| Monkey Junior     |     799.000đ / năm, giá ưu đãi hiển thị | Tự học tiếng Anh; phạm vi khác VietTree                                                             |
| Monkey Pro        |   1.299.000đ / năm, giá ưu đãi hiển thị | Combo nhiều ứng dụng tiếng Anh/Toán/Tiếng Việt                                                      |
| OLM VIP           | 199.000đ / tháng; 1.400.000đ / 12 tháng | Mốc trong hướng dẫn giá và bài ưu đãi công khai; checkout bị chặn khi khảo sát nên cần xác nhận lại |
| Edupia AI Class   |            Quảng bá từ 220.000đ / tháng | Có giáo viên quốc tế và điều kiện gói; không so sánh ngang với tự học                               |

Monkey lấy từ [bảng giá đăng ký chính thức](https://monkey.edu.vn/dang-ky-hoc).
Trang này đã được truy cập và khác mốc 699.000đ trong bài cũ năm 2024–2025;
không dùng bài cũ để khẳng định giá hiện tại. Giá thanh toán/ưu đãi bổ sung có
thể khác giá thẻ sản phẩm.

OLM lấy mốc [hướng dẫn mua VIP](https://cdp.olm.vn/tin-tuc/Huong-dan-mua-tai-khoan-VIP-545093)
và đối chiếu bài [ưu đãi hè 2026](https://cdp.olm.vn/tin-tuc/hom-nay-ngay-cuoi-khuyen-mai-chao-he-2026-683098646).
Thông tin OLM được thấy qua chỉ mục tìm kiếm; trang checkout trả 403. Chương
trình tặng thời gian tháng 6 đã kết thúc, không coi còn hiệu lực ngày khảo sát.

Edupia lấy từ [trang quảng bá chương trình 2026](https://hocbong.edupia.vn/hocbongai_2026).
Mốc “từ” có điều kiện, không nhân 12 rồi khẳng định học phí năm. VioEdu chỉ tìm
được bài học phí cũ 2019 nên không đưa vào bảng giá hiện tại; HOCMAI chưa xác
nhận được báo giá cùng gói/khối qua checkout nên không suy đoán giá.

## Đề xuất VietTree

VietTree hiện ưu tiên học liệu tự học, bài tập chấm tự động và đào tạo AI không
gọi model. Chưa bán kèm lớp live/gia sư hoặc model trả phí. Suy luận từ các mốc
trên: chọn giá thấp hơn gói combo lớn, có gói ngắn để gia đình trải nghiệm.

| Gói một học sinh | Giá tham khảo đề xuất | Giá ưu đãi giới thiệu |        Tiết kiệm |
| ---------------- | --------------------: | --------------------: | ---------------: |
| 30 ngày          |               99.000đ |           **79.000đ** |  20.000đ · 20,2% |
| 90 ngày          |              269.000đ |          **219.000đ** |  50.000đ · 18,6% |
| 365 ngày         |              899.000đ |          **699.000đ** | 200.000đ · 22,2% |

Thời hạn là ngày thực tế, không mặc định tháng lịch. Giá đề xuất không được
gắn nhãn “đã từng bán”; không tạo số lượng mua, đếm ngược hay khan hiếm giả.
Ưu đãi seed từ **12/10 đến hết 12/11/2026, giờ Việt Nam**. Sau đó server tự
trả giá tham khảo, không tiếp tục dùng giá sale hết hạn. Nhiều ưu đãi cùng gói
chọn giá hợp lệ thấp nhất, không cộng dồn phần trăm.

Quyền lợi cùng gói VIP: nội dung vận dụng ba môn lớp 1–4; gợi ý theo bước; kế
hoạch/nội dung VIP hiện có; phần lớn AI Academy, phòng thực hành dữ liệu và
sản phẩm từ mẫu. Không tuyên bố gói có gọi model/gia sư trực tiếp hoặc sẽ bảo
đảm xếp hạng. Kết quả, lịch sử và thành tích đã đạt vẫn xem được sau thu hồi.

## Quản trị và vận hành

Admin → **Giá VIP và ưu đãi** (`/admin/vip-pricing`): sửa giá đề xuất, bật/tắt
gói giá, tạo/sửa/đóng ưu đãi, chọn khoảng ngày. Nhập lý do và mật khẩu hiện tại
để xác nhận. Revision ngăn ghi đè; giá sale phải thấp hơn giá tham khảo; có
audit và khóa theo mã ưu đãi. Các giá đều là số nguyên VND, không dùng float
để lưu tiền. Public catalog không trả mật khẩu/ID quản trị.

Database: `vip_price_options`, `vip_promotions`, `vip_market_references` ở
migration 0011. Tắt gói giá chỉ ẩn lựa chọn tham khảo, **không thu hồi VIP đã cấp**.
Thu hồi/cấp/gia hạn vẫn qua chức năng quản lý gói riêng và không tự gia hạn.
Không tạo hóa đơn hay trạng thái “đã thanh toán” từ một thao tác xem bảng giá.

Trước thu tiền thật, người vận hành chốt giá và điều kiện với phụ huynh,
quy trình hỗ trợ/hoàn tiền/chứng từ. Tiếp theo đo tỷ lệ dùng/chuyển đổi và chi
phí VPS/hỗ trợ để điều chỉnh; không tăng số % sale bằng cách nâng giá gốc giả.
