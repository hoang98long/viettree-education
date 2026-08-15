-- ============================================================
-- VietTree Education
-- PostgreSQL Initial Schema v1
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- ENUMS
-- ============================================================

CREATE TYPE user_role AS ENUM (
    'student',
    'parent',
    'teacher',
    'admin'
);

CREATE TYPE user_status AS ENUM (
    'active',
    'inactive',
    'suspended'
);

CREATE TYPE content_type AS ENUM (
    'text',
    'image',
    'audio',
    'video',
    'example',
    'exercise',
    'quiz'
);

CREATE TYPE question_type AS ENUM (
    'single_choice',
    'multiple_choice',
    'true_false',
    'fill_blank',
    'numeric',
    'matching'
);

CREATE TYPE difficulty_level AS ENUM (
    'easy',
    'medium',
    'hard'
);

CREATE TYPE attempt_status AS ENUM (
    'in_progress',
    'completed',
    'abandoned'
);

CREATE TYPE progress_status AS ENUM (
    'not_started',
    'in_progress',
    'completed'
);

-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email VARCHAR(255) UNIQUE,
    username VARCHAR(100) UNIQUE,

    password_hash TEXT NOT NULL,

    full_name VARCHAR(255) NOT NULL,

    role user_role NOT NULL,

    status user_status NOT NULL DEFAULT 'active',

    avatar_url TEXT,

    last_login_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_role
    ON users(role);

CREATE INDEX idx_users_status
    ON users(status);

-- ============================================================
-- STUDENTS
-- ============================================================

CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL UNIQUE
        REFERENCES users(id)
        ON DELETE CASCADE,

    date_of_birth DATE,

    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 5),

    school_name VARCHAR(255),

    xp INT NOT NULL DEFAULT 0 CHECK (xp >= 0),

    level INT NOT NULL DEFAULT 1 CHECK (level >= 1),

    current_streak INT NOT NULL DEFAULT 0 CHECK (current_streak >= 0),

    longest_streak INT NOT NULL DEFAULT 0 CHECK (longest_streak >= 0),

    last_learning_date DATE,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_students_grade
    ON students(grade);

-- ============================================================
-- PARENTS
-- ============================================================

CREATE TABLE parents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL UNIQUE
        REFERENCES users(id)
        ON DELETE CASCADE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TEACHERS
-- ============================================================

CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL UNIQUE
        REFERENCES users(id)
        ON DELETE CASCADE,

    school_name VARCHAR(255),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- PARENT <-> STUDENT
-- ============================================================

CREATE TABLE parent_students (
    parent_id UUID NOT NULL
        REFERENCES parents(id)
        ON DELETE CASCADE,

    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    relationship VARCHAR(50),

    is_primary BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (parent_id, student_id)
);

CREATE INDEX idx_parent_students_student
    ON parent_students(student_id);

-- ============================================================
-- SUBJECTS
-- ============================================================

CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(50) NOT NULL UNIQUE,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    icon_url TEXT,

    display_order INT NOT NULL DEFAULT 0,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- COURSES
-- ============================================================

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    subject_id UUID NOT NULL
        REFERENCES subjects(id)
        ON DELETE RESTRICT,

    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 5),

    title VARCHAR(255) NOT NULL,

    description TEXT,

    thumbnail_url TEXT,

    display_order INT NOT NULL DEFAULT 0,

    is_published BOOLEAN NOT NULL DEFAULT FALSE,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_courses_subject
    ON courses(subject_id);

CREATE INDEX idx_courses_grade
    ON courses(grade);

-- ============================================================
-- LESSONS
-- ============================================================

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    course_id UUID NOT NULL
        REFERENCES courses(id)
        ON DELETE CASCADE,

    title VARCHAR(255) NOT NULL,

    description TEXT,

    lesson_number INT NOT NULL,

    estimated_minutes INT,

    difficulty difficulty_level NOT NULL DEFAULT 'easy',

    is_published BOOLEAN NOT NULL DEFAULT FALSE,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(course_id, lesson_number)
);

CREATE INDEX idx_lessons_course
    ON lessons(course_id);

-- ============================================================
-- LESSON CONTENTS
-- ============================================================

CREATE TABLE lesson_contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lesson_id UUID NOT NULL
        REFERENCES lessons(id)
        ON DELETE CASCADE,

    content_type content_type NOT NULL,

    title VARCHAR(255),

    content TEXT,

    media_url TEXT,

    display_order INT NOT NULL DEFAULT 0,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lesson_contents_lesson
    ON lesson_contents(lesson_id);

CREATE INDEX idx_lesson_contents_order
    ON lesson_contents(lesson_id, display_order);

