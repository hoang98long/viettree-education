"use client";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  Clock,
  Sprout,
} from "lucide-react";
import { api, dateLabel, percent } from "@/lib/api";
import type {
  Answer,
  Assessment,
  Attempt,
  Dashboard,
  History,
  Lesson,
  LessonSummary,
  Result,
  Skill,
  Subject,
  Topic,
  User,
} from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import {
  Empty,
  ErrorState,
  Loading,
  PageTitle,
  SubjectCards,
  TreeArt,
} from "@/components/ui";
import { QuestionInput } from "@/components/question-input";

function Resource<T>({
  path,
  children,
}: {
  path: string;
  children: (data: T) => React.ReactNode;
}) {
  const { data, error, loading, retry } = useResource<T>(path);
  if (loading) return <Loading />;
  if (error || !data) return <ErrorState message={error} retry={retry} />;
  return <>{children(data)}</>;
}

function Recommendations({ items }: { items: Dashboard["recommendations"] }) {
  return (
    <div className="recommendations">
      {items.map((item, index) => (
        <Link
          href={`/student/assessments/${item.assessment_id}`}
          className="recommendation"
          key={item.assessment_id}
        >
          <span className="number-dot">{index + 1}</span>
          <div>
            <h3>{item.title}</h3>
            <p>{item.explanation}</p>
          </div>
          <ArrowRight size={20} />
        </Link>
      ))}
    </div>
  );
}

export function StudentDashboard() {
  return (
    <Resource<Dashboard> path="/students/me/dashboard">
      {(data) => {
        const completed = data.history.filter(
          (attempt) => attempt.status === "graded",
        );
        const active = data.history.find(
          (attempt) => attempt.status === "in_progress",
        );
        return (
          <>
            <div className="welcome-card">
              <div>
                <span className="eyebrow">GÓC HỌC TẬP · LỚP {data.grade}</span>
                <h1>
                  Chào {data.user.display_name}! <span>🌱</span>
                </h1>
                <p>
                  Mỗi bước nhỏ đều giúp em lớn lên.
                  <br />
                  Hôm nay mình cùng khám phá điều mới nhé.
                </p>
                <Link
                  className="button"
                  href={
                    active
                      ? `/student/attempts/${active.id}`
                      : data.continue_lesson
                        ? `/student/lessons/${data.continue_lesson.id}`
                        : `/student/grades?grade=${data.grade}`
                  }
                >
                  <BookOpen size={18} />
                  {active || data.continue_lesson
                    ? "Học tiếp"
                    : "Khám phá bài học"}
                </Link>
              </div>
              <TreeArt />
            </div>
            <div className="stats-grid">
              <div className="stat">
                <span className="stat-icon green">
                  <Check />
                </span>
                <div>
                  <strong>{completed.length}</strong>
                  <span>Bài luyện tập đã nộp</span>
                </div>
              </div>
              <div className="stat">
                <span className="stat-icon blue">
                  <BookOpen />
                </span>
                <div>
                  <strong>{data.completed_lessons}</strong>
                  <span>Bài học đã luyện tập</span>
                </div>
              </div>
              <div className="stat">
                <span className="stat-icon orange">
                  <Sprout />
                </span>
                <div>
                  <strong>{data.skills.length}</strong>
                  <span>Kỹ năng đã thử sức</span>
                </div>
              </div>
            </div>
            <div className="section-heading">
              <div>
                <span className="eyebrow">CHỌN ĐIỀU EM MUỐN HỌC</span>
                <h2>Vườn kiến thức của em</h2>
              </div>
              <Link href="/student/grades">
                Xem các lớp <ArrowRight size={17} />
              </Link>
            </div>
            <SubjectCards
              subjects={data.subjects.filter((subject) =>
                ["MATH", "VIETNAMESE", "ENGLISH"].includes(subject.code),
              )}
            />
            <div className="two-columns">
              <section className="panel">
                <div className="section-heading">
                  <h2>Nhiệm vụ hôm nay</h2>
                  <span className="pill">
                    <Sprout size={14} /> Gợi ý cho em
                  </span>
                </div>
                {data.recommendations.length ? (
                  <Recommendations items={data.recommendations} />
                ) : (
                  <Empty>
                    Em đã luyện tập nhiều hôm nay. Hãy đọc bài học hoặc nghỉ
                    ngơi một chút nhé.
                  </Empty>
                )}
                {data.assignments
                  .filter((assignment) =>
                    ["assigned", "in_progress"].includes(assignment.status),
                  )
                  .map((assignment) => (
                    <Link
                      className="list-row"
                      key={assignment.id}
                      href={`/student/assessments/${assignment.assessment_id}`}
                    >
                      {assignment.title}
                      <span className="badge">Được giao</span>
                    </Link>
                  ))}
              </section>
              <section className="panel">
                <div className="section-heading">
                  <h2>Hoạt động gần đây</h2>
                  <Link href="/student/history">Xem tất cả</Link>
                </div>
                {data.history.length ? (
                  data.history.slice(0, 4).map((attempt) => (
                    <Link
                      className="list-row"
                      href={`/student/${attempt.status === "graded" ? "results" : "attempts"}/${attempt.id}`}
                      key={attempt.id}
                    >
                      <div>
                        <strong>{attempt.title}</strong>
                        <small>{dateLabel(attempt.started_at)}</small>
                      </div>
                      <span className="badge">
                        {attempt.status === "graded"
                          ? `${attempt.total_score}/${attempt.max_score}`
                          : "Đang làm"}
                      </span>
                    </Link>
                  ))
                ) : (
                  <Empty>
                    Chưa có bài luyện tập. Chọn một môn và bắt đầu, kết quả của
                    em sẽ được lưu ở đây.
                  </Empty>
                )}
              </section>
            </div>
          </>
        );
      }}
    </Resource>
  );
}

