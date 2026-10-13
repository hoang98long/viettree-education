"use client";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Statistics } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { Data } from "@/features/admin/shared";

export function AdminDashboard({ analytics = false }: { analytics?: boolean }) {
  return (
    <>
      <PageTitle
        eyebrow="VIETTREE · QUẢN TRỊ"
        title={analytics ? "Thống kê học tập" : "Tổng quan hệ thống"}
        description="Số liệu từ database hiện tại, cập nhật sau mỗi bài đã chấm."
      />
      <Data<Statistics> path="/admin/statistics">
        {(data) => (
          <>
            <div className="admin-stats">
              {[
                ["Học sinh", data.students],
                ["Bài học đã xuất bản", data.lessons],
                ["Câu hỏi đã xuất bản", data.question_versions],
                ["Đề đã xuất bản", data.assessments],
                ["Lượt làm đã chấm", data.attempts],
                [
                  "Điểm trung bình",
                  data.average_percent === null
                    ? "Chưa có"
                    : `${Math.round(data.average_percent)}%`,
                ],
              ].map(([label, value]) => (
                <article className="panel" key={String(label)}>
                  <span className="muted">{label}</span>
                  <strong>{value}</strong>
                </article>
              ))}
            </div>
            {!data.attempts ? (
              <Empty>
                Chưa có bài đã nộp. Điểm và thống kê học tập sẽ xuất hiện khi
                học sinh luyện tập.
              </Empty>
            ) : (
              <section className="panel">
                <h2>Hoạt động đã ghi nhận</h2>
                <p>
                  {data.attempts} bài đã chấm · {data.correct_answers} câu trả
                  lời đúng.
                </p>
                <p>
                  Các thống kê tổng hợp có thể rebuild từ attempts và
                  attempt_answers.
                </p>
              </section>
            )}
          </>
        )}
      </Data>
      {!analytics && (
        <div className="three-columns section-title">
          {[
            ["students", "Học sinh", "Xem và cập nhật hồ sơ tối thiểu."],
            [
              "curriculum",
              "Chương trình lớp 1–5",
              "Xem chủ đề, bài học và kỹ năng.",
            ],
            [
              "questions",
              "Ngân hàng câu hỏi",
              "Xem nội dung và lời giải đã seed.",
            ],
          ].map(([path, title, description]) => (
            <Link
              className="panel practice-card"
              href={`/admin/${path}`}
              key={path}
            >
              <h3>{title}</h3>
              <p>{description}</p>
              <span className="card-link">
                Mở <ArrowRight size={17} />
              </span>
            </Link>
          ))}
        </div>
      )}
    </>
  );
}
