"use client";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { Crown, LockKeyhole } from "lucide-react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import type {
  ContentAccess,
  Membership,
  MembershipPlan,
  LessonPreview,
} from "@/lib/types";

const featureLabels: Record<string, string> = {
  "learning.basic": "Bài học nền tảng",
  "practice.basic": "Luyện tập, chấm điểm và lời giải",
  "results.own": "Lịch sử và kết quả của em",
  "skills.own": "Cây năng lực",
  "learning_plan.basic": "Kế hoạch học 7 ngày",
  "accessibility.text_size": "Cỡ chữ dễ đọc",
  "learning.advanced": "Bài học nâng cao",
  "practice.advanced": "Luyện tập nâng cao",
  "practice.challenge": "Thử thách theo chủ đề",
  "learning_plan.adaptive": "Kế hoạch theo kỹ năng cần ôn",
};
export function membershipTime(value: string | null) {
  return value
    ? new Intl.DateTimeFormat("vi-VN", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Bangkok",
      }).format(new Date(value))
    : "—";
}
export function useMembership() {
  const resource = useResource<Membership>("/students/me/membership");
  const retry = resource.retry;
  const ends = resource.data?.ends_at;
  useEffect(() => {
    function visible() {
      if (document.visibilityState === "visible") retry();
    }
    window.addEventListener("focus", retry);
    document.addEventListener("visibilitychange", visible);
    // Poll only while this page is visible; also refresh at the exact expiry boundary.
    const interval = window.setInterval(() => {
      if (document.visibilityState === "visible") retry();
    }, 60_000);
    const remaining = ends ? new Date(ends).getTime() - Date.now() : 0;
    const expiry =
      remaining > 0 && remaining < 2_147_483_647
        ? window.setTimeout(retry, remaining + 100)
        : undefined;
    return () => {
      window.removeEventListener("focus", retry);
      document.removeEventListener("visibilitychange", visible);
      clearInterval(interval);
      clearTimeout(expiry);
    };
  }, [retry, ends]);
  return resource;
}
export function AccessBadge({ item }: { item: ContentAccess }) {
  return (
    <span
      className={`badge ${item.minimum_plan_code === "vip" ? "vip-badge" : "success"}`}
    >
      {item.minimum_plan_code === "vip" ? <Crown size={16} /> : null}
      {item.minimum_plan_code === "vip"
        ? "VIP"
        : item.minimum_plan_code === "free"
          ? "Miễn phí"
          : "Chưa sẵn sàng"}
      {item.learning_level === "advanced" ? " · Nâng cao" : ""}
      {item.locked && <LockKeyhole size={15} aria-label="Bài đang khóa" />}
    </span>
  );
}
export function MembershipSummary() {
  const membership = useMembership();
  if (membership.loading) return <Loading />;
  if (membership.error || !membership.data)
    return <ErrorState message={membership.error} retry={membership.retry} />;
  const data = membership.data;
  return (
    <section className="panel membership-summary">
      <h2>Gói học của em: {data.plan_code === "vip" ? "VIP" : "Miễn phí"}</h2>
      {data.ends_at && (
        <p>
          {data.status === "active"
            ? "VIP có hiệu lực đến"
            : data.status === "revoked"
              ? "Quyền VIP đã được thu hồi; kỳ đã cấp kết thúc"
              : "Kỳ VIP trước kết thúc"}
          : {membershipTime(data.ends_at)} (giờ Việt Nam)
        </p>
      )}
      <p>Em luôn xem được lịch sử, điểm và kết quả bài đã nộp.</p>
      <Link className="button secondary" href="/student/membership">
        Xem quyền lợi gói học
      </Link>
    </section>
  );
}
export function MembershipPage() {
  const plans = useResource<MembershipPlan[]>("/membership/plans");
  return (
    <>
      <PageTitle
        title="Gói học của em"
        description="Cùng phụ huynh tìm hiểu nội dung phù hợp với em."
      />
      <MembershipSummary />
      {plans.loading ? (
        <Loading />
      ) : plans.error ? (
        <ErrorState message={plans.error} retry={plans.retry} />
      ) : (
        <div className="two-columns membership-plans">
          {plans.data?.map((plan) => (
            <section className="panel" key={plan.code}>
              <h2>{plan.name}</h2>
              <ul>
                {plan.features.map((feature) => (
                  <li key={feature}>{featureLabels[feature] ?? feature}</li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}
      <section className="panel">
        <h2>Cùng phụ huynh tìm hiểu VIP</h2>
        <p>
          Phụ huynh có thể liên hệ đơn vị quản lý để được hỗ trợ cấp hoặc gia
          hạn VIP cho tài khoản học sinh. Gói học có thời hạn 30, 90 hoặc 365
          ngày.
        </p>
        <Link className="button secondary" href="/student/grades">
          Tiếp tục học miễn phí
        </Link>
      </section>
    </>
  );
}
export function LockedContent({
  message,
  code,
}: {
  message?: string;
  code?: string;
}) {
  const vip = !code || code === "MEMBERSHIP_REQUIRED";
  return (
    <section className="panel locked-content">
      <LockKeyhole size={32} />
      <h2>{vip ? "Cùng khám phá thêm với VIP" : "Bài học chưa khả dụng"}</h2>
      <p>
        {message ||
          "Bài này nằm trong gói VIP. Em vẫn có thể học các bài miễn phí bên dưới."}
      </p>
      <div className="quiz-actions">
        <Link className="button" href="/student/grades">
          Học bài miễn phí
        </Link>
        {vip && (
          <Link className="button secondary" href="/student/membership">
            Xem gói học cùng phụ huynh
          </Link>
        )}
      </div>
    </section>
  );
}
export function LessonPreviewPanel({ id }: { id: string }) {
  const resource = useResource<LessonPreview>(`/lessons/${id}/preview`);
  if (resource.loading) return <Loading />;
  if (resource.error || !resource.data)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  const data = resource.data;
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${data.grade} · ${data.subject_name}`}
        title={data.title}
        description={`${data.estimated_minutes} phút · Giới thiệu bài học`}
      />
      <section className="panel">
        <AccessBadge item={data} />
        <h2>Em sẽ khám phá</h2>
        <p>{data.preview.summary}</p>
        <ul>
          {data.preview.goals.map((goal) => (
            <li key={goal}>{goal}</li>
          ))}
        </ul>
      </section>
      <LockedContent code={data.lock_reason ?? undefined} />
    </>
  );
}

export function AdminMembershipPage({ id }: { id: string }) {
  const student = useResource<{ display_name: string; username: string }>(
    `/admin/students/${id}/summary`,
  );
  const membership = useResource<Membership>(
    `/admin/students/${id}/membership`,
  );
  const history = useResource<
    {
      id: string;
      operation: string;
      actor_name: string;
      created_at: string;
      response_snapshot: Membership;
    }[]
  >(`/admin/students/${id}/membership/history`);
  const [operation, setOperation] = useState("grant");
  const [days, setDays] = useState(30);
  const [reason, setReason] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const request = useRef<{ fingerprint: string; key: string } | null>(null);
  async function submit() {
    if (!confirmed) return;
    const payload =
      operation === "revoke" ? { reason } : { duration_days: days, reason };
    const fingerprint = JSON.stringify({ id, operation, payload });
    if (request.current?.fingerprint !== fingerprint)
      request.current = { fingerprint, key: crypto.randomUUID() };
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await api(`/admin/students/${id}/membership/${operation}`, {
        method: "POST",
        body: JSON.stringify(payload),
        headers: { "Idempotency-Key": request.current.key },
      });
      setNotice("Đã cập nhật gói học và ghi lịch sử thao tác.");
      request.current = null;
      setConfirmed(false);
      setReason("");
      membership.retry();
      history.retry();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  if (student.loading || membership.loading) return <Loading />;
  if (student.error || membership.error || !student.data || !membership.data)
    return (
      <ErrorState
        message={student.error || membership.error}
        retry={() => {
          student.retry();
          membership.retry();
        }}
      />
    );
  const data = membership.data;
  return (
    <>
      <PageTitle
        title={`Gói học · ${student.data.display_name}`}
        description={`Tài khoản: ${student.data.username}`}
      />
      <section className="panel">
        <h2>
          {data.plan_code === "vip"
            ? "VIP đang hoạt động"
            : "Đang dùng gói miễn phí"}
        </h2>
        <p>
          Trạng thái:{" "}
          {
            {
              free: "Chưa cấp VIP",
              active: "Còn hiệu lực",
              expired: "Hết hạn",
              revoked: "Đã thu hồi",
            }[data.status]
          }
        </p>
        <p>Kết thúc kỳ VIP: {membershipTime(data.ends_at)}</p>
      </section>
      <section className="panel">
        <h2>Cập nhật gói học</h2>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void submit();
          }}
        >
          <label>
            Thao tác
            <select
              value={operation}
              onChange={(e) => {
                setOperation(e.target.value);
                setConfirmed(false);
              }}
              disabled={busy}
            >
              <option value="grant">Cấp VIP mới</option>
              <option value="extend">Gia hạn VIP</option>
              <option value="revoke">Thu hồi VIP</option>
            </select>
          </label>
          {operation !== "revoke" && (
            <label>
              Thời hạn
              <select
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                disabled={busy}
              >
                {[30, 90, 365].map((value) => (
                  <option value={value} key={value}>
                    {value} ngày
                  </option>
                ))}
              </select>
            </label>
          )}
          <label>
            Lý do
            <textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              minLength={5}
              maxLength={500}
              required
              disabled={busy}
            />
          </label>
          <label className="confirmation-row">
            <input
              type="checkbox"
              checked={confirmed}
              onChange={(e) => setConfirmed(e.target.checked)}
              disabled={busy}
            />
            Tôi xác nhận cập nhật gói cho {student.data.username}
          </label>
          <button className="button" disabled={busy || !confirmed}>
            {busy ? "Đang lưu…" : "Xác nhận cập nhật gói"}
          </button>
          <p role="status" aria-live="polite">
            {notice}
          </p>
          {error && (
            <p role="alert" className="error-text">
              {error}
            </p>
          )}
        </form>
      </section>
      <section className="panel">
        <h2>Lịch sử gói học</h2>
        {history.loading ? (
          <Loading />
        ) : history.error ? (
          <ErrorState message={history.error} retry={history.retry} />
        ) : history.data?.length ? (
          history.data.map((item) => (
            <div className="list-row" key={item.id}>
              <div>
                <strong>
                  {
                    (
                      {
                        grant: "Cấp VIP",
                        extend: "Gia hạn",
                        revoke: "Thu hồi",
                      } as Record<string, string>
                    )[item.operation]
                  }
                </strong>
                <small>
                  {item.actor_name} · {membershipTime(item.created_at)}
                </small>
              </div>
              <span>
                Kết thúc: {membershipTime(item.response_snapshot.ends_at)}
              </span>
            </div>
          ))
        ) : (
          <Empty>Chưa có thao tác cấp gói.</Empty>
        )}
      </section>
      <Link className="button secondary" href="/admin/students">
        Về danh sách học sinh
      </Link>
    </>
  );
}
