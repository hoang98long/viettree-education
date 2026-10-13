"use client";
import type { LessonContent } from "@/lib/types";
export function ContentFields({
  value,
  content,
  busy,
}: {
  value: LessonContent;
  content: (patch: Partial<LessonContent>) => void;
  busy: boolean;
}) {
  return (
    <fieldset disabled={busy}>
      <legend>Nội dung và hướng dẫn học</legend>
      <label htmlFor="lesson-goals">
        Mục tiêu (mỗi dòng một ý, tối đa 5)
        <textarea
          id="lesson-goals"
          required
          value={(value.goals || []).join("\n")}
          onChange={(e) => content({ goals: e.target.value.split("\n") })}
        />
      </label>
      {value.blocks.map((block, i) => (
        <section className="panel studio-block" key={i}>
          <h3>Phần {i + 1}</h3>
          <label htmlFor={`block-type-${i}`}>
            Loại phần
            <select
              id={`block-type-${i}`}
              value={block.type}
              onChange={(e) =>
                content({
                  blocks: value.blocks.map((b, n) =>
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
                  blocks: value.blocks.map((b, n) =>
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
                  blocks: value.blocks.map((b, n) =>
                    n === i ? { ...b, text: e.target.value } : b,
                  ),
                })
              }
            />
          </label>
          <button
            className="button secondary"
            type="button"
            disabled={value.blocks.length <= 3}
            onClick={() =>
              content({
                blocks: value.blocks.filter((_, n) => n !== i),
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
        disabled={value.blocks.length >= 12}
        onClick={() =>
          content({
            blocks: [
              ...value.blocks,
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
          value={(value.hints || []).join("\n")}
          onChange={(e) => content({ hints: e.target.value.split("\n") })}
        />
      </label>
      <label htmlFor="lesson-free-hints">
        Số gợi ý miễn phí
        <select
          id="lesson-free-hints"
          value={value.free_hint_count ?? "all"}
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
          Ít nhất 1 gợi ý cơ bản khi phân bổ. Các gợi ý còn lại dành cho VIP; số
          miễn phí không được vượt tổng gợi ý đã nhập.
        </small>
      </label>
      <label htmlFor="lesson-reflection">
        Câu hỏi tự suy ngẫm (mỗi dòng một ý, tối đa 3)
        <textarea
          id="lesson-reflection"
          value={(value.reflection || []).join("\n")}
          onChange={(e) => content({ reflection: e.target.value.split("\n") })}
        />
      </label>
    </fieldset>
  );
}
