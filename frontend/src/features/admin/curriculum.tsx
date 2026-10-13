"use client";
import Link from "next/link";
import { useState } from "react";
import type { Curriculum } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { CurriculumMapPanel } from "@/features/curriculum/coverage";
import { Data } from "@/features/admin/shared";

export function CurriculumPage() {
  const [grade, setGrade] = useState(4);
  const [expanded, setExpanded] = useState(false);
  return (
    <>
      <PageTitle
        title="Chương trình học"
        description="Xem môn học, chủ đề, bài học và kỹ năng. Nội dung lớp 1–5 đã xuất bản."
      />
      <div className="filters">
        <label>
          Lớp
          <select
            aria-label="Lớp học liệu"
            value={grade}
            onChange={(e) => setGrade(Number(e.target.value))}
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <option key={value} value={value}>
                Lớp {value}
              </option>
            ))}
          </select>
        </label>
      </div>
      <CurriculumMapPanel key={`map:${grade}`} grade={grade} />
      <label className="check-label">
        <input
          type="checkbox"
          checked={expanded}
          onChange={(e) => setExpanded(e.target.checked)}
        />
        Mở toàn bộ danh sách bài theo chủ đề
      </label>
      <Data<Curriculum>
        key={`curriculum:${grade}`}
        path={`/admin/curriculum?grade=${grade}`}
      >
        {(data) => (
          <>
            {!data.topics.length && (
              <Empty>Chương trình lớp {grade} đang xây dựng.</Empty>
            )}
            {data.subjects.map((subject) => (
              <section className="panel curriculum-subject" key={subject.id}>
                <h2>{subject.name_vi}</h2>
                {data.topics
                  .filter((topic) => topic.subject_id === subject.id)
                  .map((topic) => (
                    <details key={`${topic.id}:${expanded}`} open={expanded}>
                      <summary>{topic.title}</summary>
                      {data.lessons
                        .filter((lesson) => lesson.topic_id === topic.id)
                        .map((lesson) => (
                          <div className="list-row" key={lesson.id}>
                            <span>{lesson.title}</span>
                            <Link
                              className="card-link"
                              href={`/admin/lessons/${lesson.id}/edit`}
                            >
                              Biên soạn
                            </Link>
                            <span className="badge">{lesson.status}</span>
                          </div>
                        ))}
                    </details>
                  ))}
                <p className="muted">
                  Kỹ năng:{" "}
                  {data.skills
                    .filter((skill) => skill.subject_id === subject.id)
                    .map((skill) => skill.name)
                    .join(" · ") || "Đang xây dựng"}
                </p>
              </section>
            ))}
          </>
        )}
      </Data>
    </>
  );
}
