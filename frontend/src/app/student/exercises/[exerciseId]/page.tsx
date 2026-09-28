'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';

type Option = { id: string; option_text: string; display_order: number };
type Question = { id: string; question_type: string; question_text: string; hint: string | null; points: number; options: Option[] };
type Exercise = { id: string; lesson_id: string; title: string | null; description: string | null; questions: Question[] };
type Result = { score: number; max_score: number; correct_count: number; total_questions: number };

export default function ExercisePage() {
  const { exerciseId } = useParams<{ exerciseId: string }>();
  const router = useRouter();
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      router.replace('/login');
      return;
    }
    fetch(`/api/v1/exercises/${exerciseId}`)
      .then((response) => {
        if (!response.ok) throw new Error('Không thể tải bài tập');
        return response.json();
      })
      .then(setExercise)
      .catch((requestError) => setError((requestError as Error).message))
      .finally(() => setLoading(false));
  }, [exerciseId, router]);

  const submit = async () => {
    if (!exercise) return;
    setSubmitting(true);
    setError('');
    try {
      const response = await fetch(`/api/v1/exercises/${exercise.id}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          answers: exercise.questions.map((question) => ({
            question_id: question.id,
            selected_option_ids: answers[question.id] ? [answers[question.id]] : [],
          })),
        }),
      });
      if (!response.ok) throw new Error('Không thể nộp bài');
      setResult(await response.json());
    } catch (requestError) {
      setError((requestError as Error).message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <main className="learningPage"><p>Đang tải bài tập...</p></main>;
  if (!exercise) return <main className="learningPage"><div className="errorBox">{error || 'Không tìm thấy bài tập.'}</div></main>;

  return (
    <main className="learningPage exercisePage">
      <header className="learningHeader compact">
        <div>
          <Link className="backLink" href="/student/subjects">← Môn học</Link>
          <p className="brand">🌳 VietTree</p>
          <h1>{exercise.title}</h1>
          <p className="pageIntro">{exercise.description}</p>
        </div>
        <span className="learningIcon">✏️</span>
      </header>

      {error && <div className="errorBox">{error}</div>}
      {result ? (
        <section className="resultPanel">
          <span className="resultEmoji">🎉</span>
          <p className="eyebrow">Hoàn thành rồi!</p>
          <h2>{result.score} / {result.max_score} điểm</h2>
          <p>Em trả lời đúng {result.correct_count} trên {result.total_questions} câu.</p>
          <button onClick={() => { setResult(null); setAnswers({}); }}>Làm lại</button>
          <Link className="secondaryButton" href="/student/subjects">Chọn bài khác</Link>
        </section>
      ) : (
        <section className="questionList">
          {exercise.questions.map((question, index) => (
            <article className="questionCard" key={question.id}>
              <div className="questionMeta"><span>Câu {index + 1}</span><small>{question.points} điểm</small></div>
              <h2>{question.question_text}</h2>
              <div className="optionGrid">
                {question.options.map((option) => (
                  <label className={answers[question.id] === option.id ? 'optionChoice selected' : 'optionChoice'} key={option.id}>
                    <input
                      type="radio"
                      name={question.id}
                      value={option.id}
                      checked={answers[question.id] === option.id}
                      onChange={() => setAnswers((current) => ({ ...current, [question.id]: option.id }))}
                    />
                    <span>{option.option_text}</span>
                  </label>
                ))}
              </div>
              {question.hint && <small className="hintText">Gợi ý: {question.hint}</small>}
            </article>
          ))}
          <button className="submitExercise" disabled={submitting} onClick={submit}>
            {submitting ? 'Đang chấm bài...' : 'Nộp bài và xem kết quả'}
          </button>
        </section>
      )}
    </main>
  );
}
