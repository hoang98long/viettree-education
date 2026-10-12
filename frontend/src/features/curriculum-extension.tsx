"use client";

import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type { ContentAccess, Page } from "@/lib/types";

type ThinkingLesson = ContentAccess & {
  id: string;
  title: string;
  subject_code: string;
  subject_name: string;
  estimated_minutes: number;
  progress_status: string | null;
};
type MapRow = {
  code: string;
  subject_code: string;
  subject_name: string;
  title: string;
  focus: string;
  active: boolean;
  free_lessons: number;
  vip_lessons: number;
  unconfigured_lessons: number;
  questions: number;
  assessments: number;
  source_url: string;
};
const subjects = [
  ["MATH", "Toán"],
  ["VIETNAMESE", "Tiếng Việt"],
  ["ENGLISH", "Tiếng Anh"],
];

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

export function CurriculumMapPanel({ grade = 4 }: { grade?: number }) {
  const [subject, setSubject] = useState(""),
    [gaps, setGaps] = useState(false);
  const resource = useResource<{ grade: number; rows: MapRow[] }>(
    `/admin/curriculum-map?grade=${grade}`,
  );
  return (
    <section className="panel section-title">
      <h2>Theo dõi học liệu lớp {grade}</h2>
      <p>
        Số liệu bài đã xuất bản theo mạch nội dung của 3 môn đang triển khai. Có
        bài trong một mạch chưa có nghĩa đã đáp ứng toàn bộ yêu cầu chương
        trình; xem phần cần bổ sung và tài liệu gốc.
      </p>
      <div className="filters">
        <label htmlFor="map-subject">
          Môn trong bảng học liệu
          <select
            id="map-subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          >
            <option value="">Tất cả</option>
            {subjects.map(([code, name]) => (
              <option value={code} key={code}>
                {name}
              </option>
            ))}
          </select>
        </label>
        <label className="check-label">
          <input
            type="checkbox"
            checked={gaps}
            onChange={(e) => setGaps(e.target.checked)}
          />
          Chỉ mạch chưa có bài miễn phí khả dụng
        </label>
      </div>
      {resource.loading ? (
        <Loading />
      ) : resource.error || !resource.data ? (
        <ErrorState message={resource.error} retry={resource.retry} />
      ) : (
        <>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Mạch và nội dung cần phát triển</th>
                  <th>Free</th>
                  <th>VIP</th>
                  <th>Câu hỏi</th>
                  <th>Bài tập</th>
                  <th>Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                {resource.data.rows
                  .filter(
                    (row) =>
                      (!subject || row.subject_code === subject) &&
                      (!gaps || !row.active || !row.free_lessons),
                  )
                  .map((row) => (
                    <tr key={row.code}>
                      <td>
                        <strong>
                          {row.subject_name} · {row.title}
                        </strong>
                        <p>{row.focus}</p>
                        <a
                          href={row.source_url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          Chương trình môn học
                        </a>
                      </td>
                      <td>{row.free_lessons}</td>
                      <td>{row.vip_lessons}</td>
                      <td>{row.questions}</td>
                      <td>{row.assessments}</td>
                      <td>
                        {!row.active
                          ? "Chưa có chủ đề hoạt động"
                          : !row.free_lessons
                            ? "Cần bài miễn phí"
                            : "Có học liệu"}
                        {row.unconfigured_lessons > 0 && (
                          <p className="notice error">
                            {row.unconfigured_lessons} bài chưa có quyền truy
                            cập
                          </p>
                        )}
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
          <p className="muted">
            Bảng đếm câu hỏi riêng biệt, không cộng trùng các phiên bản. Nội
            dung nháp chưa được tính. Chọn Biên soạn ở danh sách bên dưới để
            tiếp tục hoàn thiện bài; bài nghe/nói và văn mở cần người hướng dẫn.
          </p>
        </>
      )}
    </section>
  );
}
