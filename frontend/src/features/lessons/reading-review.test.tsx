import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ReadingReview } from "./reading-review";
import { initial } from "./form-values";

describe("Rà soát bài trước khi duyệt", () => {
  it("báo câu quá dài nhưng không đánh dấu cả bài dài đã chia thành câu ngắn", () => {
    const value = initial({ subjects: [], topics: [], skills: [] }, 1);
    value.content.blocks = [
      { type: "text", title: "Câu dài", text: Array(40).fill("học").join(" ") },
    ];
    const { rerender } = render(<ReadingReview value={value} />);
    expect(
      screen.getByText(/Phần còn câu hoặc dòng dài: Câu dài/),
    ).toBeInTheDocument();
    value.content.blocks[0].text = Array(12).fill("Em học cùng bạn.").join(" ");
    rerender(<ReadingReview value={value} />);
    expect(
      screen.queryByText(/Phần còn câu hoặc dòng dài:/),
    ).not.toBeInTheDocument();
  });
  it("phân biệt gợi ý trong bài Free với gợi ý của bài khóa VIP", () => {
    const value = initial({ subjects: [], topics: [], skills: [] }, 4);
    value.content.hints = ["Bước 1", "Bước 2", "Bước 3"];
    value.content.free_hint_count = 1;
    const { rerender } = render(<ReadingReview value={value} />);
    expect(screen.getByText("1 mức Free / 2 mức VIP")).toBeInTheDocument();
    rerender(<ReadingReview value={{ ...value, minimum_plan_code: "vip" }} />);
    expect(
      screen.getByText("3 gợi ý trong bài yêu cầu VIP"),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("1 mức Free / 2 mức VIP"),
    ).not.toBeInTheDocument();
    expect(
      screen.getByText(/Bài VIP cần phần giới thiệu riêng/),
    ).toBeInTheDocument();
  });
});
