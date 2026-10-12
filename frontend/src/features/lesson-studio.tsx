"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, dateLabel } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { LessonBody } from "@/components/lesson-body";
import type { LessonContent, LessonIllustration, Page } from "@/lib/types";

type Options = {
  subjects: { id: string; code: string; name_vi: string }[];
  topics: { id: string; subject_id: string; title: string }[];
  skills: { id: string; subject_id: string; topic_id: string; name: string }[];
};
type Payload = {
  code: string;
  grade: number;
  subject_id: string;
  topic_id: string;
  skill_ids: string[];
  title: string;
  description: string;
  estimated_minutes: number;
  sort_order: number;
  minimum_plan_code: "free" | "vip";
  learning_level: "basic" | "reinforcement" | "advanced";
  preview: { summary?: string; goals?: string[] };
  content: LessonContent;
};
type Draft = {
  id: string;
  lesson_status: string;
  draft_status: string;
  edit_revision: number;
  source_fingerprint: string;
  source_changed: boolean;
  payload: Payload;
  history: {
    action: string;
    created_at: string;
    actor_name: string | null;
    reason: string;
  }[];
};
type Summary = {
  id: string;
  title: string;
  code: string;
  status: string;
  draft_status: string | null;
  subject_name: string;
  topic_title: string;
  minimum_plan_code: string | null;
};
const statusLabels: Record<string, string> = {
  published: "Đã xuất bản",
  draft: "Nháp",
  reviewed: "Đã duyệt",
  archived: "Đã lưu trữ",
  none: "Chưa có nháp",
};

export function LessonsAdminPage() {
  const [grade, setGrade] = useState(4),
    [subject, setSubject] = useState(""),
    [status, setStatus] = useState(""),
    [search, setSearch] = useState(""),
    [page, setPage] = useState(1);
  const query = new URLSearchParams({
    grade: String(grade),
    page: String(page),
    search,
    ...(subject ? { subject_code: subject } : {}),
    ...(status ? { status } : {}),
  });
  const resource = useResource<Page<Summary>>(`/admin/lessons?${query}`);
  return (
    <>
      <PageTitle
        title="Quản lý bài học"
        description="Biên soạn, xem trước, duyệt và xuất bản. Bản nháp tách khỏi nội dung học sinh đang đọc."
      />
      <Link className="button" href="/admin/lessons/new">
        Tạo bài học
      </Link>
      <div className="filters section-title">
        <label htmlFor="studio-grade">
          Lớp
          <select
            id="studio-grade"
            value={grade}
            onChange={(e) => {
              setGrade(Number(e.target.value));
              setPage(1);
            }}
          >
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                Lớp {n}
              </option>
            ))}
          </select>
        </label>
        <label htmlFor="studio-subject">
          Lọc môn
          <select
            id="studio-subject"
            value={subject}
            onChange={(e) => {
              setSubject(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả môn</option>
            <option value="MATH">Toán</option>
            <option value="VIETNAMESE">Tiếng Việt</option>
            <option value="ENGLISH">Tiếng Anh</option>
          </select>
        </label>
        <label htmlFor="studio-status">
          Trạng thái bài học
          <select
            id="studio-status"
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            <option value="pending">Có nháp cần xử lý</option>
            <option value="published">Đã xuất bản</option>
            <option value="draft">Chưa xuất bản</option>
          </select>
        </label>
        <label htmlFor="studio-search">
          Tìm bài học
          <input
            id="studio-search"
            value={search}
            maxLength={120}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Tên hoặc mã bài"
          />
        </label>
      </div>
      {resource.loading ? (
        <Loading />
      ) : resource.error || !resource.data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <p>
            {resource.data.total} bài · Trang {page}
          </p>
          {resource.data.items.length ? (
            <div className="two-columns">
              {resource.data.items.map((item) => (
                <article className="panel studio-card" key={item.id}>
                  <span className="eyebrow">
                    {item.subject_name} ·{" "}
                    {item.minimum_plan_code?.toUpperCase() || "Chưa xuất bản"}
                  </span>
                  <h2>{item.title}</h2>
                  <p>{item.topic_title}</p>
                  <p>
                    {statusLabels[item.status]} · Bản soạn:{" "}
                    {statusLabels[item.draft_status || "none"]}
                  </p>
                  <Link
                    className="button secondary"
                    href={`/admin/lessons/${item.id}/edit`}
                  >
                    Biên soạn bài học
                  </Link>
                </article>
              ))}
            </div>
          ) : (
            <Empty>
              Chưa có bài phù hợp. Thử đổi bộ lọc hoặc tạo bài trong chủ đề đã
              có.
            </Empty>
          )}
          <div className="pagination">
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Trang trước
            </button>
            <button
              className="button secondary"
              disabled={page * 20 >= resource.data.total}
              onClick={() => setPage((p) => p + 1)}
            >
              Trang sau
            </button>
          </div>
        </>
      )}
    </>
  );
}

