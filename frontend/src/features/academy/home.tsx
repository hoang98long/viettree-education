"use client";
import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty, PageTitle } from "@/components/ui";
import { AcademyImage } from "./shared";
import {
  filterLessons,
  gameLessons,
  nextLesson,
  type LessonFilter,
} from "./catalog";
import type { CatalogLesson } from "./types";

type AcademyHome = {
  grade: number;
  catalog: CatalogLesson[];
  points: number;
  completed: number;
  assignments: {
    id: string;
    lesson_id: string;
    title: string;
    class_name: string;
    completed_at: string | null;
  }[];
};

function PlanBadge({ lesson }: { lesson: CatalogLesson }) {
  return (
    <span
      className={`badge ${lesson.minimum_plan_code === "vip" ? "vip-badge" : "success"}`}
    >
      {lesson.locked
        ? "🔒 VIP"
        : lesson.minimum_plan_code === "vip"
          ? "VIP"
          : "Miễn phí"}
    </span>
  );
}

function LessonLibrary({
  rows,
  canStudy,
  grade,
}: {
  rows: CatalogLesson[];
  canStudy: boolean;
  grade: number;
}) {
  const [filter, setFilter] = useState<LessonFilter>("all");
  const [query, setQuery] = useState("");
  const next = canStudy ? nextLesson(rows) : undefined;
  const filtered =
    !canStudy && (filter === "available" || filter === "started")
      ? []
      : filterLessons(rows, filter, query);
  const units = [...new Set(filtered.map((row) => row.unit_id))];
  const totalUnits = new Set(rows.map((row) => row.unit_id)).size;
  const narrowed = filter !== "all" || query.trim().length > 0;
  return (
    <>
      {next && (
        <section className="panel academy-resume" aria-label="Bài AI tiếp theo">
          <AcademyImage code={next.hero} alt={`Bài ${next.title}`} small />
          <div>
            <p className="eyebrow">
              {next.progress ? "BÀI EM ĐANG HỌC" : "BẮT ĐẦU TỪ ĐÂY"}
            </p>
            <h2>{next.title}</h2>
            <Link className="button" href={`/ai-academy/lessons/${next.id}`}>
              {next.progress ? "Học tiếp bài này" : "Tiếp tục khám phá"}
            </Link>
          </div>
        </section>
      )}
      <PageTitle
        title={`Lớp ${grade} · ${rows.length} bài · ${totalUnits} chủ đề`}
        description="Chọn tranh để mở bài học."
      />
      <section className="panel academy-catalog-tools" aria-label="Tìm bài AI">
        <label>
          Tìm tên bài hoặc chủ đề
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Ví dụ: sách, robot…"
          />
        </label>
        <div
          className="academy-filter-buttons"
          role="group"
          aria-label="Lọc bài AI"
        >
          {(
            [
              ["all", "Tất cả"],
              ["available", "Em có thể học"],
              ["started", "Đang học"],
              ["completed", "Đã xong"],
            ] as const
          ).map(([value, label]) => (
            <button
              key={value}
              type="button"
              className="button secondary"
              aria-pressed={filter === value}
              onClick={() => setFilter(value)}
            >
              {label}
            </button>
          ))}
        </div>
        <p role="status">
          {filtered.length} bài{narrowed ? " phù hợp" : " trong hành trình"}
        </p>
        {narrowed && (
          <button
            className="button secondary"
            onClick={() => {
              setFilter("all");
              setQuery("");
            }}
          >
            Xem tất cả bài
          </button>
        )}
      </section>
      {units.length ? (
        units.map((id, index) => {
          const lessons = filtered.filter((row) => row.unit_id === id);
          return (
            <details
              key={`${id}-${filter}-${query}`}
              className="panel academy-unit"
              open={narrowed || id === next?.unit_id || (!next && index === 0)}
            >
              <summary>
                <h2>
                  {lessons[0].unit_position}. {lessons[0].unit_title}
                </h2>
                <span>{lessons.length} bài · Mở chủ đề</span>
              </summary>
              {lessons[0].unit_cover && (
                <div className="academy-unit-cover">
                  <AcademyImage
                    code={lessons[0].unit_cover}
                    alt={`Bìa chủ đề ${lessons[0].unit_title}`}
                  />
                </div>
              )}
              <div className="academy-cards">
                {lessons.map((lesson) => (
                  <Link
                    className="academy-card"
                    key={lesson.id}
                    href={`/ai-academy/lessons/${lesson.id}`}
                  >
                    <AcademyImage
                      code={lesson.hero}
                      alt={`Tình huống ${lesson.title}`}
                    />
                    <strong>{lesson.title}</strong>
                    <PlanBadge lesson={lesson} />
                    <span>
                      {lesson.minutes} phút ·{" "}
                      {lesson.progress?.completed_at
                        ? "Đã hoàn thành"
                        : lesson.progress
                          ? "Đang khám phá"
                          : "Bắt đầu"}
                    </span>
                  </Link>
                ))}
              </div>
            </details>
          );
        })
      ) : (
        <Empty>
          {rows.length
            ? "Chưa có bài phù hợp. Em thử từ khác hoặc xem tất cả bài nhé."
            : "Chủ đề đang được biên soạn."}
        </Empty>
      )}
    </>
  );
}

