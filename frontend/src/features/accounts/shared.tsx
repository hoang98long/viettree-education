"use client";

import type { History } from "@/features/accounts/types";
import { roles } from "@/features/accounts/constants";

export function HistoryDetails({ entry }: { entry: History }) {
  const fields = [
    ["username", "Tên đăng nhập"],
    ["display_name", "Tên hiển thị"],
    ["roles", "Vai trò"],
    ["is_active", "Hoạt động"],
    ["current_grade", "Lớp"],
    ["text_size", "Cỡ chữ"],
    ["must_change_password", "Cần đổi mật khẩu tạm"],
  ];
  const render = (key: string, value: unknown) => {
    if (value === null || value === undefined) return "—";
    if (Array.isArray(value))
      return roles
        .filter(([code]) => value.includes(code))
        .map(([, name]) => name)
        .join(", ");
    if (typeof value === "boolean") return value ? "Có" : "Không";
    if (key === "text_size")
      return value === "compact"
        ? "Chữ gọn hơn"
        : value === "large"
          ? "Chữ lớn hơn"
          : "Vừa đủ lớn";
    return String(value);
  };
  return (
    <ul>
      {fields
        .filter(
          ([key]) =>
            key in entry.new_values &&
            JSON.stringify(entry.old_values?.[key]) !==
              JSON.stringify(entry.new_values[key]),
        )
        .map(([key, name]) => (
          <li key={key}>
            {name}: {render(key, entry.old_values?.[key])} →{" "}
            {render(key, entry.new_values[key])}
          </li>
        ))}
      {entry.new_values.email_changed === true && (
        <li>Đã thay đổi email liên hệ.</li>
      )}
      {entry.new_values.sessions_revoked === true && (
        <li>Đã thu hồi các phiên đăng nhập.</li>
      )}
      {typeof entry.new_values.revoked_sessions === "number" && (
        <li>Đã thu hồi {entry.new_values.revoked_sessions} bản ghi phiên.</li>
      )}
    </ul>
  );
}

export function ConfirmFields({ action }: { action: string }) {
  return (
    <>
      <label>
        Lý do {action}
        <textarea name="reason" required minLength={5} maxLength={500} />
      </label>
      <label>
        Mật khẩu của quản trị viên
        <input
          name="actor_password"
          type="password"
          required
          maxLength={256}
          autoComplete="current-password"
        />
      </label>
      <p className="muted">
        Ghi lý do cụ thể; không ghi mật khẩu vào lý do. Mật khẩu xác nhận chỉ
        dùng cho thao tác này.
      </p>
    </>
  );
}