export function Grades() {
  const search = useSearchParams();
  const initial = Number(search.get("grade") || "4");
  const [grade, setGrade] = useState(
    initial >= 1 && initial <= 5 ? initial : 4,
  );
  return (
    <>
      <PageTitle
        eyebrow="KHÁM PHÁ CHƯƠNG TRÌNH"
        title="Chọn lớp học của em"
        description="Lớp 4 đã có bài học và luyện tập. Những lớp khác đang được xây dựng."
      />
      <div className="grade-selector">
        {[1, 2, 3, 4, 5].map((value) => (
          <button
            aria-pressed={grade === value}
            className={grade === value ? "active" : ""}
            onClick={() => setGrade(value)}
            key={value}
          >
            Lớp {value}
            <small>{value === 4 ? "Học ngay" : "Sắp ra mắt"}</small>
          </button>
        ))}
      </div>
      {grade !== 4 && (
        <div className="notice">
          <Sprout />
          <div>
            <strong>Chương trình lớp {grade} đang xây dựng</strong>
            <p>
              Em có thể xem khung môn học bên dưới. Các bài học sẽ được bổ sung
              sau.
            </p>
          </div>
        </div>
      )}
      <Resource<Subject[]> key={grade} path={`/subjects?grade=${grade}`}>
        {(data) => <SubjectCards subjects={data} />}
      </Resource>
    </>
  );
}

function TopicPanel({ topic }: { topic: Topic }) {
  return (
    <article className="panel topic-panel">
      <span className="eyebrow">CHỦ ĐỀ {topic.sort_order}</span>
      <h2>{topic.title}</h2>
      <Resource<LessonSummary[]> path={`/lessons?topic_id=${topic.id}`}>
        {(lessons) =>
          lessons.length ? (
            <div>
              {lessons.map((lesson, index) => (
                <Link
                  className="list-row"
                  href={`/student/lessons/${lesson.id}`}
                  key={lesson.id}
                >
                  <span className="number-dot">{index + 1}</span>
                  <div>
                    <strong>{lesson.title}</strong>
                    <small>
                      <Clock size={13} /> {lesson.estimated_minutes} phút · Bài
                      học
                    </small>
                  </div>
                  <ArrowRight size={18} />
                </Link>
              ))}
            </div>
          ) : (
            <Empty>Bài học đang được xây dựng.</Empty>
          )
        }
      </Resource>
    </article>
  );
}

