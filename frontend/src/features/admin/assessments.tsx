"use client";
import Link from "next/link";
import { useState } from "react";
import type { Assessment } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { Data } from "@/features/admin/shared";

export function AssessmentsPage() {
  const [grade, setGrade] = useState(4);
  const [status, setStatus] = useState("");
  return (
    <>
      <PageTitle
        title="Bài luyện tập"
        description="Đề giữ cố định phiên bản câu hỏi để bảo toàn lịch sử học sinh."
      />
      <Link className="button" href="/admin/assessments/new">
        Tạo bài tập mới
      </Link>
      <div className="filters">
        <label>
          Lọc trạng thái đề
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">Tất cả</option>
            <option value="draft">Nháp</option>
            <option value="published">Đã xuất bản</option>
            <option value="archived">Đã lưu trữ</option>
          </select>
        </label>
        <label>
          Lớp
          <select
            value={grade}
            onChange={(e) => setGrade(Number(e.target.value))}
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <option key={value} value={value}>
                Lớp {value}
              </option>
            ))}
          </select>
        </label>
      </div>
      <Data<Assessment[]>
        key={grade}
        path={`/admin/assessments?grade=${grade}`}
      >
        {(items) =>
          items.length ? (
            <div className="panel table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Đề</th>
                    <th>Môn</th>
                    <th>Số câu</th>
                    <th>Trạng thái</th>
                    <th>Lượt làm</th>
                    <th>Giới hạn</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {items
                    .filter((item) => !status || item.status === status)
                    .map((item) => (
                      <tr key={item.id}>
                        <td>{item.title}</td>
                        <td>{item.subject_name}</td>
                        <td>{item.item_count}</td>
                        <td>
                          <span className="badge">{item.status}</span>
                        </td>
                        <td>{item.attempt_count}</td>
                        <td>{item.max_attempts} lượt</td>
                        <td>
                          <Link
                            className="button secondary small"
                            href={`/admin/assessments/${item.id}/edit`}
                          >
                            {item.status === "published"
                              ? "Xem / Giao bài"
                              : "Biên soạn"}
                          </Link>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          ) : (
            <Empty>Chưa có đề lớp {grade}.</Empty>
          )
        }
      </Data>
    </>
  );
}
