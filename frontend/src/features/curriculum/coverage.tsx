"use client";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading } from "@/components/ui";
import type { MapRow } from "@/features/curriculum/types";
import { subjects } from "@/features/curriculum/constants";
import { downloadCsv } from "@/lib/csv";

type ReleaseStatus = {
  release: string;
  title?: string;
  expected: { lessons: number; questions: number; assessments: number };
  published: { lessons: number; questions: number; assessments: number };
};

export function CurriculumMapPanel({ grade = 4 }: { grade?: number }) {
  const [subject, setSubject] = useState(""),
    [gaps, setGaps] = useState(false);
  const resource = useResource<{
    grade: number;
    rows: MapRow[];
    supplement?: ReleaseStatus;
    supplements?: ReleaseStatus[];
  }>(`/admin/curriculum-map?grade=${grade}`);
  const rows = (resource.data?.rows || []).filter(
    (row) =>
      (!subject || row.subject_code === subject) &&
      (!gaps || !row.active || !row.free_lessons),
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
        <button
          type="button"
          className="button secondary"
          disabled={resource.loading || !!resource.error || !rows.length}
          onClick={() =>
            downloadCsv(`viettree-hoc-lieu-lop-${grade}.csv`, [
              [
                "Khối",
                "Mã mạch",
                "Môn",
                "Tên mạch",
                "Cần phát triển",
                "Bài Free",
                "Bài VIP",
                "Chưa cấu hình quyền",
                "Câu hỏi",
                "Đề luyện tập",
                "Trạng thái",
                "Nguồn chương trình",
              ],
              ...rows.map((row) => [
                grade,
                row.code,
                row.subject_name,
                row.title,
                row.focus,
                row.free_lessons,
                row.vip_lessons,
                row.unconfigured_lessons,
                row.questions,
                row.assessments,
                row.active ? "Hoạt động" : "Chưa hoạt động",
                row.source_url,
              ]),
            ])
          }
        >
          Xuất học liệu CSV
        </button>
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
          {(
            resource.data.supplements ??
            (resource.data.supplement ? [resource.data.supplement] : [])
          ).map((release) => (
            <p
              key={release.release}
              className="notice"
              aria-label={
                release.release === "applied-2026-01"
                  ? "Học liệu tình huống bổ sung"
                  : "Học liệu khám phá bổ sung"
              }
            >
              <strong>
                {release.title || "Tình huống gần gũi"} · Lớp {grade}:
              </strong>{" "}
              {release.published.lessons}/{release.expected.lessons} bài ·{" "}
              {release.published.questions}/{release.expected.questions} câu hỏi
              · {release.published.assessments}/{release.expected.assessments}{" "}
              đề đã xuất bản.
            </p>
          ))}
          <p className="notice" aria-live="polite">
            {rows.length} mạch · {rows.reduce((n, r) => n + r.free_lessons, 0)}{" "}
            bài Free · {rows.reduce((n, r) => n + r.vip_lessons, 0)} bài VIP ·{" "}
            {rows.reduce((n, r) => n + r.questions, 0)} câu hỏi ·{" "}
            {rows.reduce((n, r) => n + r.assessments, 0)} đề. Số liệu theo bộ
            lọc đang chọn.
          </p>
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
                {rows.map((row) => (
                  <tr key={row.code}>
                    <td>
                      <strong>
                        {row.subject_name} · {row.title}
                      </strong>
                      <p>{row.focus}</p>
                      <a href={row.source_url} target="_blank" rel="noreferrer">
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
                          {row.unconfigured_lessons} bài chưa có quyền truy cập
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
