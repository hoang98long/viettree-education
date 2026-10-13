"use client";

import Link from "next/link";
import { ErrorState, Loading, PageTitle } from "@/components/ui";
import { useResource } from "@/hooks/use-resource";
import { dateTimeLabel } from "@/lib/api";

type SystemStatus = {
  status: "ok" | "attention";
  checked_at: string;
  environment: "development" | "test" | "production";
  migrations: { current: string[]; expected: string[] };
  session: { hours: number; remember_days: number };
  checks: { code: string; label: string; ok: boolean; count: number | null }[];
  cleanup: {
    retention_days: number;
    counts: { auth_sessions: number; auth_login_limits: number };
  };
};

export function SystemStatusPage() {
  const { data, error, loading, retry } = useResource<SystemStatus>(
    "/admin/system-status",
  );
  return (
    <>
      <PageTitle
        title="Kiểm tra hệ thống"
        description="Kiểm tra dữ liệu vận hành và các quyền nội dung trước khi mở lớp học."
      />
      <button className="button secondary" onClick={retry} disabled={loading}>
        Kiểm tra lại
      </button>
      {error && <ErrorState message={error} retry={retry} />}
      {loading && <Loading />}
      {data && (
        <>
          <section
            className="panel section-title"
            aria-label="Kết quả kiểm tra hệ thống"
          >
            <h2>
              {data.status === "ok"
                ? "Các kiểm tra dữ liệu đều đạt"
                : "Có hạng mục cần xử lý"}
            </h2>
            <p className="muted">
              Kiểm tra lúc {dateTimeLabel(data.checked_at)} · Môi trường{" "}
              {data.environment === "production"
                ? "triển khai thực tế"
                : "phát triển / kiểm thử"}
            </p>
            <p>
              Phiên đăng nhập {data.session.hours} giờ; ghi nhớ học sinh{" "}
              {data.session.remember_days} ngày.
            </p>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Hạng mục</th>
                    <th>Kết quả</th>
                  </tr>
                </thead>
                <tbody>
                  {data.checks.map((check) => (
                    <tr key={check.code}>
                      <td>{check.label}</td>
                      <td>
                        {check.ok ? "Đạt" : "Cần xử lý"}
                        {check.count !== null ? ` · ${check.count}` : ""}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p>
              Migration hiện tại:{" "}
              {data.migrations.current.join(", ") || "Chưa có"}.
            </p>
            <p>Migration yêu cầu: {data.migrations.expected.join(", ")}.</p>
            <Link className="button secondary" href="/admin/content-access">
              Kiểm tra quyền nội dung
            </Link>
          </section>
          <section className="panel section-title">
            <h2>Bảo trì phiên đăng nhập</h2>
            <p>
              Có {data.cleanup.counts.auth_sessions} phiên cũ và{" "}
              {data.cleanup.counts.auth_login_limits} cửa sổ giới hạn đăng nhập
              quá {data.cleanup.retention_days} ngày có thể dọn.
            </p>
            <p>
              Màn hình này chỉ kiểm tra. Người vận hành thực hiện bảo trì bằng
              công cụ server theo lịch sao lưu.
            </p>
            <p>
              Trạng thái đạt cần được kết hợp với kiểm tra HTTPS, sao lưu, phục
              hồi và thử đăng nhập/học trên server thật trước khi đưa vào sử
              dụng.
            </p>
          </section>
        </>
      )}
    </>
  );
}
