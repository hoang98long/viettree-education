'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';

type Lesson = {
  id: string;
  title: string;
  description: string | null;
  lesson_number: number;
  estimated_minutes: number | null;
  difficulty: string;
};

type Exercise = { id: string; title: string | null; description: string | null; points: number };
type Course = { title: string; subject_name: string; description: string | null; grade: number };

export default function CoursePage() {
  const { courseId } = useParams<{ courseId: string }>();
  const router = useRouter();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [exercises, setExercises] = useState<Record<string, Exercise[]>>({});
  const [course, setCourse] = useState<Course | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      router.replace('/login');
      return;
    }

    Promise.all([
      fetch(`/api/v1/catalog/courses/${courseId}`).then((response) => {
        if (!response.ok) throw new Error('Không thể tải khóa học');
        return response.json();
      }),
      fetch(`/api/v1/catalog/courses/${courseId}/lessons`).then((response) => {
        if (!response.ok) throw new Error('Không thể tải bài học');
        return response.json();
      }),
    ])
      .then(async ([coursePayload, lessonPayload]: [Course, Lesson[]]) => {
        setCourse(coursePayload);
        setLessons(lessonPayload);
        const entries = await Promise.all(lessonPayload.map(async (lesson) => {
          const response = await fetch(`/api/v1/exercises?lesson_id=${lesson.id}`);
          const lessonExercises: Exercise[] = response.ok ? await response.json() : [];
          return [lesson.id, lessonExercises] as const;
        }));
        setExercises(Object.fromEntries(entries));
      })
      .catch((requestError) => setError((requestError as Error).message));
  }, [courseId, router]);

  return (
    <main className="learningPage">
      <header className="learningHeader compact">
        <div>
          <Link className="backLink" href="/student/subjects">← Môn học</Link>
          <p className="brand">🌳 VietTree</p>
          <h1>{course?.title || 'Khóa học'}</h1>
          <p className="pageIntro">{course?.description || 'Mỗi bài học có phần luyện tập để em thực hành ngay.'}</p>
        </div>
        <span className="learningIcon">{course?.subject_name === 'Tiếng Anh' ? '🌍' : course?.subject_name === 'Tiếng Việt' ? '📚' : '🔢'}</span>
      </header>

      {error && <div className="errorBox">{error}</div>}
      <section className="lessonList">
        <div className="sectionHeading">
          <div><p className="eyebrow">{course?.subject_name || 'Lộ trình học'} · Lớp {course?.grade || 1}</p><h2>Các bài học</h2></div>
          <span>{lessons.length} bài</span>
        </div>
        {lessons.length === 0 ? (
          <div className="emptyState">Khóa học chưa có bài học được phát hành.</div>
        ) : lessons.map((lesson) => (
          <article className="lessonRow" key={lesson.id}>
            <span className="lessonNumber">{lesson.lesson_number}</span>
            <div className="lessonInfo">
              <strong>{lesson.title}</strong>
              <p>{lesson.description}</p>
              <small>{lesson.estimated_minutes || 10} phút · Mức độ {lesson.difficulty}</small>
            </div>
            <div className="exerciseLinks">
              {(exercises[lesson.id] || []).map((exercise) => (
                <Link className="exerciseButton" href={`/student/exercises/${exercise.id}`} key={exercise.id}>
                  ✏️ Làm bài
                </Link>
              ))}
              {(exercises[lesson.id] || []).length === 0 && <span className="mutedText">Chưa có bài tập</span>}
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}
