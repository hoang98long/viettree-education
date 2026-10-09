"use client";
import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";

export function useResource<T>(path: string, keepPreviousOnRefresh = false) {
  const [state, setState] = useState<{
    data: T | null;
    error: string;
    loading: boolean;
    key: string;
    errorCode?: string;
  }>({ data: null, error: "", loading: true, key: "" });
  const [version, setVersion] = useState(0);
  const retry = useCallback(() => setVersion((v) => v + 1), []);
  const key = `${path}:${version}`;
  useEffect(() => {
    const controller = new AbortController();
    api<T>(path, { signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted)
          setState({ data, error: "", loading: false, key });
      })
      .catch((error: Error) => {
        if (!controller.signal.aborted)
          setState({
            data: null,
            error: error.message,
            errorCode: error instanceof ApiError ? error.code : undefined,
            loading: false,
            key,
          });
      });
    return () => controller.abort();
  }, [path, version, key]);
  return state.key === key
    ? { ...state, retry }
    : {
        data:
          keepPreviousOnRefresh && state.key.startsWith(`${path}:`)
            ? state.data
            : null,
        error: "",
        errorCode: undefined,
        loading: true,
        retry,
      };
}
