"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { QuestionInput } from "@/components/question-input";
import type {
  Answer,
  Content,
  Page,
  Question,
  QuestionKind,
  Student,
} from "@/lib/types";

type Options = {
  subjects: { id: string; code: string; name_vi: string }[];
  topics: { id: string; subject_id: string; title: string }[];
  skills: { id: string; subject_id: string; topic_id: string; name: string }[];
  lessons: { id: string; topic_id: string; title: string }[];
};
type QuestionDraft = {
  id: string;
  question_id: string;
  code: string;
  grade: number;
  subject_id: string;
  topic_id: string;
  skill_ids: string[];
  question_type: QuestionKind;
  difficulty: number;
  content: Content;
  grading: Record<string, unknown>;
  explanation: { text: string };
  status: string;
  version: number;
  reviewed_by: string | null;
  minimum_plan_code: string;
  updated_at: string;
  edit_revision: number;
};
type AssessmentDraft = {
  id: string;
  code: string;
  grade: number;
  subject_id: string;
  topic_id: string;
  lesson_id: string | null;
  title: string;
  description: string | null;
  status: string;
  assessment_type: string;
  time_limit_seconds: number | null;
  max_attempts: number;
  minimum_plan_code: string;
  learning_level: string;
  preview: { summary?: string; goals?: string[] };
  reviewed: boolean;
  updated_at: string;
  edit_revision: number;
  effective_access: { minimum_plan_code: string | null };
  items: {
    question_version_id: string;
    points: number;
    question: QuestionDraft;
  }[];
};
const kinds: Record<QuestionKind, string> = {
  single_choice: "Chọn một đáp án",
  multiple_choice: "Chọn nhiều đáp án",
  fill_blank: "Điền khuyết",
  ordering: "Sắp xếp",
};

