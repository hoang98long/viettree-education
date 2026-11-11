import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AssessmentIntro } from "./assessment";
import type { Assessment } from "@/lib/types";

const fixture = vi.hoisted(() => ({
  retry: vi.fn(),
  error: "",
  assignmentId: "assigned-lesson",
}));
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  useSearchParams: () => ({ get: () => fixture.assignmentId }),
}));
vi.mock("@/hooks/use-resource", () => ({
  useResource: () => ({
    loading: false,
    data: null,
    error: fixture.error,
    retry: fixture.retry,
  }),
}));
const assessment = {
  id: "assessment-1",
  title: "Cộng trong phạm vi 10",
  grade: 1,
  subject_name: "Toán",
  description: "Cùng em luyện tập",
  locked: false,
  item_count: 4,
  max_attempts: 3,
  time_limit_seconds: null,
} as Assessment;
beforeEach(() => {
  fixture.error = "";
  fixture.retry.mockClear();
});

describe("Mở bài giáo viên giao khi mạng lỗi", () => {
  it("phân biệt lỗi tải với bài giao không tồn tại và cho thử lại", () => {
    fixture.error = "Kết nối tạm gián đoạn";
    render(<AssessmentIntro data={assessment} />);
    expect(screen.getByRole("alert")).toHaveTextContent(fixture.error);
    expect(
      screen.queryByText(/Chưa tìm thấy bài được giao/),
    ).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Bắt đầu/ })).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "Thử lại" }));
    expect(fixture.retry).toHaveBeenCalledOnce();
  });

  it("chỉ báo không tìm thấy khi dữ liệu tải thành công không có bài giao", () => {
    render(<AssessmentIntro data={assessment} />);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.getByText(/Chưa tìm thấy bài được giao/)).toBeInTheDocument();
  });
});
