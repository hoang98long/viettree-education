"use client";

import { useSyncExternalStore } from "react";
import { api } from "@/lib/api";
import { browserDeviceType, resolveTextSize } from "@/lib/reading-preferences";
import { useSession } from "@/lib/session";
import type { ReadingPreferences, TextSize } from "@/lib/types";

function subscribe(onChange: () => void) {
  window.addEventListener("resize", onChange);
  window.addEventListener("orientationchange", onChange);
  return () => {
    window.removeEventListener("resize", onChange);
    window.removeEventListener("orientationchange", onChange);
  };
}

const serverDeviceType = () => null;

export function useReadingPreferences() {
  const { user, updateReadingPreferences } = useSession();
  const deviceType = useSyncExternalStore(
    subscribe,
    browserDeviceType,
    serverDeviceType,
  );
  const textSize = resolveTextSize(user, deviceType);
  async function saveTextSize(size: TextSize) {
    if (!user || !deviceType)
      throw new Error("Hãy đợi trang tải xong rồi chọn cỡ chữ.");
    const ownerId = user.id;
    const preferences = await api<ReadingPreferences>(
      "/students/me/accessibility",
      {
        method: "PUT",
        body: JSON.stringify({ text_size: size, device_type: deviceType }),
      },
    );
    updateReadingPreferences(ownerId, preferences);
  }
  return { textSize, deviceType, saveTextSize };
}