function initial(options: Options, grade: number): Payload {
  const topic = options.topics[0];
  return {
    code: "",
    grade,
    subject_id: topic?.subject_id || options.subjects[0]?.id || "",
    topic_id: topic?.id || "",
    skill_ids: options.skills
      .filter((s) => s.topic_id === topic?.id)
      .map((s) => s.id),
    title: "",
    description: "",
    estimated_minutes: 15,
    sort_order: 100,
    minimum_plan_code: "free",
    learning_level: "basic",
    preview: { summary: "", goals: [] },
    content: {
      blocks: [
        { type: "text", title: "Cùng khám phá", text: "" },
        { type: "example", title: "Thử với ví dụ", text: "" },
        { type: "remember", title: "Em ghi nhớ", text: "" },
        { type: "practice", title: "Tự luyện tập", text: "" },
      ],
      goals: [],
      hints: [],
      reflection: [],
      illustration: null,
    },
  };
}
const lines = (value: string) => value.split("\n");
const illustrations: Record<LessonIllustration["kind"], string> = {
  fraction: "Thanh phân số",
  garden: "Luống rau và diện tích",
  reading: "Hành trình đọc hiểu",
  clock: "Đồng hồ",
  bars: "Biểu đồ cột",
  angles: "Góc và số đo",
  counters: "Chấm tròn để đếm (lớp 1–2)",
  cards: "Thẻ chữ và từ ngắn (lớp 1–2)",
};

