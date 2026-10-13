"use client";
import { useState, useRef } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState } from "@/components/ui";
import { AccountPicker } from "@/features/academy/account-picker";
import type { Classroom } from "@/features/classrooms/types";

export function AssignmentPanel({
  classroom,
  admin,
}: {
  classroom?: Classroom;
  admin: boolean;
}) {
  const [mode, setMode] = useState(classroom ? "class" : "individual");
  const [student, setStudent] = useState("");
  const [grade, setGrade] = useState(classroom?.grade || 4);
  const [kind, setKind] = useState("assessment");
  const [resourceId, setResourceId] = useState("");
  const [deadline, setDeadline] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const effectiveGrade = mode === "class" ? classroom?.grade || grade : grade;
  const request = useRef<{ fingerprint: string; key: string } | null>(null);
  const resources = useResource<
    { id: string; title: string; minimum_plan_code: string }[]
  >(`/classroom/resources?kind=${kind}&grade=${effectiveGrade}`);
  const current =
    resourceId ||
    resources.data?.find((r) => r.minimum_plan_code === "free")?.id ||
    resources.data?.[0]?.id ||
    "";
  async function assign() {
    setBusy(true);
    try {
      const body = {
        kind,
        resource_id: current,
        class_id: mode === "class" ? classroom?.id : null,
        student_ids: mode === "individual" ? [student] : [],
        due_at: deadline ? new Date(deadline).toISOString() : null,
      };
      const fingerprint = JSON.stringify(body);
      if (!request.current || request.current.fingerprint !== fingerprint)
        request.current = { fingerprint, key: crypto.randomUUID() };
      const result = await api<{ count: number }>("/classroom/assignments", {
        method: "POST",
        body: JSON.stringify({
          kind,
          resource_id: current,
          class_id: mode === "class" ? classroom?.id : null,
          student_ids: mode === "individual" ? [student] : [],
          due_at: deadline ? new Date(deadline).toISOString() : null,
          idempotency_key: request.current.key,
        }),
      });
      setMessage(
        `Đã giao cho ${result.count} học sinh. VIP được kiểm tra theo tài khoản nhận bài.`,
      );
    } catch (e) {
      setMessage((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel">
      <h2>Giao bài cho lớp hoặc cá nhân</h2>
      {admin && (
        <label>
          Đối tượng giao bài
          <select
            aria-label="Đối tượng giao bài"
            value={mode}
            onChange={(e) => setMode(e.target.value)}
          >
            <option value="class">Cả lớp đang chọn</option>
            <option value="individual">
              Học sinh riêng, kể cả học sinh tự do
            </option>
          </select>
        </label>
      )}
      {mode === "individual" && (
        <>
          <label>
            Khối của bài
            <select
              value={grade}
              onChange={(e) => {
                setGrade(Number(e.target.value));
                setResourceId("");
              }}
            >
              {[1, 2, 3, 4, 5].map((n) => (
                <option key={n}>{n}</option>
              ))}
            </select>
          </label>
          <AccountPicker
            label="Học sinh nhận bài riêng"
            role="student"
            grade={grade}
            value={student}
            onChange={setStudent}
          />
        </>
      )}
      <label>
        Loại bài giao
        <select
          aria-label="Loại bài giao"
          value={kind}
          onChange={(e) => {
            setKind(e.target.value);
            setResourceId("");
          }}
        >
          <option value="assessment">Bài luyện tập có chấm điểm</option>
          <option value="lesson">Bài học ba môn</option>
          <option value="ai_lesson">Bài đào tạo AI Academy</option>
        </select>
      </label>
      {resources.loading ? (
        <Loading />
      ) : resources.error ? (
        <ErrorState message={resources.error} retry={resources.retry} />
      ) : (
        <label>
          Chọn nội dung giao
          <select
            aria-label="Chọn nội dung giao"
            value={current}
            onChange={(e) => setResourceId(e.target.value)}
          >
            {resources.data?.map((r) => (
              <option key={r.id} value={r.id}>
                {r.title} · {r.minimum_plan_code === "vip" ? "VIP" : "Miễn phí"}
              </option>
            ))}
          </select>
        </label>
      )}
      <label>
        Hạn hoàn thành (không bắt buộc)
        <input
          type="datetime-local"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
        />
      </label>
      <p>
        Giao bài VIP không tự nâng gói. Nếu có học sinh chưa đủ quyền, hãy chọn
        bài miễn phí hoặc giao riêng cho tài khoản VIP.
      </p>
      <button
        className="button"
        disabled={
          busy ||
          !current ||
          (mode === "individual" && !student) ||
          (mode === "class" && !classroom?.is_active)
        }
        onClick={() => void assign()}
      >
        Giao bài đã chọn
      </button>
      <p role="status">{message}</p>
    </section>
  );
}
