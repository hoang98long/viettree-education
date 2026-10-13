"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import type { Account } from "@/features/accounts/types";
import { passwordHelp } from "@/features/accounts/constants";
import { ConfirmFields } from "@/features/accounts/shared";

export function SecurityAction({
  account,
  kind,
  onSaved,
}: {
  account: Account;
  kind: "reset-password" | "revoke-sessions";
  onSaved: () => void;
}) {
  const [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const reset = kind === "reset-password";
  return (
    <form
      className="panel account-form"
      onSubmit={async (e) => {
        e.preventDefault();
        const form = e.currentTarget,
          fields = new FormData(form);
        if (
          reset &&
          fields.get("new_password") !== fields.get("confirm_password")
        ) {
          setError("Hai mật khẩu mới chưa khớp");
          return;
        }
        setBusy(true);
        setError("");
        try {
          await api(`/admin/accounts/${account.id}/${kind}`, {
            method: "POST",
            body: JSON.stringify({
              revision: account.account_revision,
              reason: fields.get("reason"),
              actor_password: fields.get("actor_password"),
              ...(reset ? { new_password: fields.get("new_password") } : {}),
            }),
          });
          form.reset();
          onSaved();
        } catch (err) {
          setError((err as Error).message);
        } finally {
          setBusy(false);
        }
      }}
    >
      <h2>{reset ? "Đặt lại mật khẩu" : "Thu hồi phiên đăng nhập"}</h2>
      <p>
        {reset
          ? "Mật khẩu cũ sẽ mất hiệu lực, toàn bộ phiên bị thu hồi. Người dùng phải đổi mật khẩu tạm ở lần đăng nhập tiếp theo."
          : "Đăng xuất tài khoản này khỏi tất cả thiết bị. Người dùng có thể đăng nhập lại nếu tài khoản còn hoạt động."}
      </p>
      {error && (
        <p role="alert" className="notice error">
          {error}
        </p>
      )}
      <fieldset disabled={busy}>
        {reset && (
          <>
            <label>
              Mật khẩu tạm mới
              <input
                name="new_password"
                type="password"
                required
                minLength={15}
                maxLength={256}
                autoComplete="new-password"
              />
            </label>
            <label>
              Nhập lại mật khẩu tạm mới
              <input
                name="confirm_password"
                type="password"
                required
                minLength={15}
                maxLength={256}
                autoComplete="new-password"
              />
            </label>
            <p className="muted">{passwordHelp}</p>
          </>
        )}
        <ConfirmFields action={reset ? "đặt lại mật khẩu" : "thu hồi phiên"} />
        <button className="button" type="submit">
          {busy
            ? "Đang xử lý…"
            : reset
              ? "Đặt lại mật khẩu và thu hồi phiên"
              : "Thu hồi tất cả phiên"}
        </button>
      </fieldset>
    </form>
  );
}
