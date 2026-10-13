"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight, Check } from "lucide-react";
import { api } from "@/lib/api";
import type { Lesson } from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading, PageTitle } from "@/components/ui";
import { LessonBody } from "@/components/lesson-body";
import { LessonPreviewPanel } from "@/features/membership/pages";

export function LessonContent({ data }: { data: Lesson }) {
  const [completed, setCompleted] = useState(
    data.progress_status === "completed",
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    api(`/lessons/${data.id}/visit`, { method: "POST" }).catch(() => {});
  }, [data.id]);
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${data.grade} > ${data.subject_name} > ${data.topic_title}`}
        title={data.title}
        description={`${data.estimated_minutes} phút · Đọc chậm rãi theo nhịp của em`}
      />
      <LessonBody content={data.content} hintAccess={data.hint_access} />
      <section className="panel lesson-completion">
        <h2>{completed ? "Em đã đọc xong bài này" : "Em đã đọc xong chưa?"}</h2>
        <p>
          Đánh dấu để lưu tiến độ đọc của em. Bài luyện tập sẽ giúp em kiểm tra
          điều mình đã hiểu.
        </p>
        <button
          className="button"
          disabled={busy || completed}
          onClick={async () => {
            setBusy(true);
            setError("");
            try {
              await api(`/lessons/${data.id}/complete`, { method: "POST" });
              setCompleted(true);
            } catch (e) {
              setError((e as Error).message);
            } finally {
              setBusy(false);
            }
          }}
        >
          <Check size={20} />
          {completed
            ? "Đã đánh dấu đọc xong"
            : busy
              ? "Đang lưu…"
              : "Em đã đọc xong"}
        </button>
        <p role="status" aria-live="polite">
          {completed ? "Tiến độ đọc và kế hoạch học đã được cập nhật." : ""}
        </p>
        {error && (
          <p className="error-text" role="alert">
            {error}
          </p>
        )}
        <Link className="card-link" href="/student/learning-plan">
          Xem kế hoạch học <ArrowRight size={18} />
        </Link>
      </section>
      <section className="panel">
        <h2>Đến lượt em thử sức</h2>
        {!data.practice.length && (
          <p>
            Chưa có bài luyện đã xuất bản cho chủ đề này. Em có thể ôn lại ví dụ
            và trao đổi với người thân.
          </p>
        )}
        {data.practice.map((item) => (
          <Link
            className="list-row"
            key={item.id}
            href={`/student/assessments/${item.id}`}
          >
            {item.title}
            <ArrowRight size={18} />
          </Link>
        ))}
      </section>
      {!!data.next_lessons?.length && (
        <section className="panel lesson-next">
          <h2>Em có thể khám phá tiếp</h2>
          <p>Gợi ý từ bài cùng chủ đề mà em chưa đánh dấu đọc xong.</p>
          {data.next_lessons.map((item) => (
            <Link
              className="list-row"
              key={item.id}
              href={`/student/lessons/${item.id}`}
            >
              <span>{item.title}</span>
              <ArrowRight size={18} />
            </Link>
          ))}
        </section>
      )}
    </>
  );
}

export function LessonPage({ id }: { id: string }) {
  const resource = useResource<Lesson>(`/lessons/${id}`);
  if (resource.loading) return <Loading />;
  if (resource.errorCode === "MEMBERSHIP_REQUIRED")
    return <LessonPreviewPanel id={id} />;
  if (resource.error || !resource.data)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  return <LessonContent key={resource.data.id} data={resource.data} />;
}
