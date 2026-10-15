import { describe, expect, it } from "vitest";
import { hasAnswer } from "./answers";

describe("Câu có nội dung trả lời", () => {
  it("bỏ câu đã xóa và giữ số 0, dấu tiếng Việt, câu sắp xếp", () => {
    for (const answer of [
      null,
      undefined,
      { text: "" },
      { text: " \n\t " },
      { option_ids: [] },
      { ordered_ids: [] },
    ])
      expect(hasAnswer(answer)).toBe(false);
    for (const answer of [
      { text: "0" },
      { text: "cá" },
      { option_id: "a" },
      { option_ids: ["b"] },
      { ordered_ids: ["b", "a"] },
    ])
      expect(hasAnswer(answer)).toBe(true);
  });
});
