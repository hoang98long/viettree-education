"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useSession } from "@/lib/session";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty, PageTitle } from "@/components/ui";
import { AccountPicker } from "@/features/academy/account-picker";
import type { Classroom } from "@/features/classrooms/types";
import { ClassRoster, FreeLearners } from "@/features/classrooms/roster";
import { AssignmentPanel } from "@/features/classrooms/assignments";
import { RecognitionBoard } from "@/features/classrooms/recognition";

export function ClassroomsPage() {
  const { user } = useSession();
  const admin = !!user?.roles.includes("admin");
  const classes = useResource<Classroom[]>("/classroom/classes", true);
  const [chosen, setChosen] = useState("");
  const current =
    classes.data?.find((c) => c.id === chosen) || classes.data?.[0];
  return (
    <>
      <PageTitle
        title={admin ? "Lớp học và học sinh tự do" : "Lớp được phân công"}
        description="Quản lý ghi danh, giao bài cá nhân hoặc cả lớp và tuyên dương kết quả học tập."
      />
      {admin && (
        <details className="panel">
          <summary>Tạo lớp quản lý mới</summary>
          <ClassForm onSaved={classes.retry} />
        </details>
      )}
      {classes.loading && !classes.data ? (
        <Loading />
      ) : classes.error ? (
        <ErrorState message={classes.error} retry={classes.retry} />
      ) : !current ? (
        <Empty>
          Chưa có lớp được phân công. Học sinh vẫn có thể tự học theo gói của
          mình.
        </Empty>
      ) : (
        <>
          <label>
            Chọn lớp quản lý
            <select
              aria-label="Chọn lớp quản lý"
              value={current.id}
              onChange={(e) => setChosen(e.target.value)}
            >
              {classes.data?.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} · khối {c.grade} · {c.student_count} học sinh
                  {!c.is_active ? " · Đã đóng" : ""}
                </option>
              ))}
            </select>
          </label>
          {admin && (
            <details className="panel">
              <summary>Thông tin và cài đặt lớp</summary>
              <ClassForm
                key={current.id + ":" + current.edit_revision}
                initial={current}
                onSaved={classes.retry}
              />
            </details>
          )}
          <ClassRoster
            key={`roster:${current.id}`}
            classroom={current}
            admin={admin}
            onChanged={classes.retry}
          />
          <AssignmentPanel
            key={`assignment:${current.id}:${current.grade}`}
            classroom={current}
            admin={admin}
          />
          {current.is_active && (
            <RecognitionBoard
              key={`recognition:${current.id}`}
              classroom={current}
              staff
            />
          )}
        </>
      )}
      {admin && !current && <AssignmentPanel admin />}
      {admin && <FreeLearners classroom={current} onEnrolled={classes.retry} />}
    </>
  );
}

export function ClassForm({
  initial,
  onSaved,
}: {
  initial?: Classroom;
  onSaved: () => void;
}) {
  const [name, setName] = useState(initial?.name || "");
  const [grade, setGrade] = useState(initial?.grade || 4);
  const [year, setYear] = useState(initial?.academic_year || "2026-2027");
  const [teacher, setTeacher] = useState(initial?.teacher_user_id || "");
  const [school, setSchool] = useState(initial?.school_id || "");
  const [active, setActive] = useState(initial?.is_active ?? true);
  const [recognize, setRecognize] = useState(
    initial?.recognition_enabled ?? true,
  );
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const schools =
    useResource<{ id: string; name: string }[]>("/classroom/schools");
  async function save() {
    setBusy(true);
    try {
      await api(
        initial ? `/classroom/classes/${initial.id}` : "/classroom/classes",
        {
          method: initial ? "PUT" : "POST",
          body: JSON.stringify({
            name,
            grade,
            academic_year: year,
            teacher_id: teacher || null,
            school_id: school || null,
            is_active: active,
            recognition_enabled: recognize,
            revision: initial?.edit_revision,
          }),
        },
      );
      onSaved();
      setMessage("Đã lưu lớp và nhật ký.");
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <label>
        Tên lớp quản lý
        <input
          aria-label="Tên lớp quản lý"
          maxLength={160}
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </label>
      <div className="two-columns">
        <label>
          Khối lớp
          <select
            aria-label="Khối lớp quản lý"
            value={grade}
            onChange={(e) => setGrade(Number(e.target.value))}
          >
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n}>{n}</option>
            ))}
          </select>
        </label>
        <label>
          Năm học
          <input
            aria-label="Năm học"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            placeholder="2026-2027"
          />
        </label>
      </div>
      <AccountPicker
        label="Giáo viên của lớp"
        role="teacher"
        value={teacher}
        onChange={setTeacher}
      />
      <label>
        Trường
        <select value={school} onChange={(e) => setSchool(e.target.value)}>
          <option value="">Nhóm học chung, chưa gắn trường</option>
          {schools.data?.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </label>
      <label className="check-label">
        <input
          type="checkbox"
          checked={active}
          onChange={(e) => setActive(e.target.checked)}
        />{" "}
        Lớp đang hoạt động
      </label>
      <label className="check-label">
        <input
          type="checkbox"
          checked={recognize}
          onChange={(e) => setRecognize(e.target.checked)}
        />{" "}
        Hiện thành tích và tuyên dương riêng trong lớp
      </label>
      <p>
        Học sinh xem biệt danh của bạn khác. Khi đóng lớp, dữ liệu và lịch sử
        được giữ.
      </p>
      <button className="button" disabled={busy} onClick={() => void save()}>
        {initial ? "Lưu cài đặt lớp" : "Tạo lớp quản lý"}
      </button>
      <p role="status">{message}</p>
    </>
  );
}
