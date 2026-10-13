import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { GuidedText } from "./guided-text";

const story =
  "Mèo đi dạo cùng bạn nhỏ và nghỉ dưới gốc cây ở trong khu vườn của bà vào buổi sáng. Mưa rơi xuống vào buổi chiều nên bạn nhỏ ở trong phòng và lắng nghe tiếng nước rơi bên cửa sổ.";

describe("Đọc từng đoạn có tranh", () => {
  it("chỉ hiện tranh của đoạn đang đọc, vẫn mở được toàn bộ bài", () => {
    render(<GuidedText text={story} grade={1} illustrated />);
    expect(screen.getByRole("img", { name: "mèo" })).toBeInTheDocument();
    expect(screen.queryByRole("img", { name: "mưa" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Đọc tiếp" }));
    expect(screen.getByRole("img", { name: "mưa" })).toBeInTheDocument();
    expect(screen.queryByRole("img", { name: "mèo" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Xem cả phần" }));
    expect(screen.getByText(story)).toBeInTheDocument();
  });
  it("chuyển sang nội dung khác bắt đầu lại đoạn đầu", () => {
    const { rerender } = render(
      <GuidedText text={story} grade={1} illustrated />,
    );
    fireEvent.click(screen.getByRole("button", { name: "Đọc tiếp" }));
    rerender(
      <GuidedText
        text={story.replaceAll("Mèo", "Chó")}
        grade={1}
        illustrated
      />,
    );
    expect(screen.getByText("Đoạn 1/2")).toBeInTheDocument();
    expect(screen.getByRole("img", { name: "chó" })).toBeInTheDocument();
  });
});
