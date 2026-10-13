"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import { Loading, ErrorState } from "@/components/ui";
import { AcademyImage } from "./shared";
import { ActivityBoard } from "./activity-board";
import type { PlayerData } from "./types";
import { LockedContent } from "@/features/membership/pages";
import { GuidedText } from "@/components/guided-text";
import { StepJourney } from "./step-journey";

export function LessonPlayer({ id }: { id: string }) {
  const [data, setData] = useState<PlayerData | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [errorCode, setErrorCode] = useState("");
  const [passed, setPassed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [hint, setHint] = useState("");
  const [hintLevel, setHintLevel] = useState(0);
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
      setHintLevel(0);
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
    setError("");
    try {
      const level = Math.min(3, hintLevel + 1);
      const result = await api<{ message: string }>(
        `/ai-academy/lessons/${id}/hints`,
        { method: "POST", body: JSON.stringify({ step_id: step.id, level }) },
      );
      setHint(result.message);
      setHintLevel(level);
    } catch (e) {
      setError((e as Error).message);
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
        <p>{finished ? "Đã hoàn thành" : "Xem tranh · Chạm chọn · Thử lại"}</p>
      </header>
      <StepJourney
        steps={data.content.steps}
        current={index}
        nextStep={data.progress.next_step}
        completed={finished}
      />
      <div className="academy-player-layout">
        <details className="academy-step-menu">
          <summary>
            Bước {index + 1}/{data.content.steps.length} · Đổi bước
          </summary>
          <nav aria-label="Các bước bài học" className="academy-step-nav">
            {data.content.steps.map((s, i) => (
              <button
                key={s.id}
                className={i === index ? "active" : ""}
                disabled={busy || i > data.progress.next_step}
                onClick={() => {
                  setSelected(i);
                  setPassed(false);
                  setHint("");
                  setHintLevel(0);
                }}
              >
                {i < data.progress.next_step ? "✓" : i + 1} {s.title}
              </button>
            ))}
          </nav>
        </details>
        <article className="panel academy-step">
          <h2>{step.title}</h2>
          {!["activity", "quiz"].includes(step.kind) && (
            <GuidedText text={step.text} grade={data.lesson.grade} />
          )}
          {step.details_text && (
            <details className="academy-extra-reading">
              <summary>Đọc thêm nếu em muốn</summary>
              <p>{step.details_text}</p>
            </details>
          )}
          {data.flags?.voice_enabled && (
            <button
              className="button secondary"
              onClick={() => {
                if (!("speechSynthesis" in window)) {
                  setError(
                    "Thiết bị chưa có giọng đọc. Em có thể nhờ người lớn đọc cùng.",
                  );
                  return;
                }
                const voice = window.speechSynthesis
                  .getVoices()
                  .find((v) => v.localService && v.lang.startsWith("vi"));
                if (!voice) {
                  setError(
                    "Thiết bị chưa có giọng đọc tiếng Việt. Em có thể nhờ người lớn đọc cùng.",
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
              Nghe bài
            </button>
          )}
          {!["activity", "quiz"].includes(step.kind) && (
            <div className="academy-scenes">
              {step.media.map((code) => (
                <AcademyImage
                  key={code}
                  code={code}
                  alt={`${data.lesson.title} · ${step.title}`}
                />
              ))}
            </div>
          )}
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
              onReset={() => setPassed(false)}
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
          <div className="academy-help">
            <button
              className="button secondary"
              disabled={busy || hintLevel >= 3}
              onClick={() => void getHint()}
            >
              {hintLevel === 0
                ? "Em cần gợi ý"
                : hintLevel >= 3
                  ? "Đã mở hết gợi ý"
                  : "Gợi ý thêm · VIP"}
            </button>
            {hint && <p role="status">{hint}</p>}
          </div>
          {error && (
            <p role="alert" className="notice error">
              {error}
            </p>
          )}
          <div className="academy-actions">
            <button
              className="button secondary"
              disabled={busy || index === 0}
              onClick={() => {
                setSelected(index - 1);
                setPassed(false);
                setHint("");
                setHintLevel(0);
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
                : "Tiếp theo"}
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
