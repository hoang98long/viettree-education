import { BookOpen, ImageIcon, Lightbulb } from "lucide-react";
import { readingPages } from "@/lib/guided-reading";
import type { Payload } from "./types";

export function ReadingReview({ value }: { value: Payload }) {
  const budget = value.grade <= 2 ? 35 : 55;
  const count = (text: string) =>
    text.trim() ? text.trim().split(/\s+/u).length : 0;
  const blocks = value.content.blocks;
  const total = blocks.reduce((sum, block) => sum + count(block.text), 0);
  const long = blocks.filter((block) =>
    readingPages(block.text, budget).some((page) => count(page) > budget),
  );
  const hints = (value.content.hints || []).filter((hint) => hint.trim());
  const free = Math.min(hints.length, value.content.free_hint_count ?? 1);
  const empty = blocks.filter((block) => !block.text.trim());
  return (
    <aside className="panel reading-review" aria-label="Rà soát học liệu">
      <h2>Rà soát trước khi duyệt</h2>
      <p className="muted">
        Gợi ý biên soạn cho lớp {value.grade}; giáo viên vẫn kiểm tra độ đúng và
        mức phù hợp.
      </p>
      <dl>
        <div>
          <dt>
            <BookOpen aria-hidden size={20} /> Độ dài
          </dt>
          <dd>
            {total} tiếng theo khoảng trắng · {blocks.length} phần
          </dd>
        </div>
        <div>
          <dt>
            <ImageIcon aria-hidden size={20} /> Minh họa
          </dt>
          <dd>
            {value.content.illustration
              ? "Đã chọn hình minh họa"
              : "Chưa chọn hình riêng; cân nhắc thêm tranh hoặc sơ đồ phù hợp"}
          </dd>
        </div>
        <div>
          <dt>
            <Lightbulb aria-hidden size={20} /> Gợi ý
          </dt>
          <dd>
            {hints.length
              ? value.minimum_plan_code === "vip"
                ? `${hints.length} gợi ý trong bài yêu cầu VIP`
                : `${free} mức Free / ${hints.length - free} mức VIP`
              : "Chưa có gợi ý theo bước"}
          </dd>
        </div>
      </dl>
      {!!empty.length && (
        <p className="notice error">
          Phần chưa có nội dung:{" "}
          {empty.map((block) => block.title || "Chưa đặt tên").join(", ")}.
        </p>
      )}
      {!!long.length && (
        <p className="notice">
          Phần còn câu hoặc dòng dài:{" "}
          {long.map((block) => block.title).join(", ")}. Thử chia thành câu
          ngắn; giữ đầy đủ bài đọc và dòng thơ. Màn hình đọc hiện chia khoảng{" "}
          {budget} tiếng mỗi đoạn.
        </p>
      )}
      {value.minimum_plan_code === "vip" && !value.preview.summary?.trim() && (
        <p className="notice">
          Bài VIP cần phần giới thiệu riêng để học sinh Free biết mình sẽ học
          gì.
        </p>
      )}
    </aside>
  );
}
