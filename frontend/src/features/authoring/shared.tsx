"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import type {
  Options,
  QuestionDraft,
  AssessmentDraft,
} from "@/features/authoring/types";

export function ScopeFields({
  options,
  subject,
  topic,
  setSubject,
  setTopic,
  disabled = false,
}: {
  options: Options;
  subject: string;
  topic: string;
  setSubject: (value: string) => void;
  setTopic: (value: string) => void;
  disabled?: boolean;
}) {
  return (
    <div className="two-columns">
      <label>
        Môn học
        <select
          required
          disabled={disabled}
          value={subject}
          onChange={(e) => {
            const value = e.target.value;
            setSubject(value);
            setTopic(
              options.topics.find((item) => item.subject_id === value)?.id ??
                "",
            );
          }}
        >
          {options.subjects.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name_vi}
            </option>
          ))}
        </select>
      </label>
      <label>
        Chủ đề
        <select
          required
          disabled={disabled}
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        >
          <option value="">Chọn chủ đề</option>
          {options.topics
            .filter((item) => item.subject_id === subject)
            .map((item) => (
              <option key={item.id} value={item.id}>
                {item.title}
              </option>
            ))}
        </select>
      </label>
    </div>
  );
}

export function ContentActions({
  kind,
  data,
  reload,
}: {
  kind: "questions" | "assessments";
  data: QuestionDraft | AssessmentDraft;
  reload: () => void;
}) {
  const router = useRouter();
  const [reason, setReason] = useState("");
  const [newCode, setNewCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const reviewed =
    "reviewed" in data ? data.reviewed : Boolean(data.reviewed_by);
  async function act(action: string) {
    setBusy(true);
    setError("");
    try {
      const result = await api<{ id: string }>(
        `/admin/authoring/${kind}/${data.id}/${action}`,
        {
          method: "POST",
          body:
            action === "revise"
              ? undefined
              : JSON.stringify(
                  action === "clone"
                    ? { code: newCode }
                    : { expected_revision: data.edit_revision, reason },
                ),
        },
      );
      if (action === "revise" || action === "clone")
        router.push(`/admin/${kind}/${result.id}/edit`);
      else reload();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel authoring-actions">
      <h2>Duyệt và xuất bản</h2>
      <p>
        Trạng thái:{" "}
        <strong>
          {data.status === "draft"
            ? reviewed
              ? "Nháp đã duyệt"
              : "Nháp chưa duyệt"
            : data.status === "published"
              ? "Đã xuất bản"
              : "Đã lưu trữ"}
        </strong>
        . Lưu sửa bản nháp sẽ yêu cầu duyệt lại.
      </p>
      <label>
        Lý do duyệt / xuất bản / lưu trữ
        <textarea
          value={reason}
          minLength={5}
          maxLength={500}
          onChange={(e) => setReason(e.target.value)}
        />
      </label>
      <div className="quiz-actions">
        {data.status === "draft" && (
          <>
            <button
              className="button secondary"
              disabled={busy || reason.trim().length < 5}
              onClick={() => void act("review")}
            >
              Duyệt nội dung
            </button>
            <button
              className="button"
              disabled={busy || !reviewed || reason.trim().length < 5}
              onClick={() => void act("publish")}
            >
              Xuất bản
            </button>
          </>
        )}
        {data.status !== "archived" && (
          <button
            className="button secondary"
            disabled={busy || reason.trim().length < 5}
            onClick={() => void act("archive")}
          >
            Lưu trữ
          </button>
        )}
        {kind === "questions" && data.status !== "draft" && (
          <button
            className="button secondary"
            disabled={busy}
            onClick={() => void act("revise")}
          >
            Tạo phiên bản mới
          </button>
        )}
      </div>
      {kind === "assessments" && (
        <div className="clone-form">
          <label>
            Mã đề sao chép
            <input
              value={newCode}
              minLength={3}
              maxLength={100}
              pattern="[A-Za-z0-9][A-Za-z0-9_-]+"
              onChange={(e) => setNewCode(e.target.value)}
            />
          </label>
          <button
            className="button secondary"
            disabled={busy || !/^[A-Za-z0-9][A-Za-z0-9_-]{2,99}$/.test(newCode)}
            onClick={() => void act("clone")}
          >
            Sao chép thành nháp mới
          </button>
        </div>
      )}
      {error && (
        <p role="alert" className="error-text">
          {error}
        </p>
      )}
    </section>
  );
}
