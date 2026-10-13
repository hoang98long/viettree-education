"use client";

import Link from "next/link";
import { useState } from "react";
import {
  BookOpenCheck,
  ChartNoAxesCombined,
  Crown,
  NotebookPen,
  Printer,
} from "lucide-react";
import { useResource } from "@/hooks/use-resource";
import { api, ApiError, dateLabel, percent } from "@/lib/api";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { QuestionInput } from "@/components/question-input";
import { LockedContent, useMembership } from "@/features/membership/pages";
import type {
  Answer,
  AttemptItem,
  VipLibrary,
  VipMistakes,
  VipReport,
} from "@/lib/types";

function VipResource<T>({
  path,
  feature,
  children,
}: {
  path: string;
  feature: string;
  children: (data: T) => React.ReactNode;
}) {
  const resource = useResource<T>(path);
  const membership = useMembership();
  if ((membership.loading && !membership.data) || resource.loading)
    return <Loading />;
  if (membership.error)
    return <ErrorState message={membership.error} retry={membership.retry} />;
  if (
    !membership.data?.features.includes(feature) ||
    resource.errorCode === "MEMBERSHIP_REQUIRED"
  )
    return (
      <LockedContent message="Chức năng này nằm trong gói VIP. Em vẫn xem được kết quả và lịch sử của mình." />
    );
  if (resource.error || !resource.data)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  return <>{children(resource.data)}</>;
}

const tools = [
  [
    "/student/vip/mistakes",
    "Sổ tay ôn lỗi",
    "Thử lại câu đã làm sai, xem lời giải mà không đổi điểm bài cũ.",
    NotebookPen,
  ],
  [
    "/student/vip/report",
    "Báo cáo học tập",
    "Xem 7/30 ngày gần đây, so sánh kỳ trước và in cùng phụ huynh.",
    ChartNoAxesCombined,
  ],
  [
    "/student/learning-plan",
    "Kế hoạch theo kỹ năng",
    "Chọn kiểu kế hoạch Theo kỹ năng cần ôn để chuẩn bị hành trình phù hợp.",
    BookOpenCheck,
  ],
] as const;

