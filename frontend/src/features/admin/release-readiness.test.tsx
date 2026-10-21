import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import { downloadCsv } from "@/lib/csv";
import {
  ReleaseReadinessSection,
  type ReleaseStatus,
} from "./release-readiness";

vi.mock("@/lib/api", async (original) => ({
  ...(await original<typeof import("@/lib/api")>()),
  api: vi.fn(),
}));
vi.mock("@/lib/csv", () => ({ downloadCsv: vi.fn() }));
const mockApi = vi.mocked(api);
const report: ReleaseStatus = {
  status: "attention",
  checked_at: "2026-10-20T03:00:00Z",
  checks: [
    {
      code: "review_demo_accounts",
      label: "Tài khoản demo chưa xử lý",
      ok: false,
      count: 2,
    },
  ],
  curriculum: [
    {
      grade: 1,
      subject_code: "MATH",
      actual: { lessons: 30, questions: 160, assessments: 26 },
      minimum: { lessons: 25, questions: 142, assessments: 21 },
      ok: true,
    },
  ],
  academy: { baseline_published: 200, baseline_required: 200, issues: [] },
  media: { valid: true, assets: 1702 },
  next_steps: [
    {
      code: "review_demo_accounts",
      instruction: "Khóa hoặc đổi mật khẩu riêng cho tài khoản demo.",
    },
  ],
};
beforeEach(() => vi.clearAllMocks());

it("chỉ tải báo cáo khi admin yêu cầu và hiển thị việc cần xử lý", async () => {
  mockApi.mockResolvedValue(report);
  render(<ReleaseReadinessSection />);
  expect(mockApi).not.toHaveBeenCalled();
  fireEvent.click(
    screen.getByRole("button", {
      name: "Kiểm tra trước khi mở web",
    }),
  );
  await screen.findByRole("heading", { name: "Còn hạng mục trước khi mở web" });
  expect(mockApi).toHaveBeenCalledWith(
    "/admin/release-status",
    expect.objectContaining({ signal: expect.any(AbortSignal) }),
  );
  expect(
    screen.getByText(report.next_steps[0].instruction),
  ).toBeInTheDocument();
  expect(screen.getByText(/200\/200/)).toHaveTextContent("1702 SVG hợp lệ");
  fireEvent.click(
    screen.getByRole("button", { name: "Tải biên bản kiểm tra (CSV)" }),
  );
  expect(downloadCsv).toHaveBeenCalledWith(
    expect.stringMatching(/\.csv$/),
    expect.arrayContaining([
      ["Tài khoản demo chưa xử lý", "Cần xử lý", 2],
      [1, "Toán", 30, 160, 26, 25, 142, 21],
    ]),
  );
});

it("lỗi mạng có thể kiểm tra lại và báo cáo mới thay trạng thái cũ", async () => {
  mockApi
    .mockRejectedValueOnce(new Error("Mạng tạm gián đoạn"))
    .mockResolvedValueOnce({
      ...report,
      status: "ok",
      checks: [],
      next_steps: [],
    });
  render(<ReleaseReadinessSection />);
  fireEvent.click(
    screen.getByRole("button", {
      name: "Kiểm tra trước khi mở web",
    }),
  );
  await screen.findByText("Mạng tạm gián đoạn");
  fireEvent.click(
    screen.getByRole("button", { name: "Kiểm tra trước triển khai lại" }),
  );
  await screen.findByRole("heading", {
    name: "Các kiểm tra trước mở web đều đạt",
  });
  await waitFor(() =>
    expect(screen.queryByText("Mạng tạm gián đoạn")).not.toBeInTheDocument(),
  );
});
