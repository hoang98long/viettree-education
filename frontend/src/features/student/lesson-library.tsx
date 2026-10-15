"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Lightbulb,
  RefreshCw,
  Search,
  Bookmark,
} from "lucide-react";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { useUser } from "@/components/shell";
import { useResource } from "@/hooks/use-resource";
import { AccessBadge } from "@/features/membership/pages";
import type { ContentAccess } from "@/lib/types";
import { BookmarkButton } from "@/features/lessons/bookmark-button";

type Library = {
  grade: number;
  page: number;
  page_size: number;
  summary: {
    total: number;
    completed: number;
    in_progress: number;
    free: number;
    vip: number;
    bookmarked: number;
  };
  items: (ContentAccess & {
    id: string;
    title: string;
    estimated_minutes: number | null;
    topic_title: string;
    subject_code: string;
    subject_name: string;
    progress_status: string;
    category: string;
    is_bookmarked: boolean;
  })[];
};

function LibraryContent({ savedOnly }: { savedOnly: boolean }) {
  const [bookmarkedOnly, setBookmarkedOnly] = useState(savedOnly);
  const [filters, setFilters] = useState({
    subject_code: "",
    plan: "all",
    progress: "all",
    category: "all",
    search: "",
  });
  const [draft, setDraft] = useState("");
  const [page, setPage] = useState(1);
  const query = new URLSearchParams({
    plan: filters.plan,
    progress: filters.progress,
    category: filters.category,
    search: filters.search,
    page: String(page),
    bookmarked_only: String(bookmarkedOnly),
  });
  if (filters.subject_code) query.set("subject_code", filters.subject_code);
  const resource = useResource<Library>(
    `/students/me/lesson-library?${query}`,
    true,
  );
  useEffect(() => {
    // A learner may open this page while the preceding completion is still saving.
    window.addEventListener("viettree:learning-progress", resource.retry);
    window.addEventListener("viettree:lesson-bookmarks", resource.retry);
    return () => {
      window.removeEventListener("viettree:learning-progress", resource.retry);
      window.removeEventListener("viettree:lesson-bookmarks", resource.retry);
    };
  }, [resource.retry]);
  const update = (key: keyof typeof filters, value: string) => {
    setFilters((old) => ({ ...old, [key]: value }));
    setPage(1);
  };
  const data = resource.data;
  if (data && !resource.loading) {
    const lastPage = Math.max(
      1,
      Math.ceil(data.summary.total / data.page_size),
    );
    // Removing the last saved card on a page can shrink the page count.
    if (page > lastPage) setPage(lastPage);
  }
  return (
    <>
      <PageTitle
        eyebrow={data ? `BÀI HỌC CỦA EM · LỚP ${data.grade}` : "BÀI HỌC CỦA EM"}
        title={bookmarkedOnly ? "Bài học đã lưu" : "Thư viện bài học"}
        description="Tìm bài, đọc theo nhịp của em và quay lại phần đang học. Tìm kiếm có thể nhập không dấu."
      />
      <section className="library-toolbar panel" aria-label="Bộ lọc bài học">
        <button
          type="button"
          className="button secondary library-saved-toggle"
          aria-pressed={bookmarkedOnly}
          onClick={() => {
            setBookmarkedOnly((old) => !old);
            setPage(1);
          }}
        >
          <Bookmark size={18} />
          Chỉ bài đã lưu
        </button>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            update("search", draft.trim());
          }}
          className="library-search"
        >
          <label htmlFor="lesson-search">Tên bài hoặc chủ đề</label>
          <div>
            <input
              id="lesson-search"
              value={draft}
              maxLength={80}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="Ví dụ: số thập phân, doc truyen..."
            />
            <button className="button">
              <Search size={18} />
              Tìm bài
            </button>
          </div>
        </form>
        <details className="library-filter-details">
          <summary>Chọn thêm bộ lọc</summary>
          <div className="library-filters">
            <label>
              Môn học
              <select
                value={filters.subject_code}
                onChange={(e) => update("subject_code", e.target.value)}
              >
                <option value="">Ba môn</option>
                <option value="MATH">Toán</option>
                <option value="VIETNAMESE">Tiếng Việt</option>
                <option value="ENGLISH">Tiếng Anh</option>
              </select>
            </label>
            <label>
              Gói bài học
              <select
                value={filters.plan}
                onChange={(e) => update("plan", e.target.value)}
              >
                <option value="all">Free và VIP</option>
                <option value="free">Miễn phí</option>
                <option value="vip">VIP</option>
              </select>
            </label>
            <label>
              Tiến độ đọc
              <select
                value={filters.progress}
                onChange={(e) => update("progress", e.target.value)}
              >
                <option value="all">Tất cả</option>
                <option value="not_started">Chưa đọc</option>
                <option value="in_progress">Đang đọc</option>
                <option value="completed">Đã đọc xong</option>
              </select>
            </label>
            <label>
              Nội dung
              <select
                value={filters.category}
                onChange={(e) => update("category", e.target.value)}
              >
                <option value="all">Tất cả bài</option>
                <option value="core">Nền tảng</option>
                <option value="thinking">Tư duy, vận dụng</option>
              </select>
            </label>
          </div>
        </details>
        <div className="library-actions">
          <button
            type="button"
            className="button secondary"
            onClick={() => {
              setFilters({
                subject_code: "",
                plan: "all",
                progress: "all",
                category: "all",
                search: "",
              });
              setDraft("");
              setBookmarkedOnly(savedOnly);
              setPage(1);
            }}
          >
            Xóa bộ lọc
          </button>
          <button
            type="button"
            className="button secondary"
            onClick={resource.retry}
          >
            <RefreshCw size={17} />
            Làm mới
          </button>
        </div>
      </section>
      {resource.loading && !data ? (
        <Loading />
      ) : resource.error || !data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <div className="library-summary" aria-live="polite">
            <strong>{data.summary.total} bài phù hợp</strong>
            <span>
              {data.summary.free} Free · {data.summary.vip} VIP
            </span>
            <span>
              {data.summary.completed} đã đọc xong · {data.summary.in_progress}{" "}
              đang đọc
              {" · "}
              {data.summary.bookmarked} đã lưu
            </span>
          </div>
          {!data.items.length ? (
            <Empty>
              Chưa có bài phù hợp. Em thử đổi từ khóa hoặc xóa bộ lọc nhé.
            </Empty>
          ) : (
            <div className="lesson-library-grid">
              {data.items.map((item) => (
                <article
                  className={`library-card ${item.subject_code.toLowerCase()}`}
                  key={item.id}
                >
                  <div className="library-card-top">
                    <span className="library-card-icon" aria-hidden>
                      {item.category === "thinking" ? (
                        <Lightbulb size={27} />
                      ) : (
                        <BookOpen size={27} />
                      )}
                    </span>
                    <AccessBadge item={item} />
                  </div>
                  <small>
                    {item.subject_name} · {item.topic_title}
                  </small>
                  <h2>{item.title}</h2>
                  <div className="library-card-meta">
                    <span>
                      <Clock size={17} />
                      {item.estimated_minutes || 12} phút
                    </span>
                    <span>
                      {item.progress_status === "completed" ? (
                        <>
                          <CheckCircle2 size={17} />
                          Đã đọc xong
                        </>
                      ) : item.progress_status === "in_progress" ? (
                        "Đang đọc"
                      ) : (
                        "Chưa đọc"
                      )}
                    </span>
                  </div>
                  <Link
                    className={`button ${item.locked ? "secondary" : ""}`}
                    href={`/student/lessons/${item.id}`}
                  >
                    {item.locked
                      ? "Xem giới thiệu"
                      : item.progress_status === "in_progress"
                        ? "Đọc tiếp"
                        : "Mở bài học"}
                  </Link>
                  <BookmarkButton
                    key={`${item.id}:${item.is_bookmarked}`}
                    lessonId={item.id}
                    initialSaved={item.is_bookmarked}
                    locked={item.locked}
                  />
                </article>
              ))}
            </div>
          )}
          <nav className="library-pagination" aria-label="Trang thư viện">
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Trang trước
            </button>
            <span>
              Trang {page}/
              {Math.max(1, Math.ceil(data.summary.total / data.page_size))}
            </span>
            <button
              className="button secondary"
              disabled={page * data.page_size >= data.summary.total}
              onClick={() => setPage((p) => p + 1)}
            >
              Trang sau
            </button>
          </nav>
          <p className="muted">
            Đánh dấu đọc xong ghi lại tiến độ đọc. Kết quả luyện tập giúp kiểm
            tra điều em hiểu.
          </p>
        </>
      )}
    </>
  );
}

export function LessonLibraryPage({
  savedOnly = false,
}: {
  savedOnly?: boolean;
}) {
  const user = useUser();
  return (
    <LibraryContent key={`${user.id}:${savedOnly}`} savedOnly={savedOnly} />
  );
}
