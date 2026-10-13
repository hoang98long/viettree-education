import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { LessonFigure } from "./lesson-body";
import type { LessonIllustration } from "@/lib/types";

const figure: LessonIllustration = {
  kind: "triangle",
  caption: "Tam giác có đáy 6 cm, chiều cao 4 cm.",
  numerator: 3,
  denominator: 8,
  rows: 3,
  columns: 4,
  hour: 8,
  minute: 0,
  base: 6,
  upper_base: 4,
  height: 4,
  radius: 2,
  length: 6,
  width: 4,
};

describe("Minh họa lớp 5", () => {
  it("có nhãn số đo rõ và tên hình cho trình đọc màn hình", () => {
    const { rerender } = render(<LessonFigure value={figure} />);
    expect(screen.getByRole("img", { name: figure.caption })).toBeVisible();
    expect(screen.getByText("Đáy 6 cm")).toBeVisible();
    expect(screen.getByText("Cao 4 cm")).toBeVisible();
    rerender(
      <LessonFigure value={{ ...figure, kind: "circle", radius: 2.5 }} />,
    );
    expect(screen.getByText("r = 2.5 cm")).toBeVisible();
    expect(screen.getByText("d = 5 cm")).toBeVisible();
    rerender(<LessonFigure value={{ ...figure, kind: "box", height: 3 }} />);
    expect(screen.getByText("Dài 6 cm")).toBeVisible();
    expect(screen.getByText("Rộng 4 cm")).toBeVisible();
    expect(screen.getByText("Cao 3 cm")).toBeVisible();
  });
  it("biểu đồ có chú giải bằng chữ, giữ nhóm 0% và vẽ được nhóm 100%", () => {
    const { container, rerender } = render(
      <LessonFigure
        value={{
          ...figure,
          kind: "pie",
          labels: ["Đọc sách", "Thể thao", "Âm nhạc"],
          values: [50, 30, 20],
        }}
      />,
    );
    const legend = screen.getByRole("list");
    expect(legend).toHaveTextContent("Đọc sách: 50%");
    expect(legend).toHaveTextContent("Thể thao: 30%");
    expect(legend).toHaveTextContent("Âm nhạc: 20%");
    rerender(
      <LessonFigure
        value={{
          ...figure,
          kind: "pie",
          labels: ["Có", "Không"],
          values: [100, 0],
        }}
      />,
    );
    expect(screen.getByRole("list")).toHaveTextContent("Không: 0%");
    expect(container.querySelector("svg circle")).not.toBeNull();
    expect(container.innerHTML).not.toMatch(/NaN|Infinity/);
  });
  it("nhiều hình có định danh truy cập riêng", () => {
    const { container } = render(
      <>
        <LessonFigure value={figure} />
        <LessonFigure value={{ ...figure, kind: "trapezoid" }} />
      </>,
    );
    const imgs = screen.getAllByRole("img");
    expect(imgs[0].getAttribute("aria-labelledby")).not.toBe(
      imgs[1].getAttribute("aria-labelledby"),
    );
    for (const img of imgs)
      expect(
        container.querySelector(
          `[id="${img.getAttribute("aria-labelledby")}"]`,
        ),
      ).not.toBeNull();
  });
  it("hình thang vẫn nằm trong khung khi đáy phía trên dài hơn", () => {
    const { container } = render(
      <LessonFigure
        value={{
          ...figure,
          kind: "trapezoid",
          base: 0.1,
          upper_base: 1000,
          height: 4,
        }}
      />,
    );
    const outline = container.querySelector("svg path")!.getAttribute("d")!;
    expect(outline).not.toMatch(/[MHL]-/);
    const measurements = within(
      container.querySelector(".geometry-measures")! as HTMLElement,
    );
    expect(measurements.getByText("1000 cm")).toBeVisible();
    expect(measurements.getByText("0,1 cm")).toBeVisible();
  });
});
