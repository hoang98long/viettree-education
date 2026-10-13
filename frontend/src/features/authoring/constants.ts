import type { QuestionKind } from "@/lib/types";

export const kinds: Record<QuestionKind, string> = {
  single_choice: "Chọn một đáp án",
  multiple_choice: "Chọn nhiều đáp án",
  fill_blank: "Điền khuyết",
  ordering: "Sắp xếp",
};
