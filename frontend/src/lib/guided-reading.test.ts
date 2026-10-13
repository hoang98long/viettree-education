import { describe, expect, it } from "vitest";
import {
  fractionPicture,
  pictureWords,
  placeValuePicture,
  readingPages,
  smallSum,
} from "./guided-reading";

describe("Đọc theo đoạn và tranh có nghĩa", () => {
  it("chia theo câu và giữ toàn bộ nội dung, không cắt chữ hoặc mất phủ định", () => {
    const text =
      "Mèo đi qua vườn. Cây lớn có bóng mát. Mèo không biết bay. Bạn nhỏ nhìn mặt trời.";
    const pages = readingPages(text, 10);
    expect(pages.length).toBeGreaterThan(1);
    expect(pages.join(" ")).toBe(text);
    expect(pages.some((page) => page.includes("Mèo không biết bay."))).toBe(
      true,
    );
  });
  it("giữ dòng thơ và không cắt một câu dài giữa chừng", () => {
    const poem =
      "Nắng lên trên lá\nChim hát trong cây\nBạn cùng đọc sách\nHọc điều hay này";
    const normalized = (value: string) => value.replace(/\s+/gu, " ").trim();
    expect(normalized(readingPages(poem, 8).join(" "))).toBe(normalized(poem));
    expect(readingPages("Một câu chưa có dấu kết thúc", 2)).toEqual([
      "Một câu chưa có dấu kết thúc",
    ]);
  });
  it("nhận từ hoàn chỉnh, không vẽ cam từ camera hoặc cá từ các", () => {
    expect(pictureWords("Các camera đang hoạt động.")).toEqual([]);
    expect(
      pictureWords("A cat, a dog, a book.").map((item) => item.code),
    ).toEqual(["cat", "dog", "book"]);
    expect(pictureWords("Mèo và cây.").map((item) => item.label)).toEqual([
      "mèo",
      "cây",
    ]);
    expect(pictureWords("Bút chì.").map((item) => item.code)).toEqual([
      "pencil",
    ]);
    expect(pictureWords("Bút mực.").map((item) => item.code)).toEqual(["pen"]);
  });
  it("chỉ minh họa phép cộng nhỏ chính xác, không hiểu nhầm thập phân/số âm", () => {
    expect(smallSum("Ví dụ: 2 + 3 = 5.")).toEqual({ a: 2, b: 3 });
    for (const text of ["2,5 + 3", "2.5 + 3", "-3 + 4", "125 + 4", "20 + 3"])
      expect(smallSum(text)).toBeNull();
  });
  it("tách đúng số có khoảng trắng và chỉ vẽ phân số có các phần bằng nhau", () => {
    expect(
      placeValuePicture("Trong số 325 418, chữ số 2 thuộc hàng chục nghìn."),
    ).toEqual([
      { digit: "3", label: "Trăm nghìn" },
      { digit: "2", label: "Chục nghìn" },
      { digit: "5", label: "Nghìn" },
      { digit: "4", label: "Trăm" },
      { digit: "1", label: "Chục" },
      { digit: "8", label: "Đơn vị" },
    ]);
    expect(placeValuePicture("Giá trị số 325,418 là thập phân.")).toBeNull();
    expect(fractionPicture("Ví dụ: 3/8 là ba phần trong tám phần.")).toEqual({
      numerator: 3,
      denominator: 8,
    });
    expect(fractionPicture("3/0")).toBeNull();
    expect(fractionPicture("5/3")).toBeNull();
  });
});
