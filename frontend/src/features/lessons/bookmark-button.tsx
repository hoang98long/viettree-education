"use client";

import { useState } from "react";
import { Bookmark } from "lucide-react";
import { api } from "@/lib/api";

export function BookmarkButton({
  lessonId,
  initialSaved,
  locked = false,
}: {
  lessonId: string;
  initialSaved: boolean;
  locked?: boolean;
}) {
  const [saved, setSaved] = useState(initialSaved);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  return (
    <div className="lesson-bookmark">
      <button
        type="button"
        className="button secondary"
        aria-pressed={saved}
        disabled={busy || (locked && !saved)}
        title={locked && !saved ? "Cần quyền học bài này để lưu" : undefined}
        onClick={async () => {
          setBusy(true);
          setError("");
          try {
            const result = await api<{ saved: boolean }>(
              `/students/me/lessons/${lessonId}/bookmark`,
              { method: "PUT", body: JSON.stringify({ saved: !saved }) },
            );
            setSaved(result.saved);
            window.dispatchEvent(new Event("viettree:lesson-bookmarks"));
          } catch (error) {
            setError((error as Error).message);
          } finally {
            setBusy(false);
          }
        }}
      >
        <Bookmark
          size={18}
          fill={saved ? "currentColor" : "none"}
          aria-hidden
        />
        {busy ? "Đang lưu…" : saved ? "Bỏ lưu bài học" : "Lưu bài học"}
      </button>
      {error && (
        <p className="error-text" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
