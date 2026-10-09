import Link from "next/link";
export default function Forbidden() {
  return (
    <main id="main" className="standalone">
      <h1>403 · Chưa có quyền truy cập</h1>
      <Link className="button" href="/login">
        Đăng nhập bằng tài khoản phù hợp
      </Link>
    </main>
  );
}
