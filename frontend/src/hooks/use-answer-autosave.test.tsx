import { StrictMode } from "react";
import { act, fireEvent, renderHook, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
const { api, push, router } = vi.hoisted(() => {
  const push = vi.fn();
  return { api: vi.fn(), push, router: { push } };
});
vi.mock("@/lib/api", () => ({ api }));
vi.mock("next/navigation", () => ({ useRouter: () => router }));
import { useAnswerAutosave } from "./use-answer-autosave";

beforeEach(() => {
  api.mockReset();
  push.mockReset();
  api.mockResolvedValue({ saved: true });
});
afterEach(() => vi.useRealTimers());

describe("Tự lưu trong trang làm bài", () => {
  it("request treo dừng sau 15 giây và giữ đáp án để retry", async () => {
    vi.useFakeTimers();
    api.mockImplementationOnce(
      (_path, options: { signal: AbortSignal }) =>
        new Promise((_resolve, reject) =>
          options.signal.addEventListener("abort", () =>
            reject(new DOMException("Hủy", "AbortError")),
          ),
        ),
    );
    const { result } = renderHook(() => useAnswerAutosave("attempt"));
    act(() => result.current.change("q", { text: "đáp án" }));
    await act(() => vi.advanceTimersByTimeAsync(15800));
    expect(result.current.saving).toBe(false);
    expect(result.current.pending).toBe(1);
    expect(result.current.error).toContain("Lưu lâu hơn dự kiến");
    await act(async () => {
      await result.current.flush();
    });
    expect(result.current.saved).toBe(true);
  });
  it("gom thao tác gõ nhanh và hoạt động trong React StrictMode", async () => {
    vi.useFakeTimers();
    const { result } = renderHook(() => useAnswerAutosave("attempt"), {
      wrapper: StrictMode,
    });
    act(() => result.current.change("q", { text: "đ" }));
    await act(() => vi.advanceTimersByTimeAsync(500));
    act(() => result.current.change("q", { text: "đúng" }));
    await act(() => vi.advanceTimersByTimeAsync(799));
    expect(api).not.toHaveBeenCalled();
    await act(() => vi.advanceTimersByTimeAsync(1));
    expect(api).toHaveBeenCalledTimes(1);
    expect(JSON.parse(api.mock.calls[0][1].body)).toEqual({
      answer: { text: "đúng" },
    });
    expect(result.current.saved).toBe(true);
  });
  it("không lặp request vô hạn khi mất mạng; online lưu lại đáp án trên trang", async () => {
    api.mockRejectedValueOnce(new Error("Mất mạng"));
    const { result } = renderHook(() => useAnswerAutosave("attempt"));
    act(() => result.current.change("q", { option_id: "a" }));
    await act(async () => {
      await result.current.flush().catch(() => {});
    });
    expect(result.current.pending).toBe(1);
    expect(result.current.error).toBe("Mất mạng");
    fireEvent(window, new Event("online"));
    await waitFor(() => expect(result.current.saved).toBe(true));
    expect(api).toHaveBeenCalledTimes(2);
  });
  it("bấm liên kết chờ lưu; khi lỗi thì giữ trang và cảnh báo đóng tab", async () => {
    const { result, unmount } = renderHook(() => useAnswerAutosave("attempt"));
    const anchor = document.createElement("a");
    anchor.href = "/student/dashboard";
    document.body.append(anchor);
    act(() => result.current.change("q", { option_id: "a" }));
    api.mockRejectedValueOnce(new Error("Mất mạng"));
    fireEvent.click(anchor);
    await waitFor(() => expect(result.current.error).toBe("Mất mạng"));
    expect(push).not.toHaveBeenCalled();
    const before = new Event("beforeunload", { cancelable: true });
    fireEvent(window, before);
    expect(before.defaultPrevented).toBe(true);
    fireEvent.click(anchor);
    await waitFor(() =>
      expect(push).toHaveBeenCalledWith("/student/dashboard"),
    );
    expect(result.current.pending).toBe(0);
    unmount();
    anchor.remove();
  });
});
