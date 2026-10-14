"use client";
import { useEffect, useState } from "react";
import { Clock3 } from "lucide-react";

export function DeadlineClock({
  deadline,
  serverTime,
}: {
  deadline: string;
  serverTime?: string;
}) {
  const [duration] = useState(() => {
    const reference = serverTime ? Date.parse(serverTime) : Date.now();
    return Math.max(0, Date.parse(deadline) - reference);
  });
  const [seconds, setSeconds] = useState(() => Math.ceil(duration / 1000));
  useEffect(() => {
    const start = performance.now();
    const tick = () =>
      setSeconds(
        Math.max(0, Math.ceil((duration - (performance.now() - start)) / 1000)),
      );
    const timer = window.setInterval(tick, 1000);
    document.addEventListener("visibilitychange", tick);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", tick);
    };
  }, [duration]);
  if (!Number.isFinite(seconds)) return null;
  const hours = Math.floor(seconds / 3600);
  const time = `${hours ? `${hours}:` : ""}${String(Math.floor(seconds / 60) % 60).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
  return (
    <div className={`deadline-clock ${seconds <= 120 ? "ending" : ""}`}>
      <span
        role="timer"
        aria-live="off"
        aria-label={`Thời gian còn lại ${time}`}
      >
        <Clock3 aria-hidden size={20} /> Còn {time}
      </span>
      {seconds <= 120 && (
        <p role="status">
          {seconds
            ? "Sắp hết giờ. Em kiểm tra và nộp bài nhé."
            : "Thời gian dự kiến đã hết. Máy chủ sẽ kiểm tra khi em lưu hoặc nộp bài."}
        </p>
      )}
    </div>
  );
}
