export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public code?: string,
    public requiredPlan?: string,
    public requestId?: string,
  ) {
    super(message);
  }
}

export async function api<T>(
  path: string,
  options: RequestInit & {
    redirectOnUnauthorized?: boolean;
    timeoutMs?: number;
  } = {},
): Promise<T> {
  const {
    redirectOnUnauthorized = true,
    timeoutMs = 45000,
    ...requestOptions
  } = options;
  const controller = new AbortController();
  const callerSignal = requestOptions.signal;
  const abort = () => controller.abort(callerSignal?.reason);
  callerSignal?.addEventListener("abort", abort, { once: true });
  if (callerSignal?.aborted) abort();
  let timedOut = false;
  const timer = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, timeoutMs);
  try {
    return await performRequest<T>(
      path,
      requestOptions,
      controller.signal,
      redirectOnUnauthorized,
    );
  } catch (error) {
    if (timedOut && !callerSignal?.aborted)
      throw new ApiError(
        0,
        "Chờ lâu hơn dự kiến. Em hãy kiểm tra mạng rồi thử lại nhé.",
        "REQUEST_TIMEOUT",
      );
    throw error;
  } finally {
    clearTimeout(timer);
    callerSignal?.removeEventListener("abort", abort);
  }
}

async function performRequest<T>(
  path: string,
  requestOptions: RequestInit,
  signal: AbortSignal,
  redirectOnUnauthorized: boolean,
): Promise<T> {
  const csrf =
    typeof document === "undefined"
      ? ""
      : document.cookie
          .split("; ")
          .find((value) => value.startsWith("viettree_csrf="))
          ?.split("=")
          .slice(1)
          .join("=") || "";
  let response: Response;
  try {
    response = await fetch(`/api/v1${path}`, {
      ...requestOptions,
      signal,
      credentials: "same-origin",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": decodeURIComponent(csrf),
        ...requestOptions.headers,
      },
    });
  } catch (error) {
    if (signal.aborted) throw signal.reason;
    if (error instanceof Error && error.name === "AbortError") throw error;
    throw new ApiError(
      0,
      "Chưa kết nối được. Em hãy kiểm tra mạng rồi thử lại nhé.",
    );
  }
  if (!response.ok) {
    const body = await response.json().catch((error: unknown) => {
      if (signal.aborted) throw error;
      return null;
    });
    signal.throwIfAborted();
    if (
      body?.detail?.code === "PASSWORD_CHANGE_REQUIRED" &&
      typeof window !== "undefined"
    ) {
      window.location.assign("/account/security");
    }
    if (
      response.status === 401 &&
      typeof window !== "undefined" &&
      path !== "/auth/login" &&
      redirectOnUnauthorized
    ) {
      window.dispatchEvent(new Event("viettree:session-expired"));
      window.location.assign("/login");
    }
    throw new ApiError(
      response.status,
      typeof body?.detail?.message === "string"
        ? body.detail.message
        : typeof body?.detail === "string"
          ? body.detail
          : "Yêu cầu chưa thành công. Hãy thử lại nhé.",
      body?.detail?.code,
      body?.detail?.required_plan,
      response.headers.get("x-request-id") || undefined,
    );
  }
  try {
    const body = (await response.json()) as T;
    signal.throwIfAborted();
    return body;
  } catch (error) {
    if (signal.aborted) throw error;
    throw new ApiError(
      response.status,
      "Dữ liệu chưa tải đủ. Em hãy thử lại nhé.",
      "INVALID_RESPONSE",
    );
  }
}

export function dateLabel(value: string | null) {
  return value
    ? new Intl.DateTimeFormat("vi-VN", {
        dateStyle: "medium",
        timeZone: "Asia/Bangkok",
      }).format(new Date(value))
    : "—";
}

export function dateTimeLabel(value: string | null) {
  return value
    ? new Intl.DateTimeFormat("vi-VN", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Bangkok",
      }).format(new Date(value))
    : "—";
}

export function percent(value: number) {
  return Math.round(Number(value) * 100);
}
