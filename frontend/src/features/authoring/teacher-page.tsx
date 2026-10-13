"use client";
import { ShieldCheck } from "lucide-react";
import { PageTitle } from "@/components/ui";

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
