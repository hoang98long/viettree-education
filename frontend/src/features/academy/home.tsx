"use client";
import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty, PageTitle } from "@/components/ui";
import { AcademyImage } from "./shared";
import type { CatalogLesson } from "./types";

export function Journey({ grade }: { grade?: number }) {
  const home = useResource<{
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
  }>("/ai-academy/home");
  const [chosen, setChosen] = useState<number | null>(null);
  const selected = chosen ?? grade ?? home.data?.grade ?? 4;
  const catalog = useResource<CatalogLesson[]>(
    `/ai-academy/catalog?grade=${selected}`,
  );
  if (home.loading) return <Loading />;
  if (home.error) return <ErrorState message={home.error} retry={home.retry} />;
  const next = catalog.data?.find(
    (l) => !l.locked && !l.progress?.completed_at,
  );
  const units = [...new Set(catalog.data?.map((l) => l.unit_id) || [])];
  return (
    <>
      <section className="academy-hero">
        <div>
          <span className="eyebrow">VIETTREE AI ACADEMY</span>
          <h1>Khám phá AI, sáng tạo an toàn</h1>
          <p>
            Em quan sát, thử làm và kiểm tra. Mầm AI sẽ đưa em qua những câu
            chuyện bằng tranh.
          </p>
          <p>
            Học lý thuyết và bài tập đơn giản, không cần dùng mô hình AI. Lớp 4
            có 3 bài nhập môn miễn phí; VIP mở thêm 33 tiết cùng phòng thực hành
            và dự án.
          </p>
          <Link className="button secondary" href="/student/membership">
            Xem gói VIP cùng phụ huynh
          </Link>
          <p>
            {home.data?.completed} bài đã khám phá · {home.data?.points} điểm
            ghi nhận
          </p>
          {next && (
            <Link className="button" href={`/ai-academy/lessons/${next.id}`}>
              Tiếp tục khám phá
            </Link>
          )}
          <p className="muted">
            Mô phỏng và học liệu đã biên soạn. Không cần khóa AI, camera hay
            microphone.
          </p>
        </div>
        <AcademyImage
          code="mascot-0"
          alt="Mầm AI chào em, robot minh họa thân thiện"
          small
        />
      </section>
      {!!home.data?.assignments.length && (
        <section className="panel">
          <h2>Bài được thầy cô giao</h2>
          <div className="academy-cards">
            {home.data.assignments.map((a) => (
              <article className="academy-card" key={a.id}>
                <h3>{a.title}</h3>
                <p>
                  {a.class_name} ·{" "}
                  {a.completed_at ? "Đã hoàn thành" : "Đang chờ em khám phá"}
                </p>
                <Link
                  className="button secondary"
                  href={`/ai-academy/lessons/${a.lesson_id}`}
                >
                  {a.completed_at ? "Ôn lại bài" : "Học bài được giao"}
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
          onChange={(e) => setChosen(Number(e.target.value))}
        >
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n} value={n}>
              Lớp {n}
              {n === home.data?.grade ? " · Lớp của em" : ""}
            </option>
          ))}
        </select>
      </label>
      {selected > (home.data?.grade ?? 4) && (
        <p className="notice">
          Em xem hành trình; bài học được mở ở lớp hiện tại và các lớp dưới.
        </p>
      )}
      <PageTitle
        title={
          selected === 4
            ? "36 tiết · 9 chủ đề"
            : `Khung lớp ${selected} · 3 bài mẫu`
        }
        description="Chọn một bài học. Thực hành từng bước, thử lại và đọc giải thích."
      />
      {catalog.loading ? (
        <Loading />
      ) : catalog.error ? (
        <ErrorState message={catalog.error} retry={catalog.retry} />
      ) : units.length ? (
        units.map((id) => {
          const rows = catalog.data!.filter((l) => l.unit_id === id);
          return (
            <section key={id} className="panel academy-unit">
              <h2>
                {rows[0].unit_position}. {rows[0].unit_title}
              </h2>
              {rows[0].unit_cover && (
                <div className="academy-unit-cover">
                  <AcademyImage
                    code={rows[0].unit_cover}
                    alt={`Bìa chủ đề ${rows[0].unit_title}`}
                  />
                </div>
              )}
              <div className="academy-cards">
                {rows.map((l) => (
                  <Link
                    className="academy-card"
                    key={l.id}
                    href={`/ai-academy/lessons/${l.id}`}
                  >
                    <AcademyImage code={l.hero} alt={`Tình huống ${l.title}`} />
                    <strong>{l.title}</strong>
                    <span
                      className={`badge ${l.minimum_plan_code === "vip" ? "vip-badge" : "success"}`}
                    >
                      {l.locked
                        ? "🔒 VIP"
                        : l.minimum_plan_code === "vip"
                          ? "VIP"
                          : "Miễn phí"}
                    </span>
                    <span>
                      {l.minutes} phút ·{" "}
                      {l.progress?.completed_at
                        ? "Đã hoàn thành"
                        : l.progress
                          ? "Đang khám phá"
                          : "Bắt đầu"}
                    </span>
                  </Link>
                ))}
              </div>
            </section>
          );
        })
      ) : (
        <Empty>Chủ đề đang được biên soạn.</Empty>
      )}
    </>
  );
}

export function GameCenter() {
  const { data, loading, error, retry } = useResource<CatalogLesson[]>(
    "/ai-academy/catalog?grade=4",
  );
  const entries = [
    ["Phân loại hình ảnh", 4],
    ["Ghép nhãn và thẻ", 19],
    ["Xếp bước thuật toán", 13],
    ["Học từ ví dụ", 5],
    ["Thử dữ liệu thiếu", 6],
    ["Prompt Builder", 8],
    ["Kiểm tra bằng chứng", 10],
    ["Bậc thang gợi ý Toán", 11],
    ["Truyện bốn khung", 24],
    ["Hội thoại tiếng Anh", 20],
  ] as const;
  return (
    <>
      <PageTitle
        title="Trò chơi học tập"
        description="Chọn/chạm hoặc dùng bàn phím. Có ba mức hỗ trợ; thử lại không bị phạt."
      />
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorState message={error} retry={retry} />
      ) : (
        <div className="academy-cards">
          {entries.map(([title, number]) => {
            const l = data?.find(
              (row) => row.code === `AI4-${String(number).padStart(2, "0")}`,
            );
            return l ? (
              <Link
                className="academy-card"
                href={`/ai-academy/lessons/${l.id}`}
                key={title}
              >
                <AcademyImage code={l.hero} alt={title} />
                <strong>{title}</strong>
                <span className="badge">
                  {l.locked ? "🔒 VIP" : "Có thể học"}
                </span>
                <span>Mở tình huống và hoạt động trong bài</span>
              </Link>
            ) : null;
          })}
        </div>
      )}
      <Link className="button secondary" href="/ai-academy/lab">
        Thử bộ phân loại và thiên lệch dữ liệu
      </Link>
    </>
  );
}
