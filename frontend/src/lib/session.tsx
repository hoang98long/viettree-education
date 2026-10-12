"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { usePathname } from "next/navigation";
import { api, ApiError } from "./api";
import type { User } from "./types";

const CACHE_MS = 30_000;
type SessionState = { user: User | null; loading: boolean; error: string };
type SessionContextValue = SessionState & {
  refresh: (force?: boolean) => Promise<void>;
  setUser: (user: User) => void;
  clear: () => void;
};
const SessionContext = createContext<SessionContextValue | null>(null);

export function homeFor(user: Pick<User, "roles" | "must_change_password">) {
  if (user.must_change_password) return "/account/security";
  const role = ["admin", "student", "teacher", "guardian"].find((value) =>
    user.roles.includes(value),
  );
  return role ? `/${role}/dashboard` : "/403";
}

// Chỉ cache trạng thái giao diện trong bộ nhớ. Quyền truy cập do backend kiểm tra.
export function SessionProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<SessionState>({
    user: null,
    loading: true,
    error: "",
  });
  const checkedAt = useRef(0);
  const generation = useRef(0);
  const pending = useRef<Promise<void> | null>(null);
  const channel = useRef<BroadcastChannel | null>(null);
  const path = usePathname();

  const invalidate = useCallback(() => {
    generation.current += 1;
    pending.current = null;
    checkedAt.current = 0;
    setState({ user: null, loading: false, error: "" });
  }, []);

  const refresh = useCallback((force = false): Promise<void> => {
    if (pending.current) return pending.current;
    if (!force && Date.now() - checkedAt.current < CACHE_MS)
      return Promise.resolve();
    const version = ++generation.current;
    const request = api<User>("/auth/me", { redirectOnUnauthorized: false })
      .then((user) => {
        if (version !== generation.current) return;
        checkedAt.current = Date.now();
        setState({ user, loading: false, error: "" });
      })
      .catch((error: Error) => {
        if (version !== generation.current) return;
        const anonymous = error instanceof ApiError && error.status === 401;
        checkedAt.current = anonymous ? Date.now() : 0;
        setState({
          user: null,
          loading: false,
          error: anonymous ? "" : error.message,
        });
      })
      .finally(() => {
        if (version === generation.current) pending.current = null;
      });
    pending.current = request;
    return request;
  }, []);

  const setUser = useCallback((user: User) => {
    generation.current += 1;
    pending.current = null;
    checkedAt.current = Date.now();
    setState({ user, loading: false, error: "" });
    channel.current?.postMessage("refresh");
  }, []);

  const clear = useCallback(() => {
    invalidate();
    channel.current?.postMessage("logout");
  }, [invalidate]);

  useEffect(() => {
    void refresh();
  }, [path, refresh]);

  useEffect(() => {
    const recheck = () => {
      if (document.visibilityState === "visible") void refresh(true);
    };
    const interval = window.setInterval(() => {
      if (document.visibilityState === "visible") void refresh();
    }, CACHE_MS);
    window.addEventListener("focus", recheck);
    window.addEventListener("pageshow", recheck);
    document.addEventListener("visibilitychange", recheck);
    window.addEventListener("viettree:session-expired", invalidate);
    if (typeof BroadcastChannel !== "undefined") {
      channel.current = new BroadcastChannel("viettree-session");
      channel.current.onmessage = (event) => {
        if (event.data !== "logout" && event.data !== "refresh") return;
        invalidate();
        if (event.data === "refresh") {
          setState({ user: null, loading: true, error: "" });
          void refresh(true);
        }
      };
    }
    return () => {
      window.clearInterval(interval);
      window.removeEventListener("focus", recheck);
      window.removeEventListener("pageshow", recheck);
      document.removeEventListener("visibilitychange", recheck);
      window.removeEventListener("viettree:session-expired", invalidate);
      channel.current?.close();
      channel.current = null;
    };
  }, [refresh, invalidate]);

  useEffect(() => {
    if (!state.user?.session_expires_at) return;
    const remaining = Date.parse(state.user.session_expires_at) - Date.now();
    if (!Number.isFinite(remaining)) return;
    const timer = window.setTimeout(
      () => {
        // Kiểm tra lại DB, không dùng đồng hồ client làm bằng chứng xác thực.
        void refresh(true);
      },
      remaining > 0 ? Math.min(remaining, 2_147_483_647) : CACHE_MS,
    );
    return () => window.clearTimeout(timer);
  }, [state.user, refresh]);

  return (
    <SessionContext.Provider value={{ ...state, refresh, setUser, clear }}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (!context) throw new Error("useSession cần SessionProvider");
  return context;
}
