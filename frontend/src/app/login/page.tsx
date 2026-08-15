'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Đăng nhập thất bại');
      }

      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      window.location.href = '/student/dashboard';
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="authPage">
      <div className="authContainer">
        <p className="brand">🌳 VietTree</p>
        <h1>Đăng nhập</h1>
        <p className="subtitle">Chào mừng bạn quay lại!</p>

        {error && <div className="errorBox">{error}</div>}

        <form onSubmit={handleLogin}>
          <div className="formGroup">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
            />
          </div>

          <div className="formGroup">
            <label htmlFor="password">Mật khẩu</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" className="primaryButton" disabled={loading}>
            {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
          </button>
        </form>

        <p className="linkText">
          Chưa có tài khoản? <Link href="/register">Đăng ký ngay</Link>
        </p>
      </div>
    </main>
  );
}
