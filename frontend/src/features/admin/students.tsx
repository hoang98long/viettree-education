"use client";
import Link from "next/link";
import { useState } from "react";
import { api } from "@/lib/api";
import type { Page, Student } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { Data, Pagination } from "@/features/admin/shared";

export function EditStudent({
  student,
  onClose,
}: {
  student: Student;
  onClose: () => void;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <div className="modal-backdrop">
      <section
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="student-edit-title"
      >
        <h2 id="student-edit-title">Hồ sơ {student.username}</h2>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const fields = new FormData(e.currentTarget);
            setBusy(true);
            setError("");
            try {
              await api(`/admin/students/${student.id}`, {
                method: "PATCH",
                body: JSON.stringify({
                  display_name: fields.get("display_name"),
                  current_grade: Number(fields.get("grade")),
                }),
              });
              onClose();
            } catch (err) {
              setError((err as Error).message);
              setBusy(false);
            }
          }}
        >
          <label htmlFor="edit-name">Tên hiển thị</label>
          <input
            autoFocus
            id="edit-name"
            name="display_name"
            defaultValue={student.display_name}
            required
            maxLength={160}
          />
          <label htmlFor="edit-grade">Lớp</label>
          <select
            id="edit-grade"
            name="grade"
            defaultValue={student.current_grade}
          >
            {[1, 2, 3, 4, 5].map((grade) => (
              <option value={grade} key={grade}>
                Lớp {grade}
              </option>
            ))}
          </select>
          {error && <p role="alert">{error}</p>}
          <div className="quiz-actions">
            <button
              type="button"
              className="button secondary"
              onClick={onClose}
              disabled={busy}
            >
              Đóng
            </button>
            <button className="button" disabled={busy}>
              {busy ? "Đang lưu…" : "Lưu hồ sơ"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

export function StudentsPage() {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Student | null>(null);
  const [refresh, setRefresh] = useState(0);
  const path = `/admin/students?search=${encodeURIComponent(search)}&page=${page}`;
  return (
    <>
      <PageTitle
        title="Học sinh"
        description="Chỉ quản lý thông tin cần thiết cho học tập."
      />
      <div className="actions">
        <Link className="button" href="/admin/accounts/new">
          Tạo tài khoản học sinh
        </Link>
        <Link className="button secondary" href="/admin/accounts">
          Quản trị mọi tài khoản
        </Link>
      </div>
      <div className="filters">
        <label>
          Tìm theo tên
          <input
            value={search}
            placeholder="Tên hiển thị hoặc tên đăng nhập"
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
      </div>
      <Data<Page<Student>> key={path + refresh} path={path}>
        {(data) => (
          <>
            {data.items.length ? (
              <div className="panel table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Học sinh</th>
                      <th>Tên đăng nhập</th>
                      <th>Lớp</th>
                      <th>Trạng thái</th>
                      <th>Hồ sơ</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.items.map((student) => (
                      <tr key={student.id}>
                        <td>{student.display_name}</td>
                        <td>{student.username}</td>
                        <td>{student.current_grade}</td>
                        <td>
                          <span className="badge">
                            {student.is_active ? "Hoạt động" : "Đã khóa"}
                          </span>
                        </td>
                        <td>
                          <button
                            className="button secondary small"
                            onClick={() => setSelected(student)}
                          >
                            Xem / cập nhật
                          </button>
                          <Link
                            className="button secondary small"
                            href={`/admin/accounts/${student.id}/edit`}
                          >
                            Quản lý tài khoản
                          </Link>
                          <Link
                            className="button secondary small"
                            href={`/admin/students/${student.id}/membership`}
                          >
                            Quản lý gói học
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <Empty>Không có học sinh phù hợp.</Empty>
            )}
            <Pagination page={page} total={data.total} onChange={setPage} />
          </>
        )}
      </Data>
      {selected && (
        <EditStudent
          student={selected}
          onClose={() => {
            setSelected(null);
            setRefresh((value) => value + 1);
          }}
        />
      )}
    </>
  );
}
