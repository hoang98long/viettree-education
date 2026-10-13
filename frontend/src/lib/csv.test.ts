import { describe, expect, it } from "vitest";
import { csvDocument } from "./csv";

describe("CSV export", () => {
  it("keeps Vietnamese, quotes, commas and multiline cells readable in Excel", () => {
    expect(
      csvDocument([["Tiếng Việt", 'Bài "mới", lớp 1', "Hai\ndòng", 12]]),
    ).toBe('\uFEFF"Tiếng Việt","Bài ""mới"", lớp 1","Hai\ndòng","12"\r\n');
  });
  it("neutralizes formulas including leading whitespace, while preserving numeric values", () => {
    const value = csvDocument([
      ["=1+1", "  +SUM(A1)", "\t@SUM(A1)", "-10", -10, "Toán"],
    ]);
    expect(value).toContain('"\'=1+1"');
    expect(value).toContain('"\'  +SUM(A1)"');
    expect(value).toContain('"\'\t@SUM(A1)"');
    expect(value).toContain('"\'-10","-10","Toán"');
  });
});
