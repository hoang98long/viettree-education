"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading, PageTitle } from "@/components/ui";
import { QuestionInput } from "@/components/question-input";
import type { Answer, QuestionKind } from "@/lib/types";
import type { Options, QuestionDraft } from "@/features/authoring/types";
import { ScopeFields, ContentActions } from "@/features/authoring/shared";
import { kinds } from "@/features/authoring/constants";

export function QuestionForm({
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
            : "Tạo câu hỏi"
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
