export type CatalogLesson = {
  minimum_plan_code: "free" | "vip";
  locked: boolean;
  id: string;
  code: string;
  title: string;
  unit_id: string;
  unit_code: string;
  unit_cover?: string;
  unit_title: string;
  unit_position: number;
  position: number;
  hero: string;
  minutes: number;
  progress: { next_step: number; completed_at: string | null } | null;
};
export type Activity = {
  kind: string;
  instruction: string;
  choices: string[];
  items: { id: string; text: string; asset?: string; answer?: string }[];
  explanation?: string;
  hints?: string[];
};
export type Question = {
  id: string;
  prompt: string;
  options: string[];
  answer?: number;
  explanation?: string;
};
export type Step = {
  id: string;
  kind: string;
  title: string;
  text: string;
  details_text?: string | null;
  media: string[];
  activity?: Activity | null;
  questions: Question[];
};
export type LessonContent = {
  objectives: string[];
  hero: string;
  cards: string[];
  steps: Step[];
  support: string;
  standard: string;
  advanced: string;
  teacher_guide?: string;
  materials: string[];
  safety_notes: string;
  [key: string]: unknown;
};
export type PlayerData = {
  passed_steps?: string[];
  flags?: Record<string, boolean>;
  lesson: { id: string; code: string; title: string; grade: number };
  content: LessonContent;
  progress: { next_step: number; completed_at: string | null };
};
export type Feedback = {
  score: number;
  feedback: {
    passed: boolean;
    message: string;
    items: { id: string; correct: boolean; explanation: string }[];
  };
};
export const base = "/ai-academy";
