"use client";
import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty, PageTitle } from "@/components/ui";
import { AcademyImage } from "./shared";
import { PrivacyControls } from "./privacy";
import { useSession } from "@/lib/session";

type Project = {
  id: string;
  title: string;
  brief: string;
  rubric: Record<string, number>;
};
type Submission = {
  id: string;
  project_id: string;
  class_id: string | null;
  revision: number;
  artifact: Record<string, string>;
  status: string;
  feedback: string | null;
};
export function ProjectWorkspace({ studio = false }: { studio?: boolean }) {
  const projects = useResource<Project[]>("/ai-academy/projects");
  const portfolio = useResource<{ submissions: Submission[] }>(
    "/ai-academy/portfolio",
  );
  const classes = useResource<{ id: string; name: string }[]>(
    "/ai-academy/classes",
  );
  if (projects.loading || portfolio.loading) return <Loading />;
  if (projects.error || portfolio.error)
    return (
      <ErrorState
        message={projects.error || portfolio.error}
        retry={() => {
          projects.retry();
          portfolio.retry();
        }}
      />
    );
  return (
    <WorkspaceForm
      studio={studio}
      projects={projects}
      portfolio={portfolio}
      classes={classes}
    />
  );
}
function WorkspaceForm({
  studio,
  projects,
  portfolio,
  classes,
}: {
  studio: boolean;
  projects: ReturnType<typeof useResource<Project[]>>;
  portfolio: ReturnType<typeof useResource<{ submissions: Submission[] }>>;
  classes: ReturnType<typeof useResource<{ id: string; name: string }[]>>;
}) {
  const old = portfolio.data?.submissions.find(
    (s) => s.project_id === projects.data?.[0]?.id,
  );
  const [artifact, setArtifact] = useState<Record<string, string>>(
    old?.artifact || {
      title: "",
      character: "Robot Mầm",
      setting: "Khu vườn mẫu",
      problem: "Cây thiếu nước",
      solution: "Hỏi người lớn và tưới vừa đủ",
      reflection: "",
    },
  );
  const [classId, setClassId] = useState(old?.class_id || "");
  const [status, setStatus] = useState(old?.status || "");
  const [error, setError] = useState("");
  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);
  const revision = useRef<number | undefined>(old?.revision);
  const current = useRef(artifact);
  useEffect(() => {
    current.current = artifact;
  }, [artifact]);
  async function save(submit = false) {
    if (!projects.data?.[0] || saving) return;
    setSaving(true);
    setError("");
    const snapshot = JSON.stringify(artifact);
    try {
      const result = await api<
        Submission & { blocked?: boolean; message?: string }
      >("/ai-academy/projects/submissions", {
        method: "POST",
        body: JSON.stringify({
          project_id: projects.data[0].id,
          class_id: classId || null,
          revision: revision.current,
          artifact,
          submit,
        }),
      });
      if (result.blocked) {
        setError(result.message || "Nội dung cần chỉnh sửa");
        return;
      }
      revision.current = result.revision;
      setStatus(submit ? "Đã gửi riêng cho giáo viên" : "Đã lưu nháp riêng");
      if (JSON.stringify(current.current) === snapshot) setDirty(false);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSaving(false);
    }
  }
  useEffect(() => {
    if (!dirty || saving || error) return;
    const timer = setTimeout(() => void save(), 1500);
    return () => clearTimeout(timer);
  }, [artifact, classId, dirty, saving, error]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    function warn(e: BeforeUnloadEvent) {
      if (dirty) {
        e.preventDefault();
        e.returnValue = "";
      }
    }
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);
  function change(key: string, value: string) {
    setArtifact((a) => ({ ...a, [key]: value }));
    setDirty(true);
    setError("");
  }
  function comic() {
    const a = artifact;
    const variants: Record<string, string[]> = {
      comic: [
        `${a.character} đến ${a.setting}.`,
        `Nhân vật nhận ra: ${a.problem}.`,
        `Nhân vật thử cách giải quyết: ${a.solution}.`,
        "Nhân vật kiểm tra kết quả và ghi điều đã học.",
      ],
      poster: [
        "Cùng bảo vệ môi trường quanh em",
        "Quan sát nhu cầu trước khi hành động.",
        "Dùng nước vừa đủ, hỏi người lớn khi cần.",
        "Kiểm tra thông điệp bằng nguồn đã học; minh họa là mẫu.",
      ],
      quiz: [
        "Câu 1: AI có luôn đúng không? Gợi ý: hãy kiểm tra bằng chứng.",
        "Câu 2: Dữ liệu mẫu cần gì? Gợi ý: có nhiều nhóm và nhãn đúng.",
        "Câu 3: Có nên nhập mật khẩu vào công cụ? Gợi ý: giữ thông tin riêng.",
        "Đáp án dự kiến: không luôn đúng; đa dạng và nhãn đúng; không nhập mật khẩu. Hãy nhờ giáo viên kiểm tra quiz.",
      ],
      classifier: [
        "Mục tiêu: phân nhóm thẻ con vật, trái cây, đồ vật.",
        "Dữ liệu: chọn ví dụ có đủ ba nhóm trong Phòng thí nghiệm.",
        "Kiểm tra: dùng thẻ khác với thẻ đã học, đếm đúng và sai.",
        "Cải tiến: sửa nhãn, thêm nhóm còn thiếu, thử bỏ màu nền. Ghi kết quả thật từ lab vào đây.",
      ],
    };
    const frames = variants[a.kind || "comic"] || variants.comic;
    setArtifact({
      ...a,
      frame1: frames[0],
      frame2: frames[1],
      frame3: frames[2],
      frame4: frames[3],
    });
    setDirty(true);
    setError("");
  }
  if (projects.loading || portfolio.loading) return <Loading />;
  if (projects.error || portfolio.error)
    return (
      <ErrorState
        message={projects.error || portfolio.error}
        retry={() => {
          projects.retry();
          portfolio.retry();
        }}
      />
    );
  if (!projects.data?.length)
    return <Empty>Chưa có dự án phù hợp lớp của em.</Empty>;
  return (
    <>
      <PageTitle
        title={studio ? "Xưởng sáng tạo của em" : "Dự án AI an toàn"}
        description="Chọn mẫu rồi thêm ý tưởng của em. Bản nháp tự lưu; em có thể gửi riêng cho thầy cô hoặc in sản phẩm."
      />
      <section className="panel">
        <label>
          Loại sản phẩm
          <select
            aria-label="Loại sản phẩm"
            value={artifact.kind || "comic"}
            onChange={(e) => change("kind", e.target.value)}
          >
            <option value="comic">Truyện bốn khung</option>
            <option value="poster">Poster</option>
            <option value="quiz">Quiz do em biên soạn</option>
            <option value="classifier">Báo cáo bộ phân loại</option>
          </select>
        </label>
        <h2>{projects.data[0].title}</h2>
        <p>{projects.data[0].brief}</p>
        <p>
          Rubric: hiểu AI 20% · thực hành 30% · sáng tạo/hợp tác 30% · an toàn
          20%.
        </p>
        <label>
          Tên sản phẩm
          <input
            maxLength={120}
            value={artifact.title || ""}
            onChange={(e) => change("title", e.target.value)}
          />
        </label>
        {[
          [
            "character",
            "Nhân vật mẫu",
            ["Robot Mầm", "Bạn nhỏ hư cấu", "Chú mèo trong tranh"],
          ],
          [
            "setting",
            "Bối cảnh mẫu",
            ["Khu vườn mẫu", "Thư viện trong truyện", "Lớp học tưởng tượng"],
          ],
          [
            "problem",
            "Vấn đề",
            ["Cây thiếu nước", "Các thẻ chưa xếp nhóm", "Sách cần sắp xếp"],
          ],
          [
            "solution",
            "Cách giải quyết",
            [
              "Hỏi người lớn và tưới vừa đủ",
              "Phân loại và kiểm tra nhãn",
              "Sắp xếp theo quy tắc rồi thử lại",
            ],
          ],
        ].map(([key, title, options]) => (
          <label key={key as string}>
            {title}
            <select
              value={artifact[key as string] || ""}
              onChange={(e) => change(key as string, e.target.value)}
            >
              {(options as string[]).map((x) => (
                <option key={x}>{x}</option>
              ))}
            </select>
          </label>
        ))}
        <button className="button secondary" onClick={comic}>
          {(artifact.kind || "comic") === "comic"
            ? "Ghép truyện 4 khung từ mẫu"
            : "Tạo bản khởi đầu từ mẫu"}
        </button>
        <div className="academy-comic">
          {[1, 2, 3, 4].map((n) => (
            <label key={n}>
              <AcademyImage
                code={`AI4-24-support-${n === 4 ? 3 : n}`}
                alt={`Khung truyện mẫu ${n}`}
              />
              <strong>Khung {n}</strong>
              <textarea
                maxLength={1500}
                value={artifact[`frame${n}`] || ""}
                onChange={(e) => change(`frame${n}`, e.target.value)}
              />
            </label>
          ))}
        </div>
        <label>
          Em tự đánh giá: đã kiểm tra gì, cần cải thiện gì?
          <textarea
            value={artifact.reflection || ""}
            maxLength={1500}
            onChange={(e) => change("reflection", e.target.value)}
          />
        </label>
        <label>
          Gửi tới lớp
          <select
            aria-label="Gửi tới lớp"
            value={classId}
            onChange={(e) => {
              setClassId(e.target.value);
              setDirty(true);
            }}
          >
            <option value="">Chưa chọn lớp · chỉ lưu riêng</option>
            {classes.data?.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
        <div className="academy-actions">
          <button
            disabled={saving}
            className="button secondary"
            onClick={() => void save()}
          >
            Lưu bản nháp
          </button>
          <button
            disabled={saving || !classId}
            className="button"
            onClick={() => void save(true)}
          >
            Nộp cho giáo viên
          </button>
          <button className="button secondary" onClick={() => window.print()}>
            In / lưu PDF
          </button>
        </div>
        <p role="status">
          {saving ? "Đang lưu…" : status}
          {dirty ? " · Có thay đổi chưa lưu" : ""}
        </p>
        {error && (
          <p role="alert" className="notice error">
            {error}
          </p>
        )}
        <p className="muted">
          Không nhập tên thật, địa chỉ hay mật khẩu. Bản nộp không tự được trưng
          bày công khai.
        </p>
      </section>
    </>
  );
}

