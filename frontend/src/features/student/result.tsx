"use client";
import Link from "next/link";
import { ArrowRight, Sprout } from "lucide-react";
import { dateLabel } from "@/lib/api";
import type { Answer, Result } from "@/lib/types";
import { PageTitle } from "@/components/ui";
import { Resource } from "@/features/student/shared";

export function renderAnswer(
  answer: Answer,
  content: Result["items"][number]["content"],
) {
  if ("text" in answer) return answer.text || "Chưa trả lời";
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
      .join(" · ") || "Chưa trả lời"
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
            <details
              className="panel result-item"
              key={item.id}
              open={!item.is_correct}
            >
              <summary>
                <span
                  className={`badge ${item.is_correct ? "success" : "warm"}`}
                >
                  {item.is_correct ? "Đúng" : "Cùng ôn lại"}
                </span>
                <strong>Câu {item.position}</strong>
                <span>
                  {item.score}/{item.points} điểm
                </span>
              </summary>
              <h3 className="question-prompt">{item.content.prompt}</h3>
              <p>
                <strong>Em trả lời:</strong>{" "}
                {renderAnswer(item.student_answer, item.content)}
              </p>
              <div className="explanation">
                <strong>Lời giải</strong>
                <p>{item.explanation.text}</p>
              </div>
            </details>
          ))}
          <Link className="button" href="/student/dashboard">
            Luyện tập tiếp <ArrowRight size={18} />
          </Link>
        </>
      )}
    </Resource>
  );
}
