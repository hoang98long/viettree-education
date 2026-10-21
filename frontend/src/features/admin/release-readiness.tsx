"use client";

import { useState } from "react";
import { ErrorState, Loading } from "@/components/ui";
import { useResource } from "@/hooks/use-resource";
import { dateTimeLabel } from "@/lib/api";
import { downloadCsv } from "@/lib/csv";
import { ReadinessChecks } from "./readiness-checks";

type Counts = { lessons: number; questions: number; assessments: number };
export type ReleaseStatus = {
  status: "ok" | "attention";
  checked_at: string;
  checks: { code: string; label: string; ok: boolean; count: number | null }[];
  curriculum: {
    grade: number;
    subject_code: string;
    actual: Counts;
    minimum: Counts;
    ok: boolean;
  }[];
  academy: {
    baseline_published: number;
    baseline_required: number;
    issues: { code: string; reason: string }[];
  };
  media: { valid: boolean; assets: number | null };
  next_steps: { code: string; instruction: string }[];
};
const SUBJECTS: Record<string, string> = {
  MATH: "Toán",
  VIETNAMESE: "Tiếng Việt",
  ENGLISH: "Tiếng Anh",
};

function exportReport(report: ReleaseStatus) {
  downloadCsv("viettree-kiem-tra-truoc-trien-khai.csv", [
    ["Thời gian kiểm tra", dateTimeLabel(report.checked_at)],
    [
      "Kết quả",
      report.status === "ok" ? "Các kiểm tra tự động đạt" : "Cần xử lý",
    ],
    ["Hạng mục", "Trạng thái", "Số lượng"],
    ...report.checks.map((check) => [
      check.label,
      check.ok ? "Đạt" : "Cần xử lý",
      check.count ?? "",
    ]),
    [
      "Lớp",
      "Môn",
      "Bài",
      "Câu hỏi",
      "Đề",
      "Bài tối thiểu",
      "Câu tối thiểu",
      "Đề tối thiểu",
    ],
    ...report.curriculum.map((row) => [
      row.grade,
      SUBJECTS[row.subject_code] ?? row.subject_code,
      row.actual.lessons,
      row.actual.questions,
      row.actual.assessments,
      row.minimum.lessons,
      row.minimum.questions,
      row.minimum.assessments,
    ]),
    ["Bài AI đã xuất bản", report.academy.baseline_published],
    ["Bài AI yêu cầu", report.academy.baseline_required],
    [
      "SVG hợp lệ",
      report.media.valid ? (report.media.assets ?? "") : "Cần xử lý",
    ],
    ["Việc cần xử lý"],
    ...report.next_steps.map((step) => [step.instruction]),
  ]);
}

function ReleaseReport() {
  const report = useResource<ReleaseStatus>("/admin/release-status");
  return (
    <>
      <button
        className="button secondary"
        onClick={report.retry}
        disabled={report.loading}
      >
        Kiểm tra trước triển khai lại
      </button>
      {report.loading && <Loading />}
      {report.error && (
        <ErrorState message={report.error} retry={report.retry} />
      )}
      {report.data && (
        <>
          <h3>
            {report.data.status === "ok"
              ? "Các kiểm tra trước mở web đều đạt"
              : "Còn hạng mục trước khi mở web"}
          </h3>
          <p className="muted">
            Kiểm tra lúc {dateTimeLabel(report.data.checked_at)}.
          </p>
          <ReadinessChecks
            checks={report.data.checks}
            label="Các kiểm tra trước triển khai"
          />
          {!!report.data.next_steps.length && (
            <div>
              <h3>Việc cần xử lý</h3>
              <ul>
                {report.data.next_steps.map((step) => (
                  <li key={step.code}>{step.instruction}</li>
                ))}
              </ul>
            </div>
          )}
          <details>
            <summary>Số lượng học liệu theo khối và môn</summary>
            <p>
              Số tối thiểu là bộ nền tảng. Tổng thực tế có cả bài bổ sung và bài
              giáo viên đã xuất bản.
            </p>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Lớp</th>
                    <th>Môn</th>
                    <th>Bài / câu / đề thực tế</th>
                    <th>Tối thiểu</th>
                    <th>Kết quả</th>
                  </tr>
                </thead>
                <tbody>
                  {report.data.curriculum.map((row) => (
                    <tr key={`${row.grade}-${row.subject_code}`}>
                      <td>{row.grade}</td>
                      <td>{SUBJECTS[row.subject_code] ?? row.subject_code}</td>
                      <td>
                        {row.actual.lessons} / {row.actual.questions} /{" "}
                        {row.actual.assessments}
                      </td>
                      <td>
                        {row.minimum.lessons} / {row.minimum.questions} /{" "}
                        {row.minimum.assessments}
                      </td>
                      <td>{row.ok ? "Đạt" : "Cần xử lý"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
          <p>
            AI Academy: {report.data.academy.baseline_published}/
            {report.data.academy.baseline_required} bài nền tảng đã xuất bản ·{" "}
            {report.data.media.valid
              ? `${report.data.media.assets} SVG hợp lệ`
              : "Cần kiểm tra file minh họa"}
            .
          </p>
          <button
            className="button secondary"
            onClick={() => exportReport(report.data!)}
          >
            Tải biên bản kiểm tra (CSV)
          </button>
          <p>
            Đối chiếu thêm HTTPS, tên miền, sao lưu và phục hồi trên VPS trước
            khi mở công khai.
          </p>
        </>
      )}
    </>
  );
}

export function ReleaseReadinessSection() {
  const [opened, setOpened] = useState(false);
  return (
    <section
      className="panel section-title"
      aria-label="Kiểm tra trước khi mở web"
    >
      <h2>Trước khi mở web</h2>
      <p>
        Xem những việc cần xử lý, đối chiếu học liệu và tải biên bản cho lần
        triển khai.
      </p>
      {opened ? (
        <ReleaseReport />
      ) : (
        <button className="button secondary" onClick={() => setOpened(true)}>
          Kiểm tra trước khi mở web
        </button>
      )}
    </section>
  );
}
