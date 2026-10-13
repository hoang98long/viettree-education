"use client";
import Link from "next/link";
import { useState } from "react";
import { dateTimeLabel } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { Page } from "@/lib/types";
import type { Account } from "@/features/accounts/types";
import { roles } from "@/features/accounts/constants";

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
