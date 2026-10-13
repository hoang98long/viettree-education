"use client";
import { useState } from "react";
import { Trophy, Medal } from "lucide-react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, Empty } from "@/components/ui";
import type { Classroom, Rank } from "@/features/classrooms/types";
import { labels } from "@/features/classrooms/constants";

export function RecognitionBoard({
  classroom,
  staff = false,
}: {
  classroom: Classroom;
  staff?: boolean;
}) {
  const [category, setCategory] = useState("MATH");
  const [period, setPeriod] = useState("month");
  const [resourceId, setResourceId] = useState("");
  const [message, setMessage] = useState("");
  const board = useResource<{
    enabled: boolean;
    rows: Rank[];
    top_three: Rank[];
    formula: string;
  }>(
    `/classroom/classes/${classroom.id}/leaderboard?category=${category}&period=${period}${resourceId ? "&resource_id=" + resourceId : ""}`,
  );
  const awards = useResource<
    {
      id: string;
      category: string;
      period_start: string;
      winners: {
        rank: number;
        alias: string;
        score: number;
        completed: number;
      }[];
    }[]
  >(`/classroom/classes/${classroom.id}/recognition`);
  async function publish() {
    try {
      await api(`/classroom/classes/${classroom.id}/recognition`, {
        method: "POST",
        body: JSON.stringify({
          category,
          period,
          resource_id: resourceId || null,
        }),
      });
      awards.retry();
      setMessage(
        "Đã ghi nhận top đầu của kỳ này; công bố lặp không tạo bản tuyên dương mới.",
      );
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <section className="panel class-recognition">
      <h2>
        <Trophy size={25} /> Thành tích trong lớp · {classroom.name}
      </h2>
      <div className="two-columns">
        <label>
          Loại kết quả
          <select
            aria-label="Loại kết quả"
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setResourceId("");
            }}
          >
            {Object.entries(labels).map(([k, v]) => (
              <option key={k} value={k}>
                {v}
              </option>
            ))}
          </select>
        </label>
        <label>
          Kỳ thành tích
          <select value={period} onChange={(e) => setPeriod(e.target.value)}>
            <option value="month">Tháng này</option>
            <option value="week">Tuần này</option>
          </select>
        </label>
      </div>
      {staff && category !== "AI_PROJECT" && (
        <RankResourceFilter
          key={category}
          category={category}
          grade={classroom.grade}
          value={resourceId}
          onChange={setResourceId}
        />
      )}
      {board.loading ? (
        <Loading />
      ) : board.error ? (
        <ErrorState message={board.error} retry={board.retry} />
      ) : !board.data?.enabled ? (
        <Empty>Lớp đang tắt bảng thành tích.</Empty>
      ) : !board.data.rows.length ? (
        <Empty>Chưa có bài đã chấm trong kỳ; tiếp tục học để có kết quả.</Empty>
      ) : (
        <>
          <div className="three-columns class-top-three">
            {board.data.top_three.map((r) => (
              <article className="panel" key={r.rank}>
                <Medal size={32} />
                <h3>
                  Top {r.rank} · {r.is_me ? "Em" : r.display_name}
                </h3>
                <strong>{r.score.toLocaleString("vi-VN")} / 100</strong>
                <p>{r.completed} bài có kết quả</p>
              </article>
            ))}
          </div>
          <p>{board.data.formula}</p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Thứ tự</th>
                  <th>Học sinh</th>
                  <th>Điểm</th>
                  <th>Bài có kết quả</th>
                </tr>
              </thead>
              <tbody>
                {board.data.rows.map((r) => (
                  <tr key={r.rank}>
                    <td>{r.rank}</td>
                    <td>
                      {r.is_me ? "Em · " : ""}
                      {r.display_name}
                    </td>
                    <td>{r.score}</td>
                    <td>{r.completed}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {staff && (
            <button className="button secondary" onClick={() => void publish()}>
              Tuyên dương top 3 của kỳ
            </button>
          )}
        </>
      )}
      <p role="status">{message}</p>
      <h3>Tuyên dương đã ghi nhận</h3>
      {awards.loading ? (
        <Loading />
      ) : awards.error ? (
        <ErrorState message={awards.error} retry={awards.retry} />
      ) : awards.data?.length ? (
        awards.data.map((a) => (
          <article className="notice success" key={a.id}>
            <strong>
              {labels[a.category]} · từ{" "}
              {new Date(a.period_start).toLocaleDateString("vi-VN")}
            </strong>
            {a.winners.map((w) => (
              <p key={w.rank}>
                Top {w.rank} · {w.alias} · {w.score}/100
              </p>
            ))}
          </article>
        ))
      ) : (
        <p>Thầy cô sẽ ghi nhận sau khi xem kết quả.</p>
      )}
    </section>
  );
}

export function RankResourceFilter({
  category,
  grade,
  value,
  onChange,
}: {
  category: string;
  grade: number;
  value: string;
  onChange: (v: string) => void;
}) {
  const resource = useResource<
    { id: string; title: string; subject_code?: string }[]
  >(
    `/classroom/resources?kind=${category === "AI" ? "ai_lesson" : "assessment"}&grade=${grade}`,
  );
  return (
    <label>
      So sánh trên cùng bài (tùy chọn)
      <select
        aria-label="Bài để so sánh"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">Tổng hợp các bài của loại này</option>
        {resource.data
          ?.filter((r) => category === "AI" || r.subject_code === category)
          .map((r) => (
            <option key={r.id} value={r.id}>
              {r.title}
            </option>
          ))}
      </select>
    </label>
  );
}
