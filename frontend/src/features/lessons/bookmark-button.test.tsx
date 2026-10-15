import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { BookmarkButton } from "./bookmark-button";

const request = vi.hoisted(() => vi.fn());
vi.mock("@/lib/api", () => ({ api: request }));

describe("Lưu bài học theo tài khoản", () => {
  beforeEach(() => request.mockReset());
  it("chỉ cập nhật khi server lưu thành công và gửi trạng thái mong muốn", async () => {
    request
      .mockResolvedValueOnce({ saved: true })
      .mockResolvedValueOnce({ saved: false });
    render(<BookmarkButton lessonId="lesson-1" initialSaved={false} />);
    fireEvent.click(screen.getByRole("button", { name: "Lưu bài học" }));
    expect(screen.getByRole("button")).toBeDisabled();
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "Bỏ lưu bài học" }),
      ).toHaveAttribute("aria-pressed", "true"),
    );
    expect(request).toHaveBeenNthCalledWith(
      1,
      "/students/me/lessons/lesson-1/bookmark",
      { method: "PUT", body: JSON.stringify({ saved: true }) },
    );
    fireEvent.click(screen.getByRole("button", { name: "Bỏ lưu bài học" }));
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "Lưu bài học" }),
      ).toHaveAttribute("aria-pressed", "false"),
    );
    expect(request).toHaveBeenNthCalledWith(
      2,
      "/students/me/lessons/lesson-1/bookmark",
      { method: "PUT", body: JSON.stringify({ saved: false }) },
    );
  });
  it("mạng lỗi giữ trạng thái hiện có và cho phép thử lại", async () => {
    request
      .mockRejectedValueOnce(new Error("Mạng tạm ngắt"))
      .mockResolvedValueOnce({ saved: true });
    render(<BookmarkButton lessonId="lesson-1" initialSaved={false} />);
    fireEvent.click(screen.getByRole("button", { name: "Lưu bài học" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Mạng tạm ngắt");
    expect(screen.getByRole("button")).toHaveAttribute("aria-pressed", "false");
    fireEvent.click(screen.getByRole("button", { name: "Lưu bài học" }));
    await waitFor(() =>
      expect(screen.getByRole("button")).toHaveAttribute(
        "aria-pressed",
        "true",
      ),
    );
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
  it("bài VIP khóa không lưu mới nhưng vẫn cho bỏ bài đã lưu", () => {
    const { rerender } = render(
      <BookmarkButton lessonId="vip" initialSaved={false} locked />,
    );
    expect(screen.getByRole("button")).toBeDisabled();
    rerender(<BookmarkButton key="saved" lessonId="vip" initialSaved locked />);
    expect(
      screen.getByRole("button", { name: "Bỏ lưu bài học" }),
    ).toBeEnabled();
  });
});
