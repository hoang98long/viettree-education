import type { LessonContent } from "@/lib/types";

export type Options = {
  subjects: { id: string; code: string; name_vi: string }[];
  topics: { id: string; subject_id: string; title: string }[];
  skills: { id: string; subject_id: string; topic_id: string; name: string }[];
};

export type Payload = {
  code: string;
  grade: number;
  subject_id: string;
  topic_id: string;
  skill_ids: string[];
  title: string;
  description: string;
  estimated_minutes: number;
  sort_order: number;
  minimum_plan_code: "free" | "vip";
  learning_level: "basic" | "reinforcement" | "advanced";
  preview: { summary?: string; goals?: string[] };
  content: LessonContent;
};

export type Draft = {
  id: string;
  lesson_status: string;
  draft_status: string;
  edit_revision: number;
  source_fingerprint: string;
  source_changed: boolean;
  payload: Payload;
  history: {
    action: string;
    created_at: string;
    actor_name: string | null;
    reason: string;
  }[];
};

export type Summary = {
  id: string;
  title: string;
  code: string;
  status: string;
  draft_status: string | null;
  subject_name: string;
  topic_title: string;
  minimum_plan_code: string | null;
};
