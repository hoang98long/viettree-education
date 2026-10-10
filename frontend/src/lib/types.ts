export type TextSize = "comfortable" | "large";
export type User = {
  id: string;
  username: string;
  display_name: string;
  roles: string[];
  text_size: TextSize;
  session_expires_at?: string | null;
};
export type Subject = {
  id: string;
  code: string;
  name_vi: string;
  topic_count: number;
  grade: number;
  status: string;
};
export type Topic = {
  id: string;
  title: string;
  code: string;
  sort_order: number;
};
export type ContentAccess = {
  minimum_plan_code: "free" | "vip" | null;
  learning_level: "basic" | "reinforcement" | "advanced";
  locked: boolean;
  lock_reason: string | null;
};
export type LessonSummary = ContentAccess & {
  id: string;
  topic_id: string;
  title: string;
  estimated_minutes: number;
  status: string;
};
export type Assessment = ContentAccess & {
  id: string;
  title: string;
  description: string;
  subject_code: string;
  subject_name: string;
  grade: number;
  topic_id: string;
  lesson_id: string;
  status: string;
  item_count: number;
  max_attempts: number;
  time_limit_seconds: number | null;
  attempt_count?: number;
  assessment_type: string;
};
export type Recommendation = {
  assessment_id: string;
  title: string;
  explanation: string;
  reason_code: string;
};
export type History = {
  id: string;
  title: string;
  status: string;
  total_score: number;
  max_score: number;
  started_at: string;
  graded_at: string | null;
  subject_name: string;
  subject_code: string;
};
export type Skill = {
  skill_id: string;
  name: string;
  subject_name: string;
  mastery_score: number;
  confidence: number;
  questions_attempted: number;
  correct_count: number;
  next_review_at: string;
};
export type Assignment = {
  id: string;
  assessment_id: string;
  title: string;
  status: string;
  available_at: string;
  due_at: string | null;
};
export type Dashboard = {
  user: User;
  grade: number;
  subjects: Subject[];
  history: History[];
  skills: Skill[];
  recommendations: Recommendation[];
  assignments: Assignment[];
  completed_lessons: number;
  continue_lesson: { id: string; title: string } | null;
};
export type QuestionKind =
  "single_choice" | "multiple_choice" | "fill_blank" | "ordering";
export type Answer =
  | { option_id: string }
  | { option_ids: string[] }
  | { text: string }
  | { ordered_ids: string[] };
export type Content = {
  prompt: string;
  options?: { id: string; text: string }[];
};
export type AttemptItem = {
  id: string;
  position: number;
  points: number;
  question_version_id: string;
  question_type: QuestionKind;
  content: Content;
  answer: Answer | null;
};
export type Attempt = {
  id: string;
  assignment_id: string;
  assessment_id: string;
  title: string;
  status: string;
  deadline: string | null;
  items: AttemptItem[];
};
export type Result = {
  id: string;
  total_score: number;
  max_score: number;
  correct_count: number;
  answered_count: number;
  graded_at: string;
  items: (AttemptItem & {
    student_answer: Answer;
    is_correct: boolean;
    score: number;
    explanation: { text: string };
    grading: Record<string, unknown>;
  })[];
};
export type Lesson = LessonSummary & {
  progress_status: "not_started" | "in_progress" | "completed";
  content: LessonContent;
  grade: number;
  subject_code: string;
  subject_name: string;
  topic_title: string;
  practice: { id: string; title: string }[];
  next_lessons: { id: string; title: string; reason: string }[];
};
export type LessonIllustration = {
  kind: "fraction" | "garden" | "reading" | "clock" | "bars" | "angles";
  caption: string;
  numerator: number;
  denominator: number;
  rows: number;
  columns: number;
  hour: number;
  minute: number;
  angle?: number;
  tick?: number;
  labels?: string[];
  values?: number[];
};
export type LessonContent = {
  category?: "core" | "thinking";
  blocks: {
    type: "text" | "example" | "remember" | "practice";
    title: string;
    text: string;
  }[];
  goals?: string[];
  hints?: string[];
  reflection?: string[];
  illustration?: LessonIllustration | null;
};
export type LearningPlan = {
  id: string;
  title: string;
  subject_code: string;
  subject_name: string;
  status: "active" | "completed" | "paused";
  mode: "basic" | "adaptive";
  explanation: string;
  start_date: string;
  end_date: string;
  completed_count: number;
  items: {
    id: string;
    position: number;
    lesson_id: string | null;
    assessment_id: string | null;
    title: string;
    status: "pending" | "in_progress" | "completed";
    due_at: string;
    completed_at: string | null;
    locked: boolean;
    lock_reason: string | null;
  }[];
};
export type Membership = {
  student_id: string;
  plan_code: "free" | "vip";
  status: "free" | "active" | "expired" | "revoked";
  subscription_plan_code: string | null;
  starts_at: string | null;
  ends_at: string | null;
  features: string[];
};
export type MembershipPlan = { code: string; name: string; features: string[] };
export type VipLibrary = {
  grade: number;
  membership: Membership;
  lessons: {
    id: string;
    title: string;
    subject_code: string;
    subject_name: string;
    topic_title: string;
    estimated_minutes: number;
    progress_status: string;
  }[];
};
export type VipMistakes = {
  total: number;
  page: number;
  page_size: number;
  items: {
    id: string;
    attempt_id: string;
    question_version_id: string;
    question_type: QuestionKind;
    content: Content;
    student_answer: Answer;
    subject_name: string;
    subject_code: string;
    assessment_title: string;
    graded_at: string;
  }[];
};
export type VipReport = {
  student_name: string;
  grade: number;
  days: number;
  starts_at: string;
  ends_at: string;
  attempt_count: number;
  score_percent: number | null;
  completed_lessons: number;
  active_days: number;
  previous: { attempt_count: number; score_percent: number | null };
  daily: {
    date: string;
    attempt_count: number;
    score_percent: number | null;
  }[];
  subjects: {
    subject_code: string;
    subject_name: string;
    attempt_count: number;
    score_percent: number | null;
  }[];
  weak_skills: {
    skill_id: string;
    name: string;
    subject_name: string;
    mastery_score: number;
    confidence: number;
    questions_attempted: number;
  }[];
};
export type LessonPreview = ContentAccess & {
  id: string;
  title: string;
  estimated_minutes: number;
  grade: number;
  subject_name: string;
  preview: { summary: string; goals: string[] };
};
export type Statistics = {
  students: number;
  users: number;
  lessons: number;
  question_versions: number;
  assessments: number;
  attempts: number;
  average_percent: number | null;
  correct_answers: number;
};
export type Student = {
  id: string;
  username: string;
  display_name: string;
  current_grade: number;
  is_active: boolean;
};
export type Question = {
  id: string;
  code: string;
  grade: number;
  question_type: string;
  difficulty: number;
  status: string;
  subject_name: string;
  content: Content;
  grading?: Record<string, unknown>;
  explanation?: { text: string };
  version: number;
  question_id: string;
  reviewed_by: string | null;
  minimum_plan_code: "free" | "vip" | null;
};
export type Page<T> = { total: number; page: number; items: T[] };
export type Curriculum = {
  subjects: { id: string; code: string; name_vi: string }[];
  topics: (Topic & { subject_id: string })[];
  lessons: LessonSummary[];
  skills: { id: string; name: string; subject_id: string }[];
};
