export type Account = {
  id: string;
  username: string;
  display_name: string;
  email: string | null;
  roles: string[];
  current_grade: number | null;
  text_size: string;
  is_active: boolean;
  account_revision: number;
  must_change_password: boolean;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
  auth_provider: string;
  password_changed_at: string | null;
};

export type History = {
  action: string;
  actor_username: string;
  created_at: string;
  old_values: Record<string, unknown> | null;
  new_values: Record<string, unknown>;
};

export type Detail = Account & { active_sessions: number; history: History[] };
