import { describe, expect, it } from "vitest";
import { detectDeviceType, resolveTextSize } from "./reading-preferences";
import type { ReadingPreferences } from "./types";

const desktop = {
  userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/145",
  maxTouchPoints: 0,
  screenWidth: 1920,
  screenHeight: 1080,
  coarsePointer: false,
};

describe("Cỡ chữ theo loại thiết bị", () => {
  it.each([
    ["desktop", desktop],
    ["desktop", { ...desktop, maxTouchPoints: 10 }],
    [
      "phone",
      {
        ...desktop,
        userAgent: "iPhone Mobile",
        screenWidth: 390,
        screenHeight: 844,
      },
    ],
    [
      "phone",
      {
        ...desktop,
        userAgent: "iPhone Mobile",
        screenWidth: 844,
        screenHeight: 390,
      },
    ],
    [
      "phone",
      {
        ...desktop,
        userAgent: "Android Mobile",
        screenWidth: 360,
        screenHeight: 800,
      },
    ],
    [
      "phone",
      { ...desktop, mobile: true, screenWidth: 390, screenHeight: 844 },
    ],
    [
      "tablet",
      { ...desktop, userAgent: "iPad", screenWidth: 768, screenHeight: 1024 },
    ],
    ["tablet", { ...desktop, userAgent: "Macintosh", maxTouchPoints: 5 }],
    [
      "tablet",
      {
        ...desktop,
        userAgent: "Android Chrome",
        screenWidth: 800,
        screenHeight: 1280,
      },
    ],
    [
      "tablet",
      {
        ...desktop,
        coarsePointer: true,
        maxTouchPoints: 10,
        screenWidth: 768,
        screenHeight: 1024,
      },
    ],
  ])("nhận diện %s từ khả năng thiết bị", (expected, info) => {
    expect(detectDeviceType(info)).toBe(expected);
  });

  it("giữ cỡ chữ mặc định cũ cho thiết bị chưa có lựa chọn riêng", () => {
    const preferences: ReadingPreferences = {
      text_size: "large",
      text_size_by_device: { phone: "compact", tablet: "comfortable" },
    };
    expect(resolveTextSize(preferences, "phone")).toBe("compact");
    expect(resolveTextSize(preferences, "tablet")).toBe("comfortable");
    expect(resolveTextSize(preferences, "desktop")).toBe("large");
    expect(resolveTextSize(preferences, null)).toBe("large");
    expect(resolveTextSize(null, "phone")).toBe("comfortable");
  });

  it("điện thoại giữ nhóm khi trình duyệt thay đổi thông tin màn hình", () => {
    for (const width of [320, 390, 768, 1280]) {
      expect(
        detectDeviceType({
          ...desktop,
          userAgent: "iPhone Mobile",
          screenWidth: width,
          screenHeight: 900,
        }),
      ).toBe("phone");
    }
  });
});
