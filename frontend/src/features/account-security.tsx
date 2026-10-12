"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, dateTimeLabel } from "@/lib/api";
import { homeFor, useSession } from "@/lib/session";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading } from "@/components/ui";
import { passwordHelp } from "@/features/accounts";
import type { User } from "@/lib/types";

type Security = {
  username: string;
  auth_provider: string;
  must_change_password: boolean;
  password_changed_at: string | null;
  active_sessions: number;
  sessions: { created_at: string; expires_at: string; is_current: boolean }[];
};

export function AccountSecurityPage() {
  const session = useSession(),
    router = useRouter();
  const resource = useResource<Security>("/auth/security");
  const [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    [notice, setNotice] = useState("");
  useEffect(() => {
    if (!session.loading && !session.user && !session.error)
      router.replace("/login");
  }, [session.loading, session.user, session.error, router]);
  if (session.error)
    return (
      <main className="standalone">
        <ErrorState
          message={session.error}
          retry={() => void session.refresh(true)}
        />
      </main>
    );
  if (session.loading || !session.user || resource.loading)
    return (
      <main className="standalone">
        <Loading />
      </main>
    );
  if (resource.error || !resource.data)
    return (
      <main className="standalone">
        <ErrorState message={resource.error} retry={resource.retry} />
      </main>
    );
  const data = resource.data;
  return (
    <main id="main" className="account-security standalone">
      <h1>Bảo mật tài khoản</h1>
      <p>
        Tài khoản: <strong>{data.username}</strong>
      </p>
      {data.must_change_password && (
        <p className="notice">
          Bạn đang dùng mật khẩu tạm. Hãy đặt mật khẩu riêng trước khi tiếp tục.
        </p>
      )}
      {notice && (
        <p role="status" className="notice">
          {notice}
        </p>
      )}
      {error && (
        <p role="alert" className="notice error">
          {error}
        </p>
      )}
      {data.auth_provider === "local" ? (
        <form
          className="panel account-form"
          onSubmit={async (e) => {
            e.preventDefault();
            const form = e.currentTarget,
              fields = new FormData(form);
            setError("");
            setNotice("");
            if (fields.get("new_password") !== fields.get("confirm_password")) {
              setError("Hai mật khẩu mới chưa khớp");
              return;
            }
            setBusy(true);
            try {
              await api("/auth/password", {
                method: "POST",
                body: JSON.stringify({
                  current_password: fields.get("current_password"),
                  new_password: fields.get("new_password"),
                }),
              });
              form.reset();
              session.setUser(await api<User>("/auth/me"));
              resource.retry();
              setNotice(
                "Đã đổi mật khẩu. Các phiên cũ đã đăng xuất; phiên hiện tại được thay mới.",
              );
            } catch (err) {
              setError((err as Error).message);
            } finally {
              setBusy(false);
            }
          }}
        >
          <h2>Đổi mật khẩu</h2>
          <p>
            {passwordHelp} Có thể nhờ người lớn hỗ trợ chọn và lưu mật khẩu.
          </p>
          <fieldset disabled={busy}>
            <label>
              Mật khẩu hiện tại
              <input
                name="current_password"
                type="password"
                required
                maxLength={256}
                autoComplete="current-password"
              />
            </label>
            <label>
              Mật khẩu mới
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
              Nhập lại mật khẩu mới
              <input
                name="confirm_password"
                type="password"
                required
                minLength={15}
                maxLength={256}
                autoComplete="new-password"
              />
            </label>
            <button className="button" type="submit">
              {busy ? "Đang xử lý…" : "Đổi mật khẩu"}
            </button>
          </fieldset>
        </form>
      ) : (
        <p>Đổi mật khẩu tại nhà cung cấp đăng nhập của bạn.</p>
      )}
      <section className="panel section-title">
        <h2>Phiên đăng nhập</h2>
        <p>
          {data.active_sessions} phiên chưa hết hạn và chưa bị thu hồi · Đổi mật
          khẩu gần nhất: {dateTimeLabel(data.password_changed_at)}
        </p>
        <ul>
          {data.sessions.map((item, index) => (
            <li key={index}>
              {item.is_current ? "Phiên hiện tại" : "Phiên khác"} · Tạo{" "}
              {dateTimeLabel(item.created_at)} · Hết hạn{" "}
              {dateTimeLabel(item.expires_at)}
            </li>
          ))}
        </ul>
        {!data.must_change_password && (
          <form
            className="account-form"
            onSubmit={async (e) => {
              e.preventDefault();
              const form = e.currentTarget,
                fields = new FormData(form);
              setBusy(true);
              setError("");
              setNotice("");
              try {
                const result = await api<{ revoked_sessions: number }>(
                  "/auth/sessions/revoke-others",
                  {
                    method: "POST",
                    body: JSON.stringify({
                      current_password: fields.get("current_password"),
                    }),
                  },
                );
                form.reset();
                resource.retry();
                setNotice(
                  `Đã thu hồi ${result.revoked_sessions} phiên khác. Phiên hiện tại được giữ.`,
                );
              } catch (err) {
                setError((err as Error).message);
              } finally {
                setBusy(false);
              }
            }}
          >
            <fieldset disabled={busy}>
              <label>
                Xác nhận mật khẩu để đăng xuất phiên khác
                <input
                  name="current_password"
                  type="password"
                  required
                  maxLength={256}
                  autoComplete="current-password"
                />
              </label>
              <button className="button secondary" type="submit">
                Đăng xuất các phiên khác
              </button>
            </fieldset>
          </form>
        )}
      </section>
      <div className="actions section-title">
        {!data.must_change_password && (
          <Link className="button" href={homeFor(session.user)}>
            Tiếp tục sử dụng
          </Link>
        )}
        <button
          disabled={busy}
          className="button secondary"
          onClick={async () => {
            setBusy(true);
            try {
              await api("/auth/logout", { method: "POST" });
              session.clear();
              router.replace("/login");
            } catch (err) {
              setError((err as Error).message);
            } finally {
              setBusy(false);
            }
          }}
        >
          Đăng xuất
        </button>
      </div>
    </main>
  );
}
