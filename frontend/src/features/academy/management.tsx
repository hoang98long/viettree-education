"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading, Empty } from "@/components/ui";

export function UnitCreator({
  grade,
  onCreated,
}: {
  grade: number;
  onCreated: () => void;
}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");
  async function create() {
    try {
      await api("/ai-academy/admin/units", {
        method: "POST",
        body: JSON.stringify({
          grade,
          title,
          description,
          code: `AI${grade}-UNIT-${crypto.randomUUID().slice(0, 8)}`,
        }),
      });
      setTitle("");
      setDescription("");
      setMessage("Đã tạo chủ đề. Khi nhân bản bài, chọn chủ đề mới làm đích.");
      onCreated();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <details className="panel">
      <summary>Tạo chủ đề mới cho lớp {grade}</summary>
      <label>
        Tên chủ đề
        <input
          maxLength={180}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </label>
      <label>
        Mô tả chủ đề
        <textarea
          maxLength={2000}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </label>
      <button className="button secondary" onClick={() => void create()}>
        Tạo chủ đề
      </button>
      <p role="status">{message}</p>
    </details>
  );
}

export function ModerationInbox() {
  const reviews = useResource<
    { id: string; reason_code: string; status: string; created_at: string }[]
  >("/ai-academy/admin/moderation");
  const requests = useResource<
    { id: string; created_at: string; metadata: { state: string } }[]
  >("/ai-academy/admin/privacy-requests");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  async function review(id: string) {
    try {
      await api(`/ai-academy/admin/moderation/${id}/review`, {
        method: "POST",
      });
      reviews.retry();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  async function resolve(id: string, approved: boolean) {
    try {
      await api(`/ai-academy/admin/privacy-requests/${id}/resolve`, {
        method: "POST",
        body: JSON.stringify({
          approved,
          actor_password: password,
          reason: "Nhà trường đã xem xét yêu cầu gỡ nội dung sản phẩm",
        }),
      });
      setPassword("");
      requests.retry();
      setMessage("Đã xử lý yêu cầu và lưu audit.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  if (reviews.loading || requests.loading) return <Loading />;
  if (reviews.error || requests.error)
    return (
      <ErrorState
        message={reviews.error || requests.error}
        retry={() => {
          reviews.retry();
          requests.retry();
        }}
      />
    );
  return (
    <>
      <section className="panel">
        <h2>Cảnh báo an toàn</h2>
        <p>Chỉ lưu mã lý do; nội dung bị chặn không được lưu để xem lại.</p>
        {!reviews.data?.length && <Empty>Chưa có cảnh báo.</Empty>}
        {reviews.data?.map((r) => (
          <div className="list-row" key={r.id}>
            <span>
              {(
                {
                  personal_data: "Thông tin riêng",
                  unsafe: "Nội dung không phù hợp",
                  prompt_injection: "Yêu cầu vượt phạm vi",
                } as Record<string, string>
              )[r.reason_code] || "Cần xem xét"}{" "}
              · {new Date(r.created_at).toLocaleDateString("vi-VN")}
            </span>
            <button
              disabled={r.status === "reviewed"}
              className="button secondary small"
              onClick={() => void review(r.id)}
            >
              {r.status === "reviewed" ? "Đã xem xét" : "Đánh dấu đã xem xét"}
            </button>
          </div>
        ))}
      </section>
      <section className="panel">
        <h2>Yêu cầu gỡ nội dung sản phẩm</h2>
        <p>
          Khi duyệt: gỡ các trường tự viết và góp ý trong sản phẩm AI Academy.
          Giữ tài khoản, bài nộp, điểm số, lịch sử học và audit. Xử lý theo yêu
          cầu đã xác minh với gia đình.
        </p>
        <label>
          Mật khẩu xác nhận xử lý
          <input
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {!requests.data?.length && <Empty>Chưa có yêu cầu.</Empty>}
        {requests.data?.map((r) => (
          <div className="list-row" key={r.id}>
            <span>
              Yêu cầu {r.id.slice(0, 8)} ·{" "}
              {new Date(r.created_at).toLocaleDateString("vi-VN")} ·{" "}
              {r.metadata.state === "pending"
                ? "Chờ xem xét"
                : r.metadata.state === "approved"
                  ? "Đã gỡ nội dung"
                  : "Đã từ chối"}
            </span>
            {r.metadata.state === "pending" && (
              <div className="academy-actions">
                <button
                  className="button secondary small"
                  onClick={() => void resolve(r.id, true)}
                >
                  Duyệt gỡ nội dung
                </button>
                <button
                  className="button secondary small"
                  onClick={() => void resolve(r.id, false)}
                >
                  Từ chối yêu cầu
                </button>
              </div>
            )}
          </div>
        ))}
        <p role="status">{message}</p>
      </section>
    </>
  );
}

export function PromptLibrary() {
  const list = useResource<
    { mode: string; version: number; template: string; status: string }[]
  >("/ai-academy/admin/prompts");
  const [mode, setMode] = useState("ExplainConcept");
  const [template, setTemplate] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  async function act(version?: number) {
    try {
      await api(
        version
          ? `/ai-academy/admin/prompts/${mode}/${version}/approve`
          : "/ai-academy/admin/prompts",
        {
          method: "POST",
          body: JSON.stringify(
            version
              ? {
                  actor_password: password,
                  reason: "Đã kiểm thử và duyệt mẫu hướng dẫn giới hạn bài học",
                }
              : { mode, template },
          ),
        },
      );
      setPassword("");
      list.retry();
      setMessage("Đã cập nhật phiên bản và audit.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>Mẫu hướng dẫn có phiên bản</h2>
      <p>
        Giới hạn phạm vi bài học, không yêu cầu dữ liệu riêng hoặc đáp án thay
        học sinh. Mẫu mới chỉ được dùng sau khi duyệt.
      </p>
      <label>
        Chế độ
        <select
          aria-label="Chế độ mẫu"
          value={mode}
          onChange={(e) => setMode(e.target.value)}
        >
          {[
            "ExplainConcept",
            "GiveHint",
            "AskSocraticQuestion",
            "ReviewStudentDraft",
            "PracticeEnglish",
            "BrainstormStory",
            "GenerateTeacherDraft",
            "GenerateImagePrompt",
          ].map((m) => (
            <option key={m}>{m}</option>
          ))}
        </select>
      </label>
      <label>
        Mẫu hướng dẫn
        <textarea
          maxLength={3000}
          value={template}
          onChange={(e) => setTemplate(e.target.value)}
        />
      </label>
      <button className="button secondary" onClick={() => void act()}>
        Lưu mẫu nháp
      </button>
      <label>
        Mật khẩu xác nhận duyệt
        <input
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      {list.loading ? (
        <Loading />
      ) : list.error ? (
        <ErrorState message={list.error} retry={list.retry} />
      ) : (
        list.data
          ?.filter((p) => p.mode === mode)
          .map((p) => (
            <article className="academy-artifact" key={p.version}>
              <h3>
                Phiên bản {p.version} ·{" "}
                {p.status === "approved"
                  ? "Đã duyệt"
                  : p.status === "draft"
                    ? "Bản nháp"
                    : "Lưu trữ"}
              </h3>
              <p>{p.template}</p>
              {p.status === "draft" && (
                <button
                  className="button secondary"
                  onClick={() => void act(p.version)}
                >
                  Duyệt mẫu này
                </button>
              )}
            </article>
          ))
      )}
      <p role="status">{message}</p>
    </section>
  );
}
