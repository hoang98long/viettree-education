'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

type Subject = { id: string; code: string; name: string; description: string | null };

type Course = {
  id: string;
  subject_id: string;
  grade: number;
  title: string;
  description: string | null;
  is_published: boolean;
};

export default function SubjectsPage() {
  const router = useRouter();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.replace('/login');
      return;
    }

    const loadSubjects = async () => {
      try {
        const response = await fetch('/api/v1/catalog/subjects');
        if (!response.ok) throw new Error('Không thể tải danh sách môn học');
        const payload: Subject[] = await response.json();
        setSubjects(payload);
        if (payload[0]) setSelectedSubject(payload[0].id);
      } catch (requestError) {
        setError((requestError as Error).message);
      }
    };

    loadSubjects();
  }, [router]);

  useEffect(() => {
    if (!selectedSubject) return;
    fetch(`/api/v1/catalog/courses?subject_id=${selectedSubject}`)
      .then((response) => {
        if (!response.ok) throw new Error('Không thể tải khóa học');
        return response.json();
      })
      .then(setCourses)
      .catch((requestError) => setError((requestError as Error).message));
  }, [selectedSubject]);

  return (
    <main className="learningPage">
      <header className="learningHeader">
        <div>
          <Link className="backLink" href="/student/dashboard">← Dashboard</Link>
          <p className="brand">🌳 VietTree</p>
          <h1>Môn học của em</h1>
          <p className="pageIntro">Chọn một môn để tiếp tục học và làm bài tập.</p>
        </div>
        <span className="learningIcon">📚</span>
      </header>

      {error && <div className="errorBox">{error}</div>}

      <nav className="subjectTabs" aria-label="Môn học">
        {subjects.map((subject) => (
          <button
            className={selectedSubject === subject.id ? 'subjectTab active' : 'subjectTab'}
            key={subject.id}
            onClick={() => setSelectedSubject(subject.id)}
          >
            {subject.name}
          </button>
        ))}
      </nav>

      <section className="courseList">
        <div className="sectionHeading">
          <div>
            <p className="eyebrow">Lớp 1</p>
            <h2>Khóa học đang mở</h2>
          </div>
          <span>{courses.length} khóa học</span>
        </div>
        {courses.length === 0 ? (
          <div className="emptyState">Môn học này chưa có khóa học được phát hành.</div>
        ) : (
          courses.map((course) => (
            <Link className="courseRow" href={`/student/subjects/${course.id}`} key={course.id}>
              <span className="courseBadge">{course.title.slice(0, 1)}</span>
              <span className="courseInfo">
                <strong>{course.title}</strong>
                <small>{course.description || 'Khám phá các bài học thú vị.'}</small>
              </span>
              <span className="courseArrow">→</span>
            </Link>
          ))
        )}
      </section>
    </main>
  );
}
