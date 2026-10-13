"use client";
import Link from "next/link";
import { ArrowRight, BookOpen, Check, Sprout } from "lucide-react";
import { dateLabel } from "@/lib/api";
import type { Dashboard } from "@/lib/types";
import { Empty, SubjectCards, TreeArt } from "@/components/ui";
import { Resource } from "@/features/student/shared";

export function Recommendations({
  items,
}: {
  items: Dashboard["recommendations"];
}) {
  return (
    <div className="recommendations">
      {items.map((item, index) => (
        <Link
          href={`/student/assessments/${item.assessment_id}`}
          className="recommendation"
          key={item.assessment_id}
        >
          <span className="number-dot">{index + 1}</span>
          <div>
            <h3>{item.title}</h3>
            <p>{item.explanation}</p>
          </div>
          <ArrowRight size={20} />
        </Link>
      ))}
    </div>
  );
}

export function StudentDashboard() {
  return (
    <Resource<Dashboard> path="/students/me/dashboard">
      {(data) => {
        const completed = data.history.filter(
          (attempt) => attempt.status === "graded",
        );
        const active = data.history.find(
          (attempt) => attempt.status === "in_progress",
        );
        return (
          <>
            <div className="welcome-card">
              <div>
                <span className="eyebrow">GÓC HỌC TẬP · LỚP {data.grade}</span>
                <h1>
                  Chào {data.user.display_name}! <span>🌱</span>
                </h1>
                <p>
                  Mỗi bước nhỏ đều giúp em lớn lên.
                  <br />
                  Hôm nay mình cùng khám phá điều mới nhé.
                </p>
                <Link
                  className="button"
                  href={
                    active
                      ? `/student/attempts/${active.id}`
                      : data.continue_lesson
                        ? `/student/lessons/${data.continue_lesson.id}`
                        : `/student/grades?grade=${data.grade}`
                  }
                >
                  <BookOpen size={18} />
                  {active || data.continue_lesson
                    ? "Học tiếp"
                    : "Khám phá bài học"}
                </Link>
              </div>
              <TreeArt />
            </div>
            <div className="stats-grid">
              <div className="stat">
                <span className="stat-icon green">
                  <Check />
                </span>
                <div>
                  <strong>{completed.length}</strong>
                  <span>Bài luyện tập đã nộp</span>
                </div>
              </div>
              <div className="stat">
                <span className="stat-icon blue">
                  <BookOpen />
                </span>
                <div>
                  <strong>{data.completed_lessons}</strong>
                  <span>Bài học đã hoàn thành</span>
                </div>
              </div>
              <div className="stat">
                <span className="stat-icon orange">
                  <Sprout />
                </span>
                <div>
                  <strong>{data.skills.length}</strong>
                  <span>Kỹ năng đã thử sức</span>
                </div>
              </div>
            </div>
            <section className="panel plan-shortcut">
              <div>
                <h2>Từng bước nhỏ trong tuần này</h2>
                <p>Chọn môn, đọc bài và luyện tập theo kế hoạch của em.</p>
              </div>
              <Link className="button" href="/student/learning-plan">
                Kế hoạch học của em <ArrowRight size={18} />
              </Link>
            </section>
            <div className="section-heading">
              <div>
                <span className="eyebrow">CHỌN ĐIỀU EM MUỐN HỌC</span>
                <h2>Vườn kiến thức của em</h2>
              </div>
              <Link href="/student/grades">
                Xem các lớp <ArrowRight size={17} />
              </Link>
            </div>
            <SubjectCards
              subjects={data.subjects.filter((subject) =>
                ["MATH", "VIETNAMESE", "ENGLISH"].includes(subject.code),
              )}
            />
            <Link className="panel library-entry" href="/student/lessons">
              <BookOpen size={28} />
              <div>
                <h2>Tìm một bài học cho hôm nay</h2>
                <p>Chọn môn, Free/VIP hoặc bài đang đọc để học tiếp.</p>
              </div>
              <ArrowRight size={22} />
            </Link>
            <div className="two-columns">
              <section className="panel">
                <div className="section-heading">
                  <h2>Nhiệm vụ hôm nay</h2>
                  <span className="pill">
                    <Sprout size={14} /> Gợi ý cho em
                  </span>
                </div>
                {data.recommendations.length ? (
                  <Recommendations items={data.recommendations} />
                ) : (
                  <Empty>
                    Em đã luyện tập nhiều hôm nay. Hãy đọc bài học hoặc nghỉ
                    ngơi một chút nhé.
                  </Empty>
                )}
                {data.assignments
                  .filter((assignment) =>
                    ["assigned", "in_progress"].includes(assignment.status),
                  )
                  .map((assignment) => (
                    <Link
                      className="list-row"
                      key={assignment.id}
                      href={`/student/assessments/${assignment.assessment_id}?assignment_id=${assignment.id}`}
                    >
                      {assignment.title}
                      <span className="badge">Được giao</span>
                    </Link>
                  ))}
              </section>
              <section className="panel">
                <div className="section-heading">
                  <h2>Hoạt động gần đây</h2>
                  <Link href="/student/history">Xem tất cả</Link>
                </div>
                {data.history.length ? (
                  data.history.slice(0, 4).map((attempt) => (
                    <Link
                      className="list-row"
                      href={`/student/${attempt.status === "graded" ? "results" : "attempts"}/${attempt.id}`}
                      key={attempt.id}
                    >
                      <div>
                        <strong>{attempt.title}</strong>
                        <small>{dateLabel(attempt.started_at)}</small>
                      </div>
                      <span className="badge">
                        {attempt.status === "graded"
                          ? `${attempt.total_score}/${attempt.max_score}`
                          : "Đang làm"}
                      </span>
                    </Link>
                  ))
                ) : (
                  <Empty>
                    Chưa có bài luyện tập. Chọn một môn và bắt đầu, kết quả của
                    em sẽ được lưu ở đây.
                  </Empty>
                )}
              </section>
            </div>
          </>
        );
      }}
    </Resource>
  );
}
