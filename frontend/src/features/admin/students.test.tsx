import { act, fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, expect, it, vi } from "vitest";
import { EditStudent } from "./students";
import { api } from "@/lib/api";
import type { Student } from "@/lib/types";

vi.mock("@/lib/api", async (original) => ({
  ...(await original<typeof import("@/lib/api")>()),
  api: vi.fn(),
}));
vi.mock("@/components/modal", () => ({
  Modal: ({ children }: { children: React.ReactNode }) => (
    <section>{children}</section>
  ),
}));
const mockApi = vi.mocked(api);
beforeEach(() => {
  mockApi.mockReset();
});

it("khóa trường khi lưu, giữ nội dung và mở lại trường sau lỗi mạng", async () => {
  let reject!: (reason: Error) => void;
  mockApi.mockImplementation(
    () =>
      new Promise((_, fail) => {
        reject = fail;
      }),
  );
  const onClose = vi.fn();
  render(
    <EditStudent
      student={
        {
          id: "fake-student",
          username: "student",
          display_name: "Tên mẫu",
          current_grade: 2,
        } as Student
      }
      onClose={onClose}
    />,
  );
  const name = screen.getByLabelText("Tên hiển thị");
  fireEvent.change(name, { target: { value: "Tên đã sửa" } });
  fireEvent.click(screen.getByRole("button", { name: "Lưu hồ sơ" }));
  expect(name).toBeDisabled();
  expect(screen.getByLabelText("Lớp")).toBeDisabled();
  expect(screen.getByRole("button", { name: "Đóng" })).toBeDisabled();
  expect(JSON.parse(mockApi.mock.calls[0][1]!.body as string)).toEqual({
    display_name: "Tên đã sửa",
    current_grade: 2,
  });
  await act(async () => {
    reject(new Error("Kết nối tạm gián đoạn"));
    await Promise.resolve();
  });
  expect(screen.getByRole("alert")).toHaveTextContent("Kết nối tạm gián đoạn");
  expect(name).toBeEnabled();
  expect(name).toHaveValue("Tên đã sửa");
  expect(onClose).not.toHaveBeenCalled();
});
