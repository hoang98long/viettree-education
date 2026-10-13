import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, expect, it, vi } from "vitest";
import { ActivityBoard } from "./activity-board";
import { api } from "@/lib/api";

vi.mock("@/lib/api", async (original) => ({
  ...(await original<typeof import("@/lib/api")>()),
  api: vi.fn(),
}));
vi.mock("./shared", () => ({
  AcademyImage: ({ alt }: { alt: string }) => (
    <span role="img" aria-label={alt} />
  ),
}));
const activity = {
  kind: "classify",
  instruction: "Chọn một nhóm phù hợp.",
  choices: ["Con vật", "Trái cây"],
  items: [
    { id: "a", text: "Mèo", asset: "cat" },
    { id: "b", text: "Cam", asset: "orange" },
  ],
};
const mockApi = vi.mocked(api);
beforeEach(() => mockApi.mockReset());

it("chỉ hiện một thẻ, chạm chọn và gửi đủ câu trả lời; đổi đáp án bỏ trạng thái đạt", async () => {
  const onPass = vi.fn(),
    onReset = vi.fn();
  mockApi.mockResolvedValue({
    score: 1,
    feedback: { passed: true, message: "Đúng", items: [] },
  });
  render(
    <ActivityBoard
      lessonId="lesson"
      stepId="practice"
      activity={activity}
      questions={[]}
      onPass={onPass}
      onReset={onReset}
    />,
  );
  expect(screen.getByRole("img", { name: "Mèo" })).toBeInTheDocument();
  expect(screen.queryByRole("img", { name: "Cam" })).not.toBeInTheDocument();
  expect(screen.getByText("Thẻ tiếp")).toBeDisabled();
  fireEvent.click(screen.getByRole("button", { name: "Con vật" }));
  fireEvent.click(screen.getByText("Thẻ tiếp"));
  expect(screen.getByText("Kiểm tra lựa chọn")).toBeDisabled();
  fireEvent.click(screen.getByRole("button", { name: "Trái cây" }));
  fireEvent.click(screen.getByText("Kiểm tra lựa chọn"));
  await waitFor(() => expect(onPass).toHaveBeenCalledTimes(1));
  const body = JSON.parse(mockApi.mock.calls[0][1]!.body as string);
  expect(body.answers).toEqual({ a: "Con vật", b: "Trái cây" });
  fireEvent.click(screen.getByText("Thẻ trước"));
  fireEvent.click(screen.getByRole("button", { name: "Trái cây" }));
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(onReset).toHaveBeenCalledTimes(3);
});

it("checkpoint hiện lần lượt, không chấm trước khi đã chọn đủ", async () => {
  const questions = [
    {
      id: "q1",
      prompt: "Mèo thuộc nhóm nào?",
      options: ["Con vật", "Trái cây"],
    },
    { id: "q2", prompt: "Máy luôn đúng không?", options: ["Không", "Có"] },
  ];
  render(
    <ActivityBoard
      lessonId="lesson"
      stepId="checkpoint"
      questions={questions}
      onPass={vi.fn()}
    />,
  );
  expect(screen.queryByText("Máy luôn đúng không?")).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole("radio", { name: "Con vật" }));
  fireEvent.click(screen.getByText("Thẻ tiếp"));
  expect(screen.getByText("Kiểm tra lựa chọn")).toBeDisabled();
  fireEvent.click(screen.getByRole("radio", { name: "Không" }));
  expect(screen.getByText("Kiểm tra lựa chọn")).toBeEnabled();
});
