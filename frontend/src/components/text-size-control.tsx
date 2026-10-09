"use client";
import { useState } from "react";
import { useAccessibility } from "./shell";
import type { TextSize } from "@/lib/types";

export function TextSizeControl() {
  const { textSize, saveTextSize } = useAccessibility();
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  async function choose(size: TextSize) {
    setBusy(true);
    setMessage("");
    setError("");
    try {
      await saveTextSize(size);
      setMessage("Đã lưu cỡ chữ cho em.");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel reading-settings">
      <h2>Chữ dễ đọc cho em</h2>
      <p>
        Chọn cỡ chữ em thấy thoải mái. Lần sau đăng nhập, em vẫn dùng cỡ chữ
        này.
      </p>
      <div className="text-size-choices" role="group" aria-label="Cỡ chữ">
        {(
          [
            ["comfortable", "Chữ vừa đủ lớn"],
            ["large", "Chữ lớn hơn"],
          ] as const
        ).map(([size, label]) => (
          <button
            key={size}
            className={`button ${textSize === size ? "" : "secondary"}`}
            aria-pressed={textSize === size}
            disabled={busy}
            onClick={() => choose(size)}
          >
            {label}
          </button>
        ))}
      </div>
      <p className="reading-preview">Mỗi ngày em học thêm một điều hay. 🌱</p>
      <p role="status" aria-live="polite">
        {busy ? "Đang lưu cỡ chữ…" : message}
      </p>
      {error && (
        <p className="error-text" role="alert">
          {error}
        </p>
      )}
    </section>
  );
}
