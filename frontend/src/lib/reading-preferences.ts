import type { DeviceType, ReadingPreferences, TextSize } from "./types";

export const deviceLabels: Record<DeviceType, string> = {
  phone: "Điện thoại",
  tablet: "Máy tính bảng",
  desktop: "Máy tính",
};

type DeviceInfo = {
  userAgent: string;
  mobile?: boolean;
  maxTouchPoints: number;
  screenWidth: number;
  screenHeight: number;
  coarsePointer: boolean;
};

export function detectDeviceType(info: DeviceInfo): DeviceType {
  const { userAgent, maxTouchPoints } = info;
  if (
    /iPad|Tablet|PlayBook|Silk/i.test(userAgent) ||
    (/Macintosh/i.test(userAgent) && maxTouchPoints > 1) ||
    (/Android/i.test(userAgent) && !/Mobile/i.test(userAgent))
  )
    return "tablet";
  if (info.mobile || /Mobi|iPhone|iPod/i.test(userAgent)) return "phone";
  // Fallback for browsers hiding device names; rotation preserves the shortest side.
  const shortestSide = Math.min(info.screenWidth, info.screenHeight);
  if (info.coarsePointer && maxTouchPoints > 0)
    return shortestSide >= 600 ? "tablet" : "phone";
  return "desktop";
}

export function browserDeviceType(): DeviceType {
  const clientHints = navigator as Navigator & {
    userAgentData?: { mobile: boolean };
  };
  return detectDeviceType({
    userAgent: navigator.userAgent,
    mobile: clientHints.userAgentData?.mobile,
    maxTouchPoints: navigator.maxTouchPoints,
    screenWidth: window.screen.width,
    screenHeight: window.screen.height,
    coarsePointer: window.matchMedia("(pointer: coarse)").matches,
  });
}

export function resolveTextSize(
  preferences: ReadingPreferences | null,
  device: DeviceType | null,
): TextSize {
  return (
    (device && preferences?.text_size_by_device?.[device]) ||
    preferences?.text_size ||
    "comfortable"
  );
}
