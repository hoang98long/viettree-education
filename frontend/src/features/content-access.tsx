"use client";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { api } from "@/lib/api";
import { ErrorState, Loading, PageTitle } from "@/components/ui";
import { AccessBadge } from "@/features/membership";
import type { ContentAccess } from "@/lib/types";

type Resource = ContentAccess & {
  id: string;
  title: string;
  kind: "lesson" | "assessment";
  subject_name: string;
  status: string;
  configured_plan_code: string | null;
  preview: { summary?: string; goals?: string[] } | null;
};
function PolicyEditor({ item, close }: { item: Resource; close: () => void }) {
  const [plan, setPlan] = useState(item.configured_plan_code ?? "free");
  const [level, setLevel] = useState(item.learning_level);
  const [summary, setSummary] = useState(item.preview?.summary ?? "");
  const [goal, setGoal] = useState(item.preview?.goals?.join("\n") ?? "");
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  return (
    <div className="modal-backdrop">
      <section
        className="modal wide"
        role="dialog"
        aria-modal="true"
        aria-labelledby="policy-title"
      >
        <h2 id="policy-title">Quyền nội dung · {item.title}</h2>
        <form
          onSubmit={async (event) => {
            event.preventDefault();
            setBusy(true);
            setError("");
            try {
              await api(`/admin/content/${item.kind}/${item.id}/policy`, {
                method: "PUT",
                body: JSON.stringify({
                  minimum_plan_code: plan,
                  learning_level: level,
                  preview: {
                    summary,
                    goals: goal
                      .split("\n")
                      .map((value) => value.trim())
                      .filter(Boolean),
                  },
                  reason,
                }),
              });
              close();
            } catch (e) {
              setError((e as Error).message);
              setBusy(false);
            }
          }}
        >
          <label>
            Gói tối thiểu
            <select
              autoFocus
              value={plan}
              onChange={(e) => setPlan(e.target.value)}
            >
              <option value="free">Miễn phí</option>
              <option value="vip">VIP</option>
            </select>
          </label>
          <label>
            Mức nội dung
            <select
              value={level}
              onChange={(e) =>
                setLevel(e.target.value as Resource["learning_level"])
              }
            >
              <option value="basic">Nền tảng</option>
              <option value="reinforcement">Củng cố</option>
              <option value="advanced">Nâng cao</option>
            </select>
          </label>
          <label>
            Đoạn giới thiệu
            <textarea
              value={summary}
              maxLength={350}
              onChange={(e) => setSummary(e.target.value)}
            />
          </label>
          <label>
            Mục tiêu học (tối đa 5 dòng, mỗi dòng 120 ký tự)
            <textarea value={goal} onChange={(e) => setGoal(e.target.value)} />
          </label>
          <label>
            Lý do thay đổi
            <textarea
              value={reason}
              required
              minLength={5}
              maxLength={500}
              onChange={(e) => setReason(e.target.value)}
            />
          </label>
          <p>
            Đề có bài học hoặc câu hỏi dùng trong nội dung VIP vẫn yêu cầu VIP,
            kể cả khi chọn nhãn miễn phí cho riêng đề.
          </p>
          {error && (
            <p role="alert" className="error-text">
              {error}
            </p>
          )}
          <div className="quiz-actions">
            <button
              type="button"
              className="button secondary"
              disabled={busy}
              onClick={close}
            >
              Đóng
            </button>
            <button className="button" disabled={busy}>
              {busy ? "Đang lưu…" : "Lưu quyền nội dung"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
export function ContentAccessPage() {
  const resource = useResource<Resource[]>("/admin/content-access");
  const [selected, setSelected] = useState<Resource | null>(null);
  const [filter, setFilter] = useState("all");
  if (resource.loading) return <Loading />;
  if (resource.error)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  return (
    <>
      <PageTitle
        title="Quyền nội dung Free / VIP"
        description="Phân loại gói học độc lập với độ khó. Mọi thay đổi được lưu audit."
      />
      <label className="content-filter">
        Lọc gói
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">Tất cả</option>
          <option value="free">Miễn phí</option>
          <option value="vip">VIP</option>
        </select>
      </label>
      <section className="panel">
        {resource.data
          ?.filter(
            (item) => filter === "all" || item.minimum_plan_code === filter,
          )
          .map((item) => (
            <div className="list-row" key={`${item.kind}:${item.id}`}>
              <div>
                <strong>{item.title}</strong>
                <small>
                  {item.subject_name} ·{" "}
                  {item.kind === "lesson" ? "Bài học" : "Bài luyện"} ·{" "}
                  {item.status}
                </small>
              </div>
              <AccessBadge item={item} />
              <button
                className="button secondary small"
                onClick={() => setSelected(item)}
              >
                Cấu hình quyền
              </button>
            </div>
          ))}
      </section>
      {selected && (
        <PolicyEditor
          key={selected.id}
          item={selected}
          close={() => {
            setSelected(null);
            resource.retry();
          }}
        />
      )}
    </>
  );
}
