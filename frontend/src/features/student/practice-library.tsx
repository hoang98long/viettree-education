"use client";

import Link from "next/link";
import { useState } from "react";
import {
  BookOpen,
  CheckCircle2,
  Lightbulb,
  RefreshCw,
  Search,
} from "lucide-react";
import { useResource } from "@/hooks/use-resource";
import { useUser } from "@/components/shell";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { AccessBadge } from "@/features/membership/pages";
import type { ContentAccess } from "@/lib/types";

type PracticeLibraryData = {
  grade: number;
  page: number;
  page_size: number;
  summary: {
    total: number;
    review: number;
    mastered: number;
    not_started: number;
  };
  items: (ContentAccess & {
    id: string;
    title: string;
    lesson_id: string | null;
    time_limit_seconds: number | null;
    assessment_type: string;
    subject_code: string;
    subject_name: string;
    topic_title: string | null;
    item_count: number;
    graded_count: number;
    best_percent: number | null;
    latest_percent: number | null;
    progress_status: "not_started" | "review" | "mastered";
  })[];
};

const initialFilters = {
  subject_code: "",
  plan: "all",
  progress: "all",
  max_questions: "",
  search: "",
  kind: "all",
};
const kindNames: Record<string, string> = {
  practice: "Luyện tập",
  homework: "Bài được giao",
  quiz: "Thử thách",
  test: "Kiểm tra",
  placement: "Khởi đầu",
  adaptive: "Theo năng lực",
};
const percent = (value: number) =>
  value.toLocaleString("vi-VN", { maximumFractionDigits: 2 });
const progressNames = {
  not_started: "Chưa nộp bài",
  review: "Ôn thêm nhé",
  mastered: "Đã đạt từ 80%",
};

