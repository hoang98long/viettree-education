'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Mật khẩu không khớp');
      return;
    }

    setLoading(true);

    try {
      const res = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: fullName,
          email,
          password,
          role: 'student',
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Đăng ký thất bại');
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
        <h1>Đăng ký</h1>
        <p className="subtitle">Bắt đầu hành trình học tập của bạn!</p>

        {error && <div className="errorBox">{error}</div>}

        <form onSubmit={handleRegister}>
          <div className="formGroup">
            <label htmlFor="fullName">Họ và tên</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Nguyễn Văn A"
              required
              minLength={2}
            />
          </div>

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
              minLength={8}
            />
          </div>

          <div className="formGroup">
            <label htmlFor="confirmPassword">Xác nhận mật khẩu</label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              required
              minLength={8}
            />
          </div>

          <button type="submit" className="primaryButton" disabled={loading}>
            {loading ? 'Đang đăng ký...' : 'Đăng ký'}
          </button>
        </form>

        <p className="linkText">
          Đã có tài khoản? <Link href="/login">Đăng nhập</Link>
        </p>
      </div>
    </main>
  );
}
