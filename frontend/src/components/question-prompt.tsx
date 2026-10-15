"use client";
import { GuidedText } from "./guided-text";

export function QuestionPrompt({
  text,
  grade,
  headingLevel = 2,
}: {
  text: string;
  grade?: number;
  headingLevel?: 2 | 3;
}) {
  const Heading = headingLevel === 3 ? "h3" : "h2";
  // Authored reading questions separate the full passage and question with a
  // blank line. Preserve every preceding paragraph, including poem line breaks.
  const boundary = text.lastIndexOf("\n\n");
  if (boundary < 0 || !text.slice(boundary + 2).trim())
    return <Heading className="question-prompt">{text}</Heading>;
  const passage = text
    .slice(0, boundary)
    .replace(/^Ngữ liệu của bài:\s*\n/u, "");
  const prompt = text.slice(boundary + 2);
  return (
    <>
      <Heading className="question-prompt">{prompt}</Heading>
      <details className="question-reading" open>
        <summary>Bài đọc để tìm câu trả lời</summary>
        <GuidedText text={passage} grade={grade} />
      </details>
    </>
  );
}
