"use client";
import Link from "next/link";
import { ArrowRight, Sprout } from "lucide-react";
import { dateLabel } from "@/lib/api";
import type { Answer, Result } from "@/lib/types";
import { PageTitle } from "@/components/ui";
import { Resource } from "@/features/student/shared";
import { GuidedText } from "@/components/guided-text";
import { QuestionPrompt } from "@/components/question-prompt";
import { hasAnswer } from "@/lib/answers";

export function renderAnswer(
  answer: Answer,
  content: Result["items"][number]["content"],
) {
  if (!hasAnswer(answer)) return "Chưa trả lời";
  if ("text" in answer) return answer.text;
  const ids =
    "option_id" in answer
      ? [answer.option_id]
      : "option_ids" in answer
        ? answer.option_ids
        : "ordered_ids" in answer
          ? answer.ordered_ids
          : [];
  return (
    ids
      .map(
        (id) => content.options?.find((option) => option.id === id)?.text || id,
      )
      .join("ordered_ids" in answer ? " → " : " · ") || "Chưa trả lời"
  );
}

// This component receives answer keys only from the authorized, submitted result.
// Never infer an answer from an explanation or show it in an active attempt.
export function ResultItemReview({
  item,
  grade,
}: {
  item: Result["items"][number];
  grade?: number;
}) {
  const key = item.grading;
  const ids =
    item.question_type === "single_choice"
      ? [key.correct_option_id]
      : item.question_type === "multiple_choice"
        ? key.correct_option_ids
        : item.question_type === "ordering"
          ? key.ordered_ids
          : null;
  const labels = Array.isArray(ids)
    ? ids.map((id) => item.content.options?.find((o) => o.id === id)?.text)
    : [];
  const accepted = Array.isArray(key.accepted_answers)
    ? key.accepted_answers.filter(
        (value): value is string => typeof value === "string",
      )
    : [];
  const expected =
    item.question_type === "fill_blank"
      ? accepted[0]
      : labels.length && labels.every((label) => typeof label === "string")
        ? labels.join(item.question_type === "ordering" ? " → " : " · ")
        : undefined;
  return (
    <details className="panel result-item" open={!item.is_correct}>
      <summary>
        <span className={`badge ${item.is_correct ? "success" : "warm"}`}>
          {item.is_correct ? "Đúng" : "Cùng ôn lại"}
        </span>
        <strong>Câu {item.position}</strong>
        <span>
          {item.score}/{item.points} điểm
        </span>
      </summary>
      <QuestionPrompt
        text={item.content.prompt}
        grade={grade}
        headingLevel={3}
      />
      <p>
        <strong>Em trả lời:</strong>{" "}
        {renderAnswer(item.student_answer, item.content)}
      </p>
      {expected && (
        <p className="notice">
          <strong>
            {item.question_type === "fill_blank"
              ? "Một đáp án đúng:"
              : "Đáp án đúng:"}
          </strong>{" "}
          {expected}
        </p>
      )}
      {item.question_type === "fill_blank" && accepted.length > 1 && (
        <details>
          <summary>Các cách trả lời được chấp nhận</summary>
          <ul>
            {accepted.map((value, i) => (
              <li key={i}>{value}</li>
            ))}
          </ul>
        </details>
      )}
      <div className="explanation">
        <strong>Cùng hiểu cách làm</strong>
        <GuidedText text={item.explanation.text} grade={grade} />
      </div>
    </details>
  );
}

export function ResultPage({ id }: { id: string }) {
  return (
    <Resource<Result> path={`/attempts/${id}/result`}>
      {(data) => (
        <>
          <PageTitle
            eyebrow="KẾT QUẢ LUYỆN TẬP"
            title="Mỗi lần thử là một lần tiến bộ!"
          />
          <section className="result-banner">
            <div className="score-circle">
              {data.total_score}
              <small>/ {data.max_score} điểm</small>
            </div>
            <div>
              <h2>Em đã hoàn thành bài luyện tập</h2>
              <p>
                {data.correct_count} câu đúng · {dateLabel(data.graded_at)}
              </p>
              <p>
                Đọc lời giải để hiểu điều đã làm tốt và điều mình có thể luyện
                thêm nhé.
              </p>
              <Link className="button" href="/student/progress">
                Xem cây năng lực <Sprout size={18} />
              </Link>
            </div>
          </section>
          <h2 className="section-title">Cùng xem lại từng câu</h2>
          {data.items.map((item) => (
            <ResultItemReview key={item.id} item={item} grade={data.grade} />
          ))}
          <Link className="button" href="/student/dashboard">
            Luyện tập tiếp <ArrowRight size={18} />
          </Link>
        </>
      )}
    </Resource>
  );
}
