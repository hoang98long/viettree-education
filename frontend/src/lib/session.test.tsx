import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api";
import { homeFor, SessionProvider, useSession } from "./session";
import type { User } from "./types";

vi.mock("next/navigation", () => ({ usePathname: () => "/" }));
vi.mock("./api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./api")>()),
  api: vi.fn(),
}));

const student: User = {
  id: "student-one",
  username: "one",
  display_name: "Học sinh một",
  roles: ["student"],
  text_size: "comfortable",
  session_expires_at: new Date(Date.now() + 8 * 3600_000).toISOString(),
};
const mockApi = vi.mocked(api);
function Probe({ name = "one" }: { name?: string }) {
  const {
    user,
    loading,
    error,
    refresh,
    setUser,
    updateReadingPreferences,
    clear,
  } = useSession();
  return (
    <div>
      <output data-testid={name}>
        {loading
          ? "loading"
          : error
            ? `error:${error}`
            : (user?.id ?? "anonymous")}
      </output>
      <button onClick={() => void refresh()}>cached-{name}</button>
      <button onClick={() => void refresh(true)}>force-{name}</button>
      <button onClick={() => setUser(student)}>login-{name}</button>
      <button onClick={() => setUser({ ...student, id: "student-two" })}>
        switch-{name}
      </button>
      <button
        onClick={() =>
          updateReadingPreferences(student.id, {
            text_size: "comfortable",
            text_size_by_device: { phone: "compact" },
          })
        }
      >
        choose-{name}
      </button>
      <output data-testid={`preferences-${name}`}>
        {JSON.stringify(user?.text_size_by_device)}
      </output>
      <button onClick={clear}>logout-{name}</button>
    </div>
  );
}
function mount() {
  return render(
    <SessionProvider>
      <Probe />
      <Probe name="two" />
    </SessionProvider>,
  );
}
function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((done) => {
    resolve = done;
  });
  return { promise, resolve };
}

