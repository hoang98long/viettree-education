"use client";
import { useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { Activity, Feedback, Question } from "./types";
import { AcademyImage } from "./shared";

export function ActivityBoard({
  lessonId,
  stepId,
  activity,
  questions,
  onPass,
  onDenied,
}: {
  lessonId: string;
  stepId: string;
  activity?: Activity | null;
  questions: Question[];
  onPass: () => void;
  onDenied?: (message: string) => void;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [level, setLevel] = useState(2);
  const [result, setResult] = useState<Feedback | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const items = activity
    ? level < 3
      ? activity.items.slice(0, level + 1)
      : activity.items
    : [];
  async function grade() {
    setBusy(true);
    setError("");
    try {
      const body = await api<Feedback>(
        `/ai-academy/lessons/${lessonId}/attempts`,
        {
          method: "POST",
          body: JSON.stringify({
            step_id: stepId,
            idempotency_key: crypto.randomUUID(),
            level,
            answers,
          }),
        },
      );
      setResult(body);
      if (body.feedback.passed) onPass();
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
      {activity && (
        <>
          <p>{activity.instruction}</p>
          <label>
            Mức thực hành
            <select
              value={level}
              onChange={(e) => {
                setLevel(Number(e.target.value));
                setAnswers({});
                setResult(null);
              }}
            >
              <option value={1}>Hỗ trợ · ít thẻ</option>
              <option value={2}>Tiêu chuẩn</option>
              <option value={3}>Thử thách · đầy đủ thẻ</option>
            </select>
          </label>
          {["sequence", "comic"].includes(activity.kind) && (
            <p className="muted">
              Chọn số thứ tự. Có thể kéo thẻ tới số, hoặc chọn bằng chạm/bàn
              phím.
            </p>
          )}
          <div className="academy-choices">
            {items.map((item) => (
              <label
                key={item.id}
                className="academy-tile"
                draggable={["classify", "sequence", "comic"].includes(
                  activity.kind,
                )}
                onDragStart={(e) =>
                  e.dataTransfer.setData("text/plain", item.id)
                }
              >
                <strong>{item.text}</strong>
                {item.asset && (
                  <AcademyImage code={item.asset} alt={item.text} small />
                )}
                <select
                  aria-label={`Lựa chọn: ${item.text}`}
                  value={answers[item.id] || ""}
                  onChange={(e) =>
                    setAnswers({ ...answers, [item.id]: e.target.value })
                  }
                >
                  <option value="">Em chọn…</option>
                  {activity.choices.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              </label>
            ))}
          </div>
          <div className="academy-dropzones">
            {activity.choices.map((choice) => (
              <button
                key={choice}
                className="button secondary"
                aria-label={`Vùng chọn ${choice}`}
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  e.preventDefault();
                  const id = e.dataTransfer.getData("text/plain");
                  if (items.some((item) => item.id === id))
                    setAnswers({ ...answers, [id]: choice });
                }}
                onClick={() => {
                  const next = items.find((i) => !answers[i.id]);
                  if (next) setAnswers({ ...answers, [next.id]: choice });
                }}
              >
                {choice}
              </button>
            ))}
          </div>
        </>
      )}
      {questions.map((q) => (
        <fieldset key={q.id} className="academy-question">
          <legend>{q.prompt}</legend>
          {q.options.map((option, index) => (
            <label key={index}>
              <input
                type="radio"
                name={q.id}
                value={index}
                checked={answers[q.id] === String(index)}
                onChange={() =>
                  setAnswers({ ...answers, [q.id]: String(index) })
                }
              />
              {option}
            </label>
          ))}
        </fieldset>
      ))}
      <button className="button" disabled={busy} onClick={() => void grade()}>
        {busy ? "Đang kiểm tra…" : "Kiểm tra lựa chọn"}
      </button>
      {error && (
        <p role="alert" className="notice error">
          {error}
        </p>
      )}
      {result && (
        <div role="status" className="notice">
          <strong>{result.feedback.message}</strong>
          <p>{Math.round(result.score * 100)}% · Em có thể thử lại.</p>
          {result.feedback.items.map((item) => (
            <p key={item.id}>
              {item.correct ? "✓ Có căn cứ" : "↻ Cần thử lại"} ·{" "}
              {item.explanation}
            </p>
          ))}
        </div>
      )}
    </section>
  );
}
