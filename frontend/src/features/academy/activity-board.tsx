"use client";
import { useRef, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { Activity, Feedback, Question } from "./types";
import { AcademyImage } from "./shared";
import { WordPicture } from "@/components/word-picture";

export function ActivityBoard({
  lessonId,
  stepId,
  activity,
  questions,
  onPass,
  onReset,
  onDenied,
}: {
  lessonId: string;
  stepId: string;
  activity?: Activity | null;
  questions: Question[];
  onPass: () => void;
  onReset?: () => void;
  onDenied?: (message: string) => void;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [level, setLevel] = useState(2);
  const [cursor, setCursor] = useState(0);
  const [result, setResult] = useState<Feedback | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const submission = useRef<{ signature: string; key: string } | null>(null);
  const items = activity
    ? level < 3
      ? activity.items.slice(0, level + 1)
      : activity.items
    : [];
  const entries = activity ? items : questions;
  const current = entries[cursor];
  const item = activity ? items[cursor] : null;
  const question = activity ? null : questions[cursor];
  const allAnswered = entries.every((entry) => answers[entry.id] !== undefined);

  function choose(id: string, value: string) {
    setAnswers((previous) => ({ ...previous, [id]: value }));
    setResult(null);
    setError("");
    onReset?.();
  }
  async function grade() {
    setBusy(true);
    setError("");
    try {
      const signature = JSON.stringify({ lessonId, stepId, level, answers });
      if (submission.current?.signature !== signature) {
        submission.current = { signature, key: crypto.randomUUID() };
      }
      const body = await api<Feedback>(
        `/ai-academy/lessons/${lessonId}/attempts`,
        {
          method: "POST",
          body: JSON.stringify({
            step_id: stepId,
            idempotency_key: submission.current.key,
            level,
            answers,
          }),
        },
      );
      setResult(body);
      if (body.feedback.passed) onPass();
      else onReset?.();
    } catch (e) {
      setError((e as Error).message);
      if (e instanceof ApiError && e.code === "MEMBERSHIP_REQUIRED")
        onDenied?.(e.message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="academy-board" aria-label="Hoạt động tương tác">
      <p className="academy-card-counter" aria-live="polite">
        {activity ? "Thẻ" : "Câu"} {cursor + 1}/{entries.length} · Chọn một đáp
        án
      </p>
      {item && (
        <div className="academy-focus-card">
          {item.asset && (
            <AcademyImage code={item.asset} alt={item.text} small />
          )}
          <h3>{item.text}</h3>
          <div
            className="academy-tap-choices"
            role="group"
            aria-label={`Lựa chọn cho ${item.text}`}
          >
            {activity!.choices.map((choice) => (
              <button
                key={choice}
                className={`button ${answers[item.id] === choice ? "" : "secondary"}`}
                aria-pressed={answers[item.id] === choice}
                disabled={busy}
                onClick={() => choose(item.id, choice)}
              >
                <WordPicture text={choice} />
                {choice}
              </button>
            ))}
          </div>
        </div>
      )}
      {question && (
        <fieldset className="academy-question">
          <legend>{question.prompt}</legend>
          {question.options.map((option, index) => (
            <label
              key={index}
              className={
                answers[question.id] === String(index) ? "selected" : ""
              }
            >
              <input
                type="radio"
                name={`${lessonId}-${stepId}-${question.id}`}
                checked={answers[question.id] === String(index)}
                disabled={busy}
                onChange={() => choose(question.id, String(index))}
              />
              <WordPicture text={option} />
              <span>{option}</span>
            </label>
          ))}
        </fieldset>
      )}
      <div className="academy-card-navigation">
        <button
          className="button secondary"
          disabled={busy || cursor === 0}
          onClick={() => setCursor(cursor - 1)}
        >
          Thẻ trước
        </button>
        {cursor < entries.length - 1 ? (
          <button
            className="button"
            disabled={busy || !current || answers[current.id] === undefined}
            onClick={() => setCursor(cursor + 1)}
          >
            Thẻ tiếp
          </button>
        ) : (
          <button
            className="button"
            disabled={busy || !allAnswered}
            onClick={() => void grade()}
          >
            {busy ? "Đang kiểm tra…" : "Kiểm tra lựa chọn"}
          </button>
        )}
      </div>
      {allAnswered && cursor < entries.length - 1 && (
        <button
          className="button secondary"
          disabled={busy}
          onClick={() => void grade()}
        >
          Kiểm tra lựa chọn
        </button>
      )}
      {activity && (
        <details className="academy-help">
          <summary>Đổi số thẻ thực hành</summary>
          <label>
            Mức thực hành
            <select
              value={level}
              disabled={busy}
              onChange={(e) => {
                setLevel(Number(e.target.value));
                setCursor(0);
                setAnswers({});
                setResult(null);
                onReset?.();
              }}
            >
              <option value={1}>Ít thẻ</option>
              <option value={2}>Vừa đủ</option>
              <option value={3}>Thử thêm</option>
            </select>
          </label>
        </details>
      )}
      {error && (
        <p role="alert" className="notice error">
          {error}
        </p>
      )}
      {result && (
        <div role="status" className="notice">
          <strong>
            {result.feedback.passed
              ? "✓ Em đã làm được!"
              : "↻ Mình thử lại nhé."}
          </strong>
          <p>
            {Math.round(result.score * 100)}% ·{" "}
            {result.feedback.passed
              ? "Em có thể học tiếp."
              : "Xem lại thẻ và chọn lại."}
          </p>
          <details>
            <summary>Xem cách kiểm tra</summary>
            {result.feedback.items.map((entry) => (
              <p key={entry.id}>
                {entry.correct ? "✓" : "↻"} {entry.explanation}
              </p>
            ))}
          </details>
        </div>
      )}
    </section>
  );
}