beforeEach(() => {
  mockApi.mockReset();
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("Phiên dùng chung và cache giao diện", () => {
  it("gộp yêu cầu từ nhiều thành phần và chỉ cache 30 giây", async () => {
    vi.useFakeTimers();
    mockApi.mockResolvedValue(student);
    mount();
    await act(async () => {});
    expect(screen.getByTestId("one")).toHaveTextContent(student.id);
    expect(screen.getByTestId("two")).toHaveTextContent(student.id);
    fireEvent.click(screen.getByText("cached-one"));
    fireEvent.click(screen.getByText("cached-two"));
    expect(mockApi).toHaveBeenCalledTimes(1);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(30_000);
    });
    expect(mockApi).toHaveBeenCalledTimes(2);
  });

  it("gộp các lần kiểm tra bắt buộc đang chờ", async () => {
    mockApi.mockResolvedValueOnce(student);
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
    const request = deferred<User>();
    mockApi.mockReturnValueOnce(request.promise);
    fireEvent.click(screen.getByText("force-one"));
    fireEvent.click(screen.getByText("force-two"));
    expect(mockApi).toHaveBeenCalledTimes(2);
    await act(async () => {
      request.resolve(student);
    });
  });

  it("kiểm tra lại khi quay về tab và xóa trạng thái khi server trả 401", async () => {
    mockApi.mockResolvedValueOnce(student);
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
    mockApi.mockRejectedValueOnce(new ApiError(401, "Hết phiên"));
    await act(async () => {
      window.dispatchEvent(new Event("focus"));
    });
    expect(screen.getByTestId("one")).toHaveTextContent("anonymous");
    expect(mockApi).toHaveBeenLastCalledWith("/auth/me", {
      redirectOnUnauthorized: false,
    });
  });

  it("không hiểu lỗi mạng là chưa đăng nhập, cho phép kiểm tra lại", async () => {
    mockApi.mockRejectedValueOnce(new ApiError(503, "Mất kết nối"));
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent("error:Mất kết nối"),
    );
    mockApi.mockResolvedValueOnce(student);
    fireEvent.click(screen.getByText("force-one"));
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
  });

  it("yêu cầu cũ không thể khôi phục cache sau đăng xuất", async () => {
    const request = deferred<User>();
    mockApi.mockReturnValueOnce(request.promise);
    mount();
    fireEvent.click(screen.getByText("logout-one"));
    await act(async () => {
      request.resolve(student);
    });
    expect(screen.getByTestId("one")).toHaveTextContent("anonymous");
  });

  it("kết quả kiểm tra cũ không ghi đè lần đăng nhập mới", async () => {
    const request = deferred<User>();
    mockApi.mockReturnValueOnce(request.promise);
    mount();
    fireEvent.click(screen.getByText("login-one"));
    await act(async () => {
      request.resolve({ ...student, id: "old-account" });
    });
    expect(screen.getByTestId("one")).toHaveTextContent(student.id);
  });

  it("hết thời hạn sẽ kiểm tra backend và xóa trạng thái dù không chuyển trang", async () => {
    vi.useFakeTimers();
    mockApi.mockResolvedValueOnce({
      ...student,
      session_expires_at: new Date(Date.now() + 1000).toISOString(),
    });
    mount();
    await act(async () => {});
    mockApi.mockRejectedValueOnce(new ApiError(401, "Hết phiên"));
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1000);
    });
    expect(screen.getByTestId("one")).toHaveTextContent("anonymous");
  });

  it("xóa cache khi API bảo vệ báo hết phiên", async () => {
    mockApi.mockResolvedValueOnce(student);
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
    act(() => {
      window.dispatchEvent(new Event("viettree:session-expired"));
    });
    expect(screen.getByTestId("one")).toHaveTextContent("anonymous");
  });

  it("đồng bộ đăng xuất giữa các tab và không phát tán thông tin tài khoản", async () => {
    const postMessage = vi.fn();
    let receive!: (event: { data: string }) => void;
    vi.stubGlobal(
      "BroadcastChannel",
      class {
        postMessage = postMessage;
        close = vi.fn();
        set onmessage(value: typeof receive) {
          receive = value;
        }
      },
    );
    mockApi.mockResolvedValueOnce(student);
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
    fireEvent.click(screen.getByText("login-one"));
    expect(postMessage).toHaveBeenLastCalledWith("refresh");
    act(() => {
      receive({ data: "logout" });
    });
    expect(screen.getByTestId("one")).toHaveTextContent("anonymous");
  });

  it("chọn trang chủ đúng vai trò, ưu tiên admin với tài khoản nhiều vai trò", () => {
    expect(homeFor(student)).toBe("/student/dashboard");
    expect(homeFor({ roles: ["student", "admin"] })).toBe("/admin/dashboard");
    expect(homeFor({ roles: ["teacher"] })).toBe("/teacher/dashboard");
    expect(homeFor({ roles: ["guardian"] })).toBe("/guardian/dashboard");
    expect(homeFor({ roles: [] })).toBe("/403");
  });

  it("cỡ chữ mới cập nhật cache ngay và yêu cầu kiểm tra cũ không ghi đè", async () => {
    mockApi.mockResolvedValueOnce(student);
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
    const oldRequest = deferred<User>();
    mockApi.mockReturnValueOnce(oldRequest.promise);
    fireEvent.click(screen.getByText("force-one"));
    fireEvent.click(screen.getByText("choose-one"));
    await act(async () => {
      oldRequest.resolve(student);
    });
    expect(screen.getByTestId("preferences-one")).toHaveTextContent(
      '"phone":"compact"',
    );
    fireEvent.click(screen.getByText("cached-one"));
    expect(mockApi).toHaveBeenCalledTimes(2);
  });

  it.each(["logout-one", "switch-one"])(
    "lưu cỡ chữ muộn không đổi tài khoản sau %s",
    async (action) => {
      mockApi.mockResolvedValueOnce(student);
      mount();
      await waitFor(() =>
        expect(screen.getByTestId("one")).toHaveTextContent(student.id),
      );
      fireEvent.click(screen.getByText(action));
      fireEvent.click(screen.getByText("choose-one"));
      expect(screen.getByTestId("one")).toHaveTextContent(
        action === "logout-one" ? "anonymous" : "student-two",
      );
      expect(screen.getByTestId("preferences-one")).toBeEmptyDOMElement();
    },
  );

  it("đổi cỡ chữ chỉ báo các tab kiểm tra lại, không gửi dữ liệu tài khoản", async () => {
    const postMessage = vi.fn();
    let receive!: (event: { data: string }) => void;
    vi.stubGlobal(
      "BroadcastChannel",
      class {
        postMessage = postMessage;
        close = vi.fn();
        set onmessage(value: typeof receive) {
          receive = value;
        }
      },
    );
    mockApi.mockResolvedValueOnce(student);
    mount();
    await waitFor(() =>
      expect(screen.getByTestId("one")).toHaveTextContent(student.id),
    );
    fireEvent.click(screen.getByText("choose-one"));
    expect(postMessage).toHaveBeenLastCalledWith("preferences");
    const updated = {
      ...student,
      text_size_by_device: { desktop: "large" as const },
    };
    const oldRequest = deferred<User>();
    mockApi.mockReturnValueOnce(oldRequest.promise);
    fireEvent.click(screen.getByText("force-one"));
    mockApi.mockResolvedValueOnce(updated);
    act(() => {
      receive({ data: "preferences" });
    });
    expect(screen.getByTestId("one")).toHaveTextContent(student.id);
    await waitFor(() =>
      expect(screen.getByTestId("preferences-one")).toHaveTextContent(
        '"desktop":"large"',
      ),
    );
    await act(async () => {
      oldRequest.resolve(student);
    });
    expect(screen.getByTestId("preferences-one")).toHaveTextContent(
      '"desktop":"large"',
    );
  });
});
