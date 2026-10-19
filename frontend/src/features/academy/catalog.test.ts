import { expect, it } from "vitest";
import { filterLessons, gameLessons, nextLesson } from "./catalog";
import type { CatalogLesson } from "./types";

function lesson(id: string, extra: Partial<CatalogLesson> = {}): CatalogLesson {
  return {
    id,
    code: `AI1-${id}`,
    title: "Robot tìm sách",
    minimum_plan_code: "free",
    locked: false,
    unit_id: "reason",
    unit_code: "AI1-reason",
    unit_title: "Giải thích lựa chọn",
    unit_position: 11,
    position: 1,
    hero: "hero",
    minutes: 10,
    progress: null,
    ...extra,
  };
}
const started = {
  next_step: 3,
  completed_at: null,
  updated_at: "2026-10-19T07:00:00Z",
};

it("học tiếp bài mở gần nhất, bỏ qua VIP bị thu hồi và bài hoàn thành", () => {
  const rows = [
    lesson("01"),
    lesson("39", { progress: started }),
    lesson("40", {
      locked: true,
      progress: { ...started, updated_at: "2026-10-19T09:00:00Z" },
    }),
    lesson("37", {
      progress: { ...started, updated_at: "2026-10-19T06:00:00Z" },
    }),
    lesson("02", { progress: { ...started, completed_at: "2026-10-19" } }),
  ];
  expect(nextLesson(rows)?.id).toBe("39");
  expect(nextLesson([rows[0], rows[2], rows[4]])?.id).toBe("01");
  expect(nextLesson([rows[2], rows[4]])).toBeUndefined();
});

it("tìm không dấu theo tên bài và chủ đề, kết hợp trạng thái", () => {
  const rows = [
    lesson("39", { progress: started }),
    lesson("40", { title: "Thẻ bị che kín", locked: true }),
    lesson("01", { progress: { ...started, completed_at: "2026-10-19" } }),
  ];
  expect(
    filterLessons(rows, "all", "  giai thich  sach ").map((row) => row.id),
  ).toEqual(["39", "01"]);
  expect(filterLessons(rows, "available", "the bi che")).toEqual([]);
  expect(filterLessons(rows, "started", "").map((row) => row.id)).toEqual([
    "39",
  ]);
  expect(filterLessons(rows, "completed", "").map((row) => row.id)).toEqual([
    "01",
  ]);
});

it("chọn trò chơi từ danh mục đúng lớp, ưu tiên bài miễn phí trong mỗi chủ đề", () => {
  const rows = [
    lesson("40", { locked: true }),
    lesson("39"),
    lesson("01", { unit_id: "around" }),
  ];
  expect(gameLessons(rows).map((row) => row.id)).toEqual(["39", "01"]);
  expect(gameLessons([])).toEqual([]);
});
