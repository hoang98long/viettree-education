'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

type DashboardResponse = {
  student_id: string | null;
  full_name: string;
  total_xp: number;
  stars: number;
  streak_days: number;
  level: number;
  next_goal: string;
  continue_lesson: string;
  subjects: string[];
};

const defaultSubjectCards = [
  { icon: '🔢', name: 'Toán', color: 'orange', progress: 68, lesson: 'Phép cộng trong phạm vi 10' },
  { icon: '📚', name: 'Tiếng Việt', color: 'purple', progress: 42, lesson: 'Vần an, ang' },
  { icon: '🌍', name: 'Tiếng Anh', color: 'blue', progress: 25, lesson: 'My family' },
];

export default function StudentDashboard() {
  const router = useRouter();
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.replace('/login');
      return;
    }

    const loadDashboard = async () => {
      try {
        const res = await fetch('/api/v1/students/me/dashboard', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          if (res.status === 401) {
            localStorage.removeItem('token');
            router.replace('/login');
            return;
          }
          throw new Error('Không thể tải dữ liệu học tập');
        }

        const payload = await res.json();
        setData(payload);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [router]);

  if (loading) {
    return (
      <main className="dashboard" style={{ display: 'grid', placeItems: 'center', minHeight: '100vh' }}>
        <p>Đang tải dashboard...</p>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="dashboard" style={{ display: 'grid', placeItems: 'center', minHeight: '100vh' }}>
        <div>
          <p className="brand">🌳 VietTree</p>
          <p>{error || 'Không thể tải dashboard.'}</p>
        </div>
      </main>
    );
  }

  const subjectCards = defaultSubjectCards.map((subject) => ({
    ...subject,
    name: data.subjects[defaultSubjectCards.findIndex((item) => item.name === subject.name)] || subject.name,
  }));

  return (
    <main className="dashboard">
      <header>
        <p className="brand">🌳 VietTree</p>
        <div className="stats">
          <span>⚡ {data.total_xp} XP</span>
          <span>⭐ {data.stars}</span>
          <span>🔥 {data.streak_days} ngày</span>
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="eyebrow">Chào buổi sáng, {data.full_name.split(' ').slice(-1)[0]}! 👋</p>
          <h1>Hôm nay mình cùng học nhé!</h1>
          <p>Em đã học rất chăm chỉ rồi đó.</p>
        </div>
        <div className="goal">
          <span>🎯</span>
          <div>
            <b>Mục tiêu hôm nay</b>
            <small>12 / 20 phút</small>
          </div>
          <strong>{Math.min(100, Math.round((data.total_xp / 150) * 100))}%</strong>
        </div>
      </section>

      <section>
        <h2>Học tiếp</h2>
        <article className="continueCard">
          <span>🔢</span>
          <div>
            <p>Toán lớp 1</p>
            <h3>{data.continue_lesson}</h3>
            <small>{data.next_goal}</small>
          </div>
          <button>Tiếp tục →</button>
        </article>
      </section>

      <section>
        <h2>Môn học của em</h2>
        <Link className="learningLink" href="/student/subjects">Xem tất cả môn học →</Link>
        <div className="subjectGrid">
          {subjectCards.map((subject) => (
            <article key={subject.name} className={`subjectCard ${subject.color}`}>
              <span>{subject.icon}</span>
              <h3>{subject.name}</h3>
              <p>{subject.lesson}</p>
              <div className="progress">
                <i style={{ width: `${subject.progress}%` }} />
              </div>
              <small>{subject.progress}% hoàn thành</small>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2>Thành tích mới nhất</h2>
        <div className="badges">
          <span>🏅 {data.level >= 2 ? 'Nhà toán học nhí' : 'Bắt đầu hành trình'}</span>
          <span>🌟 Siêu chăm chỉ</span>
          <span>📖 Yêu đọc sách</span>
        </div>
      </section>
    </main>
  );
}
