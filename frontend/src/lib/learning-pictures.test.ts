import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { pictureForLabel, pictureWords } from "./learning-pictures";

describe("Tranh từ vựng trong thẻ và đáp án", () => {
  it("hiểu nhãn Việt/Anh và nhãn có biểu tượng trong học liệu lớp nhỏ", () => {
    expect(pictureForLabel("🎒 bag")?.code).toBe("schoolbag");
    expect(pictureForLabel("  A cat. ")?.code).toBe("cat");
    expect(pictureForLabel("Hình tam giác")?.code).toBe("triangle");
    expect(pictureForLabel("Màu xanh dương")?.code).toBe("color-blue");
    expect(pictureForLabel("cục tẩy".normalize("NFD"))?.code).toBe("eraser");
  });
  it("không suy đoán hình từ phủ định, câu dài, số lượng hoặc từ tương tự", () => {
    for (const text of [
      "Không phải mèo",
      "Two cats",
      "Cá biết bay",
      "camera",
      "Các bạn",
      "3 + 5",
      "cat and dog",
      "red bag",
    ])
      expect(pictureForLabel(text)).toBeNull();
    expect(pictureWords("Các camera ở lớp.")).toEqual([]);
  });
  it("có file ảnh hợp lệ cho toàn bộ nhóm mới và đúng màu được ghi trên nhãn", () => {
    const labels = [
      "bag",
      "pen",
      "ruler",
      "eraser",
      "desk",
      "chair",
      "school",
      "bus",
      "bicycle",
      "car",
      "rain",
      "cloud",
      "flower",
      "milk",
      "water",
      "bread",
      "egg",
      "circle",
      "square",
      "triangle",
      "rectangle",
      "red",
      "blue",
      "green",
      "yellow",
      "purple",
      "pink",
      "brown",
      "black",
      "white",
    ];
    for (const label of labels) {
      const picture = pictureForLabel(label)!;
      const path = resolve("public/learning", `${picture.code}.svg`);
      expect(existsSync(path), label).toBe(true);
      expect(readFileSync(path, "utf8"), label).toContain("<title>");
    }
    expect(
      readFileSync(resolve("public/learning/color-red.svg"), "utf8"),
    ).toContain('fill="#e87969"');
    expect(
      readFileSync(resolve("public/learning/color-white.svg"), "utf8"),
    ).toContain('fill="#ffffff"');
  });
});
