export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public code?: string,
    public requiredPlan?: string,
  ) {
    super(message);
  }
}

export async function api<T>(
  path: string,
  options: RequestInit & { redirectOnUnauthorized?: boolean } = {},
): Promise<T> {
  const { redirectOnUnauthorized = true, ...requestOptions } = options;
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
      credentials: "same-origin",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": decodeURIComponent(csrf),
        ...requestOptions.headers,
      },
    });
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") throw error;
    throw new ApiError(
      0,
      "Chưa kết nối được. Em hãy kiểm tra mạng rồi thử lại nhé.",
    );
  }
  if (!response.ok) {
    const body = await response.json().catch(() => null);
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
    );
  }
  return response.json() as Promise<T>;
}

export function dateLabel(value: string | null) {
  return value
    ? new Intl.DateTimeFormat("vi-VN", {
        dateStyle: "medium",
        timeZone: "Asia/Bangkok",
      }).format(new Date(value))
    : "—";
}

export function percent(value: number) {
  return Math.round(Number(value) * 100);
}
