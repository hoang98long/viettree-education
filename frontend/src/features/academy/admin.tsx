"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, PageTitle, Empty } from "@/components/ui";
import { ContentEditor } from "./editor";
import { AcademyImage } from "./shared";
import { TeacherAcademy } from "./staff";
import { AccountPicker } from "./account-picker";
import { ModerationInbox, PromptLibrary, UnitCreator } from "./management";
import "./academy.css";

export function AcademyAdmin({
  contentOnly = false,
}: {
  contentOnly?: boolean;
}) {
  const [tab, setTab] = useState("content");
  const overview = useResource<{
    counts: Record<string, number>;
    flags: Record<string, boolean>;
    providers: { code: string; enabled: boolean; policy_approved: boolean }[];
    training_only: boolean;
    quality: {
      baseline_published: number;
      baseline_required: number;
      issues: { code: string; reason: string }[];
    };
  }>("/ai-academy/admin/overview");
  return (
    <div className="academy-page">
      <PageTitle
        title="Quản trị AI Academy"
        description="Nội dung có phiên bản, media cần kiểm duyệt, dịch vụ ngoài mặc định tắt."
      />
      <nav aria-label="Mục quản trị Academy" className="academy-admin-tabs">
        {[
          ["content", "Bài học"],
          ["media", "Thư viện hình"],
          ["policy", "Chính sách AI"],
          ["classes", "Lớp và quyền"],
          ["teacher", "Bài nộp / báo cáo"],
          ["jobs", "Tạo SVG"],
          ["moderation", "An toàn / dữ liệu"],
          ["prompts", "Mẫu hướng dẫn"],
          ["overview", "Tổng quan"],
        ]
          .filter(
            ([v]) =>
              !contentOnly ||
              ["content", "media", "jobs", "overview"].includes(v),
          )
          .map(([v, t]) => (
            <button
              className="button secondary"
              key={v}
              onClick={() => setTab(v)}
            >
              {t}
            </button>
          ))}
      </nav>
      {tab === "content" && <ContentLibrary />}
      {tab === "media" && <MediaLibrary />}
      {tab === "policy" && (
        <AISettings
          flags={overview.data?.flags || {}}
          trainingOnly={overview.data?.training_only ?? true}
          onSaved={overview.retry}
        />
      )}{" "}
      {tab === "classes" && <ClassSetup />}
      {tab === "teacher" && <TeacherAcademy />}
      {tab === "jobs" && <GenerationQueue />}
      {tab === "moderation" && <ModerationInbox />}
      {tab === "prompts" && <PromptLibrary />}
      {tab === "overview" &&
        (overview.loading ? (
          <Loading />
        ) : overview.error ? (
          <ErrorState message={overview.error} retry={overview.retry} />
        ) : (
          <section className="panel">
            <h2>Số liệu thật</h2>
            <p>
              Độ phủ bài gốc đã xuất bản:{" "}
              {overview.data?.quality.baseline_published}/
              {overview.data?.quality.baseline_required}
            </p>
            {overview.data?.quality.issues.map((issue, i) => (
              <p className="notice error" key={issue.code + ":" + i}>
                {issue.code}:{" "}
                {(
                  {
                    baseline_not_published:
                      "Bài gốc chưa được xuất bản hoặc đang ẩn",
                    invalid_lesson_structure:
                      "Thiếu cấu trúc bước/hoạt động/câu hỏi hợp lệ",
                    missing_approved_media:
                      "Có hình thiếu hoặc chưa được duyệt",
                    invalid_rubric:
                      "Rubric thiếu tiêu chí hoặc tổng trọng số không đúng",
                  } as Record<string, string>
                )[issue.reason] || "Cần kiểm tra nội dung"}
              </p>
            ))}
            {Object.entries(overview.data?.counts || {}).map(([k, v]) => (
              <p key={k}>
                {(
                  {
                    ai_lessons: "Bài học",
                    ai_media_assets: "Hình minh họa",
                    ai_attempts: "Lượt thực hành",
                    ai_progress: "Tiến độ học",
                    ai_project_submissions: "Sản phẩm",
                    ai_moderation_reviews: "Cảnh báo an toàn",
                  } as Record<string, string>
                )[k] || k}
                : {v}
              </p>
            ))}
            <p>
              Đối chiếu bài published của các khối với danh mục học liệu hiện
              tại; bài mới/draft không thay bài đang học.
            </p>
            <p>
              Không coi số lượt làm là chẩn đoán năng lực. Provider cần flag,
              chính sách, quota và chấp thuận còn hiệu lực.
            </p>
          </section>
        ))}
    </div>
  );
}
function ContentLibrary() {
  const [grade, setGrade] = useState(4);
  const [unitRefresh, setUnitRefresh] = useState(0);
  const [id, setId] = useState("");
  const { data, loading, error, retry } = useResource<
    { id: string; title: string; code: string }[]
  >(`/ai-academy/admin/lessons?grade=${grade}`);
  return (
    <>
      <UnitCreator
        grade={grade}
        onCreated={() => setUnitRefresh((v) => v + 1)}
      />
      <label>
        Khối lớp
        <select
          value={grade}
          onChange={(e) => {
            setGrade(Number(e.target.value));
            setId("");
          }}
        >
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n} value={n}>
              Lớp {n}
            </option>
          ))}
        </select>
      </label>
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorState message={error} retry={retry} />
      ) : (
        <label>
          Chọn bài để biên soạn hoặc nhân bản
          <select
            value={id || data?.[0]?.id || ""}
            onChange={(e) => setId(e.target.value)}
          >
            {data?.map((l) => (
              <option key={l.id} value={l.id}>
                {l.code} · {l.title}
              </option>
            ))}
          </select>
        </label>
      )}
      {(id || data?.[0]?.id) && (
        <ContentEditor
          key={(id || data![0].id) + unitRefresh}
          id={id || data![0].id}
          grade={grade}
          onSaved={retry}
        />
      )}
    </>
  );
}
function MediaLibrary() {
  const [page, setPage] = useState(1);
  const list = useResource<
    { id: string; code: string; alt: string; status: string; license: string }[]
  >(`/ai-academy/admin/media?page=${page}`);
  const [alt, setAlt] = useState("");
  const [license, setLicense] = useState("");
  const [source, setSource] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  async function upload() {
    try {
      if (!file || file.size > 512000)
        throw new Error("Chọn PNG/JPEG/WebP/AVIF tối đa 512 KB.");
      const data = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result).split(",")[1]);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
      await api("/ai-academy/admin/media", {
        method: "POST",
        body: JSON.stringify({ data, alt, license, source }),
      });
      setMessage(
        "Ảnh được chuẩn hóa, bỏ metadata, tạo 3 biến thể và đang chờ duyệt.",
      );
      list.retry();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  async function review(id: string, approved: boolean) {
    try {
      await api(`/ai-academy/admin/media/${id}/review`, {
        method: "POST",
        body: JSON.stringify({ approved }),
      });
      list.retry();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <>
      <section className="panel">
        <h2>Tải ảnh học thuật</h2>
        <p>
          Không dùng ảnh nhận dạng trẻ. SVG tùy ý không được tải lên; bộ SVG nội
          bộ được tạo bằng code.
        </p>
        <label>
          File ảnh
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp,image/avif"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </label>
        <label>
          Mô tả thay thế tiếng Việt
          <input value={alt} onChange={(e) => setAlt(e.target.value)} />
        </label>
        <label>
          Nguồn / người tạo
          <input value={source} onChange={(e) => setSource(e.target.value)} />
        </label>
        <label>
          Giấy phép / quyền sử dụng
          <input value={license} onChange={(e) => setLicense(e.target.value)} />
        </label>
        <button className="button" onClick={() => void upload()}>
          Tải lên để kiểm duyệt
        </button>
        <p role="status">{message}</p>
      </section>
      {list.loading ? (
        <Loading />
      ) : list.error ? (
        <ErrorState message={list.error} retry={list.retry} />
      ) : (
        <div className="academy-cards">
          {list.data?.map((m) => (
            <article className="academy-card" key={m.id}>
              <AcademyImage code={m.code} alt={m.alt} />
              <strong>{m.alt}</strong>
              <small>{m.code}</small>
              <p>
                {m.status} · {m.license}
              </p>
              <div className="academy-actions">
                <button
                  className="button secondary small"
                  onClick={() => void review(m.id, true)}
                >
                  Duyệt hình
                </button>
                <button
                  className="button secondary small"
                  onClick={() => void review(m.id, false)}
                >
                  Thu hồi
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
      <div className="academy-actions">
        <button
          className="button secondary"
          disabled={page === 1}
          onClick={() => setPage((p) => p - 1)}
        >
          Trang trước
        </button>
        <span>Trang {page}</span>
        <button
          className="button secondary"
          disabled={(list.data?.length || 0) < 60}
          onClick={() => setPage((p) => p + 1)}
        >
          Trang sau
        </button>
      </div>
    </>
  );
}
function AISettings({
  flags,
  trainingOnly,
  onSaved,
}: {
  flags: Record<string, boolean>;
  trainingOnly: boolean;
  onSaved: () => void;
}) {
  const [password, setPassword] = useState("");
  const [approved, setApproved] = useState(false);
  const [message, setMessage] = useState("");
  async function set(code: string, enabled: boolean) {
    try {
      await api("/ai-academy/admin/policy", {
        method: "POST",
        body: JSON.stringify({
          code,
          enabled,
          approve_local_model: approved,
          actor_password: password,
          reason: "Cập nhật chính sách vận hành Academy",
        }),
      });
      setPassword("");
      onSaved();
      setMessage("Đã cập nhật có audit.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>AI và quyền sử dụng</h2>
      <p>
        Hiện ưu tiên đào tạo lý thuyết và bài thực hành từ mẫu. Gọi mô hình được
        tắt trong chế độ đào tạo; học sinh không cần khóa AI.
      </p>
      <label>
        Mật khẩu quản trị để xác nhận
        <input
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      {!trainingOnly && (
        <label>
          <input
            type="checkbox"
            checked={approved}
            onChange={(e) => setApproved(e.target.checked)}
          />{" "}
          Đã kiểm thử mô hình local và duyệt chính sách trước khi bật trợ giảng
        </label>
      )}
      {Object.entries(flags)
        .filter(
          ([code]) =>
            !trainingOnly ||
            !["tutor_enabled", "image_generation_enabled"].includes(code),
        )
        .map(([code, enabled]) => (
          <div className="list-row" key={code}>
            <span>
              {{
                tutor_enabled: "Trợ giảng bằng mô hình local",
                voice_enabled: "Đọc nội dung bằng giọng local có sẵn",
                student_creative_enabled: "Xưởng sáng tạo từ mẫu",
                image_generation_enabled:
                  "Tạo ảnh bằng mô hình (chưa có adapter được duyệt)",
              }[code] || code}{" "}
              · {enabled ? "Bật" : "Tắt"}
            </span>
            <button
              className="button secondary small"
              onClick={() => void set(code, !enabled)}
            >
              {enabled ? "Tắt" : "Bật"}
            </button>
          </div>
        ))}
      <p role="status">{message}</p>
    </section>
  );
}
function ClassSetup() {
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [grade, setGrade] = useState(4);
  const [teacher, setTeacher] = useState("");
  const [classId, setClassId] = useState("");
  const [student, setStudent] = useState("");
  const [staffId, setStaffId] = useState("");
  const [guardianId, setGuardianId] = useState("");
  const [childId, setChildId] = useState("");
  const [verified, setVerified] = useState(false);
  const [role, setRole] = useState("editor");
  const [message, setMessage] = useState("");
  const classes = useResource<{ id: string; name: string }[]>(
    "/ai-academy/classes",
  );
  async function act(path: string, data: object) {
    try {
      await api("/ai-academy/admin/" + path, {
        method: "POST",
        body: JSON.stringify({
          ...data,
          actor_password: password,
          reason: "Phân công và xác minh bởi quản trị",
        }),
      });
      setPassword("");
      classes.retry();
      setMessage("Đã cập nhật có audit.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>Phân công bằng tài khoản hiện có</h2>
      <p>
        Tạo tài khoản giáo viên/phụ huynh trong Quản trị tài khoản trước, rồi
        chọn người phụ trách và học sinh đang hoạt động để phân công.
      </p>
      <label>
        Mật khẩu xác nhận
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <label>
        Tên lớp
        <input value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <label>
        Khối
        <select
          value={grade}
          onChange={(e) => setGrade(Number(e.target.value))}
        >
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n}>{n}</option>
          ))}
        </select>
      </label>
      <label>
        Giáo viên phụ trách
        <AccountPicker
          label="Giáo viên phụ trách"
          role="teacher"
          value={teacher}
          onChange={setTeacher}
        />
      </label>
      <button
        className="button secondary"
        onClick={() =>
          void act("classes", { name, grade, teacher_id: teacher })
        }
      >
        Tạo lớp được phân công
      </button>
      <label>
        Lớp ghi danh
        <select
          value={classId || classes.data?.[0]?.id || ""}
          onChange={(e) => setClassId(e.target.value)}
        >
          {classes.data?.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </label>
      <label>
        Học sinh ghi danh
        <AccountPicker
          label="Học sinh ghi danh"
          role="student"
          grade={grade}
          value={student}
          onChange={setStudent}
        />
      </label>
      <button
        className="button secondary"
        onClick={() =>
          void act(`classes/${classId || classes.data?.[0]?.id}/enroll`, {
            student_id: student,
          })
        }
      >
        Ghi danh học sinh cùng khối
      </button>
      <label>
        Giáo viên được cấp quyền
        <AccountPicker
          label="Giáo viên được cấp quyền"
          role="teacher"
          value={staffId}
          onChange={setStaffId}
        />
      </label>
      <label>
        Quyền Academy
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="editor">Biên soạn</option>
          <option value="reviewer">Kiểm duyệt</option>
        </select>
      </label>
      <button
        className="button secondary"
        onClick={() =>
          void act("staff", { user_id: staffId, role, grant: true })
        }
      >
        Cấp quyền
      </button>
      <button
        className="button secondary"
        onClick={() =>
          void act("staff", { user_id: staffId, role, grant: false })
        }
      >
        Thu hồi quyền
      </button>
      <p role="status">{message}</p>
      <h3>Liên kết phụ huynh với học sinh</h3>
      <p>
        Chỉ đánh dấu đã xác minh sau khi nhà trường kiểm tra người giám hộ. Thu
        hồi xác minh sẽ chặn quyền xem dữ liệu và chấp thuận mô hình.
      </p>
      <AccountPicker
        label="Phụ huynh liên kết"
        role="guardian"
        value={guardianId}
        onChange={setGuardianId}
      />
      <AccountPicker
        label="Học sinh liên kết"
        role="student"
        value={childId}
        onChange={setChildId}
      />
      <label>
        <input
          type="checkbox"
          checked={verified}
          onChange={(e) => setVerified(e.target.checked)}
        />{" "}
        Đã xác minh người giám hộ
      </label>
      <button
        className="button secondary"
        onClick={() =>
          void act("guardian-links", {
            guardian_id: guardianId,
            student_id: childId,
            verified,
          })
        }
      >
        Lưu liên kết phụ huynh
      </button>
    </section>
  );
}
function GenerationQueue() {
  const jobs = useResource<{ id: string; template: string; status: string }[]>(
    "/ai-academy/admin/jobs",
  );
  const [template, setTemplate] = useState("robot");
  const [message, setMessage] = useState("");
  async function create() {
    try {
      await api("/ai-academy/admin/jobs", {
        method: "POST",
        body: JSON.stringify({ template, palette: 0 }),
      });
      jobs.retry();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  async function run(id: string) {
    try {
      await api(`/ai-academy/admin/jobs/${id}/run`, { method: "POST" });
      jobs.retry();
      setMessage("Đã tạo SVG từ mẫu, chờ duyệt trong Thư viện hình.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>Hàng đợi minh họa SVG</h2>
      <p>
        Thực sự tạo file vector bằng template. Không phải dịch vụ sinh ảnh bằng
        mô hình; không gọi API trả phí.
      </p>
      <label>
        Mẫu
        <select value={template} onChange={(e) => setTemplate(e.target.value)}>
          <option value="robot">Robot</option>
          <option value="poster">Poster môi trường</option>
          <option value="comic">Truyện 4 khung</option>
        </select>
      </label>
      <button className="button" onClick={() => void create()}>
        Thêm job vào hàng đợi
      </button>
      {jobs.data?.length ? (
        jobs.data.map((j) => (
          <div className="list-row" key={j.id}>
            <span>
              {j.template} · {j.status}
            </span>
            <button
              className="button secondary"
              disabled={j.status !== "queued"}
              onClick={() => void run(j.id)}
            >
              Tạo bản xem trước
            </button>
          </div>
        ))
      ) : (
        <Empty>Chưa có job.</Empty>
      )}
      <p role="status">{message}</p>
    </section>
  );
}
