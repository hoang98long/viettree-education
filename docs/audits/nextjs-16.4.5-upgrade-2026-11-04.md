# Nâng Next.js 16.4.0 → 16.4.5 — 04/11/2026

Đã cài Next.js **16.4.5** và ghim chính xác trong `frontend/package.json`.
Lockfile cập nhật `@next/env` và tám biến thể SWC Windows/macOS/Linux lên
16.4.5; không đổi phiên bản React hoặc các dependency khác. `npm ls` hợp lệ.

Đây là bản sửa bảo mật, theo [ghi chú phát hành chính thức](https://github.com/vercel/next.js/releases/tag/v16.4.5).
Không cần thay đổi mã ứng dụng hoặc migration database trong dự án này.

Thông báo `No supported coding agent found` xuất hiện ở bước chuyển công việc
cho agent của CLI. Theo [hướng dẫn Next.js](https://nextjs.org/docs/app/guides/upgrading/agent-upgrade),
CLI có thể mở agent đã cài hoặc sao chép prompt. Lần này công việc đã được
thực hiện trực tiếp trong phiên Codex; không cần cài thêm agent để hoàn thành
bản nâng cấp này.

| Kiểm chứng                                            | Kết quả                                  |
| ----------------------------------------------------- | ---------------------------------------- |
| Frontend component                                    | 93 passed / 23 file                      |
| Browser desktop/mobile trên bản production standalone | 22 passed / 2,9 phút                     |
| ESLint, Prettier                                      | Đạt                                      |
| TypeScript và production build                        | Đạt                                      |
| `npm audit --omit=dev`                                | 0 lỗ hổng đã biết tại thời điểm kiểm tra |

Browser dùng `.next/standalone/server.js` của Next 16.4.5, có sao chép `public`
và `.next/static` theo cách đóng gói hiện tại. Kiểm tra đăng nhập, chuyển trang,
ảnh SVG, gợi ý Free/VIP, đọc/lưu tiến độ, làm/nộp/chấm bài và bộ lọc trên cả
năm khối. Dữ liệu ghi chỉ nằm trong `viettree-visual-browser-test`; database
học thật không thay đổi. Server test tại 3001/8001 đã dừng sau kiểm thử.

Build cuối dùng cấu hình API mặc định `http://localhost:8000`; không để địa chỉ
API test trong bản build local. File `next-env.d.ts` được trả về trạng thái
gốc sau bước build để không đưa thay đổi tự sinh vào Git.

Máy local này đã cài xong; khởi động lại frontend đang chạy để nạp phiên bản
mới. Máy khác, trong thư mục `frontend`:

```powershell
npm ci
npm run build
npm run typecheck
```

Khi deploy VPS, lấy source/lockfile mới và build lại image frontend theo
[hướng dẫn triển khai](../deploy-vps.md), sau đó khởi động lại dịch vụ frontend.
Kiểm chứng trên đây chạy production Node tại Windows local, chưa chạy Docker
Linux hoặc VPS thật trong đợt này. Kết quả audit giới hạn ở dependency production.
