import type { Options, Payload } from "@/features/lessons/types";

export function initial(options: Options, grade: number): Payload {
  const topic = options.topics[0];
  return {
    code: "",
    grade,
    subject_id: topic?.subject_id || options.subjects[0]?.id || "",
    topic_id: topic?.id || "",
    skill_ids: options.skills
      .filter((s) => s.topic_id === topic?.id)
      .map((s) => s.id),
    title: "",
    description: "",
    estimated_minutes: 15,
    sort_order: 100,
    minimum_plan_code: "free",
    learning_level: "basic",
    preview: { summary: "", goals: [] },
    content: {
      blocks: [
        { type: "text", title: "Cùng khám phá", text: "" },
        { type: "example", title: "Thử với ví dụ", text: "" },
        { type: "remember", title: "Em ghi nhớ", text: "" },
        { type: "practice", title: "Tự luyện tập", text: "" },
      ],
      goals: [],
      hints: [],
      reflection: [],
      illustration: null,
    },
  };
}

export const lines = (value: string) => value.split("\n");
