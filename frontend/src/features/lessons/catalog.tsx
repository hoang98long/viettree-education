"use client";
import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { Page } from "@/lib/types";
import type { Summary } from "@/features/lessons/types";
import { statusLabels } from "@/features/lessons/constants";

export function LessonsAdminPage() {
  const [grade, setGrade] = useState(4),
    [subject, setSubject] = useState(""),
    [status, setStatus] = useState(""),
    [search, setSearch] = useState(""),
    [page, setPage] = useState(1);
  const query = new URLSearchParams({
    grade: String(grade),
    page: String(page),
    search,
    ...(subject ? { subject_code: subject } : {}),
    ...(status ? { status } : {}),
  });
  const resource = useResource<Page<Summary>>(`/admin/lessons?${query}`);
  return (
    <>
      <PageTitle
        title="Quản lý bài học"
        description="Biên soạn, xem trước, duyệt và xuất bản. Bản nháp tách khỏi nội dung học sinh đang đọc."
      />
      <Link className="button" href="/admin/lessons/new">
        Tạo bài học
      </Link>
      <div className="filters section-title">
        <label htmlFor="studio-grade">
          Lớp
          <select
            id="studio-grade"
            value={grade}
            onChange={(e) => {
              setGrade(Number(e.target.value));
              setPage(1);
            }}
          >
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                Lớp {n}
              </option>
            ))}
          </select>
        </label>
        <label htmlFor="studio-subject">
          Lọc môn
          <select
            id="studio-subject"
            value={subject}
            onChange={(e) => {
              setSubject(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả môn</option>
            <option value="MATH">Toán</option>
            <option value="VIETNAMESE">Tiếng Việt</option>
            <option value="ENGLISH">Tiếng Anh</option>
          </select>
        </label>
        <label htmlFor="studio-status">
          Trạng thái bài học
          <select
            id="studio-status"
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            <option value="pending">Có nháp cần xử lý</option>
            <option value="published">Đã xuất bản</option>
            <option value="draft">Chưa xuất bản</option>
          </select>
        </label>
        <label htmlFor="studio-search">
          Tìm bài học
          <input
            id="studio-search"
            value={search}
            maxLength={120}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Tên hoặc mã bài"
          />
        </label>
      </div>
      {resource.loading ? (
        <Loading />
      ) : resource.error || !resource.data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <p>
            {resource.data.total} bài · Trang {page}
          </p>
          {resource.data.items.length ? (
            <div className="two-columns">
              {resource.data.items.map((item) => (
                <article className="panel studio-card" key={item.id}>
                  <span className="eyebrow">
                    {item.subject_name} ·{" "}
                    {item.minimum_plan_code?.toUpperCase() || "Chưa xuất bản"}
                  </span>
                  <h2>{item.title}</h2>
                  <p>{item.topic_title}</p>
                  <p>
                    {statusLabels[item.status]} · Bản soạn:{" "}
                    {statusLabels[item.draft_status || "none"]}
                  </p>
                  <Link
                    className="button secondary"
                    href={`/admin/lessons/${item.id}/edit`}
                  >
                    Biên soạn bài học
                  </Link>
                </article>
              ))}
            </div>
          ) : (
            <Empty>
              Chưa có bài phù hợp. Thử đổi bộ lọc hoặc tạo bài trong chủ đề đã
              có.
            </Empty>
          )}
          <div className="pagination">
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Trang trước
            </button>
            <button
              className="button secondary"
              disabled={page * 20 >= resource.data.total}
              onClick={() => setPage((p) => p + 1)}
            >
              Trang sau
            </button>
          </div>
        </>
      )}
    </>
  );
}
