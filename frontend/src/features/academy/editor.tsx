"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState } from "@/components/ui";
import type { LessonContent, Step } from "./types";
import { AcademyImage } from "./shared";

type Detail = {
  lesson: {
    id: string;
    code: string;
    title: string;
    unit_id: string;
    position: number;
    revision: number;
  };
  versions: {
    id: string;
    version: number;
    status: string;
    payload: LessonContent;
  }[];
};
export function ContentEditor({
  id,
  grade,
  onSaved,
}: {
  id: string;
  grade: number;
  onSaved: () => void;
}) {
  const resource = useResource<Detail>(`/ai-academy/admin/lessons/${id}`);
  if (resource.loading) return <Loading />;
  if (resource.error)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  if (!resource.data) return null;
  return (
    <EditorForm
      key={resource.data.lesson.revision}
      id={id}
      grade={grade}
      current={resource.data}
      onSaved={onSaved}
      retry={resource.retry}
    />
  );
}
function EditorForm({
  id,
  grade,
  current,
  onSaved,
  retry,
}: {
  id: string;
  grade: number;
  current: Detail;
  onSaved: () => void;
  retry: () => void;
}) {
  const resource = { retry };
  const [content, setContent] = useState<LessonContent>(
    structuredClone(current.versions[0].payload),
  );
  const [title, setTitle] = useState(
    (current.versions[0].payload.title_override as string) ||
      current.lesson.title,
  );
  const [message, setMessage] = useState("");
  const [preview, setPreview] = useState(false);
  const [busy, setBusy] = useState(false);
  const units = useResource<{ id: string; title: string }[]>(
    `/ai-academy/admin/units?grade=${grade}`,
  );
  const [targetUnit, setTargetUnit] = useState(current.lesson.unit_id);
  const [position, setPosition] = useState(current.lesson.position);
  const [copyPosition, setCopyPosition] = useState(100);
  const [guidance, setGuidance] = useState("");
  async function proposeGuide() {
    setBusy(true);
    try {
      const data = await api<{
        mode: string;
        teacher_guide: string;
        notice: string;
      }>(`/ai-academy/admin/lessons/${id}/teacher-draft`, { method: "POST" });
      setGuidance(data.teacher_guide);
      setMessage(
        `${data.mode === "ollama" ? "Mô hình local" : "Mẫu nội bộ"} · ${data.notice}`,
      );
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function changeStep(index: number, values: Partial<Step>) {
    setContent((c) =>
      c
        ? {
            ...c,
            steps: c.steps.map((s, i) =>
              i === index ? { ...s, ...values } : s,
            ),
          }
        : c,
    );
  }
  function move(index: number, delta: number) {
    setContent((c) => {
      if (!c) return c;
      const steps = [...c.steps];
      const next = index + delta;
      if (next < 0 || next >= steps.length) return c;
      [steps[index], steps[next]] = [steps[next], steps[index]];
      return { ...c, steps };
    });
  }
  async function save(duplicate = false) {
    setBusy(true);
    try {
      const l = current.lesson;
      await api(
        duplicate
          ? "/ai-academy/admin/lessons"
          : `/ai-academy/admin/lessons/${id}`,
        {
          method: duplicate ? "POST" : "PUT",
          body: JSON.stringify({
            unit_id: duplicate ? targetUnit : l.unit_id,
            code: duplicate
              ? l.code + "-copy-" + crypto.randomUUID().slice(0, 8)
              : l.code,
            title: duplicate ? title + " (bản sao)" : title,
            position: duplicate ? copyPosition : position,
            revision: duplicate ? undefined : l.revision,
            content,
          }),
        },
      );
      setMessage("Đã lưu phiên bản nháp; cần gửi duyệt trước khi xuất bản.");
      resource.retry();
      onSaved();
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function workflow(action: string) {
    setBusy(true);
    try {
      await api(`/ai-academy/admin/lessons/${id}/${action}`, {
        method: "POST",
        body: JSON.stringify({ revision: current.lesson.revision }),
      });
      resource.retry();
      onSaved();
      setMessage("Đã cập nhật trạng thái.");
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function exportJson() {
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(content, null, 2)], {
        type: "application/json",
      }),
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = current.lesson.code + ".json";
    link.click();
    URL.revokeObjectURL(url);
  }
  async function importJson(file: File | undefined) {
    if (!file) return;
    try {
      if (file.size > 300000) throw new Error("File tối đa 300 KB");
      const raw = JSON.parse(await file.text());
      if (!Array.isArray(raw.steps) || !Array.isArray(raw.objectives))
        throw new Error("Thiếu steps/objectives");
      setContent(raw);
      setMessage("Đã nhập vào bản đang sửa; server sẽ kiểm tra khi lưu.");
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel">
      <h2>Biên soạn {current.lesson.code}</h2>
      <p>
        Phiên bản {current.versions[0].version} · {current.versions[0].status} ·
        revision {current.lesson.revision}.
      </p>
      <div className="academy-actions">
        <button
          className="button secondary"
          onClick={() => setPreview(!preview)}
        >
          {preview ? "Quay lại biên soạn" : "Xem trước học sinh"}
        </button>
        <button
          className="button secondary"
          disabled={busy}
          onClick={() => void proposeGuide()}
        >
          Gợi ý giáo án riêng
        </button>
        <button className="button secondary" onClick={exportJson}>
          Xuất JSON
        </button>
        <label>
          Nhập JSON
          <input
            type="file"
            accept=".json,application/json"
            onChange={(e) => void importJson(e.target.files?.[0])}
          />
        </label>
      </div>
      {guidance && (
        <aside className="notice">
          <h3>Đề xuất cần giáo viên kiểm tra</h3>
          <p>{guidance}</p>
          <button
            className="button secondary"
            onClick={() => setContent({ ...content, teacher_guide: guidance })}
          >
            Đưa vào bản đang biên soạn
          </button>
        </aside>
      )}
      <label>
        Phiên bản để phục hồi thành nháp
        <select
          onChange={(e) => {
            const v = current.versions.find((v) => v.id === e.target.value);
            if (v) setContent(structuredClone(v.payload));
          }}
          defaultValue={current.versions[0].id}
        >
          {current.versions.map((v) => (
            <option key={v.id} value={v.id}>
              v{v.version} · {v.status}
            </option>
          ))}
        </select>
      </label>
      {preview ? (
        <div className="academy-step">
          <h3>{title}</h3>
          <AcademyImage code={content.hero} alt={title} />
          {content.steps.map((s) => (
            <section key={s.id}>
              <h4>{s.title}</h4>
              <p>{s.text}</p>
              {s.media.map((code) => (
                <AcademyImage key={code} code={code} alt={s.title} />
              ))}
              {s.questions.map((q) => (
                <fieldset key={q.id}>
                  <legend>{q.prompt}</legend>
                  {q.options.map((o) => (
                    <p key={o}>○ {o}</p>
                  ))}
                </fieldset>
              ))}
            </section>
          ))}
          <p>Xem trước chỉ đọc; không ghi điểm/tiến độ học sinh.</p>
        </div>
      ) : (
        <>
          <label>
            Tên bài
            <input
              value={title}
              maxLength={180}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>
          <label>
            Mục tiêu (mỗi dòng một mục)
            <textarea
              value={content.objectives.join("\n")}
              onChange={(e) =>
                setContent({
                  ...content,
                  objectives: e.target.value.split("\n"),
                })
              }
            />
          </label>
          <label>
            Hướng dẫn giáo viên
            <textarea
              value={content.teacher_guide || ""}
              onChange={(e) =>
                setContent({ ...content, teacher_guide: e.target.value })
              }
            />
          </label>
          <label>
            Hình mở bài (mã media đã duyệt)
            <input
              value={content.hero}
              onChange={(e) => setContent({ ...content, hero: e.target.value })}
            />
          </label>
          {content.steps.map((s, index) => (
            <section key={s.id} className="academy-editor-step">
              <h3>
                Bước {index + 1} · {s.kind}
              </h3>
              <label>
                Tiêu đề bước
                <input
                  value={s.title}
                  onChange={(e) => changeStep(index, { title: e.target.value })}
                />
              </label>
              <label>
                Nội dung
                <textarea
                  value={s.text}
                  onChange={(e) => changeStep(index, { text: e.target.value })}
                />
              </label>
              <label>
                Mã hình (cách nhau bằng dấu phẩy)
                <input
                  value={s.media.join(", ")}
                  onChange={(e) =>
                    changeStep(index, {
                      media: e.target.value
                        .split(",")
                        .map((x) => x.trim())
                        .filter(Boolean),
                    })
                  }
                />
              </label>
              {s.questions.map((q, qi) => (
                <fieldset key={q.id}>
                  <legend>Câu {qi + 1}</legend>
                  <label>
                    Câu hỏi
                    <input
                      value={q.prompt}
                      onChange={(e) =>
                        changeStep(index, {
                          questions: s.questions.map((v, i) =>
                            i === qi ? { ...v, prompt: e.target.value } : v,
                          ),
                        })
                      }
                    />
                  </label>
                  <label>
                    Lựa chọn (mỗi dòng)
                    <textarea
                      value={q.options.join("\n")}
                      onChange={(e) =>
                        changeStep(index, {
                          questions: s.questions.map((v, i) =>
                            i === qi
                              ? { ...v, options: e.target.value.split("\n") }
                              : v,
                          ),
                        })
                      }
                    />
                  </label>
                  <label>
                    Đáp án đúng
                    <select
                      value={q.answer ?? 0}
                      onChange={(e) =>
                        changeStep(index, {
                          questions: s.questions.map((v, i) =>
                            i === qi
                              ? { ...v, answer: Number(e.target.value) }
                              : v,
                          ),
                        })
                      }
                    >
                      {q.options.map((o, i) => (
                        <option key={i} value={i}>
                          {o}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Giải thích
                    <textarea
                      value={q.explanation || ""}
                      onChange={(e) =>
                        changeStep(index, {
                          questions: s.questions.map((v, i) =>
                            i === qi
                              ? { ...v, explanation: e.target.value }
                              : v,
                          ),
                        })
                      }
                    />
                  </label>
                </fieldset>
              ))}
              {s.activity && (
                <>
                  <label>
                    Hướng dẫn hoạt động
                    <textarea
                      value={s.activity.instruction}
                      onChange={(e) =>
                        changeStep(index, {
                          activity: {
                            ...s.activity!,
                            instruction: e.target.value,
                          },
                        })
                      }
                    />
                  </label>
                  {s.activity.items.map((item, ii) => (
                    <label key={item.id}>
                      {item.text} · nhãn đúng
                      <select
                        value={item.answer}
                        onChange={(e) =>
                          changeStep(index, {
                            activity: {
                              ...s.activity!,
                              items: s.activity!.items.map((v, i) =>
                                i === ii ? { ...v, answer: e.target.value } : v,
                              ),
                            },
                          })
                        }
                      >
                        {s.activity!.choices.map((c) => (
                          <option key={c}>{c}</option>
                        ))}
                      </select>
                    </label>
                  ))}
                </>
              )}
              <div className="academy-actions">
                <button
                  className="button secondary small"
                  disabled={!index}
                  onClick={() => move(index, -1)}
                >
                  Đưa lên
                </button>
                <button
                  className="button secondary small"
                  disabled={index === content.steps.length - 1}
                  onClick={() => move(index, 1)}
                >
                  Đưa xuống
                </button>
              </div>
            </section>
          ))}
          <label>
            Hỗ trợ học sinh
            <textarea
              value={content.support}
              onChange={(e) =>
                setContent({ ...content, support: e.target.value })
              }
            />
          </label>
          <label>
            Thử thách nâng cao
            <textarea
              value={content.advanced}
              onChange={(e) =>
                setContent({ ...content, advanced: e.target.value })
              }
            />
          </label>
        </>
      )}
      <div className="academy-actions">
        <label>
          Thứ tự bài khi xuất bản
          <input
            aria-label="Thứ tự bài khi xuất bản"
            type="number"
            min={1}
            max={200}
            value={position}
            onChange={(e) => setPosition(Number(e.target.value))}
          />
        </label>
        <label>
          Chủ đề đích khi nhân bản
          <select
            aria-label="Chủ đề đích khi nhân bản"
            value={targetUnit}
            onChange={(e) => setTargetUnit(e.target.value)}
          >
            {units.data?.map((u) => (
              <option key={u.id} value={u.id}>
                {u.title}
              </option>
            ))}
          </select>
        </label>
        <label>
          Thứ tự bản sao
          <input
            aria-label="Thứ tự bản sao"
            type="number"
            min={1}
            max={200}
            value={copyPosition}
            onChange={(e) => setCopyPosition(Number(e.target.value))}
          />
        </label>
        <button className="button" disabled={busy} onClick={() => void save()}>
          Lưu phiên bản nháp
        </button>
        <button
          className="button secondary"
          disabled={busy}
          onClick={() => void save(true)}
        >
          Nhân bản bài
        </button>
        {[
          ["submit", "Gửi duyệt"],
          ["review", "Duyệt nội dung"],
          ["publish", "Xuất bản"],
          ["archive", "Ẩn bài"],
        ].map(([a, t]) => (
          <button
            className="button secondary"
            disabled={busy}
            key={a}
            onClick={() => void workflow(a)}
          >
            {t}
          </button>
        ))}
      </div>
      <p role="status">{message}</p>
    </section>
  );
}