export function VipLibraryPage() {
  const [subject, setSubject] = useState("");
  const [unfinished, setUnfinished] = useState(false);
  return (
    <>
      <PageTitle
        eyebrow="CÙNG KHÁM PHÁ THÊM"
        title="Góc học VIP"
        description="Bài học nâng cao, ôn lỗi và theo dõi hành trình của riêng em."
      />
      <VipResource<VipLibrary>
        path="/students/me/vip/library"
        feature="vip.library"
      >
        {(data) => (
          <>
            <div className="three-columns vip-tools">
              {tools.map(([href, title, description, Icon]) => (
                <Link href={href} className="panel" key={href}>
                  <Icon size={28} />
                  <h2>{title}</h2>
                  <p>{description}</p>
                  <span className="card-link">Mở chức năng →</span>
                </Link>
              ))}
            </div>
            <section className="panel">
              <h2>Hành trình nâng cao lớp {data.grade}</h2>
              <p>
                {
                  data.lessons.filter(
                    (item) => item.progress_status === "completed",
                  ).length
                }
                /{data.lessons.length} bài đã đọc xong. Đọc xong không thay thế
                kết quả luyện tập.
              </p>
              <div className="filters">
                <label htmlFor="vip-library-subject">
                  Môn học
                  <select
                    id="vip-library-subject"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                  >
                    <option value="">Tất cả môn</option>
                    {[
                      ...new Map(
                        data.lessons.map((item) => [
                          item.subject_code,
                          item.subject_name,
                        ]),
                      ).entries(),
                    ].map(([code, name]) => (
                      <option key={code} value={code}>
                        {name}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="vip-check">
                  <input
                    type="checkbox"
                    checked={unfinished}
                    onChange={(e) => setUnfinished(e.target.checked)}
                  />
                  Chỉ bài chưa đọc xong
                </label>
              </div>
            </section>
            <div className="two-columns">
              {data.lessons
                .filter(
                  (item) =>
                    (!subject || item.subject_code === subject) &&
                    (!unfinished || item.progress_status !== "completed"),
                )
                .map((item) => (
                  <article className="panel" key={item.id}>
                    <span className="badge vip-badge">
                      <Crown size={16} /> VIP · {item.subject_name}
                    </span>
                    <h2>{item.title}</h2>
                    <p>
                      {item.topic_title} · {item.estimated_minutes} phút
                    </p>
                    <p>
                      {item.progress_status === "completed"
                        ? "Đã đọc xong"
                        : item.progress_status === "in_progress"
                          ? "Đang đọc"
                          : "Sẵn sàng khám phá"}
                    </p>
                    <Link
                      href={`/student/lessons/${item.id}`}
                      className="button secondary"
                    >
                      {item.progress_status === "completed"
                        ? "Đọc lại"
                        : "Mở bài học"}
                    </Link>
                  </article>
                ))}
            </div>
            {!data.lessons.filter(
              (item) =>
                (!subject || item.subject_code === subject) &&
                (!unfinished || item.progress_status !== "completed"),
            ).length && (
              <Empty>
                Chưa có bài phù hợp bộ lọc. Em có thể đổi môn hoặc đọc lại bài
                đã học.
              </Empty>
            )}
          </>
        )}
      </VipResource>
    </>
  );
}

function MistakeCard({ item }: { item: VipMistakes["items"][number] }) {
  const [answer, setAnswer] = useState<Answer | null>(null);
  const [feedback, setFeedback] = useState<{
    is_correct: boolean;
    explanation: { text: string };
  } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [locked, setLocked] = useState(false);
  const question: AttemptItem = {
    ...item,
    position: 1,
    points: 0,
    answer: null,
  };
  async function check() {
    if (!answer) return;
    setBusy(true);
    setError("");
    setFeedback(null);
    try {
      setFeedback(
        await api(`/students/me/vip/mistakes/${item.id}/check`, {
          method: "POST",
          body: JSON.stringify({ answer }),
        }),
      );
    } catch (error) {
      if (error instanceof ApiError && error.code === "MEMBERSHIP_REQUIRED")
        setLocked(true);
      setError((error as Error).message);
    } finally {
      setBusy(false);
    }
  }
  if (locked) return <LockedContent />;
  return (
    <article className="panel vip-mistake">
      <span className="eyebrow">
        {item.subject_name} · {dateLabel(item.graded_at)}
      </span>
      <h2>{item.content.prompt}</h2>
      <p>Từ bài: {item.assessment_title}</p>
      <QuestionInput
        item={question}
        answer={answer}
        disabled={busy}
        onChange={(value) => {
          setAnswer(value);
          setFeedback(null);
        }}
      />
      <div className="quiz-actions">
        <button className="button" disabled={busy || !answer} onClick={check}>
          {busy ? "Đang kiểm tra…" : "Kiểm tra câu tự ôn"}
        </button>
        <Link
          className="button secondary"
          href={`/student/results/${item.attempt_id}`}
        >
          Xem bài làm gốc
        </Link>
      </div>
      {error && (
        <p className="notice error" role="alert">
          {error}
        </p>
      )}
      {feedback && (
        <div className="explanation" role="status">
          <strong>
            {feedback.is_correct
              ? "Em đã trả lời đúng!"
              : "Cùng xem lời giải rồi thử lại nhé."}
          </strong>
          <p>{feedback.explanation.text}</p>
          <p>Phần tự ôn không đổi điểm bài cũ.</p>
        </div>
      )}
    </article>
  );
}

export function VipMistakesPage() {
  const [subject, setSubject] = useState("");
  const [page, setPage] = useState(1);
  const path = `/students/me/vip/mistakes?${new URLSearchParams({ page: String(page), ...(subject ? { subject_code: subject } : {}) })}`;
  return (
    <>
      <PageTitle
        title="Sổ tay ôn lỗi"
        description="Câu sai ở lần chấm gần nhất của mỗi phiên bản câu hỏi. Làm lại đúng trong bài chính thức sẽ đưa câu ra khỏi sổ; tự ôn không đổi điểm."
      />
      <Link href="/student/vip" className="card-link">
        ← Về Góc học VIP
      </Link>
      <label className="filters" htmlFor="vip-mistakes-subject">
        Lọc theo môn
        <select
          id="vip-mistakes-subject"
          value={subject}
          onChange={(e) => {
            setSubject(e.target.value);
            setPage(1);
          }}
        >
          <option value="">Tất cả</option>
          <option value="MATH">Toán</option>
          <option value="VIETNAMESE">Tiếng Việt</option>
          <option value="ENGLISH">Tiếng Anh</option>
        </select>
      </label>
      <VipResource<VipMistakes> path={path} feature="review.mistakes">
        {(data) => (
          <>
            <p>
              {data.total} câu cần ôn · Trang {data.page}
            </p>
            {data.items.length ? (
              data.items.map((item) => (
                <MistakeCard key={item.id} item={item} />
              ))
            ) : (
              <Empty>
                Chưa có câu cần ôn trong bộ lọc này. Em có thể luyện tập rồi
                quay lại.
              </Empty>
            )}
            <div className="quiz-actions">
              <button
                className="button secondary"
                disabled={page === 1}
                onClick={() => setPage((value) => value - 1)}
              >
                Trang trước
              </button>
              <button
                className="button secondary"
                disabled={page * data.page_size >= data.total}
                onClick={() => setPage((value) => value + 1)}
              >
                Trang sau
              </button>
            </div>
          </>
        )}
      </VipResource>
    </>
  );
}

export function VipReportPage() {
  const [days, setDays] = useState(7);
  const score = (value: number | null) =>
    value === null ? "Chưa có dữ liệu" : `${value}%`;
  return (
    <>
      <div className="vip-no-print">
        <PageTitle
          title="Báo cáo học tập"
          description="Dành cho em cùng phụ huynh xem lại hành trình, không xếp hạng với bạn khác."
        />
        <Link href="/student/vip" className="card-link">
          ← Về Góc học VIP
        </Link>
        <label className="filters" htmlFor="vip-report-days">
          Khoảng thời gian
          <select
            id="vip-report-days"
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
          >
            <option value={7}>7 ngày gần đây</option>
            <option value={30}>30 ngày gần đây</option>
          </select>
        </label>
      </div>
      <VipResource<VipReport>
        path={`/students/me/vip/report?days=${days}`}
        feature="reports.personal"
      >
        {(data) => (
          <section className="vip-report-print">
            <div className="panel">
              <h2>
                {data.student_name} · Lớp {data.grade}
              </h2>
              <p>
                {dateLabel(data.starts_at)} – {dateLabel(data.ends_at)} · gồm
                hôm nay, giờ Việt Nam
              </p>
              <button
                className="button secondary vip-no-print"
                onClick={() => window.print()}
              >
                <Printer size={18} />
                In / lưu PDF
              </button>
            </div>
            <div className="three-columns">
              <article className="panel">
                <h3>Bài luyện đã nộp</h3>
                <strong className="skill-percent">{data.attempt_count}</strong>
                <p>{data.active_days} ngày có bài luyện đã nộp</p>
              </article>
              <article className="panel">
                <h3>Tỷ lệ điểm đạt</h3>
                <strong className="skill-percent">
                  {score(data.score_percent)}
                </strong>
                <p>
                  Kỳ trước: {score(data.previous.score_percent)} (
                  {data.previous.attempt_count} bài). Điểm tính theo tổng điểm
                  đạt / tổng điểm tối đa; các đề có thể khác nhau.
                </p>
              </article>
              <article className="panel">
                <h3>Bài đọc hoàn thành</h3>
                <strong className="skill-percent">
                  {data.completed_lessons}
                </strong>
                <p>Xác nhận đọc xong trong kỳ; không dùng làm điểm năng lực.</p>
              </article>
            </div>
            <section className="panel">
              <h2>Theo môn học</h2>
              {data.subjects.length ? (
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Môn</th>
                        <th>Bài đã nộp</th>
                        <th>Tỷ lệ điểm</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.subjects.map((item) => (
                        <tr key={item.subject_code}>
                          <td>{item.subject_name}</td>
                          <td>{item.attempt_count}</td>
                          <td>{score(item.score_percent)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <Empty>
                  Chưa có bài luyện đã nộp trong khoảng thời gian này.
                </Empty>
              )}
            </section>
            <section className="panel">
              <h2>Nhịp luyện tập từng ngày</h2>
              <div className="vip-daily" role="list">
                {data.daily.map((item) => (
                  <div key={item.date} role="listitem">
                    <span>{dateLabel(item.date)}</span>
                    <strong>{item.attempt_count} bài</strong>
                    <span>{score(item.score_percent)}</span>
                  </div>
                ))}
              </div>
            </section>
            <section className="panel">
              <h2>Kỹ năng cần ôn từ toàn bộ lịch sử</h2>
              <p>
                Chỉ hiển thị kỹ năng đã có ít nhất 5 câu được chấm. Đây là gợi ý
                ôn tập, không phải kết luận về học lực.
              </p>
              {data.weak_skills.length ? (
                <ul>
                  {data.weak_skills.map((item) => (
                    <li key={item.skill_id}>
                      <strong>{item.name}</strong> · {item.subject_name} ·{" "}
                      {percent(item.mastery_score)}% · độ tin cậy{" "}
                      {percent(item.confidence)}%
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Chưa có kỹ năng cần ôn đủ dữ liệu để hiển thị.</p>
              )}
              <p>
                Cùng em đọc lại lời giải, hỏi em vì sao chọn đáp án, rồi thử một
                bài ngắn. Có thể dùng kế hoạch theo kỹ năng để chọn bước tiếp
                theo.
              </p>
              <Link
                className="button secondary vip-no-print"
                href="/student/learning-plan"
              >
                Chuẩn bị kế hoạch học
              </Link>
            </section>
          </section>
        )}
      </VipResource>
    </>
  );
}
