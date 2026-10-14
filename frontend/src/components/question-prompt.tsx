"use client";
import { GuidedText } from "./guided-text";

export function QuestionPrompt({
  text,
  grade,
}: {
  text: string;
  grade?: number;
}) {
  // Authored reading questions separate the full passage and question with a
  // blank line. Preserve every preceding paragraph, including poem line breaks.
  const boundary = text.lastIndexOf("\n\n");
  if (boundary < 0 || !text.slice(boundary + 2).trim())
    return <h2 className="question-prompt">{text}</h2>;
  const passage = text
    .slice(0, boundary)
    .replace(/^Ngữ liệu của bài:\s*\n/u, "");
  const prompt = text.slice(boundary + 2);
  return (
    <>
      <h2 className="question-prompt">{prompt}</h2>
      <details className="question-reading" open>
        <summary>Bài đọc để tìm câu trả lời</summary>
        <GuidedText text={passage} grade={grade} />
      </details>
    </>
  );
}
