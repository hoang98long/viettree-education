import Link from "next/link";
export default function NotFound() {
  return (
    <main id="main" className="standalone">
      <h1>404 · Chưa tìm thấy trang</h1>
      <p>Mình cùng trở về để tiếp tục khám phá nhé.</p>
      <Link className="button" href="/">
        Về trang chủ
      </Link>
    </main>
  );
}
