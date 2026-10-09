import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "VietTree Education · Học điều hay, lớn mỗi ngày",
  description:
    "Không gian học tập và luyện tập dành cho học sinh tiểu học Việt Nam.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body>
        <a className="skip-link" href="#main">
          Đến nội dung chính
        </a>
        {children}
      </body>
    </html>
  );
}
