import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { ResumeLearning, resumePath } from "./resume-learning";
import type { ResumeItem } from "@/lib/types";

const items: ResumeItem[] = [
  {
    kind: "ai",
    id: "ai-lesson",
    title: "Đếm lại cùng robot",
    grade: 1,
    subject_name: "Khám phá AI",
    last_activity_at: "2026-10-17T00:00:00Z",
    next_step: 3,
    step_count: 7,
  },
  {
    kind: "practice",
    id: "attempt",
    title: "Thử tính",
    grade: 1,
    subject_name: "Toán",
    last_activity_at: "2026-10-16T00:00:00Z",
  },
  {
    kind: "lesson",
    id: "reading",
    title: "Bút của Hà",
    grade: 1,
    subject_name: "Tiếng Việt",
    last_activity_at: "2026-10-15T00:00:00Z",
  },
];

it("mở đúng bài đang làm, không tạo lượt mới; hiển thị bước AI và giữ thứ tự", () => {
  render(<ResumeLearning items={items} />);
  const links = screen.getAllByRole("link");
  expect(links.map((link) => link.getAttribute("href"))).toEqual([
    "/ai-academy/lessons/ai-lesson",
    "/student/attempts/attempt",
    "/student/lessons/reading",
  ]);
  expect(screen.getByText("Bước 4/7")).toBeVisible();
  expect(resumePath(items[1])).toBe("/student/attempts/attempt");
});

it("ẩn vùng học tiếp khi không có việc đang dở", () => {
  render(<ResumeLearning items={[]} />);
  expect(
    screen.queryByRole("region", { name: "Việc học đang dở" }),
  ).not.toBeInTheDocument();
});
