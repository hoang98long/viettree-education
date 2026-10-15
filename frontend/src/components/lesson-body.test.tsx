import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { LessonBody, LessonFigure } from "./lesson-body";
import type { LessonContent } from "@/lib/types";

const content: LessonContent = {
  blocks: [
    {
      type: "text",
      title: "Cùng khám phá",
      text: "Các phần có kích thước bằng nhau.",
    },
  ],
  goals: ["Đọc một phân số"],
  hints: ["Chọn cùng một đơn vị.", "Đếm tổng số phần bằng nhau."],
  reflection: ["Em giải thích 3/8 như thế nào?"],
  illustration: {
    kind: "fraction",
    caption: "Ba trong tám phần bằng nhau được tô màu.",
    numerator: 3,
    denominator: 8,
    rows: 3,
    columns: 4,
    hour: 8,
    minute: 0,
  },
};

describe("Bài học có minh họa và hướng dẫn", () => {
  it("ô vuông 1 m² có hai cạnh bằng nhau ở cả luống dài và luống cao", () => {
    const figure = { ...content.illustration!, kind: "garden" as const };
    const { container, rerender } = render(<LessonFigure value={figure} />);
    for (const [rows, columns] of [
      [3, 4],
      [1, 8],
      [6, 1],
    ]) {
      rerender(<LessonFigure value={{ ...figure, rows, columns }} />);
      const cells = container.querySelectorAll("svg g rect");
      expect(cells).toHaveLength(rows * columns);
      for (const cell of cells) {
        expect(cell.getAttribute("width")).toBe(cell.getAttribute("height"));
        expect(Number(cell.getAttribute("x"))).toBeGreaterThanOrEqual(0);
        expect(Number(cell.getAttribute("y"))).toBeGreaterThanOrEqual(54);
      }
      expect(
        screen.getByText(
          `${rows} × ${columns} = ${rows * columns} m² · Chu vi: ${2 * (rows + columns)} m`,
        ),
      ).toBeVisible();
    }
  });
  it("chỉ mở gợi ý backend đã cấp và hiển thị quyền lợi VIP", () => {
    render(
      <LessonBody
        content={{ ...content, hints: [content.hints![0]] }}
        hintAccess={{ available: 1, total: 3, vip_locked: 2 }}
      />,
    );
    expect(
      screen.getByRole("link", { name: "Tìm hiểu gợi ý VIP" }),
    ).toHaveAttribute("href", "/student/membership");
    fireEvent.click(screen.getByRole("button", { name: "Mở gợi ý 1" }));
    expect(
      screen.getByRole("button", { name: "Đã mở hết gợi ý" }),
    ).toBeDisabled();
    expect(screen.queryByText(content.hints![1])).not.toBeInTheDocument();
  });
  it("biểu đồ có số liệu, nhãn và thang; góc được phân loại theo số đo", () => {
    const figure = {
      ...content.illustration!,
      kind: "bars" as const,
      values: [12, 16, 20],
      labels: ["A", "B", "C"],
      tick: 4,
      caption: "Số cây ba tổ trồng được",
    };
    const { container, rerender } = render(<LessonFigure value={figure} />);
    expect(screen.getByRole("img", { name: figure.caption })).toBeVisible();
    expect(screen.getByText("A")).toBeVisible();
    const svgText = Array.from(container.querySelectorAll("svg text")).map(
      (el) => el.textContent,
    );
    expect(svgText).toEqual(
      expect.arrayContaining(["0", "4", "8", "12", "16", "20"]),
    );
    rerender(
      <LessonFigure
        value={{
          ...figure,
          kind: "angles",
          angle: 120,
          caption: "Góc tù 120 độ",
        }}
      />,
    );
    expect(screen.getByText("120°")).toBeVisible();
    expect(screen.getByText("Góc tù")).toBeVisible();
    rerender(<LessonFigure value={{ ...figure, kind: "angles", angle: 90 }} />);
    expect(screen.getByText("Góc vuông")).toBeVisible();
  });
  it("mở gợi ý từng bước, chặn vượt số bước và giữ ghi chú khi mở thêm", () => {
    render(<LessonBody content={content} />);
    expect(screen.queryByText(content.hints![0])).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(content.reflection![0]), {
      target: { value: "Em chia bánh thành tám phần." },
    });
    fireEvent.click(screen.getByRole("button", { name: "Mở gợi ý 1" }));
    expect(screen.getByText(content.hints![0])).toBeVisible();
    expect(screen.queryByText(content.hints![1])).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Mở gợi ý 2" }));
    expect(
      screen.getByRole("button", { name: "Đã mở hết gợi ý" }),
    ).toBeDisabled();
    expect(screen.getByRole("status")).toHaveTextContent("Đã mở 2/2 gợi ý.");
    expect(screen.getByLabelText(content.reflection![0])).toHaveValue(
      "Em chia bánh thành tám phần.",
    );
    expect(
      screen.getByRole("img", { name: content.illustration!.caption }),
    ).toBeVisible();
  });
  it("nội dung chữ không được thực thi như HTML", () => {
    const { container } = render(
      <LessonBody
        content={{
          blocks: [
            {
              type: "text",
              title: "Câu chuyện",
              text: '<img src=x onerror="alert(1)">',
            },
          ],
        }}
      />,
    );
    expect(container.querySelector("img")).toBeNull();
    expect(screen.getByText('<img src=x onerror="alert(1)">')).toBeVisible();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
  it("hai bài xem trước có mục lục và hình với định danh riêng", () => {
    const { container } = render(
      <>
        <LessonBody content={content} />
        <LessonBody content={content} />
      </>,
    );
    const ids = Array.from(container.querySelectorAll("[id]")).map(
      (node) => node.id,
    );
    expect(new Set(ids).size).toBe(ids.length);
    for (const link of container.querySelectorAll<HTMLAnchorElement>(
      ".lesson-outline a",
    )) {
      expect(document.getElementById(link.hash.slice(1))).not.toBeNull();
    }
  });
});