-- ============================================================
-- EXERCISES
-- ============================================================

CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lesson_id UUID NOT NULL
        REFERENCES lessons(id)
        ON DELETE CASCADE,

    title VARCHAR(255),

    description TEXT,

    difficulty difficulty_level NOT NULL DEFAULT 'easy',

    points INT NOT NULL DEFAULT 1 CHECK (points >= 0),

    display_order INT NOT NULL DEFAULT 0,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_exercises_lesson
    ON exercises(lesson_id);

-- ============================================================
-- QUESTIONS
-- ============================================================

CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    exercise_id UUID NOT NULL
        REFERENCES exercises(id)
        ON DELETE CASCADE,

    question_type question_type NOT NULL,

    question_text TEXT NOT NULL,

    explanation TEXT,

    hint TEXT,

    difficulty difficulty_level NOT NULL DEFAULT 'easy',

    points INT NOT NULL DEFAULT 1 CHECK (points >= 0),

    display_order INT NOT NULL DEFAULT 0,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_questions_exercise
    ON questions(exercise_id);

-- ============================================================
-- QUESTION OPTIONS
-- ============================================================

CREATE TABLE question_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    question_id UUID NOT NULL
        REFERENCES questions(id)
        ON DELETE CASCADE,

    option_text TEXT NOT NULL,

    option_value VARCHAR(255),

    is_correct BOOLEAN NOT NULL DEFAULT FALSE,

    display_order INT NOT NULL DEFAULT 0,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_question_options_question
    ON question_options(question_id);

-- ============================================================
-- QUIZZES
-- ============================================================

CREATE TABLE quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    lesson_id UUID NOT NULL
        REFERENCES lessons(id)
        ON DELETE CASCADE,

    title VARCHAR(255) NOT NULL,

    description TEXT,

    passing_score NUMERIC(5,2),

    time_limit_seconds INT,

    max_attempts INT,

    is_published BOOLEAN NOT NULL DEFAULT FALSE,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_quizzes_lesson
    ON quizzes(lesson_id);

-- ============================================================
-- QUIZ QUESTIONS
-- ============================================================

CREATE TABLE quiz_questions (
    quiz_id UUID NOT NULL
        REFERENCES quizzes(id)
        ON DELETE CASCADE,

    question_id UUID NOT NULL
        REFERENCES questions(id)
        ON DELETE CASCADE,

    display_order INT NOT NULL DEFAULT 0,

    points INT NOT NULL DEFAULT 1 CHECK (points >= 0),

    PRIMARY KEY (quiz_id, question_id)
);

CREATE INDEX idx_quiz_questions_order
    ON quiz_questions(quiz_id, display_order);

-- ============================================================
-- EXERCISE ATTEMPTS
-- ============================================================

CREATE TABLE exercise_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    exercise_id UUID NOT NULL
        REFERENCES exercises(id)
        ON DELETE CASCADE,

    status attempt_status NOT NULL DEFAULT 'in_progress',

    score NUMERIC(7,2),

    max_score NUMERIC(7,2),

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    completed_at TIMESTAMPTZ,

    time_spent_seconds INT,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_exercise_attempts_student
    ON exercise_attempts(student_id);

CREATE INDEX idx_exercise_attempts_exercise
    ON exercise_attempts(exercise_id);

-- ============================================================
-- ANSWER SUBMISSIONS
-- ============================================================

CREATE TABLE answer_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    attempt_id UUID NOT NULL
        REFERENCES exercise_attempts(id)
        ON DELETE CASCADE,

    question_id UUID NOT NULL
        REFERENCES questions(id)
        ON DELETE CASCADE,

    answer_text TEXT,

    selected_option_ids UUID[],

    is_correct BOOLEAN,

    score NUMERIC(7,2),

    answered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_answer_submissions_attempt
    ON answer_submissions(attempt_id);

CREATE INDEX idx_answer_submissions_question
    ON answer_submissions(question_id);

-- ============================================================
-- QUIZ ATTEMPTS
-- ============================================================

CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    quiz_id UUID NOT NULL
        REFERENCES quizzes(id)
        ON DELETE CASCADE,

    status attempt_status NOT NULL DEFAULT 'in_progress',

    score NUMERIC(7,2),

    max_score NUMERIC(7,2),

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    completed_at TIMESTAMPTZ,

    time_spent_seconds INT,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_quiz_attempts_student
    ON quiz_attempts(student_id);

CREATE INDEX idx_quiz_attempts_quiz
    ON quiz_attempts(quiz_id);

-- ============================================================
-- LEARNING PROGRESS
-- ============================================================

