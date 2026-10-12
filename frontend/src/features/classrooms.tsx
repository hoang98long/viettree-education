"use client";
import Link from "next/link";
import { useState, useRef } from "react";
import { Trophy, Medal } from "lucide-react";
import { api } from "@/lib/api";
import { useSession } from "@/lib/session";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty, PageTitle } from "@/components/ui";
import { AccountPicker } from "./academy/account-picker";

type Classroom = {
  id: string;
  name: string;
  grade: number;
  academic_year: string;
  school_id: string | null;
  teacher_user_id: string | null;
  is_active: boolean;
  edit_revision: number;
  recognition_enabled: boolean;
  student_count: number;
};
type Learner = {
  id: string;
  display_name: string;
  username: string;
  current_grade: number;
};
const labels: Record<string, string> = {
  MATH: "Toán",
  VIETNAMESE: "Tiếng Việt",
  ENGLISH: "Tiếng Anh",
  AI: "AI · câu hỏi lý thuyết",
  AI_PROJECT: "AI · sản phẩm được chấm",
};
export function ClassroomsPage() {
  const { user } = useSession();
  const admin = !!user?.roles.includes("admin");
  const classes = useResource<Classroom[]>("/classroom/classes");
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
      {classes.loading ? (
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
            key={current.id}
            classroom={current}
            admin={admin}
            onChanged={classes.retry}
          />
          <AssignmentPanel
            key={current.id + ":" + current.grade}
            classroom={current}
            admin={admin}
          />
          {current.is_active && (
            <RecognitionBoard key={current.id} classroom={current} staff />
          )}
        </>
      )}
      {admin && !current && <AssignmentPanel admin />}
      {admin && <FreeLearners classroom={current} onEnrolled={classes.retry} />}
    </>
  );
}
function ClassForm({
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
      <label>
        <input
          type="checkbox"
          checked={active}
          onChange={(e) => setActive(e.target.checked)}
        />{" "}
        Lớp đang hoạt động
      </label>
      <label>
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
function ClassRoster({
  classroom,
  admin,
  onChanged,
}: {
  classroom: Classroom;
  admin: boolean;
  onChanged: () => void;
}) {
  const roster = useResource<{ items: Learner[]; total: number }>(
    `/classroom/students?class_id=${classroom.id}&grade=${classroom.grade}`,
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
        </>
      )}
      <p role="status">{message}</p>
    </section>
  );
}
function FreeLearners({
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
function AssignmentPanel({
  classroom,
  admin,
}: {
  classroom?: Classroom;
  admin: boolean;
}) {
  const [mode, setMode] = useState(classroom ? "class" : "individual");
  const [student, setStudent] = useState("");
  const [grade, setGrade] = useState(classroom?.grade || 4);
  const [kind, setKind] = useState("assessment");
  const [resourceId, setResourceId] = useState("");
  const [deadline, setDeadline] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const effectiveGrade = mode === "class" ? classroom?.grade || grade : grade;
  const request = useRef<{ fingerprint: string; key: string } | null>(null);
  const resources = useResource<
    { id: string; title: string; minimum_plan_code: string }[]
  >(`/classroom/resources?kind=${kind}&grade=${effectiveGrade}`);
  const current =
    resourceId ||
    resources.data?.find((r) => r.minimum_plan_code === "free")?.id ||
    resources.data?.[0]?.id ||
    "";
  async function assign() {
    setBusy(true);
    try {
      const body = {
        kind,
        resource_id: current,
        class_id: mode === "class" ? classroom?.id : null,
        student_ids: mode === "individual" ? [student] : [],
        due_at: deadline ? new Date(deadline).toISOString() : null,
      };
      const fingerprint = JSON.stringify(body);
      if (!request.current || request.current.fingerprint !== fingerprint)
        request.current = { fingerprint, key: crypto.randomUUID() };
      const result = await api<{ count: number }>("/classroom/assignments", {
        method: "POST",
        body: JSON.stringify({
          kind,
          resource_id: current,
          class_id: mode === "class" ? classroom?.id : null,
          student_ids: mode === "individual" ? [student] : [],
          due_at: deadline ? new Date(deadline).toISOString() : null,
          idempotency_key: request.current.key,
        }),
      });
      setMessage(
        `Đã giao cho ${result.count} học sinh. VIP được kiểm tra theo tài khoản nhận bài.`,
      );
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel">
      <h2>Giao bài cho lớp hoặc cá nhân</h2>
      {admin && (
        <label>
          Đối tượng giao bài
          <select
            aria-label="Đối tượng giao bài"
            value={mode}
            onChange={(e) => setMode(e.target.value)}
          >
            <option value="class">Cả lớp đang chọn</option>
            <option value="individual">
              Học sinh riêng, kể cả học sinh tự do
            </option>
          </select>
        </label>
      )}
      {mode === "individual" && (
        <>
          <label>
            Khối của bài
            <select
              value={grade}
              onChange={(e) => {
                setGrade(Number(e.target.value));
                setResourceId("");
              }}
            >
              {[1, 2, 3, 4, 5].map((n) => (
                <option key={n}>{n}</option>
              ))}
            </select>
          </label>
          <AccountPicker
            label="Học sinh nhận bài riêng"
            role="student"
            grade={grade}
            value={student}
            onChange={setStudent}
          />
        </>
      )}
      <label>
        Loại bài giao
        <select
          aria-label="Loại bài giao"
          value={kind}
          onChange={(e) => {
            setKind(e.target.value);
            setResourceId("");
          }}
        >
          <option value="assessment">Bài luyện tập có chấm điểm</option>
          <option value="lesson">Bài học ba môn</option>
          <option value="ai_lesson">Bài đào tạo AI Academy</option>
        </select>
      </label>
      {resources.loading ? (
        <Loading />
      ) : resources.error ? (
        <ErrorState message={resources.error} retry={resources.retry} />
      ) : (
        <label>
          Chọn nội dung giao
          <select
            aria-label="Chọn nội dung giao"
            value={current}
            onChange={(e) => setResourceId(e.target.value)}
          >
            {resources.data?.map((r) => (
              <option key={r.id} value={r.id}>
                {r.title} · {r.minimum_plan_code === "vip" ? "VIP" : "Miễn phí"}
              </option>
            ))}
          </select>
        </label>
      )}
      <label>
        Hạn hoàn thành (không bắt buộc)
        <input
          type="datetime-local"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
        />
      </label>
      <p>
        Giao bài VIP không tự nâng gói. Nếu có học sinh chưa đủ quyền, hãy chọn
        bài miễn phí hoặc giao riêng cho tài khoản VIP.
      </p>
      <button
        className="button"
        disabled={
          busy ||
          !current ||
          (mode === "individual" && !student) ||
          (mode === "class" && !classroom?.is_active)
        }
        onClick={() => void assign()}
      >
        Giao bài đã chọn
      </button>
      <p role="status">{message}</p>
    </section>
  );
}
type Rank = {
  rank: number;
  display_name: string;
  alias: string;
  score: number;
  completed: number;
  is_me: boolean;
};
export function RecognitionBoard({
  classroom,
  staff = false,
}: {
  classroom: Classroom;
  staff?: boolean;
}) {
  const [category, setCategory] = useState("MATH");
  const [period, setPeriod] = useState("month");
  const [resourceId, setResourceId] = useState("");
  const [message, setMessage] = useState("");
  const board = useResource<{
    enabled: boolean;
    rows: Rank[];
    top_three: Rank[];
    formula: string;
  }>(
    `/classroom/classes/${classroom.id}/leaderboard?category=${category}&period=${period}${resourceId ? "&resource_id=" + resourceId : ""}`,
  );
  const awards = useResource<
    {
      id: string;
      category: string;
      period_start: string;
      winners: {
        rank: number;
        alias: string;
        score: number;
        completed: number;
      }[];
    }[]
  >(`/classroom/classes/${classroom.id}/recognition`);
  async function publish() {
    try {
      await api(`/classroom/classes/${classroom.id}/recognition`, {
        method: "POST",
        body: JSON.stringify({
          category,
          period,
          resource_id: resourceId || null,
        }),
      });
      awards.retry();
      setMessage(
        "Đã ghi nhận top đầu của kỳ này; công bố lặp không tạo bản tuyên dương mới.",
      );
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel class-recognition">
      <h2>
        <Trophy size={25} /> Thành tích trong lớp · {classroom.name}
      </h2>
      <div className="two-columns">
        <label>
          Loại kết quả
          <select
            aria-label="Loại kết quả"
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setResourceId("");
            }}
          >
            {Object.entries(labels).map(([k, v]) => (
              <option key={k} value={k}>
                {v}
              </option>
            ))}
          </select>
        </label>
        <label>
          Kỳ thành tích
          <select value={period} onChange={(e) => setPeriod(e.target.value)}>
            <option value="month">Tháng này</option>
            <option value="week">Tuần này</option>
          </select>
        </label>
      </div>
      {staff && category !== "AI_PROJECT" && (
        <RankResourceFilter
          key={category}
          category={category}
          grade={classroom.grade}
          value={resourceId}
          onChange={setResourceId}
        />
      )}
      {board.loading ? (
        <Loading />
      ) : board.error ? (
        <ErrorState message={board.error} retry={board.retry} />
      ) : !board.data?.enabled ? (
        <Empty>Lớp đang tắt bảng thành tích.</Empty>
      ) : !board.data.rows.length ? (
        <Empty>Chưa có bài đã chấm trong kỳ; tiếp tục học để có kết quả.</Empty>
      ) : (
        <>
          <div className="three-columns class-top-three">
            {board.data.top_three.map((r) => (
              <article className="panel" key={r.rank}>
                <Medal size={32} />
                <h3>
                  Top {r.rank} · {r.is_me ? "Em" : r.display_name}
                </h3>
                <strong>{r.score.toLocaleString("vi-VN")} / 100</strong>
                <p>{r.completed} bài có kết quả</p>
              </article>
            ))}
          </div>
          <p>{board.data.formula}</p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Thứ tự</th>
                  <th>Học sinh</th>
                  <th>Điểm</th>
                  <th>Bài có kết quả</th>
                </tr>
              </thead>
              <tbody>
                {board.data.rows.map((r) => (
                  <tr key={r.rank}>
                    <td>{r.rank}</td>
                    <td>
                      {r.is_me ? "Em · " : ""}
                      {r.display_name}
                    </td>
                    <td>{r.score}</td>
                    <td>{r.completed}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {staff && (
            <button className="button secondary" onClick={() => void publish()}>
              Tuyên dương top 3 của kỳ
            </button>
          )}
        </>
      )}
      <p role="status">{message}</p>
      <h3>Tuyên dương đã ghi nhận</h3>
      {awards.loading ? (
        <Loading />
      ) : awards.error ? (
        <ErrorState message={awards.error} retry={awards.retry} />
      ) : awards.data?.length ? (
        awards.data.map((a) => (
          <article className="notice success" key={a.id}>
            <strong>
              {labels[a.category]} · từ{" "}
              {new Date(a.period_start).toLocaleDateString("vi-VN")}
            </strong>
            {a.winners.map((w) => (
              <p key={w.rank}>
                Top {w.rank} · {w.alias} · {w.score}/100
              </p>
            ))}
          </article>
        ))
      ) : (
        <p>Thầy cô sẽ ghi nhận sau khi xem kết quả.</p>
      )}
    </section>
  );
}
function RankResourceFilter({
  category,
  grade,
  value,
  onChange,
}: {
  category: string;
  grade: number;
  value: string;
  onChange: (v: string) => void;
}) {
  const resource = useResource<{ id: string; title: string }[]>(
    `/classroom/resources?kind=${category === "AI" ? "ai_lesson" : "assessment"}&grade=${grade}`,
  );
  return (
    <label>
      So sánh trên cùng bài (tùy chọn)
      <select
        aria-label="Bài để so sánh"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">Tổng hợp các bài của loại này</option>
        {resource.data?.map((r) => (
          <option key={r.id} value={r.id}>
            {r.title}
          </option>
        ))}
      </select>
    </label>
  );
}
export function StudentClassroom() {
  const classes = useResource<Classroom[]>("/classroom/classes");
  const achievements = useResource<{
    categories: { category: string; completed: number; score: number | null }[];
    reading_completed: number;
    note: string;
  }>("/classroom/my-achievements");
  const assignments = useResource<
    {
      id: string;
      kind: string;
      resource_id: string;
      assignment_id: string | null;
      title: string;
      class_name: string | null;
    }[]
  >("/classroom/my-assignments");
  const [chosen, setChosen] = useState("");
  const current =
    classes.data?.find((c) => c.id === chosen) || classes.data?.[0];
  return (
    <>
      <PageTitle
        title="Lớp và thành tích của em"
        description="Kết quả học của em luôn được giữ, dù học tự do hay trong lớp."
      />
      <section className="panel">
        <h2>Kết quả tháng này theo từng loại</h2>
        {achievements.loading ? (
          <Loading />
        ) : achievements.error ? (
          <ErrorState message={achievements.error} retry={achievements.retry} />
        ) : (
          <>
            <div className="three-columns">
              {achievements.data?.categories.map((c) => (
                <article className="panel" key={c.category}>
                  <h3>{labels[c.category]}</h3>
                  <p>
                    {c.completed} bài ·{" "}
                    {c.score === null ? "Chưa có điểm" : `${c.score}/100`}
                  </p>
                </article>
              ))}
            </div>
            <p>
              {achievements.data?.reading_completed} bài đã đọc.{" "}
              {achievements.data?.note}
            </p>
          </>
        )}
      </section>
      <section className="panel">
        <h2>Bài được giao cho em</h2>
        {assignments.loading ? (
          <Loading />
        ) : assignments.error ? (
          <ErrorState message={assignments.error} retry={assignments.retry} />
        ) : assignments.data?.length ? (
          assignments.data.map((a) => (
            <article className="list-row" key={a.id}>
              <span>
                {a.title} · {a.class_name || "Giao riêng"}
              </span>
              <Link
                className="button secondary small"
                href={
                  a.kind === "ai_lesson"
                    ? `/ai-academy/lessons/${a.resource_id}`
                    : a.kind === "lesson"
                      ? `/student/lessons/${a.resource_id}`
                      : `/student/assessments/${a.resource_id}`
                }
              >
                Mở bài được giao
              </Link>
            </article>
          ))
        ) : (
          <Empty>Em có thể chọn bài phù hợp trong thư viện để tự học.</Empty>
        )}
      </section>
      {classes.loading ? (
        <Loading />
      ) : classes.error ? (
        <ErrorState message={classes.error} retry={classes.retry} />
      ) : current ? (
        <>
          <label>
            Lớp của em
            <select
              value={current.id}
              onChange={(e) => setChosen(e.target.value)}
            >
              {classes.data?.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
          <RecognitionBoard key={current.id} classroom={current} />
        </>
      ) : (
        <Empty>
          Em đang học tự do. Khi nhà trường ghi danh, lớp của em sẽ xuất hiện ở
          đây.
        </Empty>
      )}
    </>
  );
}
