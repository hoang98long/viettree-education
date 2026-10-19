import type { CatalogLesson } from "./types";

export type LessonFilter = "all" | "available" | "started" | "completed";

function searchable(text: string) {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase();
}

export function filterLessons(
  rows: CatalogLesson[],
  filter: LessonFilter,
  query: string,
) {
  const words = searchable(query.trim()).split(/\s+/).filter(Boolean);
  return rows.filter((row) => {
    if (filter === "available" && row.locked) return false;
    if (
      filter === "started" &&
      (!row.progress || row.progress.completed_at || row.locked)
    )
      return false;
    if (filter === "completed" && !row.progress?.completed_at) return false;
    const text = searchable(`${row.title} ${row.unit_title}`);
    return words.every((word) => text.includes(word));
  });
}

export function nextLesson(rows: CatalogLesson[]) {
  const available = rows.filter(
    (row) => !row.locked && !row.progress?.completed_at,
  );
  return (
    available
      .filter((row) => row.progress)
      .sort((a, b) =>
        (b.progress?.updated_at ?? "").localeCompare(
          a.progress?.updated_at ?? "",
        ),
      )[0] ?? available[0]
  );
}

export function gameLessons(rows: CatalogLesson[]) {
  return [...new Set(rows.map((row) => row.unit_id))].map((unit) => {
    const choices = rows.filter((row) => row.unit_id === unit);
    return (
      nextLesson(choices) ?? choices.find((row) => !row.locked) ?? choices[0]
    );
  });
}
