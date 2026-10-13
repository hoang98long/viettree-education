"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { dateTimeLabel } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { useUser } from "@/components/shell";
import { useSession } from "@/lib/session";
import type { Detail } from "@/features/accounts/types";
import { AccountForm } from "@/features/accounts/form";
import { actionNames } from "@/features/accounts/constants";
import { SecurityAction } from "@/features/accounts/security-action";
import { HistoryDetails } from "@/features/accounts/shared";

export function AccountEditorPage({ id }: { id?: string }) {
  const router = useRouter(),
    user = useUser(),
    session = useSession();
  const resource = useResource<Detail>(
    id ? `/admin/accounts/${id}` : "/admin/accounts?page=1",
  );
  const [notice, setNotice] = useState("");
  if (id && resource.loading) return <Loading />;
  if (id && (resource.error || !resource.data))
    return <ErrorState message={resource.error} retry={resource.retry} />;
  const account = id ? resource.data! : undefined;
  return (
    <>
      <PageTitle
        title={account ? `Quản lý: ${account.username}` : "Tạo tài khoản"}
      />
      <Link className="button secondary" href="/admin/accounts">
        Về danh sách tài khoản
      </Link>
      {notice && (
        <p role="status" className="notice">
          {notice}
        </p>
      )}
      <div className="account-layout section-title">
        <AccountForm
          key={account ? `${account.id}:${account.account_revision}` : "new"}
          account={account}
          onSaved={(result) => {
            if (!id) {
              router.push(`/admin/accounts/${result.id}/edit`);
              return;
            }
            setNotice("Đã lưu tài khoản.");
            resource.retry();
            if (id === user.id) void session.refresh(true);
          }}
        />
        {account && (
          <div>
            <section className="panel">
              <h2>Hoạt động tài khoản</h2>
              <p>
                Tạo: {dateTimeLabel(account.created_at)} · Sửa:{" "}
                {dateTimeLabel(account.updated_at)}
              </p>
              <p>Truy cập gần nhất: {dateTimeLabel(account.last_login_at)}</p>
              <p>Đổi mật khẩu: {dateTimeLabel(account.password_changed_at)}</p>
              <p>
                {account.active_sessions} phiên chưa hết hạn và chưa bị thu hồi
              </p>
              <p>
                {account.must_change_password
                  ? "Cần đổi mật khẩu tạm"
                  : "Đã thiết lập mật khẩu"}
              </p>
              {account.roles.includes("student") && (
                <Link
                  className="button secondary"
                  href={`/admin/students/${account.id}/membership`}
                >
                  Quản lý gói Free/VIP
                </Link>
              )}
              {id === user.id && (
                <Link className="button secondary" href="/account/security">
                  Đổi mật khẩu của tôi
                </Link>
              )}
            </section>
            {id !== user.id && account.auth_provider === "local" && (
              <SecurityAction
                key={`reset:${account.account_revision}`}
                account={account}
                kind="reset-password"
                onSaved={() => {
                  setNotice("Đã đặt lại mật khẩu và thu hồi các phiên.");
                  resource.retry();
                }}
              />
            )}
            <SecurityAction
              key={`sessions:${account.account_revision}`}
              account={account}
              kind="revoke-sessions"
              onSaved={() => {
                if (id === user.id) {
                  session.clear();
                  router.replace("/login");
                  return;
                }
                setNotice("Đã thu hồi tất cả phiên đăng nhập.");
                resource.retry();
              }}
            />
          </div>
        )}
      </div>
      {account && (
        <section className="panel section-title">
          <h2>Nhật ký tài khoản</h2>
          <p>
            20 thao tác gần nhất. Không lưu mật khẩu, hash hay mã phiên vào nhật
            ký.
          </p>
          {!account.history.length ? (
            <Empty>Chưa có thao tác quản trị tài khoản.</Empty>
          ) : (
            account.history.map((entry, index) => (
              <article className="account-history" key={index}>
                <h3>{actionNames[entry.action] || "Thao tác tài khoản"}</h3>
                <p>
                  {entry.actor_username || "Tài khoản không còn khả dụng"} ·{" "}
                  {dateTimeLabel(entry.created_at)}
                </p>
                <p>{String(entry.new_values.reason || "")}</p>
                <details>
                  <summary>Chi tiết thay đổi</summary>
                  <HistoryDetails entry={entry} />
                </details>
              </article>
            ))
          )}
        </section>
      )}
    </>
  );
}
