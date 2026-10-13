"use client";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { ArrowRight, Clock, Sprout } from "lucide-react";
import type {
  ContentAccess,
  Assessment,
  LessonSummary,
  Subject,
  Topic,
} from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import { Empty, PageTitle, SubjectCards } from "@/components/ui";
import { AccessBadge } from "@/features/membership/pages";
import { Resource } from "@/features/student/shared";

export function Grades() {
  const search = useSearchParams();
  const initial = Number(search.get("grade"));
  const profile = useResource<{ current_grade: number }>(
    "/students/me/profile",
  );
  const availability =
    useResource<{ grade: number; status: string }[]>("/grades");
  const [selectedGrade, setGrade] = useState<number | null>(
    initial >= 1 && initial <= 5 ? initial : null,
  );
  const grade = selectedGrade ?? profile.data?.current_grade ?? 4;
  const isAvailable = (value: number) =>
    availability.data?.some(
      (item) => item.grade === value && item.status === "available",
    ) ?? false;
  return (
    <>
      <PageTitle
        eyebrow="KHÁM PHÁ CHƯƠNG TRÌNH"
        title="Chọn lớp học của em"
        description="Lớp 1–5 đã có bài học, luyện tập và bài tư duy cho ba môn. Lớp 1–2 học từng bước ngắn; lớp 5 có thập phân, biểu đồ và đọc hiểu mở rộng."
      />
      <div className="grade-selector">
        {[1, 2, 3, 4, 5].map((value) => (
          <button
            aria-pressed={grade === value}
            className={grade === value ? "active" : ""}
            onClick={() => setGrade(value)}
            key={value}
          >
            Lớp {value}
            <small>{isAvailable(value) ? "Học ngay" : "Đang chuẩn bị"}</small>
          </button>
        ))}
      </div>
      {availability.data && !isAvailable(grade) && (
        <div className="notice">
          <Sprout />
          <div>
            <strong>Chương trình lớp {grade} đang xây dựng</strong>
            <p>
              Em có thể xem khung môn học bên dưới. Các bài học sẽ được bổ sung
              sau.
            </p>
          </div>
        </div>
      )}
      {profile.data &&
        profile.data.current_grade !== grade &&
        isAvailable(grade) && (
          <p className="notice">
            Hồ sơ của em đang ở lớp {profile.data.current_grade}. Em có thể xem
            danh mục lớp {grade}; nhờ quản trị viên đổi lớp trong hồ sơ để học
            và luyện tập lớp này.
          </p>
        )}
      <Resource<Subject[]> key={grade} path={`/subjects?grade=${grade}`}>
        {(data) => <SubjectCards subjects={data} />}
      </Resource>
    </>
  );
}

export function matchesContent(item: ContentAccess, filter: string) {
  return (
    filter === "all" ||
    (filter === "free"
      ? item.minimum_plan_code === "free"
      : item.learning_level === "advanced")
  );
}

export function TopicPanel({
  topic,
  filter = "all",
}: {
  topic: Topic;
  filter?: string;
}) {
  return (
    <article className="panel topic-panel">
      <span className="eyebrow">CHỦ ĐỀ {topic.sort_order}</span>
      <h2>{topic.title}</h2>
      <Resource<LessonSummary[]> path={`/lessons?topic_id=${topic.id}`}>
        {(lessons) =>
          lessons.some((lesson) => matchesContent(lesson, filter)) ? (
            <div>
              {lessons
                .filter((lesson) => matchesContent(lesson, filter))
                .map((lesson, index) => (
                  <Link
                    className="list-row"
                    href={`/student/lessons/${lesson.id}`}
                    key={lesson.id}
                  >
                    <span className="number-dot">{index + 1}</span>
                    <div>
                      <strong>{lesson.title}</strong>
                      <AccessBadge item={lesson} />
                      <small>
                        <Clock size={13} /> {lesson.estimated_minutes} phút ·
                        Bài học
                      </small>
                    </div>
                    <ArrowRight size={18} />
                  </Link>
                ))}
            </div>
          ) : (
            <Empty>
              {filter === "all"
                ? "Bài học đang được xây dựng."
                : "Chưa có bài học phù hợp với bộ lọc này."}
            </Empty>
          )
        }
      </Resource>
    </article>
  );
}

export function SubjectPage({ code }: { code: string }) {
  const [filter, setFilter] = useState("all");
  const query = useSearchParams();
  const grade = Number(query.get("grade") || 4);
  const name =
    (
      {
        MATH: "Toán",
        VIETNAMESE: "Tiếng Việt",
        ENGLISH: "Tiếng Anh",
      } as Record<string, string>
    )[code] || code;
  return (
    <>
      <PageTitle
        eyebrow={`LỚP ${grade} > ${name.toUpperCase()}`}
        title={`Cùng khám phá ${name}`}
        description="Đọc bài học, thử ví dụ rồi chọn bài luyện tập phù hợp."
      />
      <label className="content-filter">
        Loại nội dung
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">Tất cả</option>
          <option value="free">Miễn phí</option>
          <option value="advanced">Nâng cao</option>
        </select>
      </label>
      <Resource<Topic[]>
        path={`/topics?grade=${grade}&subject_code=${encodeURIComponent(code)}`}
      >
        {(topics) =>
          topics.length ? (
            <div className="two-columns">
              {topics.map((topic) => (
                <TopicPanel key={topic.id} topic={topic} filter={filter} />
              ))}
            </div>
          ) : (
            <Empty>
              Chương trình lớp {grade} · {name} đang xây dựng. Em hãy quay lại
              lớp 3 hoặc lớp 4 để khám phá học liệu nhé.
            </Empty>
          )
        }
      </Resource>
      <h2 className="section-title">Bài luyện tập</h2>
      <Resource<Assessment[]>
        path={`/assessments?grade=${grade}&subject_code=${encodeURIComponent(code)}`}
      >
        {(assessments) =>
          assessments.some((item) => matchesContent(item, filter)) ? (
            <div className="two-columns">
              {assessments
                .filter((item) => matchesContent(item, filter))
                .map((assessment) => (
                  <Link
                    className="panel practice-card"
                    key={assessment.id}
                    href={`/student/assessments/${assessment.id}`}
                  >
                    <span className="badge">{assessment.item_count} câu</span>
                    <AccessBadge item={assessment} />
                    <h3>{assessment.title}</h3>
                    <p>{assessment.description}</p>
                    <span className="card-link">
                      Thử sức <ArrowRight size={17} />
                    </span>
                  </Link>
                ))}
            </div>
          ) : (
            <Empty>Chưa có bài luyện tập cho lớp này.</Empty>
          )
        }
      </Resource>
    </>
  );
}
