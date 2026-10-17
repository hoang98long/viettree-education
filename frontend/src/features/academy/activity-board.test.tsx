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

it("gửi lại sau lỗi mạng dùng cùng mã; đổi đáp án tạo mã mới", async () => {
  mockApi.mockRejectedValueOnce(new Error("Mạng gián đoạn"));
  mockApi.mockResolvedValue({
    score: 0,
    feedback: { passed: false, message: "Thử lại", items: [] },
  });
  render(
    <ActivityBoard
      lessonId="lesson"
      stepId="practice"
      activity={activity}
      questions={[]}
      onPass={vi.fn()}
    />,
  );
  fireEvent.click(screen.getByRole("button", { name: "Con vật" }));
  fireEvent.click(screen.getByText("Thẻ tiếp"));
  fireEvent.click(screen.getByRole("button", { name: "Trái cây" }));
  fireEvent.click(screen.getByText("Kiểm tra lựa chọn"));
  await screen.findByRole("alert");
  fireEvent.click(screen.getByText("Kiểm tra lựa chọn"));
  await screen.findByRole("status");
  const submitted = () =>
    mockApi.mock.calls.map((call) => JSON.parse(call[1]!.body as string));
  expect(submitted()[0].idempotency_key).toBe(submitted()[1].idempotency_key);
  fireEvent.click(screen.getByRole("button", { name: "Con vật" }));
  fireEvent.click(screen.getByText("Kiểm tra lựa chọn"));
  await waitFor(() => expect(mockApi).toHaveBeenCalledTimes(3));
  expect(submitted()[2].idempotency_key).not.toBe(
    submitted()[1].idempotency_key,
  );
});

it("quay về thẻ chưa đúng, xem một giải thích và bỏ kết quả cũ khi đổi đáp án", async () => {
  mockApi.mockResolvedValue({
    score: 0.5,
    feedback: {
      passed: false,
      message: "Thử lại",
      items: [
        { id: "a", correct: false, explanation: "Mèo là con vật." },
        { id: "b", correct: true, explanation: "Cam là trái cây." },
      ],
    },
  });
  const onReset = vi.fn();
  render(
    <ActivityBoard
      lessonId="lesson"
      stepId="practice"
      activity={activity}
      questions={[]}
      onPass={vi.fn()}
      onReset={onReset}
    />,
  );
  fireEvent.click(screen.getByRole("button", { name: "Trái cây" }));
  fireEvent.click(screen.getByText("Thẻ tiếp"));
  fireEvent.click(screen.getByRole("button", { name: "Trái cây" }));
  fireEvent.click(screen.getByText("Kiểm tra lựa chọn"));
  await screen.findByRole("status");
  expect(screen.getByRole("note")).toHaveTextContent("Cam là trái cây.");
  expect(screen.queryByText("Mèo là con vật.")).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Thẻ 1 · Xem lại" }));
  expect(screen.getByRole("note")).toHaveTextContent("Mèo là con vật.");
  expect(screen.getByRole("button", { name: "Trái cây" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  fireEvent.click(screen.getByRole("button", { name: "Con vật" }));
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(screen.queryByRole("note")).not.toBeInTheDocument();
  expect(onReset).toHaveBeenCalled();
  expect(screen.getByText("Kiểm tra lựa chọn")).toBeEnabled();
});
