export function readingPages(text: string, limit = 55): string[] {
  const chunks = text
    .split(/(?<=\n)|(?<=[.!?])\s+/u)
    .filter((part) => part.trim());
  const pages: string[] = [];
  let current = "";
  for (const chunk of chunks) {
    if (current && `${current} ${chunk}`.trim().split(/\s+/u).length > limit) {
      pages.push(current.trim());
      current = "";
    }
    current += `${current && !current.endsWith("\n") ? " " : ""}${chunk}`;
  }
  if (current.trim()) pages.push(current.trim());
  return pages.length ? pages : [text];
}

export { pictureWords } from "./learning-pictures";

export function smallSum(text: string) {
  const match = /(?:^|[^\d.,−-])(\d{1,2})\s*\+\s*(\d{1,2})(?![\d.,])/u.exec(
    text,
  );
  if (!match) return null;
  const a = Number(match[1]),
    b = Number(match[2]);
  return a + b <= 20 ? { a, b } : null;
}

export function fractionPicture(text: string) {
  const match = /(?:^|[^\d/.,])(\d{1,2})\/(\d{1,2})(?![\d/.,])/u.exec(text);
  if (!match) return null;
  const numerator = Number(match[1]),
    denominator = Number(match[2]);
  return denominator >= 2 &&
    denominator <= 12 &&
    numerator >= 0 &&
    numerator <= denominator
    ? { numerator, denominator }
    : null;
}

export function placeValuePicture(text: string) {
  if (!/chữ số|hàng nghìn|giá trị.*số|hàng trăm/iu.test(text)) return null;
  const match =
    /(?:^|[^\p{L}\d.,−-])(\d{1,3}(?: \d{3}){1,2}|\d{3,6})(?!\d|[.,]\d)/u.exec(
      text,
    );
  if (!match) return null;
  const digits = match[1].replace(/\s/gu, "").split("");
  const labels = [
    "Đơn vị",
    "Chục",
    "Trăm",
    "Nghìn",
    "Chục nghìn",
    "Trăm nghìn",
    "Triệu",
    "Chục triệu",
    "Trăm triệu",
  ];
  return digits.map((digit, index) => ({
    digit,
    label: labels[digits.length - index - 1],
  }));
}
