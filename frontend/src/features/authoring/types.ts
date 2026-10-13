import type { Content, QuestionKind } from "@/lib/types";

export type Options = {
  subjects: { id: string; code: string; name_vi: string }[];
  topics: { id: string; subject_id: string; title: string }[];
  skills: { id: string; subject_id: string; topic_id: string; name: string }[];
  lessons: { id: string; topic_id: string; title: string }[];
};

export type QuestionDraft = {
  id: string;
  question_id: string;
  code: string;
  grade: number;
  subject_id: string;
  topic_id: string;
  skill_ids: string[];
  question_type: QuestionKind;
  difficulty: number;
  content: Content;
  grading: Record<string, unknown>;
  explanation: { text: string };
  status: string;
  version: number;
  reviewed_by: string | null;
  minimum_plan_code: string;
  updated_at: string;
  edit_revision: number;
};

export type AssessmentDraft = {
  id: string;
  code: string;
  grade: number;
  subject_id: string;
  topic_id: string;
  lesson_id: string | null;
  title: string;
  description: string | null;
  status: string;
  assessment_type: string;
  time_limit_seconds: number | null;
  max_attempts: number;
  minimum_plan_code: string;
  learning_level: string;
  preview: { summary?: string; goals?: string[] };
  reviewed: boolean;
  updated_at: string;
  edit_revision: number;
  effective_access: { minimum_plan_code: string | null };
  items: {
    question_version_id: string;
    points: number;
    question: QuestionDraft;
  }[];
};
