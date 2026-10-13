// Only concrete words have pictures. A whole sentence must never become a
// guessed answer or a misleading illustration of a different object.
const vocabulary = [
  ["cat", ["cat", "mèo", "con mèo"]],
  ["dog", ["dog", "chó", "con chó"]],
  ["bird", ["bird", "chim", "con chim"]],
  ["fish", ["fish", "cá", "con cá"]],
  ["rabbit", ["rabbit", "thỏ", "con thỏ"]],
  ["turtle", ["turtle", "rùa", "con rùa"]],
  ["apple", ["apple", "táo", "quả táo"]],
  ["orange", ["orange", "cam", "quả cam"]],
  ["banana", ["banana", "chuối", "quả chuối"]],
  ["book", ["book", "sách", "quyển sách"]],
  ["pencil", ["pencil", "bút chì"]],
  ["pen", ["pen", "bút mực", "bút"]],
  ["plant", ["plant", "cây"]],
  ["house", ["house", "ngôi nhà"]],
  ["sun", ["sun", "mặt trời", "sunny", "có nắng"]],
  ["clock", ["clock", "đồng hồ"]],
  ["ball", ["ball", "quả bóng"]],
  ["schoolbag", ["bag", "schoolbag", "cặp sách", "cặp"]],
  ["ruler", ["ruler", "thước kẻ", "thước"]],
  ["eraser", ["eraser", "cục tẩy", "tẩy"]],
  ["desk", ["desk", "bàn học"]],
  ["chair", ["chair", "ghế"]],
  ["school", ["school", "trường học"]],
  ["bus", ["bus", "xe buýt"]],
  ["bicycle", ["bicycle", "bike", "xe đạp"]],
  ["car", ["car", "ô tô", "xe hơi"]],
  ["rain", ["rain", "rainy", "có mưa", "mưa"]],
  ["cloud", ["cloud", "đám mây", "cloudy", "nhiều mây"]],
  ["flower", ["flower", "bông hoa"]],
  ["milk", ["milk", "sữa"]],
  ["water", ["water", "nước uống"]],
  ["bread", ["bread", "bánh mì"]],
  ["egg", ["egg", "trứng", "quả trứng"]],
  ["circle", ["circle", "hình tròn"]],
  ["square", ["square", "hình vuông"]],
  ["triangle", ["triangle", "hình tam giác"]],
  ["rectangle", ["rectangle", "hình chữ nhật"]],
] as const;

const colors = [
  ["red", "đỏ"],
  ["blue", "xanh dương", "xanh da trời"],
  ["green", "xanh lá", "xanh lá cây"],
  ["yellow", "vàng"],
  ["purple", "tím"],
  ["pink", "hồng"],
  ["brown", "nâu"],
  ["black", "đen"],
  ["white", "trắng"],
] as const;

function normalizedLabel(text: string) {
  return text
    .toLocaleLowerCase("vi")
    .normalize("NFC")
    .trim()
    .replace(/^[^\p{L}\p{N}]+/u, "")
    .replace(/[.!?]+$/u, "")
    .trim()
    .replace(/\s+/gu, " ");
}

export function pictureForLabel(text: string) {
  const label = normalizedLabel(text);
  for (const [code, ...names] of colors) {
    if ([code, ...names, ...names.map((name) => `màu ${name}`)].includes(label))
      return { code: `color-${code}`, label };
  }
  for (const [code, names] of vocabulary) {
    if (
      names.some(
        (name) =>
          label === name || label === `a ${name}` || label === `an ${name}`,
      )
    )
      return { code, label };
  }
  return null;
}

export function pictureWords(text: string) {
  const lower = text.toLocaleLowerCase("vi").normalize("NFC");
  return vocabulary
    .flatMap(([code, names]) => {
      const label = names.find((word) =>
        new RegExp(
          `(^|[^\\p{L}])${word}${word === "bút" ? "(?!\\s+chì)" : ""}([^\\p{L}]|$)`,
          "u",
        ).test(lower),
      );
      return label ? [{ code, label }] : [];
    })
    .slice(0, 4);
}
