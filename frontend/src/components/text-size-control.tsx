"use client";
import { useState } from "react";
import { useAccessibility } from "./shell";
import type { TextSize } from "@/lib/types";
import { deviceLabels } from "@/lib/reading-preferences";

export function TextSizeControl() {
  const { textSize, deviceType, saveTextSize } = useAccessibility();
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
    <section
      id="reading-settings"
      className="panel reading-settings"
      aria-labelledby="reading-settings-title"
    >
      <h2 id="reading-settings-title">Chữ dễ đọc cho em</h2>
      <p>
        Chọn cỡ chữ em thấy thoải mái. Chữ gọn hơn giúp em học trên điện thoại.
        Lựa chọn được lưu riêng cho điện thoại, máy tính bảng và máy tính của
        em.
      </p>
      <p className="reading-device">
        {deviceType
          ? `Đang chọn cho: ${deviceLabels[deviceType]}.`
          : "Đang nhận diện thiết bị…"}
      </p>
      <div className="text-size-choices" role="group" aria-label="Cỡ chữ">
        {(
          [
            ["compact", "Chữ gọn hơn"],
            ["comfortable", "Chữ vừa đủ lớn"],
            ["large", "Chữ lớn hơn"],
          ] as const
        ).map(([size, label]) => (
          <button
            key={size}
            className={`button ${textSize === size ? "" : "secondary"}`}
            aria-pressed={textSize === size}
            disabled={busy || !deviceType}
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
