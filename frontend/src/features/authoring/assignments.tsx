"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading } from "@/components/ui";
import type { Page, Student } from "@/lib/types";

export function AssignmentPanel({ id }: { id: string }) {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const students = useResource<Page<Student>>(
    `/admin/students?search=${encodeURIComponent(search)}&page=${page}`,
  );
  const [selected, setSelected] = useState<string[]>([]);
  const [available, setAvailable] = useState("");
  const [due, setDue] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  return (
    <section className="panel">
      <h2>Giao bài cho học sinh</h2>
      <p>
        Chọn tối đa 50 học sinh. Hệ thống kiểm tra lớp và gói của từng em; nếu
        có em chưa đủ quyền, toàn bộ lần giao sẽ dừng.
      </p>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          setBusy(true);
          setError("");
          setNotice("");
          try {
            const result = await api<{ count: number }>(
              `/admin/authoring/assessments/${id}/assign`,
              {
                method: "POST",
                body: JSON.stringify({
                  student_ids: selected,
                  available_at: available
                    ? new Date(available).toISOString()
                    : null,
                  due_at: due ? new Date(due).toISOString() : null,
                }),
              },
            );
            setNotice(
              `Đã giao hoặc mở lại nhiệm vụ cho ${result.count} học sinh.`,
            );
          } catch (e) {
            setError((e as Error).message);
          } finally {
            setBusy(false);
          }
        }}
      >
        <label>
          Tìm học sinh để giao
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
        {students.loading ? (
          <Loading />
        ) : students.error ? (
          <ErrorState message={students.error} retry={students.retry} />
        ) : (
          students.data?.items.map((student) => (
            <label className="confirmation-row" key={student.id}>
              <input
                type="checkbox"
                disabled={
                  busy ||
                  !student.is_active ||
                  (!selected.includes(student.id) && selected.length >= 50)
                }
                checked={selected.includes(student.id)}
                onChange={(e) =>
                  setSelected(
                    e.target.checked
                      ? [...selected, student.id]
                      : selected.filter((value) => value !== student.id),
                  )
                }
              />
              {student.display_name} ({student.username}) · Lớp{" "}
              {student.current_grade}
            </label>
          ))
        )}
        <div className="quiz-actions">
          <button
            type="button"
            className="button secondary"
            disabled={page === 1}
            onClick={() => setPage((value) => value - 1)}
          >
            Trang trước học sinh
          </button>
          <span>
            Trang {page} · Đã chọn {selected.length}
          </span>
          <button
            type="button"
            className="button secondary"
            disabled={!students.data || page * 20 >= students.data.total}
            onClick={() => setPage((value) => value + 1)}
          >
            Trang sau học sinh
          </button>
        </div>
        <div className="two-columns">
          <label>
            Giờ mở (để trống = ngay bây giờ)
            <input
              type="datetime-local"
              value={available}
              onChange={(e) => setAvailable(e.target.value)}
            />
          </label>
          <label>
            Hạn nộp (không bắt buộc)
            <input
              type="datetime-local"
              value={due}
              onChange={(e) => setDue(e.target.value)}
            />
          </label>
        </div>
        <button className="button" disabled={busy || !selected.length}>
          {busy ? "Đang giao…" : "Xác nhận giao bài"}
        </button>
        <p role="status">{notice}</p>
        {error && (
          <p className="error-text" role="alert">
            {error}
          </p>
        )}
      </form>
    </section>
  );
}
