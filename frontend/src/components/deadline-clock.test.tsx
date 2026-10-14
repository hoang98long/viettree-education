import { act, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DeadlineClock } from "./deadline-clock";

afterEach(() => vi.useRealTimers());
describe("Thời gian làm bài", () => {
  it("lấy mốc máy chủ dù giờ trên thiết bị sai và cập nhật sau khi đổi giờ thiết bị", () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2040-01-01"));
    render(
      <DeadlineClock
        serverTime="2026-10-14T01:00:00Z"
        deadline="2026-10-14T01:02:01Z"
      />,
    );
    expect(screen.getByRole("timer")).toHaveTextContent("02:01");
    expect(screen.queryByRole("status")).not.toBeInTheDocument();
    act(() => vi.advanceTimersByTime(1000));
    expect(screen.getByRole("status")).toHaveTextContent("Sắp hết giờ");
    vi.setSystemTime(new Date("2050-01-01"));
    act(() => vi.advanceTimersByTime(1000));
    expect(screen.getByRole("timer")).toHaveTextContent("01:59");
  });
  it("hết giờ không chạy dưới 0 hoặc tự gọi nộp bài", () => {
    vi.useFakeTimers();
    render(
      <DeadlineClock
        serverTime="2026-10-14T01:00:00Z"
        deadline="2026-10-14T01:00:01Z"
      />,
    );
    act(() => vi.advanceTimersByTime(5000));
    expect(screen.getByRole("timer")).toHaveTextContent("00:00");
    expect(screen.getByRole("status")).toHaveTextContent("Máy chủ sẽ kiểm tra");
  });
});
