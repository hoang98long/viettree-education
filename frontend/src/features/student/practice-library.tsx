"use client";
import Link from "next/link";
import { useState } from "react";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";
import { AccessBadge } from "@/features/membership/pages";
import type { Assessment, User } from "@/lib/types";

export function PracticeLibrary() {
  const profile = useResource<User & { current_grade: number }>(
    "/students/me/profile",
  );
  const resource = useResource<Assessment[]>(
    `/assessments?grade=${profile.data?.current_grade ?? 4}`,
  );
  const [search, setSearch] = useState("");
  const [subject, setSubject] = useState("");
  const [plan, setPlan] = useState("");
  const [kind, setKind] = useState("");
  const names: Record<string, string> = {
    practice: "Luyện tập",
    homework: "Bài được giao",
    quiz: "Thử thách",
    test: "Kiểm tra",
    placement: "Khởi đầu",
    adaptive: "Theo năng lực",
  };
  const items =
    resource.data?.filter(
      (item) =>
        (!subject || item.subject_code === subject) &&
        (!plan || item.minimum_plan_code === plan) &&
        (!kind || item.assessment_type === kind) &&
        `${item.title} ${item.description}`
          .toLocaleLowerCase("vi")
          .includes(search.toLocaleLowerCase("vi")),
    ) ?? [];
  return (
    <>
      <PageTitle
        title="Thư viện luyện tập của em"
        description="Tìm bài theo môn và chủ đề, rồi thử sức theo nhịp của em. Điểm và kết quả được lưu khi em nộp bài."
      />
      <div className="filters library-filters">
        <label>
          Tìm bài luyện tập
          <input value={search} onChange={(e) => setSearch(e.target.value)} />
        </label>
        <label>
          Môn luyện tập
          <select value={subject} onChange={(e) => setSubject(e.target.value)}>
            <option value="">Tất cả</option>
            {Array.from(
              new Map(
                resource.data?.map((item) => [
                  item.subject_code,
                  item.subject_name,
                ]),
              ).entries(),
            ).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Gói bài luyện
          <select value={plan} onChange={(e) => setPlan(e.target.value)}>
            <option value="">Tất cả</option>
            <option value="free">Miễn phí</option>
            <option value="vip">VIP</option>
          </select>
        </label>
        <label>
          Loại bài luyện
          <select value={kind} onChange={(e) => setKind(e.target.value)}>
            <option value="">Tất cả</option>
            {Object.entries(names).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </label>
      </div>
      {profile.loading || resource.loading ? (
        <Loading />
      ) : profile.error || resource.error ? (
        <ErrorState
          message={profile.error || resource.error}
          retry={() => {
            profile.retry();
            resource.retry();
          }}
        />
      ) : items.length ? (
        <div className="two-columns">
          {items.map((item) => (
            <Link
              key={item.id}
              className="panel practice-card"
              href={`/student/assessments/${item.id}`}
            >
              <AccessBadge item={item} />
              <h2>{item.title}</h2>
              <p>{item.description}</p>
              <p>
                {item.item_count} câu ·{" "}
                {names[item.assessment_type] ?? "Luyện tập"} ·{" "}
                {item.time_limit_seconds
                  ? `${item.time_limit_seconds / 60} phút`
                  : "Học theo nhịp của em"}
              </p>
              <span className="card-link">
                {item.locked ? "Xem giới thiệu" : "Mở bài luyện tập"}
              </span>
            </Link>
          ))}
        </div>
      ) : (
        <Empty>
          Chưa có bài phù hợp. Em thử đổi bộ lọc hoặc chọn môn khác nhé.
        </Empty>
      )}
    </>
  );
}
