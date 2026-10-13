import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { QuestionInput } from "./question-input";
import type { AttemptItem } from "@/lib/types";
const item: AttemptItem = {
  id: "item",
  question_version_id: "q",
  position: 1,
  points: 1,
  question_type: "single_choice",
  content: {
    prompt: "Chọn",
    options: [
      { id: "a", text: "Một" },
      { id: "b", text: "Hai" },
    ],
  },
  answer: null,
};
describe("QuestionInput", () => {
  it("tranh chỉ minh họa nhãn đáp án, giữ tên radio và giá trị gửi backend", () => {
    const onChange = vi.fn();
    const { container } = render(
      <QuestionInput
        item={{
          ...item,
          content: {
            prompt: "Chọn từ",
            options: [
              { id: "a", text: "bag" },
              { id: "b", text: "cat" },
              { id: "c", text: "Không phải mèo" },
            ],
          },
        }}
        answer={null}
        onChange={onChange}
      />,
    );
    expect(container.querySelectorAll(".word-picture")).toHaveLength(2);
    expect(container.querySelector("img")).toHaveAttribute("alt", "");
    fireEvent.click(screen.getByRole("radio", { name: /bag/ }));
    expect(onChange).toHaveBeenCalledWith({ option_id: "a" });
  });
  it("gửi lựa chọn đơn, không chứa điểm", () => {
    const onChange = vi.fn();
    render(<QuestionInput item={item} answer={null} onChange={onChange} />);
    fireEvent.click(screen.getByRole("radio", { name: /Một/ }));
    expect(onChange).toHaveBeenCalledWith({ option_id: "a" });
  });
  it("multiple_choice giữ nhiều đáp án", () => {
    const onChange = vi.fn();
    render(
      <QuestionInput
        item={{ ...item, question_type: "multiple_choice" }}
        answer={{ option_ids: ["a"] }}
        onChange={onChange}
      />,
    );
    fireEvent.click(screen.getByRole("checkbox", { name: /Hai/ }));
    expect(onChange).toHaveBeenCalledWith({ option_ids: ["a", "b"] });
  });
  it("fill_blank giữ dấu tiếng Việt", () => {
    const onChange = vi.fn();
    render(
      <QuestionInput
        item={{ ...item, question_type: "fill_blank" }}
        answer={null}
        onChange={onChange}
      />,
    );
    fireEvent.change(screen.getByRole("textbox"), {
      target: { value: "ngọt" },
    });
    expect(onChange).toHaveBeenCalledWith({ text: "ngọt" });
  });
  it("ordering hỗ trợ bàn phím bằng nút và thứ tự chính xác", () => {
    const onChange = vi.fn();
    render(
      <QuestionInput
        item={{ ...item, question_type: "ordering" }}
        answer={null}
        onChange={onChange}
      />,
    );
    expect(
      screen.getByRole("button", { name: "Đưa mục 1 lên" }),
    ).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "Đưa mục 1 xuống" }));
    expect(onChange).toHaveBeenCalledWith({ ordered_ids: ["b", "a"] });
  });
});
