"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowLeft, ArrowRight, Plus, ShieldCheck } from "lucide-react";
import { api } from "@/lib/api";
import type {
  Assessment,
  Curriculum,
  Page,
  Question,
  Statistics,
  Student,
  User,
} from "@/lib/types";
import { useResource } from "@/hooks/use-resource";
import { Empty, ErrorState, Loading, PageTitle } from "@/components/ui";

function Data<T>({
  path,
  children,
}: {
  path: string;
  children: (data: T) => React.ReactNode;
}) {
  const { data, error, loading, retry } = useResource<T>(path);
  if (loading) return <Loading />;
  if (error || !data) return <ErrorState message={error} retry={retry} />;
  return <>{children(data)}</>;
}
function Pagination({
  page,
  total,
  onChange,
}: {
  page: number;
  total: number;
  onChange: (page: number) => void;
}) {
  return (
    <div className="pagination">
      <span>
        {total} bản ghi · Trang {page}/{Math.max(1, Math.ceil(total / 20))}
      </span>
      <button
        className="button secondary"
        aria-label="Trang trước"
        disabled={page === 1}
        onClick={() => onChange(page - 1)}
      >
        <ArrowLeft size={17} />
      </button>
      <button
        className="button secondary"
        aria-label="Trang sau"
        disabled={page * 20 >= total}
        onClick={() => onChange(page + 1)}
      >
        <ArrowRight size={17} />
      </button>
    </div>
  );
}

export function AdminDashboard({ analytics = false }: { analytics?: boolean }) {
  return (
    <>
      <PageTitle
        eyebrow="VIETTREE · QUẢN TRỊ"
        title={analytics ? "Thống kê học tập" : "Tổng quan hệ thống"}
        description="Số liệu từ database hiện tại, cập nhật sau mỗi bài đã chấm."
      />
      <Data<Statistics> path="/admin/statistics">
        {(data) => (
          <>
            <div className="admin-stats">
              {[
                ["Học sinh", data.students],
                ["Bài học đã xuất bản", data.lessons],
                ["Câu hỏi đã xuất bản", data.question_versions],
                ["Đề đã xuất bản", data.assessments],
                ["Lượt làm đã chấm", data.attempts],
                [
                  "Điểm trung bình",
                  data.average_percent === null
                    ? "Chưa có"
                    : `${Math.round(data.average_percent)}%`,
                ],
              ].map(([label, value]) => (
                <article className="panel" key={String(label)}>
                  <span className="muted">{label}</span>
                  <strong>{value}</strong>
                </article>
              ))}
            </div>
            {!data.attempts ? (
              <Empty>
                Chưa có bài đã nộp. Điểm và thống kê học tập sẽ xuất hiện khi
                học sinh luyện tập.
              </Empty>
            ) : (
              <section className="panel">
                <h2>Hoạt động đã ghi nhận</h2>
                <p>
                  {data.attempts} bài đã chấm · {data.correct_answers} câu trả
                  lời đúng.
                </p>
                <p>
                  Các thống kê tổng hợp có thể rebuild từ attempts và
                  attempt_answers.
                </p>
              </section>
            )}
          </>
        )}
      </Data>
      {!analytics && (
        <div className="three-columns section-title">
          {[
            ["students", "Học sinh", "Xem và cập nhật hồ sơ tối thiểu."],
            [
              "curriculum",
              "Chương trình lớp 1–5",
              "Xem chủ đề, bài học và kỹ năng.",
            ],
            [
              "questions",
              "Ngân hàng câu hỏi",
              "Xem nội dung và lời giải đã seed.",
            ],
          ].map(([path, title, description]) => (
            <Link
              className="panel practice-card"
              href={`/admin/${path}`}
              key={path}
            >
              <h3>{title}</h3>
              <p>{description}</p>
              <span className="card-link">
                Mở <ArrowRight size={17} />
              </span>
            </Link>
          ))}
        </div>
      )}
    </>
  );
}

