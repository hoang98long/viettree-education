"use client";
import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { Page } from "@/lib/types";
import type { ThinkingLesson } from "@/features/curriculum/types";
import { subjects } from "@/features/curriculum/constants";

export function ThinkingPage() {
  const [subject, setSubject] = useState(""),
    [page, setPage] = useState(1);
  const query = new URLSearchParams({
    page: String(page),
    ...(subject ? { subject_code: subject } : {}),
  });
  const resource = useResource<Page<ThinkingLesson> & { grade: number }>(
    `/students/me/thinking?${query}`,
  );
  return (
    <>
      <PageTitle
        title="Góc tư duy và đố mẹo"
        description="Đọc kỹ dữ kiện, thử giải thích cách nghĩ, rồi luyện tập. Có bài miễn phí và bài nâng cao VIP."
      />
      <p className="notice">
        Đố mẹo có điều kiện rõ ràng. Vẽ hình hoặc lập bảng trước khi tính; mở
        gợi ý trong bài khi cần. Em có thể học theo nhịp riêng.
      </p>
      <div className="filters">
        <label htmlFor="thinking-subject">
          Môn học
          <select
            id="thinking-subject"
            value={subject}
            onChange={(e) => {
              setSubject(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            {subjects.map(([code, name]) => (
              <option value={code} key={code}>
                {name}
              </option>
            ))}
          </select>
        </label>
      </div>
      {resource.loading ? (
        <Loading />
      ) : resource.error || !resource.data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <p className="muted">
            Lớp {resource.data.grade} · {resource.data.total} bài tư duy
          </p>
          {!resource.data.items.length ? (
            <Empty>
              Chưa có bài tư duy phù hợp với lựa chọn và lớp của em.
            </Empty>
          ) : (
            <div className="thinking-grid">
              {resource.data.items.map((item) => (
                <article className="panel" key={item.id}>
                  <div className="actions">
                    <span className="badge">{item.subject_name}</span>
                    <span className="badge">
                      {item.minimum_plan_code === "vip"
                        ? "VIP"
                        : item.minimum_plan_code === "free"
                          ? "Miễn phí"
                          : "Đang chuẩn bị"}
                    </span>
                  </div>
                  <h2>{item.title}</h2>
                  <p>
                    {item.estimated_minutes} phút đọc dự kiến
                    {item.progress_status === "completed"
                      ? " · Đã đọc xong"
                      : ""}
                  </p>
                  {item.locked ? (
                    <>
                      <p>
                        {item.lock_reason === "MEMBERSHIP_REQUIRED"
                          ? "Bài nâng cao dành cho tài khoản VIP."
                          : "Bài này đang được chuẩn bị."}
                      </p>
                      <Link
                        className="button secondary"
                        href={
                          item.lock_reason === "MEMBERSHIP_REQUIRED"
                            ? "/student/membership"
                            : "/student/grades"
                        }
                      >
                        {item.lock_reason === "MEMBERSHIP_REQUIRED"
                          ? "Xem gói học"
                          : "Khám phá bài khác"}
                      </Link>
                    </>
                  ) : (
                    <Link
                      className="button"
                      href={`/student/lessons/${item.id}`}
                    >
                      Khám phá bài
                    </Link>
                  )}
                </article>
              ))}
            </div>
          )}
          <div className="pagination">
            <span>
              Trang {page}/{Math.max(1, Math.ceil(resource.data.total / 20))}
            </span>
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage((n) => n - 1)}
            >
              Trang trước
            </button>
            <button
              className="button secondary"
              disabled={page * 20 >= resource.data.total}
              onClick={() => setPage((n) => n + 1)}
            >
              Trang sau
            </button>
          </div>
        </>
      )}
    </>
  );
}
