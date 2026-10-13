"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import { Loading, ErrorState } from "@/components/ui";
import { AcademyImage } from "./shared";
import { ActivityBoard } from "./activities";
import type { PlayerData } from "./types";
import { LockedContent } from "@/features/membership/pages";

export function LessonPlayer({ id }: { id: string }) {
  const [data, setData] = useState<PlayerData | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [errorCode, setErrorCode] = useState("");
  const [passed, setPassed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [hint, setHint] = useState("");
  const [tried, setTried] = useState("");
  const [hintLevel, setHintLevel] = useState(1);
  useEffect(() => {
    let alive = true;
    api<PlayerData>(`/ai-academy/lessons/${id}/start`, { method: "POST" })
      .then((r) => {
        if (alive) setData(r);
      })
      .catch((e) => {
        if (alive) {
          setError(e.message);
          setErrorCode(e.code || "");
        }
      });
    return () => {
      alive = false;
    };
  }, [id]);
  if (errorCode === "MEMBERSHIP_REQUIRED")
    return (
      <>
        <LockedContent message={error} />
        <Link className="button secondary" href="/ai-academy">
          Về bài AI miễn phí
        </Link>
      </>
    );
  if (error && !data)
    return (
      <ErrorState message={error} retry={() => window.location.reload()} />
    );
  if (!data) return <Loading />;
  const index =
    selected ??
    Math.min(data.progress.next_step, data.content.steps.length - 1);
  const step = data.content.steps[index];
  const finished = Boolean(data.progress.completed_at);
  async function next() {
    setBusy(true);
    setError("");
    try {
      const state = await api<PlayerData["progress"]>(
        `/ai-academy/lessons/${id}/steps`,
        { method: "POST", body: JSON.stringify({ step_id: step.id }) },
      );
      setData((d) => (d ? { ...d, progress: state } : d));
      setSelected(Math.min(index + 1, data!.content.steps.length - 1));
      setPassed(false);
      setHint("");
    } catch (e) {
      setError((e as Error).message);
      if (e instanceof ApiError && e.code === "MEMBERSHIP_REQUIRED") {
        setErrorCode(e.code);
        setData(null);
      }
    } finally {
      setBusy(false);
    }
  }
  async function getHint() {
    setBusy(true);
    try {
      const result = await api<{ message: string; notice: string }>(
        "/ai-academy/tutor",
        {
          method: "POST",
          body: JSON.stringify({
            lesson_id: id,
            mode: "GiveHint",
            tried,
            level: hintLevel,
          }),
        },
      );
      setHint(result.message + " " + (result.notice || ""));
    } catch (e) {
      setError((e as Error).message);
      if (e instanceof ApiError && e.code === "MEMBERSHIP_REQUIRED") {
        setErrorCode(e.code);
        setData(null);
      }
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <nav className="breadcrumb" aria-label="Đường dẫn">
        <Link href="/ai-academy">AI Academy</Link>
        <span>›</span>
        <span>{data.lesson.title}</span>
      </nav>
      <header className="page-title">
        <span className="eyebrow">
          LỚP {data.lesson.grade} · {index + 1}/{data.content.steps.length}
        </span>
        <h1>{data.lesson.title}</h1>
        <p>
          Quan sát · Thử làm · Kiểm tra ·{" "}
          {finished ? "Đã hoàn thành" : "Tiến độ được lưu trên tài khoản"}
        </p>
      </header>
      <div className="academy-player-layout">
        <nav aria-label="Các bước bài học" className="academy-step-nav">
          {data.content.steps.map((s, i) => (
            <button
              key={s.id}
              className={i === index ? "active" : ""}
              disabled={i > data.progress.next_step}
              onClick={() => {
                setSelected(i);
                setPassed(false);
                setHint("");
              }}
            >
              {i < data.progress.next_step ? "✓" : i + 1} {s.title}
            </button>
          ))}
        </nav>
        <article className="panel academy-step">
          <h2>{step.title}</h2>
          <p>{step.text}</p>
          {data.flags?.voice_enabled && (
            <button
              className="button secondary"
              onClick={() => {
                if (!("speechSynthesis" in window)) {
                  setError("Chưa có giọng đọc; em đọc chữ hoặc nhờ người lớn.");
                  return;
                }
                const voice = window.speechSynthesis
                  .getVoices()
                  .find((v) => v.localService && v.lang.startsWith("vi"));
                if (!voice) {
                  setError(
                    "Chưa có giọng Việt local; không gọi dịch vụ giọng nói ngoài.",
                  );
                  return;
                }
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(step.text);
                utterance.voice = voice;
                utterance.rate = 0.85;
                window.speechSynthesis.speak(utterance);
              }}
            >
              Đọc lại bằng giọng local
            </button>
          )}
          <div className="academy-scenes">
            {step.media.map((code) => (
              <AcademyImage
                key={code}
                code={code}
                alt={`${data.lesson.title} · ${step.title}`}
              />
            ))}
          </div>
          {step.kind === "flip_card" && (
            <details>
              <summary>Mở điều em cần đối chiếu</summary>
              <p>{data.content.support}</p>
            </details>
          )}
          {(step.activity || step.questions.length > 0) && (
            <ActivityBoard
              onDenied={(message) => {
                setError(message);
                setErrorCode("MEMBERSHIP_REQUIRED");
                setData(null);
              }}
              key={step.id}
              lessonId={id}
              stepId={step.id}
              activity={step.activity}
              questions={step.questions}
              onPass={() => setPassed(true)}
            />
          )}
          <details className="academy-help">
            <summary>Thẻ hình để quan sát thêm</summary>
            <div className="academy-samples">
              {data.content.cards.map((code) => (
                <AcademyImage
                  key={code}
                  code={code}
                  alt={`Thẻ hình mẫu ${code.split("-").slice(1, -1).join(" ")} để quan sát`}
                  small
                />
              ))}
            </div>
          </details>
          <details className="academy-help">
            <summary>Gợi ý và cách học phù hợp</summary>
            <p>{data.content.support}</p>
            <label>
              Em đã thử điều gì? (dùng dữ liệu mẫu)
              <textarea
                value={tried}
                maxLength={500}
                onChange={(e) => setTried(e.target.value)}
              />
            </label>
            <label>
              Mức gợi ý
              <select
                value={hintLevel}
                onChange={(e) => setHintLevel(Number(e.target.value))}
              >
                <option value={1}>1 · Định hướng</option>
                <option value={2}>2 · Cách làm (VIP)</option>
                <option value={3}>3 · Kiểm tra (VIP)</option>
              </select>
            </label>
            <button
              className="button secondary"
              disabled={busy}
              onClick={() => void getHint()}
            >
              Xin gợi ý sau khi thử
            </button>
            {hint && <p role="status">{hint}</p>}
            <h3>Thử thách thêm</h3>
            <p>{data.content.advanced}</p>
          </details>
          {error && (
            <p role="alert" className="notice error">
              {error}
            </p>
          )}
          <div className="academy-actions">
            <button
              className="button secondary"
              disabled={index === 0}
              onClick={() => {
                setSelected(index - 1);
                setPassed(false);
              }}
            >
              Quay lại
            </button>
            <button
              className="button"
              onClick={() => void next()}
              disabled={
                busy ||
                (!passed &&
                  !data.passed_steps?.includes(step.id) &&
                  ["activity", "quiz"].includes(step.kind) &&
                  index >= data.progress.next_step)
              }
            >
              {index === data.content.steps.length - 1
                ? "Hoàn thành bài"
                : "Lưu và tiếp tục"}
            </button>
          </div>
          {finished && (
            <div role="status" className="notice">
              <h3>Em đã khám phá xong bài này!</h3>
              <Link href="/ai-academy/portfolio">Xem tiến bộ và huy hiệu</Link>
            </div>
          )}
        </article>
      </div>
    </>
  );
}
