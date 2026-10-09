# Seed lớp 4

Nguồn tự biên soạn: `backend/app/curriculum.py`; trình ghi idempotent:
`backend/app/seed.py`. Chạy từ thư mục backend: `python -m app.cli seed`.
Unique codes bắt đầu VT4-. Không seed điểm, attempts hoặc lịch sử giả.
Seed không sửa version published/assessment đã có. Xung đột nội dung làm rollback
toàn transaction và báo rõ code. Muốn cập nhật nội dung cần quy trình version mới.
`--reset-demo-passwords` là tùy chọn riêng, thu hồi phiên của hai tài khoản demo.
