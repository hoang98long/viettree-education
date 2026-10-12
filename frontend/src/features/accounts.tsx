"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api, dateTimeLabel } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { Page } from "@/lib/types";
import { useUser } from "@/components/shell";
import { useSession } from "@/lib/session";

type Account = {
  id: string;
  username: string;
  display_name: string;
  email: string | null;
  roles: string[];
  current_grade: number | null;
  text_size: string;
  is_active: boolean;
  account_revision: number;
  must_change_password: boolean;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
  auth_provider: string;
  password_changed_at: string | null;
};
type History = {
  action: string;
  actor_username: string;
  created_at: string;
  old_values: Record<string, unknown> | null;
  new_values: Record<string, unknown>;
};
type Detail = Account & { active_sessions: number; history: History[] };
const roles = [
  ["student", "Học sinh"],
  ["guardian", "Phụ huynh"],
  ["teacher", "Giáo viên"],
  ["admin", "Quản trị viên"],
];
const actionNames: Record<string, string> = {
  account_created: "Tạo tài khoản",
  account_updated: "Cập nhật tài khoản",
  account_password_reset: "Đặt lại mật khẩu",
  account_password_changed: "Tự đổi mật khẩu",
  account_sessions_revoked: "Thu hồi toàn bộ phiên",
  account_other_sessions_revoked: "Đăng xuất các phiên khác",
};
export const passwordHelp =
  "Dùng ít nhất 15 ký tự, có thể là cụm vài từ dễ nhớ. Không dùng tên đăng nhập hay mật khẩu phổ biến. Mật khẩu phân biệt hoa/thường.";

function HistoryDetails({ entry }: { entry: History }) {
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
      return value === "large" ? "Chữ lớn hơn" : "Vừa đủ lớn";
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

function ConfirmFields({ action }: { action: string }) {
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

export function AccountsPage() {
  const [search, setSearch] = useState(""),
    [role, setRole] = useState(""),
    [status, setStatus] = useState(""),
    [grade, setGrade] = useState(""),
    [page, setPage] = useState(1);
  const params = new URLSearchParams({
    search,
    page: String(page),
    ...(role ? { role } : {}),
    ...(status ? { status } : {}),
    ...(grade ? { grade } : {}),
  });
  const resource = useResource<Page<Account>>(`/admin/accounts?${params}`);
  return (
    <>
      <PageTitle
        title="Quản trị tài khoản"
        description="Quản lý thông tin, vai trò, trạng thái và bảo mật. Gói Free/VIP được quản lý riêng cho học sinh."
      />
      <div className="actions">
        <Link className="button" href="/admin/accounts/new">
          Tạo tài khoản
        </Link>
        <Link className="button secondary" href="/account/security">
          Bảo mật của tôi
        </Link>
      </div>
      <div className="filters section-title">
        <label>
          Tìm tài khoản
          <input
            type="search"
            value={search}
            maxLength={160}
            placeholder="Tên đăng nhập, tên hiển thị hoặc email"
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
        <label>
          Vai trò
          <select
            value={role}
            onChange={(e) => {
              setRole(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            {roles.map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Trạng thái
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            <option value="active">Hoạt động</option>
            <option value="inactive">Đã khóa</option>
          </select>
        </label>
        <label>
          Lớp của học sinh
          <select
            value={grade}
            onChange={(e) => {
              setGrade(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                Lớp {n}
              </option>
            ))}
          </select>
        </label>
      </div>
      {resource.loading ? (
        <Loading />
      ) : resource.error || !resource.data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          {!resource.data.items.length ? (
            <Empty>Chưa có tài khoản phù hợp.</Empty>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Tài khoản</th>
                    <th>Vai trò/lớp</th>
                    <th>Trạng thái</th>
                    <th>Truy cập gần nhất</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {resource.data.items.map((item) => (
                    <tr key={item.id}>
                      <td>
                        <strong>{item.display_name}</strong>
                        <p>{item.username}</p>
                        <small>{item.email || "Chưa có email liên hệ"}</small>
                      </td>
                      <td>
                        {roles
                          .filter(([code]) => item.roles.includes(code))
                          .map(([, name]) => name)
                          .join(", ")}
                        {item.roles.includes("student") && (
                          <p>Lớp {item.current_grade}</p>
                        )}
                      </td>
                      <td>
                        {item.is_active ? "Hoạt động" : "Đã khóa"}
                        {item.must_change_password && <p>Cần đổi mật khẩu</p>}
                      </td>
                      <td>{dateTimeLabel(item.last_login_at)}</td>
                      <td>
                        <Link
                          className="button secondary small"
                          href={`/admin/accounts/${item.id}/edit`}
                        >
                          Quản lý
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="pagination">
            <span>
              {resource.data.total} tài khoản · Trang {page}/
              {Math.max(1, Math.ceil(resource.data.total / 20))}
            </span>
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage((n) => n - 1)}
            >
              Trang trước
            </button>
            <button
              className="button secondary"
              disabled={page * 20 >= resource.data.total}
              onClick={() => setPage((n) => n + 1)}
            >
              Trang sau
            </button>
          </div>
        </>
      )}
    </>
  );
}

function AccountForm({
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
              Cỡ chữ học sinh
              <select
                name="text_size"
                defaultValue={account?.text_size || "comfortable"}
              >
                <option value="comfortable">Vừa đủ lớn</option>
                <option value="large">Chữ lớn hơn</option>
              </select>
            </label>
            <p className="muted">
              Hiện có học liệu lớp 3 và lớp 4. Đổi lớp không xóa kết quả cũ; gói
              mặc định Free. Quản lý VIP ở trang gói học.
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

function SecurityAction({
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
