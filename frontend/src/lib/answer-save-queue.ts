import type { Answer } from "./types";

export type SaveState = {
  pending: number;
  saving: boolean;
  error: string;
  saved: boolean;
};

// One request at a time: a slow response must not remove a newer answer.
export class AnswerSaveQueue {
  private pending = new Map<string, Answer>();
  private operation: Promise<void> | null = null;
  private controller: AbortController | null = null;
  private active = true;
  private listeners = new Set<() => void>();
  private state: SaveState = {
    pending: 0,
    saving: false,
    error: "",
    saved: false,
  };

  constructor(
    private save: (
      id: string,
      answer: Answer,
      signal: AbortSignal,
    ) => Promise<unknown>,
  ) {}

  snapshot = () => this.state;
  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };

  private update(values: Partial<SaveState>) {
    this.state = { ...this.state, ...values, pending: this.pending.size };
    this.listeners.forEach((listener) => listener());
  }

  change(id: string, answer: Answer) {
    this.pending.set(id, structuredClone(answer));
    this.update({ saved: false, error: "" });
  }

  resume() {
    this.active = true;
  }
  stop() {
    this.active = false;
    this.controller?.abort();
  }

  flush = (): Promise<void> => {
    if (this.operation) return this.operation;
    if (!this.pending.size) return Promise.resolve();
    if (!this.active)
      return Promise.reject(new Error("Trang làm bài đã đóng."));
    this.update({ saving: true, error: "" });
    this.operation = this.drain().finally(() => {
      this.operation = null;
      this.update({ saving: false });
    });
    return this.operation;
  };

  private async drain() {
    try {
      while (this.pending.size) {
        if (!this.active) throw new Error("Trang làm bài đã đóng.");
        const [id, answer] = this.pending.entries().next().value!;
        this.controller = new AbortController();
        await this.save(id, answer, this.controller.signal);
        if (!this.active) throw new Error("Trang làm bài đã đóng.");
        if (this.pending.get(id) === answer) this.pending.delete(id);
        this.update({});
      }
      this.update({ saved: true });
    } catch (error) {
      if (this.active)
        this.update({
          error:
            error instanceof Error
              ? error.message
              : "Chưa lưu được. Em thử lại nhé.",
        });
      throw error;
    } finally {
      this.controller = null;
    }
  }
}
