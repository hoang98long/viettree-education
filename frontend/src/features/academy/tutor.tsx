"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { PageTitle, Loading, ErrorState } from "@/components/ui";
import { PromptBuilder } from "./lab";
import type { CatalogLesson } from "./types";

export function LessonTutor() {
  const home = useResource<{ catalog: CatalogLesson[] }>("/ai-academy/home");
  const [lesson, setLesson] = useState("");
  const [mode, setMode] = useState("ExplainConcept");
  const [tried, setTried] = useState("");
  const [result, setResult] = useState<{
    mode: string;
    message: string;
    notice: string;
  } | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function ask() {
    setBusy(true);
    setError("");
    try {
      setResult(
        await api("/ai-academy/tutor", {
          method: "POST",
          body: JSON.stringify({
            lesson_id: lesson || home.data?.catalog[0]?.id,
            mode,
            tried,
          }),
        }),
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <PageTitle
        title="Trợ giảng theo bài học"
        description="Chọn nhiệm vụ trong bài đã duyệt. Không phải chatbot internet; không gửi nguyên văn bài làm hoặc hồ sơ của em tới mô hình."
      />
      {home.loading ? (
        <Loading />
      ) : home.error ? (
        <ErrorState message={home.error} retry={home.retry} />
      ) : (
        <section className="panel">
          <label>
            Bài đang học
            <select
              value={lesson || home.data?.catalog[0]?.id || ""}
              onChange={(e) => setLesson(e.target.value)}
            >
              {home.data?.catalog.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.title}
                </option>
              ))}
            </select>
          </label>
          <label>
            Em cần hỗ trợ
            <select value={mode} onChange={(e) => setMode(e.target.value)}>
              {[
                ["ExplainConcept", "Giải thích ý chính"],
                ["GiveHint", "Gợi ý sau khi em thử"],
                ["AskSocraticQuestion", "Câu hỏi gợi mở"],
                ["ReviewStudentDraft", "Bảng tự kiểm tra bản nháp"],
                ["PracticeEnglish", "Hội thoại mẫu"],
                ["BrainstormStory", "Tìm ý truyện"],
              ].map(([v, t]) => (
                <option key={v} value={v}>
                  {t}
                </option>
              ))}
            </select>
          </label>
          <label>
            Em đã thử gì? Chỉ dùng dữ liệu mẫu
            <textarea
              value={tried}
              maxLength={500}
              onChange={(e) => setTried(e.target.value)}
            />
          </label>
          <button className="button" disabled={busy} onClick={() => void ask()}>
            Nhận hướng dẫn
          </button>
          {error && (
            <p role="alert" className="notice error">
              {error}
            </p>
          )}
          {result && (
            <div role="status" className="notice">
              <strong>
                {result.mode === "ollama"
                  ? "Gợi ý do mô hình tạo"
                  : result.mode === "blocked"
                    ? "Cần điều chỉnh yêu cầu"
                    : "Hướng dẫn nội bộ / mô phỏng"}
              </strong>
              <p>{result.message}</p>
              <p>{result.notice}</p>
            </div>
          )}
        </section>
      )}
      <PromptBuilder />
    </>
  );
}
