"use client";
import { useEffect, useState, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { AnswerSaveQueue } from "@/lib/answer-save-queue";
import type { Answer } from "@/lib/types";

export function useAnswerAutosave(attemptId: string) {
  const router = useRouter();
  const [queue] = useState(
    () =>
      new AnswerSaveQueue(async (id, answer, signal) => {
        const controller = new AbortController();
        const abort = () => controller.abort();
        let timedOut = false;
        signal.addEventListener("abort", abort, { once: true });
        if (signal.aborted) abort();
        const timer = window.setTimeout(() => {
          timedOut = true;
          controller.abort();
        }, 15000);
        try {
          return await api(`/attempts/${attemptId}/answers/${id}`, {
            method: "PUT",
            body: JSON.stringify({ answer }),
            signal: controller.signal,
            redirectOnUnauthorized: false,
          });
        } catch (error) {
          if (timedOut)
            throw new Error("Lưu lâu hơn dự kiến. Em thử lưu lại nhé.");
          throw error;
        } finally {
          window.clearTimeout(timer);
          signal.removeEventListener("abort", abort);
        }
      }),
  );
  const state = useSyncExternalStore(
    queue.subscribe,
    queue.snapshot,
    queue.snapshot,
  );
  const [revision, setRevision] = useState(0);

  useEffect(() => {
    queue.resume();
    return () => queue.stop();
  }, [queue]);

  useEffect(() => {
    if (!state.pending || state.saving || state.error) return;
    const timer = window.setTimeout(() => {
      void queue.flush().catch(() => {});
    }, 800);
    return () => window.clearTimeout(timer);
  }, [queue, state.pending, state.saving, state.error, revision]);

  useEffect(() => {
    let navigation = 0;
    const retry = () => {
      void queue.flush().catch(() => {});
    };
    const warn = (event: BeforeUnloadEvent) => {
      if (queue.snapshot().pending) {
        event.preventDefault();
        event.returnValue = "";
      }
    };
    const leave = (event: MouseEvent) => {
      if (
        !queue.snapshot().pending ||
        event.defaultPrevented ||
        event.button !== 0 ||
        event.ctrlKey ||
        event.metaKey ||
        event.shiftKey ||
        event.altKey
      )
        return;
      const anchor =
        event.target instanceof Element
          ? event.target.closest("a[href]")
          : null;
      if (
        !(anchor instanceof HTMLAnchorElement) ||
        anchor.target ||
        anchor.hasAttribute("download")
      )
        return;
      const target = new URL(anchor.href);
      if (
        target.origin !== window.location.origin ||
        (target.pathname === window.location.pathname &&
          target.search === window.location.search)
      )
        return;
      event.preventDefault();
      const request = ++navigation;
      void queue
        .flush()
        .then(() => {
          if (request === navigation)
            router.push(`${target.pathname}${target.search}${target.hash}`);
        })
        .catch(() => {});
    };
    window.addEventListener("online", retry);
    window.addEventListener("beforeunload", warn);
    document.addEventListener("click", leave, true);
    return () => {
      window.removeEventListener("online", retry);
      window.removeEventListener("beforeunload", warn);
      document.removeEventListener("click", leave, true);
    };
  }, [queue, router]);

  return {
    ...state,
    change(id: string, answer: Answer) {
      queue.change(id, answer);
      setRevision((value) => value + 1);
    },
    flush: queue.flush,
  };
}