export function SubjectPage({ code }: { code: string }) {
  const query = useSearchParams();
  const grade = Number(query.get("grade") || 4);
  const name =
    (
      {
        MATH: "Toán",
        VIETNAMESE: "Tiếng Việt",
        ENGLISH: "Tiếng Anh",
      } as Record<string, string>
    )[code] || code;
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${grade} > ${name.toUpperCase()}`}
        title={`Cùng khám phá ${name}`}
        description="Đọc bài học, thử ví dụ rồi chọn bài luyện tập phù hợp."
      />
      <Resource<Topic[]>
        path={`/topics?grade=${grade}&subject_code=${encodeURIComponent(code)}`}
      >
        {(topics) =>
          topics.length ? (
            <div className="two-columns">
              {topics.map((topic) => (
                <TopicPanel key={topic.id} topic={topic} />
              ))}
            </div>
          ) : (
            <Empty>
              Chương trình lớp {grade} · {name} đang xây dựng. Em hãy quay lại
              lớp 4 để bắt đầu học nhé.
            </Empty>
          )
        }
      </Resource>
      <h2 className="section-title">Bài luyện tập</h2>
      <Resource<Assessment[]>
        path={`/assessments?grade=${grade}&subject_code=${encodeURIComponent(code)}`}
      >
        {(assessments) =>
          assessments.length ? (
            <div className="two-columns">
              {assessments.map((assessment) => (
                <Link
                  className="panel practice-card"
                  key={assessment.id}
                  href={`/student/assessments/${assessment.id}`}
                >
                  <span className="badge">{assessment.item_count} câu</span>
                  <h3>{assessment.title}</h3>
                  <p>{assessment.description}</p>
                  <span className="card-link">
                    Thử sức <ArrowRight size={17} />
                  </span>
                </Link>
              ))}
            </div>
          ) : (
            <Empty>Chưa có bài luyện tập cho lớp này.</Empty>
          )
        }
      </Resource>
    </>
  );
}

function LessonContent({ data }: { data: Lesson }) {
  useEffect(() => {
    api(`/lessons/${data.id}/visit`, { method: "POST" }).catch(() => {});
  }, [data.id]);
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${data.grade} > ${data.subject_name} > ${data.topic_title}`}
        title={data.title}
        description={`${data.estimated_minutes} phút · Đọc chậm rãi theo nhịp của em`}
      />
      <div className="lesson-blocks">
        {data.content.blocks.map((block, index) => (
          <section className={`lesson-block ${block.type}`} key={index}>
            <h2>{block.title}</h2>
            <p>{block.text}</p>
          </section>
        ))}
      </div>
      <section className="panel">
        <h2>Đến lượt em thử sức</h2>
        {data.practice.map((item) => (
          <Link
            className="list-row"
            key={item.id}
            href={`/student/assessments/${item.id}`}
          >
            {item.title}
            <ArrowRight size={18} />
          </Link>
        ))}
      </section>
    </>
  );
}
export function LessonPage({ id }: { id: string }) {
  return (
    <Resource<Lesson> path={`/lessons/${id}`}>
      {(data) => <LessonContent data={data} />}
    </Resource>
  );
}