function OtherGradeLibrary({
  grade,
  canStudy,
}: {
  grade: number;
  canStudy: boolean;
}) {
  const catalog = useResource<CatalogLesson[]>(
    `/ai-academy/catalog?grade=${grade}`,
  );
  if (catalog.loading) return <Loading />;
  if (catalog.error)
    return <ErrorState message={catalog.error} retry={catalog.retry} />;
  return (
    <LessonLibrary
      key={grade}
      rows={catalog.data ?? []}
      canStudy={canStudy}
      grade={grade}
    />
  );
}

export function Journey({ grade }: { grade?: number }) {
  const home = useResource<AcademyHome>("/ai-academy/home");
  const [chosen, setChosen] = useState<number | null>(null);
  if (home.loading) return <Loading />;
  if (home.error || !home.data)
    return (
      <ErrorState
        message={home.error || "Chưa tải được hành trình."}
        retry={home.retry}
      />
    );
  const selected = chosen ?? grade ?? home.data.grade;
  return (
    <>
      <section className="academy-hero">
        <div>
          <span className="eyebrow">VIETTREE AI ACADEMY</span>
          <h1>Khám phá AI, sáng tạo an toàn</h1>
          <p>Xem tranh. Chạm chọn. Thử lại cùng Mầm AI.</p>
          <Link className="button secondary" href="/student/membership">
            Xem gói VIP cùng phụ huynh
          </Link>
          <p>
            {home.data.completed} bài đã khám phá · {home.data.points} điểm ghi
            nhận
          </p>
        </div>
        <AcademyImage
          code="mascot-0"
          alt="Mầm AI chào em, robot minh họa thân thiện"
          small
        />
      </section>
      {!!home.data.assignments.length && (
        <section className="panel">
          <h2>Bài được thầy cô giao</h2>
          <div className="academy-cards">
            {home.data.assignments.map((assignment) => (
              <article className="academy-card" key={assignment.id}>
                <h3>{assignment.title}</h3>
                <p>
                  {assignment.class_name} ·{" "}
                  {assignment.completed_at
                    ? "Đã hoàn thành"
                    : "Đang chờ em khám phá"}
                </p>
                <Link
                  className="button secondary"
                  href={`/ai-academy/lessons/${assignment.lesson_id}`}
                >
                  {assignment.completed_at ? "Ôn lại bài" : "Học bài được giao"}
                </Link>
              </article>
            ))}
          </div>
        </section>
      )}
      <label className="academy-grade">
        Chọn lớp để khám phá
        <select
          value={selected}
          onChange={(event) => setChosen(Number(event.target.value))}
        >
          {[1, 2, 3, 4, 5].map((number) => (
            <option key={number} value={number}>
              Lớp {number}
              {number === home.data!.grade ? " · Lớp của em" : ""}
            </option>
          ))}
        </select>
      </label>
      {selected > home.data.grade && (
        <p className="notice">
          Em xem hành trình; bài học được mở ở lớp hiện tại và các lớp dưới.
        </p>
      )}
      {selected === home.data.grade ? (
        <LessonLibrary
          key={selected}
          rows={home.data.catalog}
          grade={selected}
          canStudy
        />
      ) : (
        <OtherGradeLibrary
          key={selected}
          grade={selected}
          canStudy={selected <= home.data.grade}
        />
      )}
    </>
  );
}

export function GameCenter() {
  const home = useResource<AcademyHome>("/ai-academy/home");
  const [onlyAvailable, setOnlyAvailable] = useState(false);
  if (home.loading) return <Loading />;
  if (home.error || !home.data)
    return (
      <ErrorState
        message={home.error || "Chưa tải được trò chơi."}
        retry={home.retry}
      />
    );
  const rows = gameLessons(home.data.catalog);
  const entries = onlyAvailable ? rows.filter((row) => !row.locked) : rows;
  return (
    <>
      <PageTitle
        title={`Trò chơi học tập · Lớp ${home.data.grade}`}
        description="Mỗi tranh mở một bài có hoạt động chạm chọn. Thử lại không bị phạt."
      />
      <div
        className="academy-filter-buttons"
        role="group"
        aria-label="Lọc trò chơi"
      >
        <button
          className="button secondary"
          aria-pressed={!onlyAvailable}
          onClick={() => setOnlyAvailable(false)}
        >
          Tất cả chủ đề
        </button>
        <button
          className="button secondary"
          aria-pressed={onlyAvailable}
          onClick={() => setOnlyAvailable(true)}
        >
          Em có thể học
        </button>
      </div>
      <div className="academy-cards">
        {entries.map((lesson) => (
          <Link
            className="academy-card"
            href={`/ai-academy/lessons/${lesson.id}`}
            key={lesson.id}
          >
            <AcademyImage code={lesson.hero} alt={lesson.title} />
            <span className="eyebrow">{lesson.unit_title}</span>
            <strong>{lesson.title}</strong>
            <PlanBadge lesson={lesson} />
            <span>
              {lesson.progress?.completed_at
                ? "Chơi và ôn lại"
                : lesson.progress
                  ? "Tiếp tục hoạt động"
                  : "Mở hoạt động trong bài"}
            </span>
          </Link>
        ))}
      </div>
      {!entries.length && <Empty>Chưa có hoạt động phù hợp.</Empty>}
      <Link className="button secondary" href="/ai-academy">
        Xem toàn bộ bài AI
      </Link>
      <Link className="button secondary" href="/ai-academy/lab">
        Thử bộ phân loại và thiên lệch dữ liệu · VIP
      </Link>
    </>
  );
}
