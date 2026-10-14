"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { api } from "@/lib/api";
import type { Answer, Attempt } from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { QuestionInput } from "@/components/question-input";
import { LockedContent } from "@/features/membership/pages";
import { useAnswerAutosave } from "@/hooks/use-answer-autosave";
import { DeadlineClock } from "@/components/deadline-clock";
import { QuestionPrompt } from "@/components/question-prompt";

export function Quiz({ data }: { data: Attempt }) {
  const router = useRouter();
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, Answer>>(() =>
    Object.fromEntries(
      data.items
        .filter((item) => item.answer)
        .map((item) => [item.id, item.answer!]),
    ),
  );
  const autosave = useAnswerAutosave(data.id);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
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
    await autosave.flush();
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
          {data.deadline && (
            <DeadlineClock
              key={`${data.deadline}:${data.server_time}`}
              deadline={data.deadline}
              serverTime={data.server_time}
            />
          )}
          <QuestionPrompt
            key={item.id}
            text={item.content.prompt}
            grade={data.grade}
          />
          <QuestionInput
            item={item}
            answer={answers[item.id] || null}
            disabled={busy}
            onChange={(answer) => {
              setAnswers((previous) => ({ ...previous, [item.id]: answer }));
              autosave.change(item.id, answer);
            }}
          />
          {error && (
            <div className="notice error" role="alert">
              {error}
            </div>
          )}
          {autosave.error && (
            <div className="notice error" role="alert">
              <p>{autosave.error}</p>
              <p>
                Câu trả lời vẫn ở trang này. Em giữ trang mở và thử lưu lại nhé.
              </p>
              <button
                className="button secondary"
                disabled={busy || autosave.saving}
                onClick={() => void action(() => {})}
              >
                Thử lưu lại
              </button>
            </div>
          )}
          <p className="save-message" role="status">
            {autosave.saving
              ? "Đang lưu…"
              : autosave.error
                ? "Chưa lưu được"
                : autosave.pending
                  ? "Chờ lưu câu trả lời…"
                  : autosave.saved
                    ? "Đã lưu câu trả lời. Em có thể quay lại bài này."
                    : data.items.some((saved) => saved.answer)
                      ? "Đã tải các câu trả lời đã lưu."
                      : "Bài tự lưu sau khi em trả lời."}
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
  const resource = useResource<Attempt>(`/attempts/${id}`);
  if (resource.loading) return <Loading />;
  if (
    resource.errorCode === "MEMBERSHIP_REQUIRED" ||
    resource.errorCode === "MEMBERSHIP_REVOKED"
  )
    return <LockedContent message={resource.error} code={resource.errorCode} />;
  if (resource.error || !resource.data)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  return <Quiz key={id} data={resource.data} />;
}
