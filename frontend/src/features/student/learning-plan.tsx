"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowRight, Check, BookOpen, ListChecks } from "lucide-react";
import { useResource } from "@/hooks/use-resource";
import { useUser } from "@/components/shell";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { api } from "@/lib/api";
import type { LearningPlan, Subject, User } from "@/lib/types";
import { useMembership } from "@/features/membership/pages";

function shortDate(value: string) {
  return new Intl.DateTimeFormat("vi-VN", {
    day: "numeric",
    month: "numeric",
    timeZone: "Asia/Bangkok",
  }).format(new Date(value.length === 10 ? `${value}T12:00:00+07:00` : value));
}

export function LearningPlanPage() {
  const user = useUser();
  const membership = useMembership();
  const adaptiveAvailable = membership.data?.features.includes(
    "learning_plan.adaptive",
  );
  const [mode, setMode] = useState("basic");
  const profile = useResource<User & { current_grade: number }>(
    "/students/me/profile",
  );
  const subjects = useResource<Subject[]>(
    `/subjects?grade=${profile.data?.current_grade ?? 4}`,
  );
  const plans = useResource<LearningPlan[]>("/students/me/learning-plans");
  const [subject, setSubject] = useState("MATH");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const availableSubjects =
    subjects.data?.filter((item) => item.status === "available") ?? [];
  const selectedSubject = availableSubjects.some(
    (item) => item.code === subject,
  )
    ? subject
    : (availableSubjects[0]?.code ?? "");
  async function create() {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await api<LearningPlan>("/students/me/learning-plans", {
        method: "POST",
        body: JSON.stringify({
          subject_code: selectedSubject,
          mode: adaptiveAvailable ? mode : "basic",
        }),
      });
      setNotice("Kế hoạch đã sẵn sàng. Em hãy bắt đầu từ bước đầu tiên nhé!");
      plans.retry();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  if (profile.loading || subjects.loading) return <Loading />;
  if (profile.error)
    return <ErrorState message={profile.error} retry={profile.retry} />;
  if (subjects.error)
    return <ErrorState message={subjects.error} retry={subjects.retry} />;
  return (
    <>
      <PageTitle
        eyebrow="TỪNG BƯỚC NHỎ, MỖI NGÀY"
        title="Kế hoạch học của em"
        description={`${user.display_name} có thể học theo nhịp của mình. Ngày gợi ý giúp em sắp xếp, không phải hạn nộp bài.`}
      />
      <section className="panel plan-builder">
        <div>
          <h2>7 ngày cùng môn em chọn</h2>
          <p>
            Mỗi kế hoạch có tối đa 3 bài học mới và bài luyện tập đi kèm. Em đọc
            bài, đánh dấu đã đọc rồi thử sức nhé.
          </p>
        </div>
        {availableSubjects.length ? (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void create();
            }}
          >
            <label>
              Môn em muốn học
              <select
                value={selectedSubject}
                onChange={(e) => setSubject(e.target.value)}
                disabled={busy}
              >
                {availableSubjects.map((item) => (
                  <option key={item.id} value={item.code}>
                    {item.name_vi}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Kiểu kế hoạch
              <select
                value={adaptiveAvailable ? mode : "basic"}
                onChange={(e) => setMode(e.target.value)}
                disabled={busy}
              >
                <option value="basic">Cơ bản · Miễn phí</option>
                <option value="adaptive" disabled={!adaptiveAvailable}>
                  Theo kỹ năng cần ôn · VIP
                </option>
              </select>
            </label>
            <button className="button" disabled={busy}>
              {busy ? "Đang chuẩn bị…" : "Chuẩn bị kế hoạch"}
            </button>
          </form>
        ) : (
          <Empty>
            Chương trình lớp {profile.data?.current_grade} đang xây dựng. Khi có
            bài học, em có thể lập kế hoạch ở đây.
          </Empty>
        )}
        <p role="status" aria-live="polite">
          {notice}
        </p>
        {error && (
          <p className="error-text" role="alert">
            {error}
          </p>
        )}
      </section>
      {plans.loading ? (
        <Loading />
      ) : plans.error ? (
        <ErrorState message={plans.error} retry={plans.retry} />
      ) : !plans.data?.length ? (
        <Empty>
          Em chưa có kế hoạch. Chọn một môn phía trên để bắt đầu nhé.
        </Empty>
      ) : (
        plans.data.map((plan) => {
          const next = plan.items.find((item) => item.status !== "completed");
          return (
            <section className="panel learning-plan" key={plan.id}>
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    {plan.subject_name} · {shortDate(plan.start_date)} –{" "}
                    {shortDate(plan.end_date)}
                  </span>
                  <h2>{plan.title}</h2>
                </div>
                <span
                  className={`badge ${plan.status === "completed" ? "success" : ""}`}
                >
                  {plan.status === "completed"
                    ? "Đã hoàn thành"
                    : plan.status === "paused"
                      ? "Tạm dừng"
                      : "Đang học"}
                </span>
              </div>
              <p>
                {plan.mode === "adaptive" ? "Kế hoạch VIP" : "Kế hoạch cơ bản"}{" "}
                · {plan.explanation}
              </p>
              {plan.status === "paused" && (
                <p className="notice">
                  Gói VIP hiện chưa có hiệu lực. Tiến độ đã được giữ lại; em có
                  thể tạo kế hoạch cơ bản để tiếp tục học.
                </p>
              )}
              <p>
                {plan.completed_count}/{plan.items.length} bước đã hoàn thành
              </p>
              <progress
                className="plan-progress"
                max={plan.items.length}
                value={plan.completed_count}
                aria-label={`Tiến độ ${plan.subject_name}`}
              />
              <ol className="plan-steps">
                {plan.items.map((item) => (
                  <li
                    key={item.id}
                    data-completed={item.status === "completed"}
                  >
                    <span className="plan-step-number" aria-hidden="true">
                      {item.status === "completed" ? (
                        <Check size={22} />
                      ) : (
                        item.position
                      )}
                    </span>
                    <div>
                      <span className="plan-step-kind">
                        {item.lesson_id ? (
                          <BookOpen size={18} />
                        ) : (
                          <ListChecks size={18} />
                        )}
                        {item.lesson_id ? "Đọc bài học" : "Luyện tập"} · Gợi ý{" "}
                        {shortDate(item.due_at)}
                      </span>
                      <h3>{item.title}</h3>
                      <p>
                        {item.status === "completed"
                          ? "Em đã hoàn thành bước này"
                          : item.status === "in_progress"
                            ? "Em đang học bước này"
                            : "Sẵn sàng khám phá"}
                      </p>
                    </div>
                    <Link
                      className={`button ${item.id === next?.id ? "" : "secondary"}`}
                      href={`/student/${item.lesson_id ? "lessons" : "assessments"}/${item.lesson_id ?? item.assessment_id}`}
                      aria-label={`${item.locked ? "Xem giới thiệu" : item.status === "completed" ? "Xem lại" : "Mở"}: ${item.title}`}
                    >
                      {item.locked
                        ? "Xem giới thiệu"
                        : item.status === "completed"
                          ? "Xem lại"
                          : item.id === next?.id
                            ? "Học tiếp"
                            : "Mở bài"}
                      <ArrowRight size={18} />
                    </Link>
                  </li>
                ))}
              </ol>
              {plan.status === "completed" && (
                <p className="notice">
                  Em đã đi hết kế hoạch này! Khi sẵn sàng, hãy chọn thêm bài học
                  mới phía trên.
                </p>
              )}
            </section>
          );
        })
      )}
    </>
  );
}