function EditStudent({
  student,
  onClose,
}: {
  student: Student;
  onClose: () => void;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <div className="modal-backdrop">
      <section
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="student-edit-title"
      >
        <h2 id="student-edit-title">Hồ sơ {student.username}</h2>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const fields = new FormData(e.currentTarget);
            setBusy(true);
            setError("");
            try {
              await api(`/admin/students/${student.id}`, {
                method: "PATCH",
                body: JSON.stringify({
                  display_name: fields.get("display_name"),
                  current_grade: Number(fields.get("grade")),
                }),
              });
              onClose();
            } catch (err) {
              setError((err as Error).message);
              setBusy(false);
            }
          }}
        >
          <label htmlFor="edit-name">Tên hiển thị</label>
          <input
            autoFocus
            id="edit-name"
            name="display_name"
            defaultValue={student.display_name}
            required
            maxLength={160}
          />
          <label htmlFor="edit-grade">Lớp</label>
          <select
            id="edit-grade"
            name="grade"
            defaultValue={student.current_grade}
          >
            {[1, 2, 3, 4, 5].map((grade) => (
              <option value={grade} key={grade}>
                Lớp {grade}
              </option>
            ))}
          </select>
          {error && <p role="alert">{error}</p>}
          <div className="quiz-actions">
            <button
              type="button"
              className="button secondary"
              onClick={onClose}
              disabled={busy}
            >
              Đóng
            </button>
            <button className="button" disabled={busy}>
              {busy ? "Đang lưu…" : "Lưu hồ sơ"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

export function StudentsPage() {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Student | null>(null);
  const [refresh, setRefresh] = useState(0);
  const path = `/admin/students?search=${encodeURIComponent(search)}&page=${page}`;
  return (
    <>
      <PageTitle
        title="Học sinh"
        description="Chỉ quản lý thông tin cần thiết cho học tập."
      />
      <div className="filters">
        <label>
          Tìm theo tên
          <input
            value={search}
            placeholder="Tên hiển thị của học sinh"
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
      </div>
      <Data<Page<Student>> key={path + refresh} path={path}>
        {(data) => (
          <>
            {data.items.length ? (
              <div className="panel table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Học sinh</th>
                      <th>Tên đăng nhập</th>
                      <th>Lớp</th>
                      <th>Trạng thái</th>
                      <th>Hồ sơ</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.items.map((student) => (
                      <tr key={student.id}>
                        <td>{student.display_name}</td>
                        <td>{student.username}</td>
                        <td>{student.current_grade}</td>
                        <td>
                          <span className="badge">
                            {student.is_active ? "Hoạt động" : "Đã khóa"}
                          </span>
                        </td>
                        <td>
                          <button
                            className="button secondary small"
                            onClick={() => setSelected(student)}
                          >
                            Xem / cập nhật
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <Empty>Không có học sinh phù hợp.</Empty>
            )}
            <Pagination page={page} total={data.total} onChange={setPage} />
          </>
        )}
      </Data>
      {selected && (
        <EditStudent
          student={selected}
          onClose={() => {
            setSelected(null);
            setRefresh((value) => value + 1);
          }}
        />
      )}
    </>
  );
}

function QuestionDetail({ id, onClose }: { id: string; onClose: () => void }) {
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
  const path = `/admin/questions?grade=${grade}&page=${page}&search=${encodeURIComponent(search)}${subject ? `&subject_code=${subject}` : ""}`;
  return (
    <>
      <div className="section-heading">
        <PageTitle
          title="Ngân hàng câu hỏi"
          description="Chế độ xem. Nội dung được quản lý bằng seed có phiên bản."
        />
        <Link className="button" href="/admin/questions/new">
          <Plus size={18} />
          Tạo bài tập
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
                        <td className="mono">{question.code}</td>
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

export function AuthoringScaffold() {
  return (
    <>
      <PageTitle eyebrow="KHUNG CHỨC NĂNG" title="Tạo bài tập" />
      <div className="notice">
        <ShieldCheck />
        <div>
          <strong>Chức năng tạo bài tập đang được phát triển</strong>
          <p>
            Khung bên dưới minh họa các trường dự kiến. Lưu nháp, chỉnh sửa,
            duyệt và xuất bản chưa được triển khai.
          </p>
        </div>
      </div>
      <section className="panel">
        <fieldset disabled className="authoring-fields">
          <div className="three-columns">
            {["Lớp", "Môn", "Chủ đề", "Bài học", "Kỹ năng", "Loại câu hỏi"].map(
              (label) => (
                <label key={label}>
                  {label}
                  <select aria-label={label}>
                    <option>Chọn {label.toLowerCase()}</option>
                  </select>
                </label>
              ),
            )}
          </div>
          <label>
            Nội dung
            <textarea rows={4} placeholder="Nội dung câu hỏi" />
          </label>
          <label>
            Lựa chọn
            <textarea rows={3} placeholder="Các lựa chọn trả lời" />
          </label>
          <label>
            Đáp án
            <input />
          </label>
          <label>
            Lời giải
            <textarea rows={3} />
          </label>
          <label>
            Độ khó
            <select>
              <option>1 — Cơ bản</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
              <option>5 — Nâng cao</option>
            </select>
          </label>
          <div className="quiz-actions">
            <button className="button secondary">Xem trước</button>
            <button className="button secondary">Lưu nháp</button>
            <button className="button">Duyệt / Xuất bản</button>
          </div>
        </fieldset>
      </section>
    </>
  );
}

export function CurriculumPage() {
  const [grade, setGrade] = useState(4);
  return (
    <>
      <PageTitle
        title="Chương trình học"
        description="Xem môn học, chủ đề, bài học và kỹ năng. Nội dung lớp 4 đã xuất bản."
      />
      <div className="filters">
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
      <Data<Curriculum> key={grade} path={`/admin/curriculum?grade=${grade}`}>
        {(data) => (
          <>
            {!data.topics.length && (
              <Empty>Chương trình lớp {grade} đang xây dựng.</Empty>
            )}
            {data.subjects.map((subject) => (
              <section className="panel curriculum-subject" key={subject.id}>
                <h2>{subject.name_vi}</h2>
                {data.topics
                  .filter((topic) => topic.subject_id === subject.id)
                  .map((topic) => (
                    <details key={topic.id} open>
                      <summary>{topic.title}</summary>
                      {data.lessons
                        .filter((lesson) => lesson.topic_id === topic.id)
                        .map((lesson) => (
                          <div className="list-row" key={lesson.id}>
                            <span>{lesson.title}</span>
                            <span className="badge">{lesson.status}</span>
                          </div>
                        ))}
                    </details>
                  ))}
                <p className="muted">
                  Kỹ năng:{" "}
                  {data.skills
                    .filter((skill) => skill.subject_id === subject.id)
                    .map((skill) => skill.name)
                    .join(" · ") || "Đang xây dựng"}
                </p>
              </section>
            ))}
          </>
        )}
      </Data>
    </>
  );
}
export function AssessmentsPage() {
  const [grade, setGrade] = useState(4);
  return (
    <>
      <PageTitle
        title="Bài luyện tập"
        description="Đề giữ cố định phiên bản câu hỏi để bảo toàn lịch sử học sinh."
      />
      <div className="filters">
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
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.id}>
                      <td>{item.title}</td>
                      <td>{item.subject_name}</td>
                      <td>{item.item_count}</td>
                      <td>
                        <span className="badge">{item.status}</span>
                      </td>
                      <td>{item.attempt_count}</td>
                      <td>{item.max_attempts} lượt</td>
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
export function SettingsPage() {
  return (
    <>
      <PageTitle title="Cài đặt và vận hành" />
      <section className="panel">
        <h2>Thông tin phiên bản MVP</h2>
        <p>
          Giao diện tiếng Việt · Chương trình lớp 1–5 · Nội dung lớp 4: Toán,
          Tiếng Việt, Tiếng Anh.
        </p>
        <p>
          Cá nhân hóa rule_v1: dựa trên câu trả lời đã chấm và lịch ôn tập, có
          độ tin cậy theo lượng dữ liệu.
        </p>
        <p>
          Tài khoản demo chỉ dành cho local development. Cấu hình kết nối và mật
          khẩu được quản lý ngoài giao diện bằng biến môi trường.
        </p>
        <p>
          Hướng dẫn seed, backup, migration và chạy kiểm thử nằm trong README
          của dự án.
        </p>
      </section>
      <section className="panel section-title">
        <h2>Tài khoản hệ thống</h2>
        <Data<User[]> path="/admin/users">
          {(users) =>
            users.map((user) => (
              <div className="list-row" key={user.id}>
                <strong>{user.display_name}</strong>
                <span>{user.username}</span>
              </div>
            ))
          }
        </Data>
      </section>
    </>
  );
}
