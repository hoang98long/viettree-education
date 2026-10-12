"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { ErrorState, Loading, PageTitle } from "@/components/ui";
import { AcademyImage } from "./shared";

type Sample = { id: string; asset: string; label: string; features: number[] };
export function ClassificationLab() {
  const { data, error, loading, retry } = useResource<{ samples: Sample[] }>(
    "/ai-academy/lab",
  );
  const [training, setTraining] = useState<string[]>([
    "sample-0",
    "sample-8",
    "sample-16",
  ]);
  const [colorOnly, setColorOnly] = useState(false);
  const [results, setResults] = useState<
    {
      id: string;
      predicted: string;
      actual: string;
      correct: boolean;
      explanation: string;
    }[]
  >([]);
  const [failure, setFailure] = useState("");
  async function run() {
    try {
      const tests = data!.samples
        .filter((s) => !training.includes(s.id))
        .slice(0, 8)
        .map((s) => s.id);
      const r = await api<{ results: typeof results }>("/ai-academy/lab", {
        method: "POST",
        body: JSON.stringify({
          training_ids: training,
          test_ids: tests,
          features: colorOnly ? [4] : [0, 1, 2, 3],
        }),
      });
      setResults(r.results);
      setFailure("");
    } catch (e) {
      setFailure((e as Error).message);
    }
  }
  return (
    <>
      <PageTitle
        title="Phòng thí nghiệm dữ liệu"
        description="Mô phỏng so khớp đặc điểm với mẫu gần nhất. Không phải mô hình AI lớn; dữ liệu là thẻ minh họa."
      />
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorState message={error} retry={retry} />
      ) : (
        <>
          <section className="panel">
            <h2>1. Chọn ví dụ để học</h2>
            <p>
              Chọn tối đa 16 thẻ; giữ mẫu khác để thử. Thử bỏ một nhóm hoặc chỉ
              dùng màu để quan sát lỗi.
            </p>
            <div className="academy-samples">
              {data?.samples.map((sample) => (
                <label key={sample.id} className="academy-tile">
                  <AcademyImage
                    code={sample.asset}
                    alt={`Ví dụ ${sample.label}`}
                    small
                  />
                  <input
                    type="checkbox"
                    checked={training.includes(sample.id)}
                    onChange={(e) =>
                      setTraining((t) =>
                        e.target.checked
                          ? t.length < 16
                            ? [...t, sample.id]
                            : t
                          : t.filter((id) => id !== sample.id),
                      )
                    }
                  />
                  {sample.label}
                </label>
              ))}
            </div>
            <label>
              <input
                type="checkbox"
                checked={colorOnly}
                onChange={(e) => setColorOnly(e.target.checked)}
              />{" "}
              Chỉ dùng màu nền · thử thiên lệch dữ liệu
            </label>
            <button
              className="button"
              disabled={!training.length}
              onClick={() => void run()}
            >
              2. Thử với mẫu mới
            </button>
          </section>
          {failure && (
            <p className="notice error" role="alert">
              {failure}
            </p>
          )}
          {results.length > 0 && (
            <section className="panel" aria-live="polite">
              <h2>3. Kiểm tra và cải tiến</h2>
              <p>
                {results.filter((r) => r.correct).length}/{results.length} mẫu
                đúng trong lượt thử này; chưa chứng minh áp dụng cho mọi dữ
                liệu.
              </p>
              {results.map((r) => (
                <div className="list-row" key={r.id}>
                  <span>
                    {r.id}: dự đoán {r.predicted} · nhãn mẫu {r.actual}
                  </span>
                  <strong>{r.correct ? "✓ Phù hợp" : "↻ Cần kiểm tra"}</strong>
                </div>
              ))}
              <p>{results[0].explanation}</p>
            </section>
          )}
        </>
      )}
    </>
  );
}

export function PromptBuilder() {
  const [goal, setGoal] = useState("Hiểu phân số");
  const [context, setContext] = useState(
    "Bánh chia 8 phần bằng nhau, tô 3 phần",
  );
  const [format, setFormat] = useState("2 câu ngắn");
  return (
    <section className="panel">
      <h2>Prompt Builder</h2>
      <p>Ghép mảnh đã biên soạn; không nhập thông tin riêng.</p>
      <label>
        Mục tiêu
        <select value={goal} onChange={(e) => setGoal(e.target.value)}>
          {["Hiểu phân số", "Tìm ý về cây", "Ôn từ vựng trường học"].map(
            (x) => (
              <option key={x}>{x}</option>
            ),
          )}
        </select>
      </label>
      <label>
        Ngữ cảnh
        <select value={context} onChange={(e) => setContext(e.target.value)}>
          {[
            "Bánh chia 8 phần bằng nhau, tô 3 phần",
            "Quan sát cây trong tranh lớp học",
            "Thẻ book, pencil và school",
          ].map((x) => (
            <option key={x}>{x}</option>
          ))}
        </select>
      </label>
      <label>
        Định dạng
        <select value={format} onChange={(e) => setFormat(e.target.value)}>
          {["2 câu ngắn", "3 bước gợi ý", "bảng hai cột"].map((x) => (
            <option key={x}>{x}</option>
          ))}
        </select>
      </label>
      <p className="notice" aria-live="polite">
        Em muốn {goal.toLowerCase()}. Ngữ cảnh: {context}. Chỉ gợi ý để em tự
        làm; trình bày bằng {format}. Nhắc cách kiểm tra.
      </p>
      <p className="muted">
        Bản ghép câu hỏi, chưa gửi đến mô hình. Câu hỏi rõ vẫn cần kiểm chứng
        câu trả lời.
      </p>
    </section>
  );
}
