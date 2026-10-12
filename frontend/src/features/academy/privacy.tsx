"use client";
import { useState } from "react";
import { api } from "@/lib/api";

export function PrivacyControls({ studentId }: { studentId: string }) {
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  async function act(exporting: boolean) {
    setBusy(true);
    try {
      if (exporting) {
        const data = await api(`/ai-academy/privacy/${studentId}/export`);
        const url = URL.createObjectURL(
          new Blob([JSON.stringify(data, null, 2)], {
            type: "application/json",
          }),
        );
        const link = document.createElement("a");
        link.href = url;
        link.download = "viettree-ai-academy.json";
        link.click();
        URL.revokeObjectURL(url);
        setMessage(
          "Đã xuất dữ liệu AI Academy của tài khoản này. Giữ file ở nơi riêng tư.",
        );
      } else {
        await api("/ai-academy/privacy/project-text-removal", {
          method: "POST",
          body: JSON.stringify({ student_id: studentId }),
        });
        setMessage(
          "Đã gửi nhà trường yêu cầu gỡ nội dung tự viết trong sản phẩm. Hồ sơ học và audit tối thiểu vẫn được giữ.",
        );
      }
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="academy-privacy">
      <p>
        Quyền dữ liệu: xuất hồ sơ AI Academy hoặc yêu cầu nhà trường gỡ phần nội
        dung tự viết trong sản phẩm.
      </p>
      <div className="academy-actions">
        <button
          disabled={busy}
          className="button secondary"
          onClick={() => void act(true)}
        >
          Xuất dữ liệu riêng
        </button>
        <button
          disabled={busy}
          className="button secondary"
          onClick={() => void act(false)}
        >
          Yêu cầu gỡ nội dung sản phẩm
        </button>
      </div>
      <p role="status">{message}</p>
    </div>
  );
}