function LessonForm({
  options,
  grade,
  original,
}: {
  options: Options;
  grade: number;
  original?: Draft;
}) {
  const router = useRouter();
  const [draft, setDraft] = useState(original);
  const [form, setForm] = useState<Payload>(
    original?.payload || initial(options, grade),
  );
  const [dirty, setDirty] = useState(false),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [preview, setPreview] = useState(false),
    [reason, setReason] = useState("");
  const update = (values: Partial<Payload>) => {
    setForm((f) => ({ ...f, ...values }));
    setDirty(true);
    setNotice("");
  };
  const content = (values: Partial<LessonContent>) =>
    update({ content: { ...form.content, ...values } });
  useEffect(() => {
    if (!dirty) return;
    const warn = (e: BeforeUnloadEvent) => {
      e.preventDefault();
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);
  const selectedTopics = options.topics.filter(
    (t) => t.subject_id === form.subject_id,
  );
  const applicableSkills = options.skills.filter(
    (s) => s.subject_id === form.subject_id,
  );
  function selectTopic(topicId: string, subjectId = form.subject_id) {
    update({
      subject_id: subjectId,
      topic_id: topicId,
      skill_ids: options.skills
        .filter((s) => s.topic_id === topicId)
        .map((s) => s.id),
    });
  }
  async function save() {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const normalized = {
        ...form,
        content: {
          ...form.content,
          goals: (form.content.goals || [])
            .map((s) => s.trim())
            .filter(Boolean),
          hints: (form.content.hints || [])
            .map((s) => s.trim())
            .filter(Boolean),
          reflection: (form.content.reflection || [])
            .map((s) => s.trim())
            .filter(Boolean),
        },
        preview: {
          ...form.preview,
          goals: (form.preview.goals || [])
            .map((s) => s.trim())
            .filter(Boolean),
        },
      };
      const result = await api<Draft>(
        `/admin/lessons${draft ? `/${draft.id}` : ""}`,
        {
          method: draft ? "PUT" : "POST",
          body: JSON.stringify({
            ...normalized,
            expected_revision: draft?.edit_revision || 0,
            source_fingerprint: draft?.source_fingerprint || null,
          }),
        },
      );
      setDraft(result);
      setForm(result.payload);
      setDirty(false);
      setNotice("Đã lưu nháp. Chỉ bản đã xuất bản hiển thị cho học sinh.");
      if (!draft) router.replace(`/admin/lessons/${result.id}/edit`);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function action(name: "review" | "publish" | "reset") {
    if (!draft) return;
    if (
      name === "reset" &&
      !window.confirm(
        "Tạo nháp từ bài hiện tại sẽ bỏ nội dung nháp đang có. Tiếp tục?",
      )
    )
      return;
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const result = await api<Draft>(`/admin/lessons/${draft.id}/${name}`, {
        method: "POST",
        body: JSON.stringify({
          expected_revision: draft.edit_revision,
          reason,
        }),
      });
      setDraft(result);
      setForm(result.payload);
      setDirty(false);
      setNotice(
        name === "publish"
          ? "Đã xuất bản bài học."
          : name === "review"
            ? "Đã duyệt bản nháp. Có thể xuất bản."
            : "Đã tạo nháp từ bản hiện tại. Hãy kiểm tra trước khi duyệt.",
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <div className="notice">
        {draft
          ? `Bài: ${statusLabels[draft.lesson_status]} · Bản soạn: ${statusLabels[draft.draft_status]} · Revision ${draft.edit_revision}`
          : "Bài mới chưa xuất bản"}
        . Mỗi lần sửa cần lưu và duyệt lại.
      </div>
      {draft?.source_changed && (
        <p className="notice error" role="alert">
          Bài hoặc quyền truy cập đã thay đổi ở nơi khác. Tạo nháp từ bản hiện
          tại để tiếp tục; thao tác này bỏ nháp cũ.
        </p>
      )}
      <form
        className="studio-form"
        onSubmit={(e) => {
          e.preventDefault();
          void save();
        }}
      >
        <fieldset disabled={busy}>
          <legend>Thông tin bài học</legend>
          <label htmlFor="lesson-category">
            Nhóm bài học
            <select
              id="lesson-category"
              value={form.content.category || "core"}
              onChange={(e) =>
                content({ category: e.target.value as "core" | "thinking" })
              }
            >
              <option value="core">Bài học theo chủ đề</option>
              <option value="thinking">Góc tư duy và đố mẹo</option>
            </select>
          </label>
          <div className="two-columns">
            <label htmlFor="lesson-code">
              Mã bài học
              <input
                id="lesson-code"
                required
                pattern="[A-Za-z0-9][A-Za-z0-9_-]+"
                minLength={3}
                maxLength={100}
                value={form.code}
                disabled={!!draft}
                onChange={(e) => update({ code: e.target.value })}
              />
            </label>
            <label htmlFor="lesson-title">
              Tên bài học
              <input
                id="lesson-title"
                required
                minLength={5}
                maxLength={255}
                value={form.title}
                onChange={(e) => update({ title: e.target.value })}
              />
            </label>
            <label htmlFor="lesson-subject">
              Môn học
              <select
                id="lesson-subject"
                value={form.subject_id}
                disabled={!!draft}
                onChange={(e) =>
                  selectTopic(
                    options.topics.find((t) => t.subject_id === e.target.value)
                      ?.id || "",
                    e.target.value,
                  )
                }
              >
                {options.subjects.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name_vi}
                  </option>
                ))}
              </select>
            </label>
            <label htmlFor="lesson-topic">
              Chủ đề
              <select
                id="lesson-topic"
                required
                disabled={!!draft}
                value={form.topic_id}
                onChange={(e) => selectTopic(e.target.value)}
              >
                <option value="">Chọn chủ đề</option>
                {selectedTopics.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.title}
                  </option>
                ))}
              </select>
            </label>
            <label htmlFor="lesson-duration">
              Thời lượng đọc dự kiến (phút)
              <input
                id="lesson-duration"
                type="number"
                required
                min={1}
                max={60}
                value={form.estimated_minutes}
                onChange={(e) =>
                  update({ estimated_minutes: Number(e.target.value) })
                }
              />
            </label>
            <label htmlFor="lesson-order">
              Thứ tự trong chủ đề
              <input
                id="lesson-order"
                type="number"
                required
                min={0}
                max={999}
                value={form.sort_order}
                onChange={(e) => update({ sort_order: Number(e.target.value) })}
              />
            </label>
            <label htmlFor="lesson-plan">
              Gói bài học
              <select
                id="lesson-plan"
                value={form.minimum_plan_code}
                onChange={(e) =>
                  update({
                    minimum_plan_code: e.target
                      .value as Payload["minimum_plan_code"],
                  })
                }
              >
                <option value="free">Free</option>
                <option value="vip">VIP</option>
              </select>
            </label>
            <label htmlFor="lesson-level">
              Mức nội dung
              <select
                id="lesson-level"
                value={form.learning_level}
                onChange={(e) =>
                  update({
                    learning_level: e.target.value as Payload["learning_level"],
                  })
                }
              >
                <option value="basic">Nền tảng</option>
                <option value="reinforcement">Củng cố</option>
                <option value="advanced">Nâng cao</option>
              </select>
            </label>
          </div>
          <label htmlFor="lesson-description">
            Mô tả bài học
            <textarea
              id="lesson-description"
              maxLength={2000}
              value={form.description}
              onChange={(e) => update({ description: e.target.value })}
            />
          </label>
          <fieldset className="studio-skills">
            <legend>Kỹ năng của bài (ít nhất một)</legend>
            {applicableSkills.map((skill) => (
              <label key={skill.id}>
                <input
                  type="checkbox"
                  checked={form.skill_ids.includes(skill.id)}
                  onChange={(e) =>
                    update({
                      skill_ids: e.target.checked
                        ? [...form.skill_ids, skill.id]
                        : form.skill_ids.filter((id) => id !== skill.id),
                    })
                  }
                />
                {skill.name}
              </label>
            ))}
          </fieldset>
        </fieldset>
        <fieldset disabled={busy}>
          <legend>Nội dung và hướng dẫn học</legend>
          <label htmlFor="lesson-goals">
            Mục tiêu (mỗi dòng một ý, tối đa 5)
            <textarea
              id="lesson-goals"
              required
              value={(form.content.goals || []).join("\n")}
              onChange={(e) => content({ goals: e.target.value.split("\n") })}
            />
          </label>
          {form.content.blocks.map((block, i) => (
            <section className="panel studio-block" key={i}>
              <h3>Phần {i + 1}</h3>
              <label htmlFor={`block-type-${i}`}>
                Loại phần
                <select
                  id={`block-type-${i}`}
                  value={block.type}
                  onChange={(e) =>
                    content({
                      blocks: form.content.blocks.map((b, n) =>
                        n === i
                          ? { ...b, type: e.target.value as typeof block.type }
                          : b,
                      ),
                    })
                  }
                >
                  <option value="text">Giải thích</option>
                  <option value="example">Ví dụ</option>
                  <option value="remember">Ghi nhớ</option>
                  <option value="practice">Tự luyện</option>
                </select>
              </label>
              <label htmlFor={`block-title-${i}`}>
                Tiêu đề phần {i + 1}
                <input
                  id={`block-title-${i}`}
                  required
                  minLength={2}
                  maxLength={160}
                  value={block.title}
                  onChange={(e) =>
                    content({
                      blocks: form.content.blocks.map((b, n) =>
                        n === i ? { ...b, title: e.target.value } : b,
                      ),
                    })
                  }
                />
              </label>
              <label htmlFor={`block-text-${i}`}>
                Nội dung phần {i + 1}
                <textarea
                  id={`block-text-${i}`}
                  required
                  minLength={5}
                  maxLength={6000}
                  rows={5}
                  value={block.text}
                  onChange={(e) =>
                    content({
                      blocks: form.content.blocks.map((b, n) =>
                        n === i ? { ...b, text: e.target.value } : b,
                      ),
                    })
                  }
                />
              </label>
              <button
                className="button secondary"
                type="button"
                disabled={form.content.blocks.length <= 3}
                onClick={() =>
                  content({
                    blocks: form.content.blocks.filter((_, n) => n !== i),
                  })
                }
              >
                Bỏ phần {i + 1}
              </button>
            </section>
          ))}
          <button
            className="button secondary"
            type="button"
            disabled={form.content.blocks.length >= 12}
            onClick={() =>
              content({
                blocks: [
                  ...form.content.blocks,
                  { type: "text", title: "Phần mới", text: "" },
                ],
              })
            }
          >
            Thêm phần bài học
          </button>
          <label htmlFor="lesson-hints">
            Gợi ý từng bước (mỗi dòng một ý, tối đa 5)
            <textarea
              id="lesson-hints"
              value={(form.content.hints || []).join("\n")}
              onChange={(e) => content({ hints: e.target.value.split("\n") })}
            />
          </label>
          <label htmlFor="lesson-free-hints">
            Số gợi ý miễn phí
            <select
              id="lesson-free-hints"
              value={form.content.free_hint_count ?? "all"}
              onChange={(e) =>
                content({
                  free_hint_count:
                    e.target.value === "all" ? null : Number(e.target.value),
                })
              }
            >
              <option value="all">Tất cả gợi ý hiện có</option>
              {[1, 2, 3, 4, 5].map((count) => (
                <option key={count} value={count}>
                  {count} gợi ý đầu
                </option>
              ))}
            </select>
            <small>
              Ít nhất 1 gợi ý cơ bản khi phân bổ. Các gợi ý còn lại dành cho
              VIP; số miễn phí không được vượt tổng gợi ý đã nhập.
            </small>
          </label>
          <label htmlFor="lesson-reflection">
            Câu hỏi tự suy ngẫm (mỗi dòng một ý, tối đa 3)
            <textarea
              id="lesson-reflection"
              value={(form.content.reflection || []).join("\n")}
              onChange={(e) =>
                content({ reflection: e.target.value.split("\n") })
              }
            />
          </label>
        </fieldset>
        <fieldset disabled={busy}>
          <legend>Minh họa cho bài học</legend>
          <label htmlFor="lesson-illustration">
            Chọn minh họa
            <select
              id="lesson-illustration"
              value={form.content.illustration?.kind || ""}
              onChange={(e) =>
                content({
                  illustration: e.target.value
                    ? {
                        kind: e.target.value as LessonIllustration["kind"],
                        caption: "",
                        numerator: 3,
                        denominator: 8,
                        rows: 3,
                        columns: 4,
                        hour: 8,
                        minute: 0,
                        count: 5,
                        angle: 60,
                        tick: 4,
                        labels:
                          e.target.value === "cards"
                            ? ["a", "ă", "â"]
                            : ["Tổ 1", "Tổ 2", "Tổ 3"],
                        values: [12, 16, 20],
                      }
                    : null,
                })
              }
            >
              <option value="">Không dùng minh họa</option>
              {Object.entries(illustrations).map(([kind, label]) => (
                <option key={kind} value={kind}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          {form.content.illustration && (
            <>
              <label htmlFor="lesson-caption">
                Chú thích hình (nêu rõ ý nghĩa và số liệu)
                <textarea
                  id="lesson-caption"
                  required
                  minLength={5}
                  maxLength={400}
                  value={form.content.illustration.caption}
                  onChange={(e) =>
                    content({
                      illustration: {
                        ...form.content.illustration!,
                        caption: e.target.value,
                      },
                    })
                  }
                />
              </label>
              <div className="two-columns">
                {(form.content.illustration.kind === "fraction"
                  ? [
                      ["numerator", "Số phần tô màu", 0, 12],
                      ["denominator", "Tổng số phần", 1, 12],
                    ]
                  : form.content.illustration.kind === "garden"
                    ? [
                        ["rows", "Số hàng ô vuông", 1, 6],
                        ["columns", "Số cột ô vuông", 1, 8],
                      ]
                    : form.content.illustration.kind === "clock"
                      ? [
                          ["hour", "Giờ (0–23)", 0, 23],
                          ["minute", "Phút", 0, 59],
                        ]
                      : form.content.illustration.kind === "angles"
                        ? [["angle", "Số đo góc (độ)", 1, 180]]
                        : form.content.illustration.kind === "counters"
                          ? [["count", "Số chấm tròn (0–20)", 0, 20]]
                          : form.content.illustration.kind === "bars"
                            ? [["tick", "Số đơn vị mỗi vạch", 1, 20]]
                            : []
                ).map(([key, label, min, max]) => (
                  <label key={key} htmlFor={`figure-${key}`}>
                    {label}
                    <input
                      id={`figure-${key}`}
                      type="number"
                      required
                      min={Number(min)}
                      max={Number(max)}
                      value={Number(
                        form.content.illustration![
                          key as keyof LessonIllustration
                        ] ?? 0,
                      )}
                      onChange={(e) =>
                        content({
                          illustration: {
                            ...form.content.illustration!,
                            [key]: Number(e.target.value),
                          },
                        })
                      }
                    />
                  </label>
                ))}
              </div>
              {form.content.illustration.kind === "cards" && (
                <label>
                  Thẻ chữ/từ (1–6 thẻ, phân cách bằng dấu phẩy)
                  <input
                    value={(form.content.illustration.labels || []).join(", ")}
                    onChange={(e) =>
                      content({
                        illustration: {
                          ...form.content.illustration!,
                          labels: e.target.value
                            .split(",")
                            .map((v) => v.trim()),
                        },
                      })
                    }
                  />
                </label>
              )}
              {form.content.illustration.kind === "bars" && (
                <fieldset>
                  <legend>Số liệu biểu đồ (1–6 cột)</legend>
                  {(form.content.illustration.values || [12, 16, 20]).map(
                    (number, i) => (
                      <div className="two-columns" key={i}>
                        <label htmlFor={`bar-label-${i}`}>
                          Nhãn cột {i + 1}
                          <input
                            id={`bar-label-${i}`}
                            required
                            maxLength={18}
                            value={
                              (form.content.illustration!.labels || [
                                "Tổ 1",
                                "Tổ 2",
                                "Tổ 3",
                              ])[i]
                            }
                            onChange={(e) => {
                              const labels = [
                                ...(form.content.illustration!.labels || [
                                  "Tổ 1",
                                  "Tổ 2",
                                  "Tổ 3",
                                ]),
                              ];
                              labels[i] = e.target.value;
                              content({
                                illustration: {
                                  ...form.content.illustration!,
                                  labels,
                                },
                              });
                            }}
                          />
                        </label>
                        <label htmlFor={`bar-value-${i}`}>
                          Giá trị cột {i + 1}
                          <input
                            id={`bar-value-${i}`}
                            type="number"
                            min={0}
                            max={100}
                            required
                            value={number}
                            onChange={(e) => {
                              const values = [
                                ...(form.content.illustration!.values || [
                                  12, 16, 20,
                                ]),
                              ];
                              values[i] = Number(e.target.value);
                              content({
                                illustration: {
                                  ...form.content.illustration!,
                                  values,
                                },
                              });
                            }}
                          />
                        </label>
                      </div>
                    ),
                  )}
                  <div className="actions">
                    <button
                      type="button"
                      className="button secondary"
                      disabled={
                        (form.content.illustration.values || [12, 16, 20])
                          .length >= 6
                      }
                      onClick={() =>
                        content({
                          illustration: {
                            ...form.content.illustration!,
                            labels: [
                              ...(form.content.illustration!.labels || [
                                "Tổ 1",
                                "Tổ 2",
                                "Tổ 3",
                              ]),
                              "Cột mới",
                            ],
                            values: [
                              ...(form.content.illustration!.values || [
                                12, 16, 20,
                              ]),
                              0,
                            ],
                          },
                        })
                      }
                    >
                      Thêm cột
                    </button>
                    <button
                      type="button"
                      className="button secondary"
                      disabled={
                        (form.content.illustration.values || [12, 16, 20])
                          .length <= 1
                      }
                      onClick={() =>
                        content({
                          illustration: {
                            ...form.content.illustration!,
                            labels: (
                              form.content.illustration!.labels || [
                                "Tổ 1",
                                "Tổ 2",
                                "Tổ 3",
                              ]
                            ).slice(0, -1),
                            values: (
                              form.content.illustration!.values || [12, 16, 20]
                            ).slice(0, -1),
                          },
                        })
                      }
                    >
                      Bỏ cột cuối
                    </button>
                  </div>
                </fieldset>
              )}
            </>
          )}
        </fieldset>
        <fieldset disabled={busy}>
          <legend>Giới thiệu riêng cho bài bị khóa</legend>
          <p>
            Chỉ nhập mục tiêu và giới thiệu; không chép toàn bộ nội dung hoặc
            lời giải vào đây.
          </p>
          <label htmlFor="lesson-preview-summary">
            Đoạn giới thiệu
            <textarea
              id="lesson-preview-summary"
              maxLength={500}
              value={form.preview.summary || ""}
              onChange={(e) =>
                update({
                  preview: { ...form.preview, summary: e.target.value },
                })
              }
            />
          </label>
          <label htmlFor="lesson-preview-goals">
            Mục tiêu giới thiệu (mỗi dòng một ý)
            <textarea
              id="lesson-preview-goals"
              value={(form.preview.goals || []).join("\n")}
              onChange={(e) =>
                update({
                  preview: { ...form.preview, goals: lines(e.target.value) },
                })
              }
            />
          </label>
        </fieldset>
        <div className="quiz-actions">
          <button
            className="button"
            disabled={
              busy ||
              !form.topic_id ||
              !form.skill_ids.length ||
              draft?.source_changed
            }
          >
            {busy ? "Đang xử lý…" : "Lưu nháp bài học"}
          </button>
          <button
            className="button secondary"
            type="button"
            onClick={() => setPreview((p) => !p)}
          >
            {preview ? "Đóng xem trước" : "Xem trước bài học"}
          </button>
        </div>
      </form>
      {error && (
        <p className="notice error" role="alert">
          {error}
        </p>
      )}
      {notice && (
        <p className="notice" role="status">
          {notice}
        </p>
      )}
      {draft && (
        <section className="panel studio-publishing">
          <h2>Duyệt và xuất bản</h2>
          <p>
            Lưu nháp trước khi duyệt. Mỗi thao tác kiểm tra revision; xuất bản
            cập nhật bài học, kỹ năng và quyền trong cùng transaction.
          </p>
          <label htmlFor="lesson-reason">
            Lý do duyệt / xuất bản / tạo lại nháp
            <input
              id="lesson-reason"
              value={reason}
              maxLength={500}
              onChange={(e) => setReason(e.target.value)}
            />
          </label>
          <div className="quiz-actions">
            <button
              className="button secondary"
              disabled={
                busy ||
                dirty ||
                reason.trim().length < 5 ||
                draft.draft_status !== "draft" ||
                draft.source_changed
              }
              onClick={() => void action("review")}
            >
              Duyệt bài học
            </button>
            <button
              className="button"
              disabled={
                busy ||
                dirty ||
                reason.trim().length < 5 ||
                draft.draft_status !== "reviewed" ||
                draft.source_changed
              }
              onClick={() => void action("publish")}
            >
              Xuất bản bài học
            </button>
            <button
              className="button secondary"
              disabled={busy || reason.trim().length < 5}
              onClick={() => void action("reset")}
            >
              Tạo nháp từ bản hiện tại
            </button>
          </div>
          {dirty && <p>Có thay đổi chưa lưu. Hãy lưu nháp trước khi duyệt.</p>}
          <h3>Lịch sử biên soạn gần nhất</h3>
          {draft.history.length ? (
            <ul>
              {draft.history.map((item, i) => (
                <li key={i}>
                  {dateLabel(item.created_at)} ·{" "}
                  {item.actor_name || "Quản trị viên"} ·{" "}
                  {(
                    {
                      "authoring.lesson.save": "Lưu nháp",
                      "authoring.lesson.review": "Duyệt",
                      "authoring.lesson.publish": "Xuất bản",
                      "authoring.lesson.reset": "Tạo lại nháp",
                    } as Record<string, string>
                  )[item.action] || item.action}
                  {item.reason ? ` · ${item.reason}` : ""}
                </li>
              ))}
            </ul>
          ) : (
            <p>Chưa có thao tác biên soạn.</p>
          )}
        </section>
      )}
      {preview && (
        <section className="studio-preview student">
          <PageTitle
            title={form.title || "Xem trước bài học"}
            description="Bản xem trước chưa ghi tiến độ hoặc xuất bản."
          />
          <LessonBody
            key={JSON.stringify(form.content)}
            content={form.content}
          />
        </section>
      )}
    </>
  );
}

function WithOptions({ original }: { original?: Draft }) {
  const [grade, setGrade] = useState(original?.payload.grade || 4);
  const options = useResource<Options>(
    `/admin/authoring/options?grade=${grade}`,
  );
  return (
    <>
      <label className="filters" htmlFor="lesson-grade">
        Lớp bài học
        <select
          id="lesson-grade"
          disabled={!!original}
          value={grade}
          onChange={(e) => setGrade(Number(e.target.value))}
        >
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n} value={n}>
              Lớp {n}
            </option>
          ))}
        </select>
      </label>
      {options.loading ? (
        <Loading />
      ) : options.error || !options.data ? (
        <ErrorState message={options.error} retry={options.retry} />
      ) : !options.data.topics.length ? (
        <Empty>
          Lớp này chưa có chủ đề để biên soạn. Chọn lớp 3 hoặc lớp 4 để tiếp
          tục.
        </Empty>
      ) : (
        <LessonForm
          key={grade}
          grade={grade}
          options={options.data}
          original={original}
        />
      )}
    </>
  );
}
function Existing({ id }: { id: string }) {
  const resource = useResource<Draft>(`/admin/lessons/${id}`);
  return resource.loading ? (
    <Loading />
  ) : resource.error || !resource.data ? (
    <ErrorState message={resource.error} retry={resource.retry} />
  ) : (
    <WithOptions original={resource.data} />
  );
}
export function LessonEditorPage({ id }: { id?: string }) {
  return (
    <>
      <PageTitle
        title={id ? "Biên soạn bài học" : "Tạo bài học mới"}
        description="Nội dung chữ, ví dụ, gợi ý và minh họa SVG. Mã/môn/lớp/chủ đề cố định sau khi tạo bài."
      />
      <Link className="card-link" href="/admin/lessons">
        ← Danh sách bài học
      </Link>
      {id ? <Existing id={id} /> : <WithOptions />}
    </>
  );
}
