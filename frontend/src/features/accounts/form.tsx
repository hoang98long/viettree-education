"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useUser } from "@/components/shell";
import type { Account } from "@/features/accounts/types";
import { roles, passwordHelp } from "@/features/accounts/constants";
import { ConfirmFields } from "@/features/accounts/shared";

export function AccountForm({
  account,
  onSaved,
}: {
  account?: Account;
  onSaved: (account: Account) => void;
}) {
  const user = useUser();
  const own = account?.id === user.id;
  const [chosen, setChosen] = useState(account?.roles || ["student"]),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  return (
    <form
      className="panel account-form"
      onSubmit={async (e) => {
        e.preventDefault();
        const form = e.currentTarget,
          fields = new FormData(form);
        setBusy(true);
        setError("");
        try {
          const result = await api<Account>(
            account ? `/admin/accounts/${account.id}` : "/admin/accounts",
            {
              method: account ? "PATCH" : "POST",
              body: JSON.stringify({
                username: fields.get("username"),
                display_name: fields.get("display_name"),
                email: fields.get("email") || null,
                roles: chosen,
                current_grade: chosen.includes("student")
                  ? Number(fields.get("grade"))
                  : null,
                text_size: fields.get("text_size") || "comfortable",
                reason: fields.get("reason"),
                actor_password: fields.get("actor_password"),
                ...(account
                  ? {
                      revision: account.account_revision,
                      is_active: own
                        ? account.is_active
                        : fields.get("is_active") === "on",
                    }
                  : {
                      password: fields.get("password"),
                      must_change_password: true,
                    }),
              }),
            },
          );
          form.reset();
          onSaved(result);
        } catch (err) {
          setError((err as Error).message);
        } finally {
          setBusy(false);
        }
      }}
    >
      <h2>
        {account ? "Thông tin và quyền truy cập" : "Thông tin tài khoản mới"}
      </h2>
      {error && (
        <p role="alert" className="notice error">
          {error}
        </p>
      )}
      <fieldset disabled={busy}>
        <label>
          Tên đăng nhập
          <input
            name="username"
            required
            minLength={3}
            maxLength={80}
            defaultValue={account?.username}
            pattern="[a-zA-Z0-9][a-zA-Z0-9._\-]{2,79}"
            autoComplete="off"
          />
        </label>
        <p className="muted">
          Chữ không dấu, số, dấu chấm, gạch dưới/gạch ngang. Không phân biệt
          hoa/thường; đổi tên đăng nhập sẽ đăng xuất các phiên.
        </p>
        <label>
          Tên hiển thị
          <input
            name="display_name"
            required
            maxLength={160}
            defaultValue={account?.display_name}
          />
        </label>
        <label>
          Email liên hệ (không bắt buộc)
          <input
            name="email"
            type="email"
            maxLength={255}
            defaultValue={account?.email || ""}
          />
        </label>
        <p className="muted">
          Email chưa được xác minh, chưa dùng để khôi phục mật khẩu. Học sinh
          không cần cung cấp email riêng.
        </p>
        <fieldset disabled={own}>
          <legend>Vai trò tài khoản</legend>
          <div className="actions">
            {roles.map(([code, name]) => (
              <label className="check-label" key={code}>
                <input
                  type="checkbox"
                  checked={chosen.includes(code)}
                  onChange={(e) =>
                    setChosen(
                      e.target.checked
                        ? [...chosen, code]
                        : chosen.filter((r) => r !== code),
                    )
                  }
                />
                {name}
              </label>
            ))}
          </div>
        </fieldset>
        {chosen.includes("student") && (
          <>
            <label>
              Lớp đang học
              <select name="grade" defaultValue={account?.current_grade || 4}>
                {[1, 2, 3, 4, 5].map((n) => (
                  <option key={n} value={n}>
                    Lớp {n}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Cỡ chữ mặc định của học sinh
              <select
                name="text_size"
                defaultValue={account?.text_size || "comfortable"}
              >
                <option value="compact">Chữ gọn hơn</option>
                <option value="comfortable">Vừa đủ lớn</option>
                <option value="large">Chữ lớn hơn</option>
              </select>
            </label>
            <p className="muted">
              Cỡ chữ mặc định áp dụng khi học sinh chưa chọn riêng cho thiết bị.{" "}
              Hiện có học liệu lớp 1–5. Đổi lớp không xóa kết quả cũ; gói mặc
              định Free. Quản lý VIP ở trang gói học.
            </p>
          </>
        )}
        {account ? (
          <label className="check-label">
            <input
              name="is_active"
              type="checkbox"
              defaultChecked={account.is_active}
              disabled={own}
            />
            Tài khoản hoạt động
          </label>
        ) : (
          <>
            <label>
              Mật khẩu tạm
              <input
                name="password"
                type="password"
                required
                minLength={15}
                maxLength={256}
                autoComplete="new-password"
              />
            </label>
            <p className="muted">
              {passwordHelp} Người dùng phải đổi mật khẩu tạm trước khi sử dụng.
            </p>
          </>
        )}
        {account && (
          <p className="notice">
            Khóa, đổi vai trò hoặc tên đăng nhập sẽ thu hồi các phiên đăng nhập.
            Giữ nguyên lịch sử học tập và thời hạn VIP. Không thể tự khóa/thay
            vai trò của mình.
          </p>
        )}
        <ConfirmFields action={account ? "cập nhật" : "tạo tài khoản"} />
        <button className="button" type="submit" disabled={!chosen.length}>
          {busy ? "Đang lưu…" : account ? "Lưu tài khoản" : "Tạo tài khoản"}
        </button>
      </fieldset>
    </form>
  );
}
