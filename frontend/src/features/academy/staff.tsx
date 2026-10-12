"use client";
import Link from "next/link";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { CatalogLesson } from "./types";
import { PrivacyControls } from "./privacy";

type Submission = {
  id: string;
  revision: number;
  artifact: Record<string, string>;
  student_id: string;
  feedback: string | null;
  status: string;
};
export function TeacherAcademy() {
  const classes = useResource<{ id: string; name: string; grade: number }[]>(
    "/ai-academy/classes",
  );
  const [chosen, setChosen] = useState("");
  const current = chosen || classes.data?.[0]?.id || "";
  const grade = classes.data?.find((c) => c.id === current)?.grade || 4;
  const lessons = useResource<CatalogLesson[]>(
    `/ai-academy/catalog?grade=${grade}`,
  );
  const [lesson, setLesson] = useState("");
  const [message, setMessage] = useState("");
  async function assign() {
    try {
      const r = await api<{ targets: number }>(
        "/ai-academy/teacher/assignments",
        {
          method: "POST",
          body: JSON.stringify({
            class_id: current,
            lesson_id: lesson || lessons.data?.[0]?.id,
          }),
        },
      );
      setMessage(`Đã giao tới ${r.targets} học sinh đang ghi danh.`);
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <div className="academy-page">
      <Link className="button secondary" href="/teacher/ai-academy/content">
        Biên soạn / kiểm duyệt theo quyền được cấp
      </Link>
      <PageTitle
        title="AI Academy · Giáo viên"
        description="Quản lý đúng các lớp được phân công; nhận xét dựa trên bằng chứng, không xếp hạng học sinh."
      />
      {classes.loading ? (
        <Loading />
      ) : classes.error ? (
        <ErrorState message={classes.error} retry={classes.retry} />
      ) : !classes.data?.length ? (
        <Empty>Admin cần phân công lớp và ghi danh học sinh trước.</Empty>
      ) : (
        <>
          <section className="panel">
            <label>
              Lớp được phân công
              <select
                aria-label="Lớp được phân công"
                value={current}
                onChange={(e) => {
                  setChosen(e.target.value);
                  setLesson("");
                }}
              >
                {classes.data.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Giao bài đã xuất bản
              <select
                value={lesson || lessons.data?.[0]?.id || ""}
                onChange={(e) => setLesson(e.target.value)}
              >
                {lessons.data?.map((l) => (
                  <option key={l.id} value={l.id}>
                    {l.title}
                  </option>
                ))}
              </select>
            </label>
            <button className="button" onClick={() => void assign()}>
              Giao bài cho lớp
            </button>
            <p role="status">{message}</p>
          </section>
          <ClassReport key={current} classId={current} />
        </>
      )}
    </div>
  );
}
export function ClassReport({ classId }: { classId: string }) {
  const { data, loading, error, retry } = useResource<{
    students: { id: string; display_name: string; completed: number }[];
    submissions: Submission[];
  }>(`/ai-academy/teacher/reports?class_id=${classId}`);
  if (loading) return <Loading />;
  if (error) return <ErrorState message={error} retry={retry} />;
  return (
    <>
      <section className="panel">
        <h2>Tiến độ lớp</h2>
        <a
          className="button secondary"
          href={`/api/v1/ai-academy/teacher/reports/export?class_id=${classId}`}
        >
          Xuất CSV của lớp được phân công
        </a>
        {data?.students.map((s) => (
          <div className="list-row" key={s.id}>
            <strong>{s.display_name}</strong>
            <span>{s.completed} bài hoàn thành</span>
          </div>
        ))}
        <button className="button secondary" onClick={retry}>
          Cập nhật báo cáo
        </button>
      </section>
      <section className="panel">
        <h2>Bài nộp và rubric</h2>
        {data?.submissions.length ? (
          data.submissions.map((s) => (
            <SubmissionReview
              key={s.id + ":" + s.revision}
              submission={s}
              onSaved={retry}
            />
          ))
        ) : (
          <Empty>Chưa có bài nộp của lớp.</Empty>
        )}
      </section>
    </>
  );
}
function SubmissionReview({
  submission: s,
  onSaved,
}: {
  submission: Submission;
  onSaved: () => void;
}) {
  const [feedback, setFeedback] = useState(s.feedback || "");
  const [scores, setScores] = useState<Record<string, number>>({
    understanding: 2,
    practice: 2,
    creativity: 2,
    safety: 2,
  });
  const [message, setMessage] = useState("");
  async function save() {
    try {
      await api(`/ai-academy/teacher/submissions/${s.id}/review`, {
        method: "POST",
        body: JSON.stringify({ revision: s.revision, feedback, scores }),
      });
      onSaved();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <article className="academy-artifact">
      <h3>{s.artifact.title}</h3>
      {Object.entries(s.artifact)
        .filter(([k]) => k !== "title")
        .map(([k, v]) => (
          <p key={k}>{v}</p>
        ))}
      <div className="filters">
        {[
          ["understanding", "Hiểu AI · 20%"],
          ["practice", "Thực hành · 30%"],
          ["creativity", "Sáng tạo/hợp tác · 30%"],
          ["safety", "An toàn · 20%"],
        ].map(([key, title]) => (
          <label key={key}>
            {title}
            <select
              value={scores[key]}
              onChange={(e) =>
                setScores({ ...scores, [key]: Number(e.target.value) })
              }
            >
              {[0, 1, 2, 3, 4].map((n) => (
                <option key={n}>{n}</option>
              ))}
            </select>
          </label>
        ))}
      </div>
      <label>
        Góp ý cụ thể
        <textarea
          minLength={10}
          maxLength={2000}
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
        />
      </label>
      <button className="button" onClick={() => void save()}>
        Lưu đánh giá riêng
      </button>
      <p role="alert">{message}</p>
    </article>
  );
}
export function GuardianAcademy() {
  const { data, loading, error, retry } = useResource<
    {
      id: string;
      display_name: string;
      current_grade: number;
      consent: boolean;
      lessons: CatalogLesson[];
    }[]
  >("/ai-academy/guardian");
  const [message, setMessage] = useState("");
  async function consent(id: string, given: boolean) {
    try {
      await api("/ai-academy/guardian/consent", {
        method: "POST",
        body: JSON.stringify({ student_id: id, given }),
      });
      retry();
      setMessage("Đã cập nhật lựa chọn theo chính sách ai-academy-v1.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <div className="academy-page">
      <PageTitle
        title="AI Academy · Phụ huynh"
        description="Chỉ hiện trẻ có liên kết được xác minh. Học liệu và mô phỏng luôn dùng được mà không bật mô hình."
      />
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorState message={error} retry={retry} />
      ) : data?.length ? (
        data.map((child) => (
          <section className="panel" key={child.id}>
            <h2>
              {child.display_name} · Lớp {child.current_grade}
            </h2>
            <p>
              {child.lessons.filter((l) => l.progress?.completed_at).length}/
              {child.lessons.length} bài hoàn thành
            </p>
            <p>
              Trợ giảng dùng mô hình chỉ khi người vận hành đã duyệt và cho
              phép. Backend gửi chế độ và ngữ liệu bài đã duyệt, không gửi
              tên/hồ sơ hay nguyên văn bài làm của trẻ. Kết quả mô hình có thể
              sai; hướng dẫn nội bộ thay thế khi chưa bật hoặc chưa chấp thuận.
            </p>
            <p>
              Chấp thuận hiện tại: {child.consent ? "Có" : "Không"} ·
              ai-academy-v1.
            </p>
            <button
              className="button secondary"
              onClick={() => void consent(child.id, !child.consent)}
            >
              {child.consent
                ? "Thu hồi chấp thuận"
                : "Cho phép trợ giảng theo chính sách trên"}
            </button>
            <PrivacyControls studentId={child.id} />
          </section>
        ))
      ) : (
        <Empty>Chưa có liên kết trẻ được xác minh.</Empty>
      )}
      <p role="status">{message}</p>
    </div>
  );
}
