"use client";
import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty, PageTitle } from "@/components/ui";
import type { Classroom } from "@/features/classrooms/types";
import { labels } from "@/features/classrooms/constants";
import { RecognitionBoard } from "@/features/classrooms/recognition";

export function StudentClassroom() {
  const classes = useResource<Classroom[]>("/classroom/classes");
  const achievements = useResource<{
    categories: { category: string; completed: number; score: number | null }[];
    reading_completed: number;
    note: string;
  }>("/classroom/my-achievements");
  const assignments = useResource<
    {
      id: string;
      kind: string;
      resource_id: string;
      assignment_id: string | null;
      title: string;
      class_name: string | null;
    }[]
  >("/classroom/my-assignments");
  const [chosen, setChosen] = useState("");
  const current =
    classes.data?.find((c) => c.id === chosen) || classes.data?.[0];
  return (
    <>
      <PageTitle
        title="Lớp và thành tích của em"
        description="Kết quả học của em luôn được giữ, dù học tự do hay trong lớp."
      />
      <section className="panel">
        <h2>Kết quả tháng này theo từng loại</h2>
        {achievements.loading ? (
          <Loading />
        ) : achievements.error ? (
          <ErrorState message={achievements.error} retry={achievements.retry} />
        ) : (
          <>
            <div className="three-columns">
              {achievements.data?.categories.map((c) => (
                <article className="panel" key={c.category}>
                  <h3>{labels[c.category]}</h3>
                  <p>
                    {c.completed} bài ·{" "}
                    {c.score === null ? "Chưa có điểm" : `${c.score}/100`}
                  </p>
                </article>
              ))}
            </div>
            <p>
              {achievements.data?.reading_completed} bài đã đọc.{" "}
              {achievements.data?.note}
            </p>
          </>
        )}
      </section>
      <section className="panel">
        <h2>Bài được giao cho em</h2>
        {assignments.loading ? (
          <Loading />
        ) : assignments.error ? (
          <ErrorState message={assignments.error} retry={assignments.retry} />
        ) : assignments.data?.length ? (
          assignments.data.map((a) => (
            <article className="list-row" key={a.id}>
              <span>
                {a.title} · {a.class_name || "Giao riêng"}
              </span>
              <Link
                className="button secondary small"
                href={
                  a.kind === "ai_lesson"
                    ? `/ai-academy/lessons/${a.resource_id}`
                    : a.kind === "lesson"
                      ? `/student/lessons/${a.resource_id}`
                      : `/student/assessments/${a.resource_id}`
                }
              >
                Mở bài được giao
              </Link>
            </article>
          ))
        ) : (
          <Empty>Em có thể chọn bài phù hợp trong thư viện để tự học.</Empty>
        )}
      </section>
      {classes.loading ? (
        <Loading />
      ) : classes.error ? (
        <ErrorState message={classes.error} retry={classes.retry} />
      ) : current ? (
        <>
          <label>
            Lớp của em
            <select
              value={current.id}
              onChange={(e) => setChosen(e.target.value)}
            >
              {classes.data?.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
          <RecognitionBoard key={current.id} classroom={current} />
        </>
      ) : (
        <Empty>
          Em đang học tự do. Khi nhà trường ghi danh, lớp của em sẽ xuất hiện ở
          đây.
        </Empty>
      )}
    </>
  );
}
