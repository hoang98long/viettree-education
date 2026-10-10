import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { LessonBody } from "./lesson-body";
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