CREATE TABLE learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    lesson_id UUID NOT NULL
        REFERENCES lessons(id)
        ON DELETE CASCADE,

    status progress_status NOT NULL DEFAULT 'not_started',

    progress_percent NUMERIC(5,2) NOT NULL DEFAULT 0
        CHECK (progress_percent BETWEEN 0 AND 100),

    best_score NUMERIC(7,2),

    attempts_count INT NOT NULL DEFAULT 0
        CHECK (attempts_count >= 0),

    time_spent_seconds BIGINT NOT NULL DEFAULT 0
        CHECK (time_spent_seconds >= 0),

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    last_accessed_at TIMESTAMPTZ,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(student_id, lesson_id)
);

CREATE INDEX idx_learning_progress_student
    ON learning_progress(student_id);

CREATE INDEX idx_learning_progress_status
    ON learning_progress(student_id, status);

-- ============================================================
-- LEARNING SESSIONS
-- ============================================================

CREATE TABLE learning_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    lesson_id UUID
        REFERENCES lessons(id)
        ON DELETE SET NULL,

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    ended_at TIMESTAMPTZ,

    duration_seconds INT,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_learning_sessions_student
    ON learning_sessions(student_id);

CREATE INDEX idx_learning_sessions_started
    ON learning_sessions(started_at);

-- ============================================================
-- ACHIEVEMENTS
-- ============================================================

CREATE TABLE achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(100) NOT NULL UNIQUE,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    icon_url TEXT,

    xp_reward INT NOT NULL DEFAULT 0
        CHECK (xp_reward >= 0),

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- STUDENT ACHIEVEMENTS
-- ============================================================

CREATE TABLE student_achievements (
    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    achievement_id UUID NOT NULL
        REFERENCES achievements(id)
        ON DELETE CASCADE,

    earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    PRIMARY KEY (student_id, achievement_id)
);

CREATE INDEX idx_student_achievements_student
    ON student_achievements(student_id);

-- ============================================================
-- XP TRANSACTIONS
-- ============================================================

CREATE TABLE xp_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id UUID NOT NULL
        REFERENCES students(id)
        ON DELETE CASCADE,

    amount INT NOT NULL,

    reason VARCHAR(255) NOT NULL,

    reference_type VARCHAR(100),

    reference_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_xp_transactions_student
    ON xp_transactions(student_id);

CREATE INDEX idx_xp_transactions_created
    ON xp_transactions(created_at);

-- ============================================================
-- REFRESH TOKENS
-- ============================================================

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    token_hash TEXT NOT NULL UNIQUE,

    expires_at TIMESTAMPTZ NOT NULL,

    revoked_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_user
    ON refresh_tokens(user_id);

CREATE INDEX idx_refresh_tokens_expires
    ON refresh_tokens(expires_at);

-- ============================================================
-- FILE ASSETS
-- ============================================================

CREATE TABLE file_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    storage_provider VARCHAR(50) NOT NULL DEFAULT 'minio',

    storage_bucket VARCHAR(255) NOT NULL,

    storage_key TEXT NOT NULL UNIQUE,

    original_filename VARCHAR(255),

    content_type VARCHAR(100),

    file_size BIGINT,

    uploaded_by UUID
        REFERENCES users(id)
        ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_file_assets_uploaded_by
    ON file_assets(uploaded_by);

-- ============================================================
-- SEED SUBJECTS
-- ============================================================

INSERT INTO subjects (
    code,
    name,
    description,
    display_order
)
VALUES
(
    'math',
    'Toán',
    'Môn Toán dành cho học sinh tiểu học',
    1
),
(
    'vietnamese',
    'Tiếng Việt',
    'Môn Tiếng Việt dành cho học sinh tiểu học',
    2
),
(
    'english',
    'Tiếng Anh',
    'Môn Tiếng Anh dành cho học sinh tiểu học',
    3
)
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- SEED ACHIEVEMENTS
-- ============================================================

INSERT INTO achievements (
    code,
    name,
    description,
    xp_reward
)
VALUES
(
    'FIRST_LESSON',
    'Bài học đầu tiên',
    'Hoàn thành bài học đầu tiên',
    50
),
(
    'FIRST_QUIZ',
    'Quiz đầu tiên',
    'Hoàn thành bài quiz đầu tiên',
    50
),
(
    'SEVEN_DAY_STREAK',
    '7 ngày liên tiếp',
    'Học tập liên tục trong 7 ngày',
    200
),
(
    'MATH_STAR',
    'Ngôi sao Toán học',
    'Hoàn thành các bài Toán đầu tiên',
    100
),
(
    'ENGLISH_STAR',
    'English Star',
    'Hoàn thành các bài Tiếng Anh đầu tiên',
    100
)
ON CONFLICT (code) DO NOTHING;