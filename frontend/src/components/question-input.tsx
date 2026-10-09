"use client";
import { ArrowDown, ArrowUp } from "lucide-react";
import type { Answer, AttemptItem } from "@/lib/types";

export function QuestionInput({
  item,
  answer,
  onChange,
  disabled = false,
}: {
  item: AttemptItem;
  answer: Answer | null;
  onChange: (answer: Answer) => void;
  disabled?: boolean;
}) {
  const options = item.content.options || [];
  if (item.question_type === "fill_blank")
    return (
      <label className="blank-answer">
        Câu trả lời của em
        <input
          disabled={disabled}
          value={answer && "text" in answer ? answer.text : ""}
          maxLength={500}
          onChange={(e) => onChange({ text: e.target.value })}
          autoComplete="off"
        />
      </label>
    );
  if (item.question_type === "ordering") {
    const ids =
      answer && "ordered_ids" in answer
        ? answer.ordered_ids
        : options.map((option) => option.id);
    function move(index: number, direction: number) {
      const reordered = [...ids];
      [reordered[index], reordered[index + direction]] = [
        reordered[index + direction],
        reordered[index],
      ];
      onChange({ ordered_ids: reordered });
    }
    return (
      <div className="ordering">
        <p className="muted">
          Dùng nút lên / xuống để sắp xếp. Em cũng có thể lưu thứ tự hiện tại.
        </p>
        {ids.map((id, index) => (
          <div className="order-item" key={id}>
            <span className="number-dot">{index + 1}</span>
            <span>{options.find((option) => option.id === id)?.text}</span>
            <button
              aria-label={`Đưa mục ${index + 1} lên`}
              disabled={disabled || index === 0}
              onClick={() => move(index, -1)}
            >
              <ArrowUp size={19} />
            </button>
            <button
              aria-label={`Đưa mục ${index + 1} xuống`}
              disabled={disabled || index === ids.length - 1}
              onClick={() => move(index, 1)}
            >
              <ArrowDown size={19} />
            </button>
          </div>
        ))}
        <button
          className="button secondary"
          disabled={disabled}
          onClick={() => onChange({ ordered_ids: ids })}
        >
          Chọn thứ tự hiện tại
        </button>
      </div>
    );
  }
  const isMultiple = item.question_type === "multiple_choice";
  const selected = answer && "option_ids" in answer ? answer.option_ids : [];
  return (
    <fieldset className="options">
      <legend>
        {isMultiple ? "Chọn tất cả đáp án phù hợp" : "Chọn một đáp án"}
      </legend>
      {options.map((option, index) => {
        const checked = isMultiple
          ? selected.includes(option.id)
          : Boolean(
              answer && "option_id" in answer && answer.option_id === option.id,
            );
        return (
          <label
            className={checked ? "option selected" : "option"}
            key={option.id}
          >
            <input
              type={isMultiple ? "checkbox" : "radio"}
              name={item.id}
              checked={checked}
              disabled={disabled}
              onChange={() =>
                onChange(
                  isMultiple
                    ? {
                        option_ids: checked
                          ? selected.filter((id) => id !== option.id)
                          : [...selected, option.id],
                      }
                    : { option_id: option.id },
                )
              }
            />
            <span className="option-letter">
              {String.fromCharCode(65 + index)}
            </span>
            <span>{option.text}</span>
          </label>
        );
      })}
    </fieldset>
  );
}
