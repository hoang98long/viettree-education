"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { Page, Question, QuestionKind } from "@/lib/types";
import type { Options, AssessmentDraft } from "@/features/authoring/types";
import { ScopeFields, ContentActions } from "@/features/authoring/shared";
import { kinds } from "@/features/authoring/constants";
import { AssignmentPanel } from "@/features/authoring/assignments";

export function AssessmentForm({
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
        title={initial ? initial.title : "Tạo bài tập"}
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
