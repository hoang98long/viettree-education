import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { PracticeLibrary } from "./practice-library";

const resource = vi.hoisted(() => ({ query: "", retry: vi.fn() }));
vi.mock("@/components/shell", () => ({ useUser: () => ({ id: "student-1" }) }));
vi.mock("@/features/membership/pages", () => ({
  AccessBadge: () => <span>Miễn phí</span>,
}));
vi.mock("@/hooks/use-resource", () => ({
  useResource: (path: string) => {
    resource.query = path;
    return {
      loading: false,
      error: "",
      retry: resource.retry,
      data: {
        grade: 2,
        page: 1,
        page_size: 12,
        summary: { total: 30, not_started: 28, review: 1, mastered: 1 },
        items: [
          {
            id: "practice-1",
            title: "Chia bút cho các bạn",
            lesson_id: "lesson-1",
            time_limit_seconds: null,
            subject_code: "MATH",
            subject_name: "Toán",
            topic_title: "Chia đều",
            item_count: 4,
            graded_count: 2,
            best_percent: 100,
            latest_percent: 0,
            progress_status: "review",
            locked: false,
          },
        ],
      },
    };
  },
}));

describe("Thư viện luyện tập", () => {
  beforeEach(() => {
    resource.query = "";
    resource.retry.mockClear();
  });
  it("hiển thị điểm 0 gần nhất và điểm tốt nhất, dẫn tới bài học để ôn", () => {
    render(<PracticeLibrary />);
    expect(screen.getByText(/Gần nhất: 0%/)).toBeInTheDocument();
    expect(screen.getByText("100%")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Luyện lại" })).toHaveAttribute(
      "href",
      "/student/assessments/practice-1",
    );
    expect(
      screen.getByRole("link", { name: "Xem bài học và gợi ý" }),
    ).toHaveAttribute("href", "/student/lessons/lesson-1");
    expect(resource.query).toContain("/students/me/practice-library?");
    expect(resource.query).not.toContain("grade=");
  });
  it("phân trang và trở về trang đầu khi lọc bài ngắn, kết quả hoặc tìm kiếm", () => {
    render(<PracticeLibrary />);
    fireEvent.click(screen.getByRole("button", { name: "Trang sau" }));
    expect(resource.query).toContain("page=2");
    fireEvent.change(screen.getByLabelText("Độ dài bài"), {
      target: { value: "4" },
    });
    expect(resource.query).toContain("max_questions=4");
    expect(resource.query).toContain("page=1");
    fireEvent.change(screen.getByLabelText("Kết quả gần nhất"), {
      target: { value: "review" },
    });
    expect(resource.query).toContain("progress=review");
    fireEvent.change(screen.getByLabelText("Tên bài hoặc chủ đề"), {
      target: { value: "chia but" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Tìm bài" }));
    expect(resource.query).toContain("search=chia+but");
    fireEvent.click(screen.getByRole("button", { name: "Xóa bộ lọc" }));
    expect(resource.query).not.toContain("max_questions=");
    expect(resource.query).toContain("progress=all");
    expect(screen.getByLabelText("Tên bài hoặc chủ đề")).toHaveValue("");
    fireEvent.click(screen.getByRole("button", { name: "Làm mới" }));
    expect(resource.retry).toHaveBeenCalledOnce();
  });
  it("chọn nhanh bài ngắn và ôn thêm, bấm lần nữa để bỏ lựa chọn", () => {
    render(<PracticeLibrary />);
    const short = screen.getByRole("button", { name: "Bài ngắn" });
    fireEvent.click(short);
    expect(short).toHaveAttribute("aria-pressed", "true");
    expect(resource.query).toContain("max_questions=6");
    fireEvent.click(short);
    expect(resource.query).not.toContain("max_questions=");
    fireEvent.click(screen.getByRole("button", { name: "Ôn thêm" }));
    expect(resource.query).toContain("progress=review");
    fireEvent.click(screen.getByRole("button", { name: "Chưa nộp" }));
    expect(resource.query).toContain("progress=not_started");
  });
});
