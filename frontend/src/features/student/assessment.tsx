"use client";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { ArrowRight, BookOpen } from "lucide-react";
import { api, dateLabel } from "@/lib/api";
import type { Assessment, Assignment } from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import { PageTitle } from "@/components/ui";
import { AccessBadge, LockedContent } from "@/features/membership/pages";
import { Resource } from "@/features/student/shared";

export function AssessmentIntro({ data }: { data: Assessment }) {
  const router = useRouter();
  const search = useSearchParams();
  const assignmentId = search.get("assignment_id");
  const assignments = useResource<Assignment[]>("/students/me/assignments");
  const task = assignments.data?.find(
    (item) => item.id === assignmentId && item.assessment_id === data.id,
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  if (data.locked)
    return (
      <>
        <PageTitle title={data.title} description={data.description} />
        <AccessBadge item={data} />
        <LockedContent code={data.lock_reason ?? undefined} />
      </>
    );
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${data.grade} > ${data.subject_name} > LUYỆN TẬP`}
        title={data.title}
        description={data.description}
      />
      <section className="panel assessment-intro">
        <span className="large-icon">
          <BookOpen size={40} />
        </span>
        <h2>Sẵn sàng thử sức chưa?</h2>
        <div className="intro-meta">
          <span>{data.item_count} câu hỏi</span>
          <span>{data.max_attempts} lượt tối đa</span>
          <span>
            {data.time_limit_seconds
              ? `${Math.round(data.time_limit_seconds / 60)} phút`
              : "Không giới hạn thời gian"}
          </span>
        </div>
        <p>
          Em có thể lưu câu trả lời và quay lại. Sau khi nộp, mình cùng xem lời
          giải để hiểu bài hơn nhé.
        </p>
        {assignmentId && (
          <p>
            {assignments.loading
              ? "Đang kiểm tra bài được giao…"
              : task
                ? `Bài được giao · Mở: ${dateLabel(task.available_at)}${task.due_at ? ` · Hạn nộp: ${dateLabel(task.due_at)}` : ""}`
                : "Chưa tìm thấy bài được giao cho em. Hãy quay lại góc học tập hoặc tải lại trang."}
          </p>
        )}
        {error && (
          <div className="notice error" role="alert">
            {error}
          </div>
        )}
        <button
          className="button"
          disabled={busy || Boolean(assignmentId && !task)}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              if (assignmentId && !task)
                throw new Error("Bài được giao chưa khả dụng");
              const assignment =
                task ??
                (await api<{ id: string }>(
                  `/students/me/assessments/${data.id}/assign-self`,
                  { method: "POST" },
                ));
              const attempt = await api<{ id: string }>("/attempts", {
                method: "POST",
                body: JSON.stringify({ assignment_id: assignment.id }),
              });
              router.push(`/student/attempts/${attempt.id}`);
            } catch (e) {
              setError((e as Error).message);
              setBusy(false);
            }
          }}
        >
          {busy ? "Đang mở bài…" : "Bắt đầu / Tiếp tục"}
          <ArrowRight size={18} />
        </button>
      </section>
    </>
  );
}

export function AssessmentPage({ id }: { id: string }) {
  return (
    <Resource<Assessment> path={`/assessments/${id}`}>
      {(data) => <AssessmentIntro data={data} />}
    </Resource>
  );
}
