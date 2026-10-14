import { describe, expect, it, vi } from "vitest";
import { AnswerSaveQueue } from "./answer-save-queue";

describe("Lưu đáp án theo thứ tự", () => {
  it("phản hồi chậm không bỏ đáp án mới; nộp thủ công chờ cùng hàng lưu", async () => {
    let resolve!: () => void;
    const save = vi
      .fn()
      .mockImplementationOnce(
        () =>
          new Promise<void>((done) => {
            resolve = done;
          }),
      )
      .mockResolvedValue(undefined);
    const queue = new AnswerSaveQueue(save);
    queue.change("q1", { text: "cũ" });
    const first = queue.flush();
    queue.change("q1", { text: "mới" });
    queue.change("q2", { option_id: "b" });
    expect(queue.flush()).toBe(first);
    expect(save).toHaveBeenCalledTimes(1);
    resolve();
    await first;
    expect(save.mock.calls.map(([id, answer]) => [id, answer])).toEqual([
      ["q1", { text: "cũ" }],
      ["q1", { text: "mới" }],
      ["q2", { option_id: "b" }],
    ]);
    expect(queue.snapshot()).toMatchObject({
      pending: 0,
      saved: true,
      error: "",
      saving: false,
    });
  });
  it("lỗi mạng giữ đáp án và chỉ xác nhận đã lưu sau retry thành công", async () => {
    const save = vi
      .fn()
      .mockRejectedValueOnce(new Error("Mất mạng"))
      .mockResolvedValue(undefined);
    const queue = new AnswerSaveQueue(save);
    queue.change("q", { option_ids: ["a", "b"] });
    await expect(queue.flush()).rejects.toThrow("Mất mạng");
    expect(queue.snapshot()).toMatchObject({
      pending: 1,
      saved: false,
      saving: false,
      error: "Mất mạng",
    });
    await queue.flush();
    expect(save.mock.calls[1][1]).toEqual({ option_ids: ["a", "b"] });
    expect(queue.snapshot()).toMatchObject({ pending: 0, saved: true });
  });
  it("lỗi câu sau không lưu lặp lại câu đã xác nhận và không giữ tham chiếu mảng ngoài", async () => {
    const save = vi
      .fn()
      .mockResolvedValueOnce(undefined)
      .mockRejectedValueOnce(new Error("Lỗi câu 2"))
      .mockResolvedValue(undefined);
    const queue = new AnswerSaveQueue(save);
    const answer = { ordered_ids: ["a", "b"] };
    queue.change("q1", answer);
    answer.ordered_ids.reverse();
    queue.change("q2", { text: "đúng" });
    await expect(queue.flush()).rejects.toThrow("Lỗi câu 2");
    expect(save.mock.calls[0][1]).toEqual({ ordered_ids: ["a", "b"] });
    await queue.flush();
    expect(save.mock.calls.map(([id]) => id)).toEqual(["q1", "q2", "q2"]);
  });
  it("rời bài hủy request đang chờ, không gửi câu còn lại bằng phiên tài khoản khác", async () => {
    const save = vi.fn(
      (_id, _answer, signal: AbortSignal) =>
        new Promise<void>((_resolve, reject) =>
          signal.addEventListener("abort", () =>
            reject(new DOMException("Hủy", "AbortError")),
          ),
        ),
    );
    const queue = new AnswerSaveQueue(save);
    queue.change("q1", { text: "một" });
    queue.change("q2", { text: "hai" });
    const pending = queue.flush();
    queue.stop();
    await expect(pending).rejects.toHaveProperty("name", "AbortError");
    expect(save).toHaveBeenCalledTimes(1);
    await expect(queue.flush()).rejects.toThrow("Trang làm bài đã đóng");
  });
});
