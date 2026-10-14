"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, dateLabel } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { LessonBody } from "@/components/lesson-body";
import type { LessonContent } from "@/lib/types";
import type { Options, Draft, Payload } from "@/features/lessons/types";
import { initial, lines } from "@/features/lessons/form-values";
import { statusLabels } from "@/features/lessons/constants";
import { ContentFields } from "@/features/lessons/content-fields";
import { IllustrationFields } from "@/features/lessons/illustration-fields";
import { ReadingReview } from "./reading-review";

export function LessonForm({
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
        <ContentFields value={form.content} content={content} busy={busy} />
        <IllustrationFields
          value={form.content}
          content={content}
          busy={busy}
        />
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
      <ReadingReview value={form} />
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

export function WithOptions({ original }: { original?: Draft }) {
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

export function Existing({ id }: { id: string }) {
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