export function Portfolio() {
  const { user } = useSession();
  const { data, loading, error, retry } = useResource<{
    badges: { badge_code: string; title: string }[];
    submissions: Submission[];
    competencies: {
      competency: string;
      evidence_count: number;
      successful_count: number;
    }[];
  }>("/ai-academy/portfolio");
  return (
    <>
      <PageTitle
        title="Sản phẩm và tiến bộ của em"
        description="Ghi nhận quá trình học; không so sánh hoặc xếp hạng với bạn khác."
      />
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorState message={error} retry={retry} />
      ) : (
        <>
          <section className="panel">
            <h2>Huy hiệu khám phá</h2>
            <div className="academy-cards">
              {data?.badges.map((b) => (
                <div className="academy-card" key={b.badge_code}>
                  <AcademyImage
                    code={`badge-${Number(b.badge_code.split("-").at(-1)) - 1}`}
                    alt={b.title}
                    small
                  />
                  <strong>{b.title}</strong>
                </div>
              ))}
            </div>
            {!data?.badges.length && (
              <Empty>Hoàn thành bài đầu tiên để ghi nhận bước khám phá.</Empty>
            )}
          </section>
          <section className="panel">
            <h2>Sản phẩm riêng tư</h2>
            {data?.submissions.map((s) => (
              <article key={s.id} className="academy-artifact">
                <h3>{s.artifact.title || "Bản nháp của em"}</h3>
                <p>
                  {s.status === "reviewed"
                    ? "Giáo viên đã phản hồi"
                    : s.status === "submitted"
                      ? "Đã gửi giáo viên"
                      : "Bản nháp riêng"}
                </p>
                {[1, 2, 3, 4].map((n) => (
                  <p key={n}>{s.artifact[`frame${n}`]}</p>
                ))}
                {s.feedback && (
                  <p className="notice">Góp ý giáo viên: {s.feedback}</p>
                )}
              </article>
            ))}
          </section>
          <section className="panel">
            <h2>Bằng chứng thực hành</h2>
            <p>
              Số lần thử và đạt phản ánh bài đã làm, không phải chẩn đoán năng
              lực.
            </p>
            {data?.competencies.map((c) => (
              <p key={c.competency}>
                {(
                  {
                    around: "Nhận biết AI",
                    data: "Dữ liệu",
                    prompt: "Viết yêu cầu",
                    math: "Toán",
                    vietnamese: "Tiếng Việt",
                    english: "Tiếng Anh",
                    creative: "Sáng tạo",
                    safety: "An toàn",
                    project: "Dự án",
                  } as Record<string, string>
                )[c.competency] || c.competency}
                : {c.successful_count}/{c.evidence_count} lượt đạt.
              </p>
            ))}
          </section>
          {user && (
            <section className="panel">
              <h2>Dữ liệu của em</h2>
              <PrivacyControls studentId={user.id} />
            </section>
          )}
        </>
      )}
    </>
  );
}
