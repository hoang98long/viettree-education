import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api";

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("Yêu cầu có thời hạn và hủy khi rời trang", () => {
  it("báo hết thời gian khi chưa có phản hồi; không tự lặp lệnh ghi dữ liệu", async () => {
    vi.useFakeTimers();
    const fetcher = vi.fn(
      (_url, init: RequestInit) =>
        new Promise((_resolve, reject) => {
          init.signal!.addEventListener("abort", () =>
            reject(new DOMException("Aborted", "AbortError")),
          );
        }),
    );
    vi.stubGlobal("fetch", fetcher);
    const request = api("/attempts/one/submit", {
      method: "POST",
      timeoutMs: 100,
    });
    const assertion = expect(request).rejects.toMatchObject({
      code: "REQUEST_TIMEOUT",
      status: 0,
    });
    await vi.advanceTimersByTimeAsync(100);
    await assertion;
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(vi.getTimerCount()).toBe(0);
  });

  it("thời hạn bao gồm cả khi đang tải body JSON", async () => {
    vi.useFakeTimers();
    vi.stubGlobal(
      "fetch",
      vi.fn(async (_url, init: RequestInit) => ({
        ok: true,
        json: () =>
          new Promise((_resolve, reject) => {
            init.signal!.addEventListener("abort", () =>
              reject(new DOMException("Aborted", "AbortError")),
            );
          }),
      })),
    );
    const assertion = expect(
      api("/lessons/one", { timeoutMs: 100 }),
    ).rejects.toMatchObject({ code: "REQUEST_TIMEOUT" });
    await vi.advanceTimersByTimeAsync(100);
    await assertion;
  });

  it("giữ nguyên tín hiệu hủy của trang và dọn timer", async () => {
    vi.useFakeTimers();
    vi.stubGlobal(
      "fetch",
      vi.fn(
        (_url, init: RequestInit) =>
          new Promise((_resolve, reject) => {
            init.signal!.addEventListener("abort", () =>
              reject(new DOMException("Aborted", "AbortError")),
            );
          }),
      ),
    );
    const controller = new AbortController();
    const assertion = expect(
      api("/lessons/one", { signal: controller.signal }),
    ).rejects.toMatchObject({ name: "AbortError" });
    controller.abort();
    await assertion;
    expect(vi.getTimerCount()).toBe(0);
  });

  it("JSON bị cắt có lỗi dễ hiểu và vẫn giữ lỗi HTTP/quyền VIP", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: () => Promise.reject(new SyntaxError()),
        })
        .mockResolvedValueOnce(
          new Response(
            JSON.stringify({
              detail: {
                message: "Cần VIP",
                code: "MEMBERSHIP_REQUIRED",
                required_plan: "vip",
              },
            }),
            { status: 403 },
          ),
        ),
    );
    await expect(api("/lessons/one")).rejects.toMatchObject({
      code: "INVALID_RESPONSE",
    });
    await expect(api("/lessons/one")).rejects.toMatchObject({
      message: "Cần VIP",
      code: "MEMBERSHIP_REQUIRED",
      requiredPlan: "vip",
    });
    expect(new ApiError(0, "Mạng")).toBeInstanceOf(Error);
  });
});
