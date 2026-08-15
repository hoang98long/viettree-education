const subjects = [
  { icon: "🔢", name: "Toán", color: "orange", progress: 68, lesson: "Phép cộng trong phạm vi 10" },
  { icon: "📚", name: "Tiếng Việt", color: "purple", progress: 42, lesson: "Vần an, ang" },
  { icon: "🌍", name: "Tiếng Anh", color: "blue", progress: 25, lesson: "My family" },
];

export default function StudentDashboard() {
  return (
    <main className="dashboard">
      <header>
        <p className="brand">🌳 VietTree</p>
        <div className="stats">
          <span>⚡ 240 XP</span>
          <span>⭐ 18</span>
          <span>🔥 4 ngày</span>
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="eyebrow">Chào buổi sáng, Minh! 👋</p>
          <h1>Hôm nay mình cùng học nhé!</h1>
          <p>Em đã học rất chăm chỉ rồi đó.</p>
        </div>
        <div className="goal">
          <span>🎯</span>
          <div>
            <b>Mục tiêu hôm nay</b>
            <small>12 / 20 phút</small>
          </div>
          <strong>60%</strong>
        </div>
      </section>

      <section>
        <h2>Học tiếp</h2>
        <article className="continueCard">
          <span>🔢</span>
          <div>
            <p>Toán lớp 1</p>
            <h3>Phép cộng trong phạm vi 10</h3>
            <small>Đã hoàn thành 3 / 5 hoạt động</small>
          </div>
          <button>Tiếp tục →</button>
        </article>
      </section>

      <section>
        <h2>Môn học của em</h2>
        <div className="subjectGrid">
          {subjects.map((subject) => (
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
          <span>🏅 Nhà toán học nhí</span>
          <span>🌟 Siêu chăm chỉ</span>
          <span>📖 Yêu đọc sách</span>
        </div>
      </section>
    </main>
  );
}