function ScopeFields({
  options,
  subject,
  topic,
  setSubject,
  setTopic,
  disabled = false,
}: {
  options: Options;
  subject: string;
  topic: string;
  setSubject: (value: string) => void;
  setTopic: (value: string) => void;
  disabled?: boolean;
}) {
  return (
    <div className="two-columns">
      <label>
        Môn học
        <select
          required
          disabled={disabled}
          value={subject}
          onChange={(e) => {
            const value = e.target.value;
            setSubject(value);
            setTopic(
              options.topics.find((item) => item.subject_id === value)?.id ??
                "",
            );
          }}
        >
          {options.subjects.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name_vi}
            </option>
          ))}
        </select>
      </label>
      <label>
        Chủ đề
        <select
          required
          disabled={disabled}
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        >
          <option value="">Chọn chủ đề</option>
          {options.topics
            .filter((item) => item.subject_id === subject)
            .map((item) => (
              <option key={item.id} value={item.id}>
                {item.title}
              </option>
            ))}
        </select>
      </label>
    </div>
  );
}
function ContentActions({
  kind,
  data,
  reload,
}: {
  kind: "questions" | "assessments";
  data: QuestionDraft | AssessmentDraft;
  reload: () => void;
}) {
  const router = useRouter();
  const [reason, setReason] = useState("");
  const [newCode, setNewCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const reviewed =
    "reviewed" in data ? data.reviewed : Boolean(data.reviewed_by);
  async function act(action: string) {
    setBusy(true);
    setError("");
    try {
      const result = await api<{ id: string }>(
        `/admin/authoring/${kind}/${data.id}/${action}`,
        {
          method: "POST",
          body:
            action === "revise"
              ? undefined
              : JSON.stringify(
                  action === "clone"
                    ? { code: newCode }
                    : { expected_revision: data.edit_revision, reason },
                ),
        },
      );
      if (action === "revise" || action === "clone")
        router.push(`/admin/${kind}/${result.id}/edit`);
      else reload();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel authoring-actions">
      <h2>Duyệt và xuất bản</h2>
      <p>
        Trạng thái:{" "}
        <strong>
          {data.status === "draft"
            ? reviewed
              ? "Nháp đã duyệt"
              : "Nháp chưa duyệt"
            : data.status === "published"
              ? "Đã xuất bản"
              : "Đã lưu trữ"}
        </strong>
        . Lưu sửa bản nháp sẽ yêu cầu duyệt lại.
      </p>
      <label>
        Lý do duyệt / xuất bản / lưu trữ
        <textarea
          value={reason}
          minLength={5}
          maxLength={500}
          onChange={(e) => setReason(e.target.value)}
        />
      </label>
      <div className="quiz-actions">
        {data.status === "draft" && (
          <>
            <button
              className="button secondary"
              disabled={busy || reason.trim().length < 5}
              onClick={() => void act("review")}
            >
              Duyệt nội dung
            </button>
            <button
              className="button"
              disabled={busy || !reviewed || reason.trim().length < 5}
              onClick={() => void act("publish")}
            >
              Xuất bản
            </button>
          </>
        )}
        {data.status !== "archived" && (
          <button
            className="button secondary"
            disabled={busy || reason.trim().length < 5}
            onClick={() => void act("archive")}
          >
            Lưu trữ
          </button>
        )}
        {kind === "questions" && data.status !== "draft" && (
          <button
            className="button secondary"
            disabled={busy}
            onClick={() => void act("revise")}
          >
            Tạo phiên bản mới
          </button>
        )}
      </div>
      {kind === "assessments" && (
        <div className="clone-form">
          <label>
            Mã đề sao chép
            <input
              value={newCode}
              minLength={3}
              maxLength={100}
              pattern="[A-Za-z0-9][A-Za-z0-9_-]+"
              onChange={(e) => setNewCode(e.target.value)}
            />
          </label>
          <button
            className="button secondary"
            disabled={busy || !/^[A-Za-z0-9][A-Za-z0-9_-]{2,99}$/.test(newCode)}
            onClick={() => void act("clone")}
          >
            Sao chép thành nháp mới
          </button>
        </div>
      )}
      {error && (
        <p role="alert" className="error-text">
          {error}
        </p>
      )}
    </section>
  );
}

function QuestionForm({
  options,
  initial,
}: {
  options: Options;
  initial?: QuestionDraft;
}) {
  const router = useRouter();
  const [subject, setSubject] = useState(
    initial?.subject_id ?? options.subjects[0]?.id ?? "",
  );
  const [topic, setTopic] = useState(
    initial?.topic_id ??
      options.topics.find((item) => item.subject_id === subject)?.id ??
      "",
  );
  const [skills, setSkills] = useState<string[]>(initial?.skill_ids ?? []);
  const [code, setCode] = useState(initial?.code ?? "");
  const [kind, setKind] = useState<QuestionKind>(
    initial?.question_type ?? "single_choice",
  );
  const [difficulty, setDifficulty] = useState(initial?.difficulty ?? 2);
  const [plan, setPlan] = useState(initial?.minimum_plan_code ?? "free");
  const [prompt, setPrompt] = useState(initial?.content.prompt ?? "");
  const [choices, setChoices] = useState(
    initial?.content.options?.map((item) => item.text).join("\n") ?? "",
  );
  const [correct, setCorrect] = useState<string[]>(
    initial?.question_type === "single_choice"
      ? [String(initial.grading.correct_option_id)]
      : initial?.question_type === "multiple_choice"
        ? (initial.grading.correct_option_ids as string[])
        : [],
  );
  const [accepted, setAccepted] = useState(
    (initial?.grading.accepted_answers as string[] | undefined)?.join("\n") ??
      "",
  );
  const [ordered, setOrdered] = useState(
    (initial?.grading.ordered_ids as string[] | undefined)?.join(",") ?? "",
  );
  const [caseSensitive, setCaseSensitive] = useState(
    Boolean(initial?.grading.case_sensitive),
  );
  const [explanation, setExplanation] = useState(
    initial?.explanation.text ?? "",
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [showPreview, setShowPreview] = useState(false);
  const [previewAnswer, setPreviewAnswer] = useState<Answer | null>(null);
  const editable = !initial || initial.status === "draft";
  // Keep saved option IDs when revising; answers in old attempts use those exact IDs.
  const choiceItems = choices
    .split("\n")
    .map((text) => text.trim())
    .filter(Boolean)
    .map((text, index) => ({
      id:
        initial?.content.options?.[index]?.id ??
        String.fromCharCode(97 + index),
      text,
    }));
  const eligibleSkills = options.skills.filter(
    (item) => item.subject_id === subject,
  );
  const skillIds = skills.length
    ? skills.filter((id) => eligibleSkills.some((item) => item.id === id))
    : [eligibleSkills.find((item) => item.topic_id === topic)?.id].filter(
        (id): id is string => Boolean(id),
      );
  function grading() {
    if (kind === "single_choice")
      return { correct_option_id: correct[0] ?? "" };
    if (kind === "multiple_choice") return { correct_option_ids: correct };
    if (kind === "ordering")
      return {
        ordered_ids: ordered
          .split(",")
          .map((id) => id.trim())
          .filter(Boolean),
      };
    return {
      accepted_answers: accepted
        .split("\n")
        .map((value) => value.trim())
        .filter(Boolean),
      case_sensitive: caseSensitive,
    };
  }
  async function save() {
    setBusy(true);
    setError("");
    try {
      const value = await api<QuestionDraft>(
        `/admin/authoring/questions${initial ? `/${initial.id}` : ""}`,
        {
          method: initial ? "PUT" : "POST",
          body: JSON.stringify({
            code,
            grade: initial?.grade ?? 4,
            subject_id: subject,
            topic_id: topic,
            skill_ids: skillIds,
            question_type: kind,
            difficulty,
            minimum_plan_code: plan,
            content: {
              prompt,
              options: kind === "fill_blank" ? [] : choiceItems,
            },
            grading: grading(),
            explanation,
            ...(initial ? { expected_revision: initial.edit_revision } : {}),
          }),
        },
      );
      router.push(`/admin/questions/${value.id}/edit`);
      router.refresh();
      if (initial) window.location.reload();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void save();
        }}
      >
        <fieldset disabled={!editable || busy} className="authoring-fields">
          <label>
            Mã câu hỏi
            <input
              required
              minLength={3}
              maxLength={100}
              pattern="[A-Za-z0-9][A-Za-z0-9_-]+"
              disabled={Boolean(initial)}
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          </label>
          <ScopeFields
            options={options}
            subject={subject}
            topic={topic}
            setSubject={(value) => {
              setSubject(value);
              setSkills([]);
            }}
            setTopic={setTopic}
            disabled={Boolean(initial)}
          />
          <label>
            Kỹ năng chính
            <select
              required
              value={skillIds[0] ?? ""}
              onChange={(e) => setSkills([e.target.value])}
            >
              <option value="">Chọn kỹ năng</option>
              {eligibleSkills.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name}
                </option>
              ))}
            </select>
          </label>
          <div className="three-columns">
            <label>
              Loại câu hỏi
              <select
                value={kind}
                onChange={(e) => {
                  setKind(e.target.value as QuestionKind);
                  setCorrect([]);
                }}
              >
                {Object.entries(kinds).map(([value, name]) => (
                  <option key={value} value={value}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Độ khó
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(Number(e.target.value))}
              >
                {[1, 2, 3, 4, 5].map((value) => (
                  <option key={value} value={value}>
                    {value}/5
                  </option>
                ))}
              </select>
            </label>
            <label>
              Gói câu hỏi
              <select value={plan} onChange={(e) => setPlan(e.target.value)}>
                <option value="free">Miễn phí</option>
                <option value="vip">VIP</option>
              </select>
            </label>
          </div>
          <label>
            Nội dung câu hỏi
            <textarea
              required
              rows={4}
              minLength={5}
              maxLength={5000}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </label>
          {kind !== "fill_blank" && (
            <label>
              Các lựa chọn (2–8 dòng, mỗi dòng một lựa chọn)
              <textarea
                required
                rows={4}
                value={choices}
                onChange={(e) => setChoices(e.target.value)}
              />
            </label>
          )}
          {(kind === "single_choice" || kind === "multiple_choice") && (
            <div className="answer-key">
              <strong>Chọn đáp án đúng</strong>
              {choiceItems.map((item) => (
                <label className="confirmation-row" key={item.id}>
                  <input
                    type={kind === "single_choice" ? "radio" : "checkbox"}
                    name="correct-key"
                    checked={correct.includes(item.id)}
                    onChange={(e) =>
                      setCorrect(
                        kind === "single_choice"
                          ? [item.id]
                          : e.target.checked
                            ? [...correct, item.id]
                            : correct.filter((id) => id !== item.id),
                      )
                    }
                  />
                  {item.id.toUpperCase()}. {item.text}
                </label>
              ))}
            </div>
          )}
          {kind === "fill_blank" && (
            <>
              <label>
                Đáp án chấp nhận (mỗi dòng một cách viết)
                <textarea
                  required
                  value={accepted}
                  onChange={(e) => setAccepted(e.target.value)}
                />
              </label>
              <label className="confirmation-row">
                <input
                  type="checkbox"
                  checked={caseSensitive}
                  onChange={(e) => setCaseSensitive(e.target.checked)}
                />
                Phân biệt chữ hoa và chữ thường
              </label>
            </>
          )}
          {kind === "ordering" && (
            <label>
              Thứ tự đúng của mã lựa chọn, ví dụ b,a,c
              <input
                required
                value={ordered}
                onChange={(e) => setOrdered(e.target.value)}
              />
              <small>
                {choiceItems
                  .map((item) => `${item.id}: ${item.text}`)
                  .join(" · ")}
              </small>
            </label>
          )}
          <label>
            Lời giải
            <textarea
              required
              minLength={5}
              maxLength={5000}
              rows={3}
              value={explanation}
              onChange={(e) => setExplanation(e.target.value)}
            />
          </label>
          <button className="button" disabled={!topic || !skillIds.length}>
            {busy ? "Đang lưu…" : "Lưu nháp câu hỏi"}
          </button>
        </fieldset>
        {error && (
          <p className="error-text" role="alert">
            {error}
          </p>
        )}
      </form>
      <button
        className="button secondary"
        onClick={() => setShowPreview((value) => !value)}
      >
        Xem trước câu hỏi
      </button>
      {showPreview && (
        <div className="author-preview">
          <p className="question-prompt">{prompt}</p>
          <QuestionInput
            item={{
              id: "preview",
              position: 1,
              points: 1,
              question_version_id: "preview",
              question_type: kind,
              content: { prompt, options: choiceItems },
              answer: null,
            }}
            answer={previewAnswer}
            onChange={setPreviewAnswer}
          />
          <p className="muted">Bản xem trước không lưu bài làm hoặc điểm.</p>
        </div>
      )}
    </section>
  );
}

export function QuestionEditorPage({ id }: { id?: string }) {
  const detail = useResource<QuestionDraft>(
    id ? `/admin/authoring/questions/${id}` : "/admin/authoring/options",
    true,
  );
  const options = useResource<Options>(
    `/admin/authoring/options?grade=${id && detail.data?.grade ? detail.data.grade : 4}`,
  );
  if ((detail.loading && !detail.data) || (options.loading && !options.data))
    return <Loading />;
  if (detail.error || options.error || !options.data)
    return (
      <ErrorState
        message={detail.error || options.error}
        retry={() => {
          detail.retry();
          options.retry();
        }}
      />
    );
  const initial = id ? detail.data! : undefined;
  return (
    <>
      <PageTitle
        title={
          initial
            ? `${initial.code} · Phiên bản ${initial.version}`
            : "Tạo câu hỏi lớp 4"
        }
        description="Lưu nháp, xem trước, duyệt rồi xuất bản. Bản đã xuất bản giữ nguyên để bảo toàn bài làm."
      />
      <QuestionForm
        key={initial ? `${initial.id}:${initial.edit_revision}` : "new"}
        options={options.data}
        initial={initial}
      />
      {initial && (
        <ContentActions kind="questions" data={initial} reload={detail.retry} />
      )}
      <Link className="button secondary" href="/admin/questions">
        Về ngân hàng câu hỏi
      </Link>
    </>
  );
}

function AssessmentForm({
  options,
  initial,
}: {
  options: Options;
  initial?: AssessmentDraft;
}) {
  const router = useRouter();
  const [code, setCode] = useState(initial?.code ?? "");
  const [subject, setSubject] = useState(
    initial?.subject_id ?? options.subjects[0]?.id ?? "",
  );
  const [topic, setTopic] = useState(
    initial?.topic_id ??
      options.topics.find((item) => item.subject_id === subject)?.id ??
      "",
  );
  const [lesson, setLesson] = useState(initial?.lesson_id ?? "");
  const [title, setTitle] = useState(initial?.title ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [kind, setKind] = useState(initial?.assessment_type ?? "practice");
  const [plan, setPlan] = useState(initial?.minimum_plan_code ?? "free");
  const [level, setLevel] = useState(initial?.learning_level ?? "basic");
  const [minutes, setMinutes] = useState(
    initial?.time_limit_seconds ? initial.time_limit_seconds / 60 : 0,
  );
  const [maxAttempts, setMaxAttempts] = useState(initial?.max_attempts ?? 5);
  const [summary, setSummary] = useState(initial?.preview.summary ?? "");
  const [goals, setGoals] = useState(initial?.preview.goals?.join("\n") ?? "");
  const [items, setItems] = useState(
    initial?.items.map((item) => ({
      question_version_id: item.question_version_id,
      points: Number(item.points),
      prompt: item.question.content.prompt,
    })) ?? [],
  );
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const subjectCode =
    options.subjects.find((item) => item.id === subject)?.code ?? "";
  const bank = useResource<Page<Question>>(
    `/admin/questions?grade=${initial?.grade ?? 4}&status=published&subject_code=${subjectCode}&search=${encodeURIComponent(search)}&page=${page}`,
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const editable = !initial || initial.status === "draft";
  async function save() {
    setBusy(true);
    setError("");
    try {
      const value = await api<AssessmentDraft>(
        `/admin/authoring/assessments${initial ? `/${initial.id}` : ""}`,
        {
          method: initial ? "PUT" : "POST",
          body: JSON.stringify({
            code,
            grade: initial?.grade ?? 4,
            subject_id: subject,
            topic_id: topic,
            lesson_id: lesson || null,
            title,
            description,
            assessment_type: kind,
            minimum_plan_code: plan,
            learning_level: level,
            time_limit_seconds: minutes ? minutes * 60 : null,
            max_attempts: maxAttempts,
            preview: {
              summary,
              goals: goals
                .split("\n")
                .map((value) => value.trim())
                .filter(Boolean),
            },
            items: items.map((item) => ({
              question_version_id: item.question_version_id,
              points: item.points,
            })),
            ...(initial ? { expected_revision: initial.edit_revision } : {}),
          }),
        },
      );
      router.push(`/admin/assessments/${value.id}/edit`);
      router.refresh();
      if (initial) window.location.reload();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function move(index: number, direction: number) {
    const reordered = [...items];
    [reordered[index], reordered[index + direction]] = [
      reordered[index + direction],
      reordered[index],
    ];
    setItems(reordered);
  }
  return (
    <section className="panel">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void save();
        }}
      >
        <fieldset disabled={!editable || busy} className="authoring-fields">
          <label>
            Mã bài tập
            <input
              required
              minLength={3}
              maxLength={100}
              pattern="[A-Za-z0-9][A-Za-z0-9_-]+"
              disabled={Boolean(initial)}
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          </label>
          <ScopeFields
            options={options}
            subject={subject}
            topic={topic}
            setSubject={(value) => {
              setSubject(value);
              setItems([]);
              setLesson("");
              setPage(1);
            }}
            setTopic={(value) => {
              setTopic(value);
              setLesson("");
            }}
          />
          <label>
            Bài học đi kèm
            <select value={lesson} onChange={(e) => setLesson(e.target.value)}>
              <option value="">Đề độc lập trong chủ đề</option>
              {options.lessons
                .filter((item) => item.topic_id === topic)
                .map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.title}
                  </option>
                ))}
            </select>
          </label>
          <label>
            Tên bài tập
            <input
              required
              minLength={5}
              maxLength={255}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>
          <label>
            Mô tả
            <textarea
              maxLength={2000}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </label>
          <div className="three-columns">
            <label>
              Loại bài tập
              <select value={kind} onChange={(e) => setKind(e.target.value)}>
                <option value="practice">Luyện tập</option>
                <option value="homework">Bài được giao</option>
                <option value="quiz">Thử thách</option>
                <option value="test">Kiểm tra</option>
              </select>
            </label>
            <label>
              Gói tối thiểu
              <select value={plan} onChange={(e) => setPlan(e.target.value)}>
                <option value="free">Miễn phí</option>
                <option value="vip">VIP</option>
              </select>
            </label>
            <label>
              Mức nội dung
              <select value={level} onChange={(e) => setLevel(e.target.value)}>
                <option value="basic">Nền tảng</option>
                <option value="reinforcement">Củng cố</option>
                <option value="advanced">Nâng cao</option>
              </select>
            </label>
          </div>
          <div className="two-columns">
            <label>
              Thời gian làm bài (phút, 0 = không giới hạn)
              <input
                type="number"
                min={0}
                max={120}
                step={1}
                value={minutes}
                onChange={(e) => setMinutes(Number(e.target.value))}
              />
            </label>
            <label>
              Số lượt tối đa
              <input
                type="number"
                min={1}
                max={20}
                value={maxAttempts}
                onChange={(e) => setMaxAttempts(Number(e.target.value))}
              />
            </label>
          </div>
          <label>
            Đoạn giới thiệu riêng
            <textarea
              maxLength={350}
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
            />
          </label>
          <label>
            Mục tiêu (tối đa 5 dòng, mỗi dòng 120 ký tự)
            <textarea
              value={goals}
              onChange={(e) => setGoals(e.target.value)}
            />
          </label>
          {editable && (
            <>
              <h2>Chọn câu hỏi đã xuất bản</h2>
              <label>
                Tìm câu để thêm
                <input
                  value={search}
                  onChange={(e) => {
                    setSearch(e.target.value);
                    setPage(1);
                  }}
                />
              </label>
              {bank.loading ? (
                <Loading />
              ) : bank.error ? (
                <ErrorState message={bank.error} retry={bank.retry} />
              ) : bank.data?.items.length ? (
                <div className="question-picker">
                  {bank.data.items.map((item) => (
                    <div className="list-row" key={item.id}>
                      <div>
                        <strong>{item.content.prompt}</strong>
                        <small>
                          {item.code} ·{" "}
                          {kinds[item.question_type as QuestionKind]} ·{" "}
                          {item.minimum_plan_code === "vip"
                            ? "VIP"
                            : "Miễn phí"}
                        </small>
                      </div>
                      <button
                        type="button"
                        className="button secondary small"
                        disabled={
                          items.some(
                            (selected) =>
                              selected.question_version_id === item.id,
                          ) || items.length >= 50
                        }
                        onClick={() =>
                          setItems([
                            ...items,
                            {
                              question_version_id: item.id,
                              points: 1,
                              prompt: item.content.prompt,
                            },
                          ])
                        }
                      >
                        Thêm câu
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <Empty>
                  Chưa có câu phù hợp. Hãy tạo và xuất bản câu hỏi trước.
                </Empty>
              )}
              <div className="quiz-actions">
                <button
                  type="button"
                  className="button secondary"
                  disabled={page === 1}
                  onClick={() => setPage((value) => value - 1)}
                >
                  Trang trước
                </button>
                <span>Trang {page}</span>
                <button
                  type="button"
                  className="button secondary"
                  disabled={!bank.data || page * 20 >= bank.data.total}
                  onClick={() => setPage((value) => value + 1)}
                >
                  Trang sau
                </button>
              </div>
            </>
          )}
          <h2>
            Đề đã chọn · {items.length} câu ·{" "}
            {items.reduce((sum, item) => sum + item.points, 0)} điểm
          </h2>
          <ol className="assessment-selection">
            {items.map((item, index) => (
              <li key={item.question_version_id}>
                <strong>
                  {index + 1}. {item.prompt}
                </strong>
                <label>
                  Điểm câu {index + 1}
                  <input
                    type="number"
                    min={0.1}
                    max={100}
                    step={0.1}
                    value={item.points}
                    onChange={(e) =>
                      setItems(
                        items.map((value, itemIndex) =>
                          itemIndex === index
                            ? { ...value, points: Number(e.target.value) }
                            : value,
                        ),
                      )
                    }
                  />
                </label>
                <div className="quiz-actions">
                  <button
                    type="button"
                    className="button secondary small"
                    disabled={index === 0}
                    onClick={() => move(index, -1)}
                  >
                    Lên
                  </button>
                  <button
                    type="button"
                    className="button secondary small"
                    disabled={index === items.length - 1}
                    onClick={() => move(index, 1)}
                  >
                    Xuống
                  </button>
                  <button
                    type="button"
                    className="button secondary small"
                    onClick={() =>
                      setItems(
                        items.filter((_, itemIndex) => itemIndex !== index),
                      )
                    }
                  >
                    Bỏ câu
                  </button>
                </div>
              </li>
            ))}
          </ol>
          <p>
            Nếu bài học hoặc câu hỏi yêu cầu VIP, đề phải chọn gói VIP trước khi
            duyệt. Bản đã xuất bản giữ cố định các câu và thứ tự.
          </p>
          <button className="button" disabled={!topic || !items.length}>
            {busy ? "Đang lưu…" : "Lưu nháp bài tập"}
          </button>
        </fieldset>
        {error && (
          <p role="alert" className="error-text">
            {error}
          </p>
        )}
      </form>
    </section>
  );
}

function AssignmentPanel({ id }: { id: string }) {
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

export function AssessmentEditorPage({ id }: { id?: string }) {
  const detail = useResource<AssessmentDraft>(
    id ? `/admin/authoring/assessments/${id}` : "/admin/authoring/options",
    true,
  );
  const options = useResource<Options>(
    `/admin/authoring/options?grade=${id && detail.data?.grade ? detail.data.grade : 4}`,
  );
  if ((detail.loading && !detail.data) || (options.loading && !options.data))
    return <Loading />;
  if (detail.error || options.error || !options.data)
    return (
      <ErrorState
        message={detail.error || options.error}
        retry={() => {
          detail.retry();
          options.retry();
        }}
      />
    );
  const initial = id ? detail.data! : undefined;
  return (
    <>
      <PageTitle
        title={initial ? initial.title : "Tạo bài tập lớp 4"}
        description="Chọn câu hỏi, sắp thứ tự, đặt điểm và thời gian; duyệt trước khi xuất bản."
      />
      <AssessmentForm
        key={initial ? `${initial.id}:${initial.edit_revision}` : "new"}
        options={options.data}
        initial={initial}
      />
      {initial && (
        <ContentActions
          kind="assessments"
          data={initial}
          reload={detail.retry}
        />
      )}
      {initial?.status === "published" && <AssignmentPanel id={initial.id} />}
      <Link className="button secondary" href="/admin/assessments">
        Về danh sách bài tập
      </Link>
    </>
  );
}
