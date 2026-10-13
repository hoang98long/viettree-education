"use client";
import Link from "next/link";
import { useState } from "react";
import { Plus } from "lucide-react";
import type { Page, Question } from "@/lib/types";
import { Empty, PageTitle } from "@/components/ui";
import { Data, Pagination } from "@/features/admin/shared";

export function QuestionDetail({
  id,
  onClose,
}: {
  id: string;
  onClose: () => void;
}) {
  return (
    <div className="modal-backdrop">
      <section
        role="dialog"
        aria-modal="true"
        aria-labelledby="question-detail-title"
        className="modal wide"
      >
        <button autoFocus className="button secondary small" onClick={onClose}>
          Đóng chi tiết
        </button>
        <Data<Question> path={`/admin/questions/${id}`}>
          {(question) => (
            <>
              <h2 id="question-detail-title">Nội dung câu hỏi</h2>
              <span className="badge">
                {question.question_type} · Độ khó {question.difficulty} ·{" "}
                {question.status}
              </span>
              <p className="question-prompt">{question.content.prompt}</p>
              <ul>
                {question.content.options?.map((option) => (
                  <li key={option.id}>
                    <strong>{option.id.toUpperCase()}.</strong> {option.text}
                  </li>
                ))}
              </ul>
              <div className="explanation">
                <h3>Đáp án · Chỉ quản trị viên</h3>
                <pre>{JSON.stringify(question.grading, null, 2)}</pre>
                <p>{question.explanation?.text}</p>
              </div>
            </>
          )}
        </Data>
      </section>
    </div>
  );
}

export function QuestionsPage() {
  const [page, setPage] = useState(1);
  const [subject, setSubject] = useState("");
  const [grade, setGrade] = useState(4);
  const [search, setSearch] = useState("");
  const [detail, setDetail] = useState<string | null>(null);
  const [status, setStatus] = useState("");
  const [kind, setKind] = useState("");
  const [plan, setPlan] = useState("");
  const path = `/admin/questions?grade=${grade}&page=${page}&search=${encodeURIComponent(search)}${subject ? `&subject_code=${subject}` : ""}${status ? `&status=${status}` : ""}${kind ? `&question_type=${kind}` : ""}${plan ? `&minimum_plan_code=${plan}` : ""}`;
  return (
    <>
      <div className="section-heading">
        <PageTitle
          title="Ngân hàng câu hỏi"
          description="Soạn nháp, duyệt và xuất bản. Sửa câu đã xuất bản bằng một phiên bản mới."
        />
        <Link className="button" href="/admin/questions/new">
          <Plus size={18} />
          Tạo câu hỏi
        </Link>
      </div>
      <div className="filters">
        <label>
          Lớp
          <select
            value={grade}
            onChange={(e) => {
              setGrade(Number(e.target.value));
              setPage(1);
            }}
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <option key={value} value={value}>
                Lớp {value}
              </option>
            ))}
          </select>
        </label>
        <label>
          Môn
          <select
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
        <label>
          Tìm mã câu hỏi
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
        <label>
          Trạng thái
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            <option value="draft">Nháp</option>
            <option value="published">Đã xuất bản</option>
            <option value="archived">Đã lưu trữ</option>
          </select>
        </label>
        <label>
          Dạng câu hỏi
          <select
            value={kind}
            onChange={(e) => {
              setKind(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            <option value="single_choice">Chọn một</option>
            <option value="multiple_choice">Chọn nhiều</option>
            <option value="fill_blank">Điền khuyết</option>
            <option value="ordering">Sắp xếp</option>
          </select>
        </label>
        <label>
          Gói nội dung
          <select
            value={plan}
            onChange={(e) => {
              setPlan(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Tất cả</option>
            <option value="free">Miễn phí</option>
            <option value="vip">VIP</option>
          </select>
        </label>
      </div>
      <Data<Page<Question>> key={path} path={path}>
        {(data) => (
          <>
            {data.items.length ? (
              <div className="panel table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Mã</th>
                      <th>Môn / Nội dung</th>
                      <th>Dạng</th>
                      <th>Độ khó</th>
                      <th>Trạng thái</th>
                      <th>Chi tiết</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.items.map((question) => (
                      <tr key={question.id}>
                        <td className="mono">
                          {question.code}
                          <small>
                            Phiên bản {question.version} ·{" "}
                            {question.minimum_plan_code === "vip"
                              ? "VIP"
                              : "Free"}
                          </small>
                        </td>
                        <td>
                          <small>{question.subject_name}</small>
                          <p className="truncate">{question.content.prompt}</p>
                        </td>
                        <td>{question.question_type}</td>
                        <td>{question.difficulty}/5</td>
                        <td>
                          <span className="badge">{question.status}</span>
                        </td>
                        <td>
                          <button
                            className="button secondary small"
                            onClick={() => setDetail(question.id)}
                          >
                            Xem
                          </button>
                          <Link
                            className="button secondary small"
                            href={`/admin/questions/${question.id}/edit`}
                          >
                            Biên soạn
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <Empty>
                Chương trình lớp {grade} đang xây dựng; chưa có câu hỏi.
              </Empty>
            )}
            <Pagination page={page} total={data.total} onChange={setPage} />
          </>
        )}
      </Data>
      {detail && <QuestionDetail id={detail} onClose={() => setDetail(null)} />}
    </>
  );
}
