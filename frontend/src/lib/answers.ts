import type { Answer } from "./types";

// Clearing an input must also clear its answered indicator, including after reload.
export function hasAnswer(answer: Answer | null | undefined): boolean {
  if (!answer) return false;
  if ("text" in answer) return answer.text.trim().length > 0;
  if ("option_id" in answer) return answer.option_id.length > 0;
  if ("option_ids" in answer) return answer.option_ids.length > 0;
  if ("ordered_ids" in answer) return answer.ordered_ids.length > 0;
  return false;
}
