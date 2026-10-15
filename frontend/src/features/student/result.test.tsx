import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { Result } from "@/lib/types";
import { renderAnswer, ResultItemReview } from "./result";

const item: Result["items"][number] = {
  id: "one",
  position: 1,
  points: 1,
  question_version_id: "v1",
  question_type: "single_choice",
  answer: null,
  student_answer: { option_id: "b" },
  content: {
    prompt: "Bé Na ở nhà với bà. Na lấy cốc nước cho bà.\n\nNa lấy gì cho bà?",
    options: [
      { id: "a", text: "Cốc nước" },
      { id: "b", text: "Bút" },
    ],
  },
  is_correct: false,
  score: 0,
  grading: { correct_option_id: "a" },
  explanation: {
    text: "Na lấy cốc nước cho bà. Em tìm chi tiết ở câu thứ hai.",
  },
};

describe("Xem lại đáp án và hiểu cách làm", () => {
  it("tách ngữ liệu, dùng đáp án chính thức và không lộ mã lựa chọn", () => {
    const { container } = render(<ResultItemReview item={item} grade={1} />);
    expect(
      screen.getByRole("heading", { level: 3, name: "Na lấy gì cho bà?" }),
    ).toBeVisible();
    expect(screen.getByText("Đáp án đúng:").parentElement).toHaveTextContent(
      "Cốc nước",
    );
    expect(screen.getByText("Em trả lời:").parentElement).toHaveTextContent(
      "Bút",
    );
    expect(container.querySelector(".question-reading")).toHaveAttribute(
      "open",
    );
    expect(container.querySelector(".result-item")).toHaveAttribute("open");
  });
  it("giữ dấu và các đáp án chấp nhận, câu xóa trắng là chưa trả lời", () => {
    render(
      <ResultItemReview
        item={{
          ...item,
          question_type: "fill_blank",
          student_answer: { text: " \n " },
          grading: { accepted_answers: ["ngọt", "vị ngọt"] },
        }}
        grade={2}
      />,
    );
    expect(screen.getByText("Em trả lời:").parentElement).toHaveTextContent(
      "Chưa trả lời",
    );
    expect(
      screen.getByText("Một đáp án đúng:").parentElement,
    ).toHaveTextContent("ngọt");
    fireEvent.click(screen.getByText("Các cách trả lời được chấp nhận"));
    expect(screen.getByText("vị ngọt")).toBeVisible();
    expect(renderAnswer({ text: "0" }, item.content)).toBe("0");
  });
  it("sắp xếp có mũi tên theo thứ tự đúng; không đoán khi thiếu đáp án", () => {
    const { rerender } = render(
      <ResultItemReview
        item={{
          ...item,
          question_type: "ordering",
          grading: { ordered_ids: ["b", "a"] },
        }}
      />,
    );
    expect(screen.getByText("Đáp án đúng:").parentElement).toHaveTextContent(
      "Bút → Cốc nước",
    );
    rerender(<ResultItemReview item={{ ...item, grading: {} }} />);
    expect(screen.queryByText("Đáp án đúng:")).not.toBeInTheDocument();
  });
});
