import Link from 'next/link';

export default function Home() {
  return (
    <main className="landing">
      <p className="brand">🌳 VietTree</p>
      <h1>Học vui, lớn khôn mỗi ngày!</h1>
      <p>Khám phá Toán, Tiếng Việt và Tiếng Anh theo cách thật thú vị.</p>
      <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap', marginTop: '24px' }}>
        <Link className="primaryButton" href="/login" style={{ margin: 0 }}>
          Đăng nhập
        </Link>
        <Link
          className="primaryButton"
          href="/register"
          style={{ margin: 0, backgroundColor: '#666' }}
        >
          Đăng ký
        </Link>
      </div>
    </main>
  );
}
