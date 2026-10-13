"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { dateLabel } from "@/lib/api";
import type { History } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { Resource } from "@/features/student/shared";

export function HistoryPage() {
  const [subject, setSubject] = useState("");
  const [date, setDate] = useState("");
  const path = `/students/me/history?${new URLSearchParams({ ...(subject ? { subject_code: subject } : {}), ...(date ? { date } : {}) })}`;
  return (
    <>
      <PageTitle
        eyebrow="HÀNH TRÌNH CỦA EM"
        title="Lịch sử luyện tập"
        description="Bài đang làm và những lần thử sức đều được lưu ở đây."
      />
      <div className="filters">
        <label>
          Môn học
          <select value={subject} onChange={(e) => setSubject(e.target.value)}>
            <option value="">Tất cả môn</option>
            <option value="MATH">Toán</option>
            <option value="VIETNAMESE">Tiếng Việt</option>
            <option value="ENGLISH">Tiếng Anh</option>
          </select>
        </label>
        <label>
          Ngày
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
      </div>
      <Resource<History[]> key={path} path={path}>
        {(items) =>
          items.length ? (
            <section className="panel">
              {items.map((attempt) => (
                <Link
                  className="list-row"
                  key={attempt.id}
                  href={`/student/${attempt.status === "graded" ? "results" : "attempts"}/${attempt.id}`}
                >
                  <div>
                    <strong>{attempt.title}</strong>
                    <small>
                      {attempt.subject_name} · {dateLabel(attempt.started_at)}
                    </small>
                  </div>
                  <span className="badge">
                    {attempt.status === "graded"
                      ? `${attempt.total_score}/${attempt.max_score}`
                      : "Tiếp tục làm"}
                  </span>
                  <ArrowRight size={18} />
                </Link>
              ))}
            </section>
          ) : (
            <Empty>
              Chưa có bài luyện tập phù hợp bộ lọc này. Em hãy chọn một môn để
              bắt đầu nhé.
            </Empty>
          )
        }
      </Resource>
    </>
  );
}
