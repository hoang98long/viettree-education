"use client";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
export function AccountPicker({
  role,
  grade,
  value,
  onChange,
  label,
}: {
  role: "teacher" | "student" | "guardian";
  grade?: number;
  value: string;
  onChange: (value: string) => void;
  label: string;
}) {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const list = useResource<{
    items: { id: string; display_name: string; username: string }[];
    total: number;
  }>(
    `/admin/accounts?status=active&role=${role}&page=${page}&search=${encodeURIComponent(search)}${grade ? "&grade=" + grade : ""}`,
  );
  return (
    <div className="academy-picker">
      <input
        aria-label={"Tìm " + label}
        type="search"
        placeholder="Tìm theo tên hoặc tài khoản"
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
          setPage(1);
        }}
      />
      <select
        aria-label={label}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">Chọn tài khoản…</option>
        {list.data?.items.map((a) => (
          <option key={a.id} value={a.id}>
            {a.display_name} · {a.username}
          </option>
        ))}
      </select>
      {list.error && <p role="alert">{list.error}</p>}
      <div className="academy-actions">
        <button
          type="button"
          className="button secondary small"
          disabled={page === 1}
          onClick={() => setPage((p) => p - 1)}
        >
          Trước
        </button>
        <span>Trang {page}</span>
        <button
          type="button"
          className="button secondary small"
          disabled={!list.data || page * 20 >= list.data.total}
          onClick={() => setPage((p) => p + 1)}
        >
          Sau
        </button>
      </div>
    </div>
  );
}
