import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { QuestionPrompt } from "./question-prompt";

describe("Câu hỏi và bài đọc tách rõ", () => {
  it("giữ đầy đủ các khổ thơ, câu hỏi cuối và ngữ liệu gốc", () => {
    const poem =
      "Khổ thứ nhất\nMèo nhìn lên cây\n\nKhổ thứ hai\nChim bay qua lá";
    const { container } = render(
      <QuestionPrompt
        text={`Ngữ liệu của bài:\n${poem}\n\nChim đang làm gì?`}
        grade={1}
      />,
    );
    expect(
      screen.getByRole("heading", { name: "Chim đang làm gì?" }),
    ).toBeInTheDocument();
    expect(container.querySelector(".reading-paragraph")?.textContent).toBe(
      poem,
    );
    expect(container.querySelectorAll("img")).toHaveLength(0);
  });
  it("bài dài có đọc từng đoạn và vẫn xem được toàn bộ; câu không có ngữ liệu giữ nguyên", () => {
    const passage = Array(25).fill("Em đọc cùng bạn.").join(" ");
    const { rerender } = render(
      <QuestionPrompt text={`${passage}\n\nEm đọc với ai?`} grade={1} />,
    );
    expect(screen.getByRole("button", { name: "Đọc tiếp" })).toBeEnabled();
    fireEvent.click(screen.getByRole("button", { name: "Xem cả phần" }));
    expect(screen.getByText(passage)).toBeInTheDocument();
    rerender(<QuestionPrompt text="2 + 3 = ?" grade={1} />);
    expect(
      screen.getByRole("heading", { name: "2 + 3 = ?" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Bài đọc để tìm câu trả lời"),
    ).not.toBeInTheDocument();
  });
});
