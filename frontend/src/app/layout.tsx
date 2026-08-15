import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = { title: "VietTree Education", description: "Học vui mỗi ngày" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="vi"><body>{children}</body></html>;
}
