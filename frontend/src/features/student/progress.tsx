"use client";
import { dateLabel, percent } from "@/lib/api";
import type { Dashboard, Skill } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { Resource } from "@/features/student/shared";
import { Recommendations } from "@/features/student/dashboard";

export function ProgressPage() {
  return (
    <>
      <PageTitle
        eyebrow="HIỂU MÌNH ĐỂ HỌC TỐT HƠN"
        title="Cây năng lực của em"
        description="Kết quả được tính từ bài em đã nộp. Cần nhiều lần luyện tập để đánh giá vững hơn."
      />
      <Resource<Skill[]> path="/students/me/skills">
        {(skills) =>
          skills.length ? (
            <div className="two-columns">
              {skills.map((skill) => (
                <article className="panel skill-card" key={skill.skill_id}>
                  <span className="eyebrow">{skill.subject_name}</span>
                  <h2>{skill.name}</h2>
                  {skill.questions_attempted < 5 ? (
                    <p className="notice">Cần luyện tập thêm để đánh giá</p>
                  ) : (
                    <>
                      <strong className="skill-percent">
                        {percent(skill.mastery_score)}%
                      </strong>
                      <div
                        className="progress-track"
                        role="progressbar"
                        aria-label={skill.name}
                        aria-valuenow={percent(skill.mastery_score)}
                        aria-valuemin={0}
                        aria-valuemax={100}
                      >
                        <span
                          style={{ width: `${percent(skill.mastery_score)}%` }}
                        />
                      </div>
                    </>
                  )}
                  <p>
                    {skill.questions_attempted} câu đã thử ·{" "}
                    {skill.correct_count} câu đúng
                  </p>
                  <p>
                    Độ tin cậy: {percent(skill.confidence)}% · Gợi ý ôn:{" "}
                    {dateLabel(skill.next_review_at)}
                  </p>
                </article>
              ))}
            </div>
          ) : (
            <Empty>
              Cây năng lực sẽ có dữ liệu sau khi em nộp bài đầu tiên. Mình bắt
              đầu nhẹ nhàng nhé!
            </Empty>
          )
        }
      </Resource>
      <section className="panel section-title">
        <h2>Gợi ý bước tiếp theo</h2>
        <Resource<
          Dashboard["recommendations"]
        > path="/students/me/recommendations">
          {(items) =>
            items.length ? (
              <Recommendations items={items} />
            ) : (
              <Empty>
                Em có thể tiếp tục đọc bài học và quay lại luyện tập sau.
              </Empty>
            )
          }
        </Resource>
      </section>
    </>
  );
}