function PracticeLibraryContent() {
  const [filters, setFilters] = useState(initialFilters);
  const [draft, setDraft] = useState("");
  const [page, setPage] = useState(1);
  const query = new URLSearchParams({
    plan: filters.plan,
    progress: filters.progress,
    search: filters.search,
    page: String(page),
    kind: filters.kind,
  });
  if (filters.subject_code) query.set("subject_code", filters.subject_code);
  if (filters.max_questions) query.set("max_questions", filters.max_questions);
  const resource = useResource<PracticeLibraryData>(
    `/students/me/practice-library?${query}`,
  );
  const data = resource.data;
  const update = (key: keyof typeof filters, value: string) => {
    setFilters((old) => ({ ...old, [key]: value }));
    setPage(1);
  };
  return (
    <>
      <PageTitle
        eyebrow={data ? `LUYỆN TẬP · LỚP ${data.grade}` : "LUYỆN TẬP"}
        title="Thư viện luyện tập của em"
        description="Chọn một bài ngắn hoặc ôn lại phần cần luyện thêm. Tìm kiếm có thể nhập không dấu."
      />
      <section className="library-toolbar panel" aria-label="Bộ lọc luyện tập">
        <form
          className="library-search"
          onSubmit={(event) => {
            event.preventDefault();
            update("search", draft.trim());
          }}
        >
          <label htmlFor="practice-search">Tên bài hoặc chủ đề</label>
          <div>
            <input
              id="practice-search"
              maxLength={80}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Ví dụ: chia but, thư viện..."
            />
            <button className="button">
              <Search size={18} />
              Tìm bài
            </button>
          </div>
        </form>
        <div
          className="library-actions practice-shortcuts"
          aria-label="Chọn nhanh bài luyện"
        >
          <button
            type="button"
            className="button secondary"
            aria-pressed={filters.max_questions === "6"}
            onClick={() =>
              update("max_questions", filters.max_questions === "6" ? "" : "6")
            }
          >
            Bài ngắn
          </button>
          <button
            type="button"
            className="button secondary"
            aria-pressed={filters.progress === "not_started"}
            onClick={() =>
              update(
                "progress",
                filters.progress === "not_started" ? "all" : "not_started",
              )
            }
          >
            Chưa nộp
          </button>
          <button
            type="button"
            className="button secondary"
            aria-pressed={filters.progress === "review"}
            onClick={() =>
              update(
                "progress",
                filters.progress === "review" ? "all" : "review",
              )
            }
          >
            Ôn thêm
          </button>
        </div>
        <details className="practice-filter-details">
          <summary>Chọn thêm bộ lọc</summary>
          <div className="library-filters practice-filters">
            <label>
              Môn luyện tập
              <select
                value={filters.subject_code}
                onChange={(event) => update("subject_code", event.target.value)}
              >
                <option value="">Ba môn</option>
                <option value="MATH">Toán</option>
                <option value="VIETNAMESE">Tiếng Việt</option>
                <option value="ENGLISH">Tiếng Anh</option>
              </select>
            </label>
            <label>
              Gói bài luyện
              <select
                value={filters.plan}
                onChange={(event) => update("plan", event.target.value)}
              >
                <option value="all">Free và VIP</option>
                <option value="free">Miễn phí</option>
                <option value="vip">VIP</option>
              </select>
            </label>
            <label>
              Kết quả gần nhất
              <select
                value={filters.progress}
                onChange={(event) => update("progress", event.target.value)}
              >
                <option value="all">Tất cả</option>
                <option value="not_started">Chưa nộp bài</option>
                <option value="review">Cần ôn thêm (dưới 80%)</option>
                <option value="mastered">Đã đạt từ 80%</option>
              </select>
            </label>
            <label>
              Độ dài bài
              <select
                value={filters.max_questions}
                onChange={(event) =>
                  update("max_questions", event.target.value)
                }
              >
                <option value="">Tất cả độ dài</option>
                <option value="4">Tối đa 4 câu</option>
                <option value="6">Tối đa 6 câu</option>
                <option value="8">Tối đa 8 câu</option>
              </select>
            </label>
            <label>
              Loại bài luyện
              <select
                value={filters.kind}
                onChange={(event) => update("kind", event.target.value)}
              >
                <option value="all">Tất cả loại bài</option>
                {Object.entries(kindNames).map(([code, name]) => (
                  <option key={code} value={code}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </details>
        <div className="library-actions">
          <button
            className="button secondary"
            type="button"
            onClick={() => {
              setFilters(initialFilters);
              setDraft("");
              setPage(1);
            }}
          >
            Xóa bộ lọc
          </button>
          <button
            className="button secondary"
            type="button"
            onClick={resource.retry}
          >
            <RefreshCw size={17} />
            Làm mới
          </button>
        </div>
      </section>
      {resource.loading ? (
        <Loading />
      ) : resource.error || !data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <div className="library-summary" aria-live="polite">
            <strong>{data.summary.total} bài luyện phù hợp</strong>
            <span>
              {data.summary.not_started} chưa nộp · {data.summary.review} cần ôn
              thêm · {data.summary.mastered} đạt từ 80%
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
                  key={item.id}
                  className={`library-card ${item.subject_code.toLowerCase()}`}
                >
                  <div className="library-card-top">
                    <span className="library-card-icon" aria-hidden>
                      {item.progress_status === "mastered" ? (
                        <CheckCircle2 size={27} />
                      ) : (
                        <Lightbulb size={27} />
                      )}
                    </span>
                    <AccessBadge item={item} />
                  </div>
                  <small>
                    {item.subject_name}
                    {item.topic_title ? ` · ${item.topic_title}` : ""}
                  </small>
                  <h2>{item.title}</h2>
                  <div className="library-card-meta">
                    <span>
                      {item.item_count} câu ·{" "}
                      {kindNames[item.assessment_type] || "Luyện tập"}
                    </span>
                    <span>{progressNames[item.progress_status]}</span>
                  </div>
                  {item.best_percent !== null && (
                    <p>
                      Tốt nhất: <strong>{percent(item.best_percent)}%</strong> ·
                      Gần nhất:{" "}
                      {item.latest_percent === null
                        ? "Chưa có"
                        : `${percent(item.latest_percent)}%`}
                    </p>
                  )}
                  {item.time_limit_seconds && (
                    <small>
                      Giới hạn {Math.ceil(item.time_limit_seconds / 60)} phút
                    </small>
                  )}
                  <Link
                    className={`button ${item.locked ? "secondary" : ""}`}
                    href={`/student/assessments/${item.id}`}
                  >
                    {item.locked
                      ? "Xem giới thiệu"
                      : item.graded_count
                        ? "Luyện lại"
                        : "Mở bài luyện tập"}
                  </Link>
                  {item.lesson_id && !item.locked && (
                    <Link
                      className="card-link"
                      href={`/student/lessons/${item.lesson_id}`}
                    >
                      <BookOpen size={17} aria-hidden /> Xem bài học và gợi ý
                    </Link>
                  )}
                </article>
              ))}
            </div>
          )}
          <nav className="library-pagination" aria-label="Trang luyện tập">
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage((old) => old - 1)}
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
              onClick={() => setPage((old) => old + 1)}
            >
              Trang sau
            </button>
          </nav>
          <p className="muted">
            “Cần ôn thêm” dựa trên lần nộp đã chấm gần nhất dưới 80%. Em có thể
            đọc lại bài học rồi thử tiếp theo nhịp của mình.
          </p>
        </>
      )}
    </>
  );
}

export function PracticeLibrary() {
  const user = useUser();
  return <PracticeLibraryContent key={user.id} />;
}
