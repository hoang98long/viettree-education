"use client";
import Link from "next/link";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState } from "@/components/ui";
import { AccountPicker } from "@/features/academy/account-picker";
import type { Classroom, Learner } from "@/features/classrooms/types";

export function ClassRoster({
  classroom,
  admin,
  onChanged,
}: {
  classroom: Classroom;
  admin: boolean;
  onChanged: () => void;
}) {
  const [page, setPage] = useState(1);
  const roster = useResource<{ items: Learner[]; total: number }>(
    `/classroom/students?class_id=${classroom.id}&grade=${classroom.grade}&page=${page}`,
  );
  const [student, setStudent] = useState("");
  const [message, setMessage] = useState("");
  async function enroll(id: string, value: boolean) {
    try {
      await api(`/classroom/classes/${classroom.id}/enrollments`, {
        method: "POST",
        body: JSON.stringify({ student_id: id, enrolled: value }),
      });
      roster.retry();
      onChanged();
      setMessage(
        value
          ? "Đã ghi danh vào lớp."
          : "Đã chuyển ra khỏi lớp; tài khoản và kết quả được giữ.",
      );
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>Học sinh trong lớp · {classroom.name}</h2>
      {admin && classroom.is_active && (
        <>
          <AccountPicker
            label="Học sinh để ghi danh"
            role="student"
            grade={classroom.grade}
            value={student}
            onChange={setStudent}
          />
          <button
            className="button secondary"
            disabled={!student}
            onClick={() => void enroll(student, true)}
          >
            Ghi danh vào lớp
          </button>
        </>
      )}
      {roster.loading ? (
        <Loading />
      ) : roster.error ? (
        <ErrorState message={roster.error} retry={roster.retry} />
      ) : (
        <>
          <p>{roster.data?.total} học sinh đang ghi danh</p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Học sinh</th>
                  <th>Khối</th>
                  <th>Quản lý</th>
                </tr>
              </thead>
              <tbody>
                {roster.data?.items.map((s) => (
                  <tr key={s.id}>
                    <td>
                      {s.display_name}
                      <br />
                      <small>{s.username}</small>
                    </td>
                    <td>{s.current_grade}</td>
                    <td>
                      {admin && (
                        <Link
                          className="button secondary small"
                          href={`/admin/students/${s.id}/membership`}
                        >
                          Gói VIP
                        </Link>
                      )}
                      <button
                        className="button secondary small"
                        onClick={() => void enroll(s.id, false)}
                      >
                        Chuyển ra khỏi lớp
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="quiz-actions">
            <button
              className="button secondary small"
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
            >
              Trang trước
            </button>
            <span>Trang {page}</span>
            <button
              className="button secondary small"
              disabled={page * 50 >= (roster.data?.total || 0)}
              onClick={() => setPage(page + 1)}
            >
              Trang sau
            </button>
          </div>
        </>
      )}
      <p role="status">{message}</p>
    </section>
  );
}

export function FreeLearners({
  classroom,
  onEnrolled,
}: {
  classroom?: Classroom;
  onEnrolled: () => void;
}) {
  const [grade, setGrade] = useState(4);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");
  const list = useResource<{ items: Learner[]; total: number }>(
    `/classroom/students?grade=${grade}&free_only=true&page=${page}&search=${encodeURIComponent(search)}`,
  );
  async function enroll(id: string) {
    try {
      await api(`/classroom/classes/${classroom!.id}/enrollments`, {
        method: "POST",
        body: JSON.stringify({ student_id: id, enrolled: true }),
      });
      list.retry();
      onEnrolled();
      setMessage("Đã ghi danh học sinh tự do.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>Học sinh tự do</h2>
      <p>
        Không có ghi danh trong lớp đang hoạt động; vẫn học và có kết quả theo
        gói Free/VIP.
      </p>
      <div className="two-columns">
        <label>
          Khối của học sinh tự do
          <select
            value={grade}
            onChange={(e) => {
              setGrade(Number(e.target.value));
              setPage(1);
            }}
          >
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n}>{n}</option>
            ))}
          </select>
        </label>
        <label>
          Tìm học sinh tự do
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
      </div>
      {list.loading ? (
        <Loading />
      ) : list.error ? (
        <ErrorState message={list.error} retry={list.retry} />
      ) : (
        <>
          <p>{list.data?.total} tài khoản</p>
          {list.data?.items.map((s) => (
            <div className="list-row" key={s.id}>
              <span>
                {s.display_name} · {s.username}
              </span>
              {classroom?.is_active && classroom.grade === grade && (
                <button
                  className="button secondary small"
                  onClick={() => void enroll(s.id)}
                >
                  Ghi danh {classroom.name}
                </button>
              )}
            </div>
          ))}
          <div className="quiz-actions">
            <button
              className="button secondary small"
              disabled={page === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Trước
            </button>
            <span>Trang {page}</span>
            <button
              className="button secondary small"
              disabled={page * 50 >= (list.data?.total || 0)}
              onClick={() => setPage((p) => p + 1)}
            >
              Sau
            </button>
          </div>
        </>
      )}
      <p role="status">{message}</p>
    </section>
  );
}