function AssessmentIntro({ data }: { data: Assessment }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${data.grade} > ${data.subject_name} > LUYỆN TẬP`}
        title={data.title}
        description={data.description}
      />
      <section className="panel assessment-intro">
        <span className="large-icon">
          <BookOpen size={40} />
        </span>
        <h2>Sẵn sàng thử sức chưa?</h2>
        <div className="intro-meta">
          <span>{data.item_count} câu hỏi</span>
          <span>{data.max_attempts} lượt tối đa</span>
          <span>
            {data.time_limit_seconds
              ? `${Math.round(data.time_limit_seconds / 60)} phút`
              : "Không giới hạn thời gian"}
          </span>
        </div>
        <p>
          Em có thể lưu câu trả lời và quay lại. Sau khi nộp, mình cùng xem lời
          giải để hiểu bài hơn nhé.
        </p>
        {error && (
          <div className="notice error" role="alert">
            {error}
          </div>
        )}
        <button
          className="button"
          disabled={busy}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              const assignment = await api<{ id: string }>(
                `/students/me/assessments/${data.id}/assign-self`,
                { method: "POST" },
              );
              const attempt = await api<{ id: string }>("/attempts", {
                method: "POST",
                body: JSON.stringify({ assignment_id: assignment.id }),
              });
              router.push(`/student/attempts/${attempt.id}`);
            } catch (e) {
              setError((e as Error).message);
              setBusy(false);
            }
          }}
        >
          {busy ? "Đang mở bài…" : "Bắt đầu / Tiếp tục"}
          <ArrowRight size={18} />
        </button>
      </section>
    </>
  );
}
export function AssessmentPage({ id }: { id: string }) {
  return (
    <Resource<Assessment> path={`/assessments/${id}`}>
      {(data) => <AssessmentIntro data={data} />}
    </Resource>
  );
}

function Quiz({ data }: { data: Attempt }) {
  const router = useRouter();
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, Answer>>(() =>
    Object.fromEntries(
      data.items
        .filter((item) => item.answer)
        .map((item) => [item.id, item.answer!]),
    ),
  );
  const [dirty, setDirty] = useState<Set<string>>(new Set());
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [review, setReview] = useState(false);
  const [confirm, setConfirm] = useState(false);
  const item = data.items[index];
  if (data.status === "graded")
    return (
      <div className="panel">
        <h1>Bài này đã nộp</h1>
        <Link className="button" href={`/student/results/${data.id}`}>
          Xem kết quả
        </Link>
      </div>
    );
  if (!item) return <Empty>Bài luyện tập chưa có câu hỏi.</Empty>;
  async function save() {
    for (const id of dirty) {
      await api(`/attempts/${data.id}/answers/${id}`, {
        method: "PUT",
        body: JSON.stringify({ answer: answers[id] }),
      });
    }
    setDirty(new Set());
    setMessage("Đã lưu câu trả lời. Em có thể quay lại bài này.");
  }
  async function action(callback: () => void) {
    setBusy(true);
    setError("");
    try {
      await save();
      callback();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <PageTitle
        eyebrow="LUYỆN TẬP · TỪNG BƯỚC NHỎ"
        title={data.title}
        description={
          data.deadline
            ? `Hạn nộp: ${new Date(data.deadline).toLocaleString("vi-VN", { timeZone: "Asia/Bangkok" })}`
            : "Không cần vội. Đọc kỹ câu hỏi và làm theo nhịp của em."
        }
      />
      <div className="quiz-layout">
        <section className="panel quiz">
          <div className="quiz-header">
            <span>
              Câu {index + 1} / {data.items.length}
            </span>
            <span className="badge">
              {Object.keys(answers).length} câu đã trả lời
            </span>
          </div>
          <div className="progress-track">
            <span
              style={{ width: `${((index + 1) / data.items.length) * 100}%` }}
            />
          </div>
          <h2 className="question-prompt">{item.content.prompt}</h2>
          <QuestionInput
            item={item}
            answer={answers[item.id] || null}
            disabled={busy}
            onChange={(answer) => {
              setAnswers((previous) => ({ ...previous, [item.id]: answer }));
              setDirty((previous) => new Set(previous).add(item.id));
              setMessage("Chưa lưu thay đổi");
            }}
          />
          {error && (
            <div className="notice error" role="alert">
              {error}
            </div>
          )}
          <p className="save-message" role="status">
            {message ||
              "Câu trả lời sẽ được lưu khi em chuyển câu hoặc bấm Lưu bài."}
          </p>
          <div className="quiz-actions">
            <button
              className="button secondary"
              disabled={busy || index === 0}
              onClick={() => action(() => setIndex(index - 1))}
            >
              <ArrowLeft size={17} />
              Câu trước
            </button>
            <button
              className="button secondary"
              disabled={busy}
              onClick={() => action(() => {})}
            >
              Lưu bài
            </button>
            <button
              className="button"
              disabled={busy}
              onClick={() =>
                action(() =>
                  index < data.items.length - 1
                    ? setIndex(index + 1)
                    : setReview(true),
                )
              }
            >
              {index < data.items.length - 1 ? "Câu tiếp" : "Xem lại"}
              <ArrowRight size={17} />
            </button>
          </div>
        </section>
        <aside className="panel question-nav">
          <h3>Các câu hỏi</h3>
          <div>
            {data.items.map((question, number) => (
              <button
                disabled={busy}
                aria-label={`Câu ${number + 1}${answers[question.id] ? ", đã trả lời" : ", chưa trả lời"}`}
                aria-current={number === index ? "step" : undefined}
                className={`${number === index ? "current" : ""} ${answers[question.id] ? "answered" : ""}`}
                key={question.id}
                onClick={() =>
                  action(() => {
                    setIndex(number);
                    setReview(false);
                  })
                }
              >
                {number + 1}
              </button>
            ))}
          </div>
          <p>
            {data.items.length - Object.keys(answers).length} câu chưa trả lời
          </p>
          <button
            className="button secondary"
            disabled={busy}
            onClick={() => action(() => setReview(true))}
          >
            Xem lại trước khi nộp
          </button>
        </aside>
      </div>
      {review && (
        <section className="panel review">
          <h2>Kiểm tra bài của em</h2>
          <p>
            {Object.keys(answers).length}/{data.items.length} câu đã trả lời. Em
            có thể chọn số câu để kiểm tra lại.
          </p>
          <div>
            {data.items.map((question, number) => (
              <button
                className="list-row"
                disabled={busy}
                key={question.id}
                onClick={() =>
                  action(() => {
                    setIndex(number);
                    setReview(false);
                  })
                }
              >
                <span>Câu {number + 1}</span>
                <span className="badge">
                  {answers[question.id] ? "Đã trả lời" : "Chưa trả lời"}
                </span>
              </button>
            ))}
          </div>
          <button
            className="button"
            disabled={busy}
            onClick={() => setConfirm(true)}
          >
            Nộp bài
          </button>
        </section>
      )}
      {confirm && (
        <div className="modal-backdrop">
          <section
            role="dialog"
            aria-modal="true"
            aria-labelledby="submit-title"
            className="modal"
          >
            <h2 id="submit-title">Em muốn nộp bài chứ?</h2>
            <p>
              Có {data.items.length - Object.keys(answers).length} câu chưa trả
              lời. Sau khi nộp, em sẽ xem được kết quả và lời giải.
            </p>
            {error && <p role="alert">{error}</p>}
            <div className="quiz-actions">
              <button
                autoFocus
                className="button secondary"
                disabled={busy}
                onClick={() => setConfirm(false)}
              >
                Quay lại kiểm tra
              </button>
              <button
                className="button"
                disabled={busy}
                onClick={async () => {
                  setBusy(true);
                  setError("");
                  try {
                    await save();
                    await api(`/attempts/${data.id}/submit`, {
                      method: "POST",
                    });
                    router.replace(`/student/results/${data.id}`);
                  } catch (e) {
                    setError((e as Error).message);
                    setBusy(false);
                  }
                }}
              >
                {busy ? "Đang nộp…" : "Xác nhận nộp"}
              </button>
            </div>
          </section>
        </div>
      )}
    </>
  );
}
export function AttemptPage({ id }: { id: string }) {
  return (
    <Resource<Attempt> path={`/attempts/${id}`}>
      {(data) => <Quiz key={id} data={data} />}
    </Resource>
  );
}

function renderAnswer(
  answer: Answer,
  content: Result["items"][number]["content"],
) {
  if ("text" in answer) return answer.text || "Chưa trả lời";
  const ids =
    "option_id" in answer
      ? [answer.option_id]
      : "option_ids" in answer
        ? answer.option_ids
        : "ordered_ids" in answer
          ? answer.ordered_ids
          : [];
  return (
    ids
      .map(
        (id) => content.options?.find((option) => option.id === id)?.text || id,
      )
      .join(" · ") || "Chưa trả lời"
  );
}
export function ResultPage({ id }: { id: string }) {
  return (
    <Resource<Result> path={`/attempts/${id}/result`}>
      {(data) => (
        <>
          <PageTitle
            eyebrow="KẾT QUẢ LUYỆN TẬP"
            title="Mỗi lần thử là một lần tiến bộ!"
          />
          <section className="result-banner">
            <div className="score-circle">
              {data.total_score}
              <small>/ {data.max_score} điểm</small>
            </div>
            <div>
              <h2>Em đã hoàn thành bài luyện tập</h2>
              <p>
                {data.correct_count} câu đúng · {dateLabel(data.graded_at)}
              </p>
              <p>
                Đọc lời giải để hiểu điều đã làm tốt và điều mình có thể luyện
                thêm nhé.
              </p>
              <Link className="button" href="/student/progress">
                Xem cây năng lực <Sprout size={18} />
              </Link>
            </div>
          </section>
          <h2 className="section-title">Cùng xem lại từng câu</h2>
          {data.items.map((item) => (
            <details
              className="panel result-item"
              key={item.id}
              open={!item.is_correct}
            >
              <summary>
                <span
                  className={`badge ${item.is_correct ? "success" : "warm"}`}
                >
                  {item.is_correct ? "Đúng" : "Cùng ôn lại"}
                </span>
                <strong>Câu {item.position}</strong>
                <span>
                  {item.score}/{item.points} điểm
                </span>
              </summary>
              <h3 className="question-prompt">{item.content.prompt}</h3>
              <p>
                <strong>Em trả lời:</strong>{" "}
                {renderAnswer(item.student_answer, item.content)}
              </p>
              <div className="explanation">
                <strong>Lời giải</strong>
                <p>{item.explanation.text}</p>
              </div>
            </details>
          ))}
          <Link className="button" href="/student/dashboard">
            Luyện tập tiếp <ArrowRight size={18} />
          </Link>
        </>
      )}
    </Resource>
  );
}

export function HistoryPage() {
  const [subject, setSubject] = useState("");
  const [date, setDate] = useState("");
  const path = `/students/me/history?${new URLSearchParams({ ...(subject ? { subject_code: subject } : {}), ...(date ? { date } : {}) })}`;
  return (
    <>
      <PageTitle
        eyebrow="HÀNH TRÌNH CỦA EM"
        title="Lịch sử luyện tập"
        description="Bài đang làm và những lần thử sức đều được lưu ở đây."
      />
      <div className="filters">
        <label>
          Môn học
          <select value={subject} onChange={(e) => setSubject(e.target.value)}>
            <option value="">Tất cả môn</option>
            <option value="MATH">Toán</option>
            <option value="VIETNAMESE">Tiếng Việt</option>
            <option value="ENGLISH">Tiếng Anh</option>
          </select>
        </label>
        <label>
          Ngày
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
      </div>
      <Resource<History[]> key={path} path={path}>
        {(items) =>
          items.length ? (
            <section className="panel">
              {items.map((attempt) => (
                <Link
                  className="list-row"
                  key={attempt.id}
                  href={`/student/${attempt.status === "graded" ? "results" : "attempts"}/${attempt.id}`}
                >
                  <div>
                    <strong>{attempt.title}</strong>
                    <small>
                      {attempt.subject_name} · {dateLabel(attempt.started_at)}
                    </small>
                  </div>
                  <span className="badge">
                    {attempt.status === "graded"
                      ? `${attempt.total_score}/${attempt.max_score}`
                      : "Tiếp tục làm"}
                  </span>
                  <ArrowRight size={18} />
                </Link>
              ))}
            </section>
          ) : (
            <Empty>
              Chưa có bài luyện tập phù hợp bộ lọc này. Em hãy chọn một môn để
              bắt đầu nhé.
            </Empty>
          )
        }
      </Resource>
    </>
  );
}
export function ProgressPage() {
  return (
    <>
      <PageTitle
        eyebrow="HIỂU MÌNH ĐỂ HỌC TỐT HƠN"
        title="Cây năng lực của em"
        description="Kết quả được tính từ bài em đã nộp. Cần nhiều lần luyện tập để đánh giá vững hơn."
      />
      <Resource<Skill[]> path="/students/me/skills">
        {(skills) =>
          skills.length ? (
            <div className="two-columns">
              {skills.map((skill) => (
                <article className="panel skill-card" key={skill.skill_id}>
                  <span className="eyebrow">{skill.subject_name}</span>
                  <h2>{skill.name}</h2>
                  {skill.questions_attempted < 5 ? (
                    <p className="notice">Cần luyện tập thêm để đánh giá</p>
                  ) : (
                    <>
                      <strong className="skill-percent">
                        {percent(skill.mastery_score)}%
                      </strong>
                      <div
                        className="progress-track"
                        role="progressbar"
                        aria-label={skill.name}
                        aria-valuenow={percent(skill.mastery_score)}
                        aria-valuemin={0}
                        aria-valuemax={100}
                      >
                        <span
                          style={{ width: `${percent(skill.mastery_score)}%` }}
                        />
                      </div>
                    </>
                  )}
                  <p>
                    {skill.questions_attempted} câu đã thử ·{" "}
                    {skill.correct_count} câu đúng
                  </p>
                  <p>
                    Độ tin cậy: {percent(skill.confidence)}% · Gợi ý ôn:{" "}
                    {dateLabel(skill.next_review_at)}
                  </p>
                </article>
              ))}
            </div>
          ) : (
            <Empty>
              Cây năng lực sẽ có dữ liệu sau khi em nộp bài đầu tiên. Mình bắt
              đầu nhẹ nhàng nhé!
            </Empty>
          )
        }
      </Resource>
      <section className="panel section-title">
        <h2>Gợi ý bước tiếp theo</h2>
        <Resource<
          Dashboard["recommendations"]
        > path="/students/me/recommendations">
          {(items) =>
            items.length ? (
              <Recommendations items={items} />
            ) : (
              <Empty>
                Em có thể tiếp tục đọc bài học và quay lại luyện tập sau.
              </Empty>
            )
          }
        </Resource>
      </section>
    </>
  );
}
export function ProfilePage() {
  return (
    <Resource<
      User & {
        current_grade: number;
        learning_preferences: Record<string, unknown>;
      }
    > path="/students/me/profile">
      {(data) => (
        <>
          <PageTitle title="Hồ sơ của em" />
          <section className="panel profile-card">
            <span className="avatar large">{data.display_name.charAt(0)}</span>
            <h2>{data.display_name}</h2>
            <dl>
              <dt>Tên đăng nhập</dt>
              <dd>{data.username}</dd>
              <dt>Lớp đang học</dt>
              <dd>Lớp {data.current_grade}</dd>
            </dl>
            <p className="muted">
              Để sửa thông tin, em hãy nhờ quản trị viên hỗ trợ. Không cần cung
              cấp ngày sinh, địa chỉ hay số điện thoại.
            </p>
          </section>
        </>
      )}
    </Resource>
  );
}
