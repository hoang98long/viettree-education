import type { ContentAccess } from "@/lib/types";

export type ThinkingLesson = ContentAccess & {
  id: string;
  title: string;
  subject_code: string;
  subject_name: string;
  estimated_minutes: number;
  progress_status: string | null;
};

export type MapRow = {
  code: string;
  subject_code: string;
  subject_name: string;
  title: string;
  focus: string;
  active: boolean;
  free_lessons: number;
  vip_lessons: number;
  unconfigured_lessons: number;
  questions: number;
  assessments: number;
  source_url: string;
};
