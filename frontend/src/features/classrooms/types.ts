export type Classroom = {
  id: string;
  name: string;
  grade: number;
  academic_year: string;
  school_id: string | null;
  teacher_user_id: string | null;
  is_active: boolean;
  edit_revision: number;
  recognition_enabled: boolean;
  student_count: number;
};

export type Learner = {
  id: string;
  display_name: string;
  username: string;
  current_grade: number;
};

export type Rank = {
  rank: number;
  display_name: string;
  alias: string;
  score: number;
  completed: number;
  is_me: boolean;
};
