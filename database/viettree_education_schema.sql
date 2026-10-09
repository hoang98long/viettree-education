-- ============================================================================
-- VIETTREE EDUCATION | PostgreSQL Database Schema v1.0
-- Target database : "viettree-education" (must already exist)
-- Compatible      : PostgreSQL 14+ (recommended 15/16/17)
-- Import example  : psql -h localhost -U postgres -d "viettree-education" \
--                   -v ON_ERROR_STOP=1 -f viettree_education_schema.sql
--
-- IMPORTANT:
--   1. Run this file WHILE CONNECTED TO database "viettree-education".
--      It does not create/drop databases or drop tables.
--   2. IDs are UUID. Content/answers/explanations are JSONB, media is in S3/MinIO.
--   3. Never expose question_versions.grading to students. Use the backend to
--      authorize requests and score submissions. The public-content view below
--      explicitly omits grading data.
--   4. No example student accounts, passwords or submitted answers are inserted.
--   5. Use Alembic migrations for schema changes after first deployment.
-- ============================================================================

BEGIN;
SET LOCAL search_path TO public;

-- ======================== A. USERS AND SCHOOLS ===============================

CREATE TABLE IF NOT EXISTS users (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username             VARCHAR(80) NOT NULL,
    email                VARCHAR(255),
    password_hash        TEXT,
    auth_provider        VARCHAR(30) NOT NULL DEFAULT 'local',
    external_subject     VARCHAR(255),
    display_name         VARCHAR(160) NOT NULL,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at        TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_users_username CHECK (LENGTH(BTRIM(username)) >= 3),
    CONSTRAINT chk_users_name CHECK (LENGTH(BTRIM(display_name)) > 0),
    CONSTRAINT chk_users_provider CHECK (LENGTH(BTRIM(auth_provider)) > 0)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_users_username_lower
    ON users (LOWER(username));
CREATE UNIQUE INDEX IF NOT EXISTS uq_users_email_lower
    ON users (LOWER(email)) WHERE email IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_users_external_identity
    ON users (auth_provider, external_subject) WHERE external_subject IS NOT NULL;

CREATE TABLE IF NOT EXISTS user_roles (
    user_id              UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role                 VARCHAR(20) NOT NULL,
    assigned_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, role),
    CONSTRAINT chk_user_roles_role
        CHECK (role IN ('student', 'guardian', 'teacher', 'admin'))
);
CREATE INDEX IF NOT EXISTS idx_user_roles_role ON user_roles(role);

CREATE TABLE IF NOT EXISTS schools (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                 VARCHAR(60) UNIQUE,
    name                 VARCHAR(255) NOT NULL,
    province             VARCHAR(100),
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS student_profiles (
    student_id           UUID PRIMARY KEY REFERENCES users(id) ON DELETE RESTRICT,
    school_id            UUID REFERENCES schools(id) ON DELETE SET NULL,
    current_grade        SMALLINT NOT NULL,
    learning_preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
    accessibility_options JSONB NOT NULL DEFAULT '{}'::jsonb,
    joined_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_student_grade CHECK (current_grade BETWEEN 1 AND 5),
    CONSTRAINT chk_student_preferences CHECK (jsonb_typeof(learning_preferences) = 'object'),
    CONSTRAINT chk_student_accessibility CHECK (jsonb_typeof(accessibility_options) = 'object')
);
CREATE INDEX IF NOT EXISTS idx_student_profiles_school_grade
    ON student_profiles(school_id, current_grade);

CREATE TABLE IF NOT EXISTS guardian_students (
    guardian_user_id     UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    relationship         VARCHAR(30) NOT NULL DEFAULT 'guardian',
    is_primary           BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at          TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (guardian_user_id, student_id),
    CONSTRAINT chk_guardian_relation
        CHECK (relationship IN ('mother', 'father', 'guardian', 'other')),
    CONSTRAINT chk_guardian_not_same CHECK (guardian_user_id <> student_id)
);
CREATE INDEX IF NOT EXISTS idx_guardian_students_student ON guardian_students(student_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_primary_guardian_per_student
    ON guardian_students(student_id) WHERE is_primary;

CREATE TABLE IF NOT EXISTS classes (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id            UUID REFERENCES schools(id) ON DELETE SET NULL,
    teacher_user_id      UUID REFERENCES users(id) ON DELETE SET NULL,
    code                 VARCHAR(80) NOT NULL,
    name                 VARCHAR(160) NOT NULL,
    grade                SMALLINT NOT NULL,
    academic_year        VARCHAR(20),
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_classes_grade CHECK (grade BETWEEN 1 AND 5)
);
CREATE INDEX IF NOT EXISTS idx_classes_school_grade ON classes(school_id, grade);
CREATE INDEX IF NOT EXISTS idx_classes_teacher ON classes(teacher_user_id);

CREATE TABLE IF NOT EXISTS class_enrollments (
    class_id             UUID NOT NULL REFERENCES classes(id) ON DELETE RESTRICT,
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    enrolled_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    left_at              TIMESTAMPTZ,
    PRIMARY KEY (class_id, student_id),
    CONSTRAINT chk_class_enrollment_dates CHECK (left_at IS NULL OR left_at >= enrolled_at)
);
CREATE INDEX IF NOT EXISTS idx_enrollments_student ON class_enrollments(student_id);

-- ======================== B. LEARNING CONTENT =================================

CREATE TABLE IF NOT EXISTS subjects (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                 VARCHAR(40) NOT NULL UNIQUE,
    name_vi              VARCHAR(160) NOT NULL,
    description          TEXT,
    sort_order           INTEGER NOT NULL DEFAULT 0,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS topics (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id           UUID NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    parent_topic_id      UUID REFERENCES topics(id) ON DELETE RESTRICT,
    grade                SMALLINT NOT NULL,
    code                 VARCHAR(100) NOT NULL,
    title                VARCHAR(255) NOT NULL,
    description          TEXT,
    sort_order           INTEGER NOT NULL DEFAULT 0,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_topics_code UNIQUE (subject_id, grade, code),
    CONSTRAINT chk_topics_grade CHECK (grade BETWEEN 1 AND 5),
    CONSTRAINT chk_topics_parent CHECK (parent_topic_id IS NULL OR parent_topic_id <> id)
);
CREATE INDEX IF NOT EXISTS idx_topics_subject_grade
    ON topics(subject_id, grade, sort_order);
CREATE INDEX IF NOT EXISTS idx_topics_parent ON topics(parent_topic_id);

CREATE TABLE IF NOT EXISTS lessons (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id             UUID NOT NULL REFERENCES topics(id) ON DELETE RESTRICT,
    code                 VARCHAR(100) NOT NULL,
    title                VARCHAR(255) NOT NULL,
    description          TEXT,
    content              JSONB NOT NULL DEFAULT '{}'::jsonb,
    sort_order           INTEGER NOT NULL DEFAULT 0,
    estimated_minutes    INTEGER,
    status               VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_by           UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_lessons_topic_code UNIQUE (topic_id, code),
    CONSTRAINT chk_lesson_content CHECK (jsonb_typeof(content) = 'object'),
    CONSTRAINT chk_lesson_duration CHECK (estimated_minutes IS NULL OR estimated_minutes > 0),
    CONSTRAINT chk_lesson_status CHECK (status IN ('draft', 'published', 'archived'))
);
CREATE INDEX IF NOT EXISTS idx_lessons_topic_order ON lessons(topic_id, sort_order);

CREATE TABLE IF NOT EXISTS skills (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id           UUID NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    topic_id             UUID REFERENCES topics(id) ON DELETE SET NULL,
    grade                SMALLINT NOT NULL,
    code                 VARCHAR(100) NOT NULL UNIQUE,
    name                 VARCHAR(255) NOT NULL,
    description          TEXT,
    sort_order           INTEGER NOT NULL DEFAULT 0,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_skills_grade CHECK (grade BETWEEN 1 AND 5)
);
CREATE INDEX IF NOT EXISTS idx_skills_subject_grade ON skills(subject_id, grade);
CREATE INDEX IF NOT EXISTS idx_skills_topic ON skills(topic_id);

CREATE TABLE IF NOT EXISTS skill_prerequisites (
    skill_id             UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    prerequisite_skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (skill_id, prerequisite_skill_id),
    CONSTRAINT chk_skill_not_own_prerequisite CHECK (skill_id <> prerequisite_skill_id)
);
CREATE INDEX IF NOT EXISTS idx_skill_prerequisites_required
    ON skill_prerequisites(prerequisite_skill_id);
-- Preventing indirect cycles in prerequisite graphs is the backend's responsibility.

CREATE TABLE IF NOT EXISTS lesson_skills (
    lesson_id            UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    skill_id             UUID NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
    is_primary           BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (lesson_id, skill_id)
);
CREATE INDEX IF NOT EXISTS idx_lesson_skills_skill ON lesson_skills(skill_id);

CREATE TABLE IF NOT EXISTS media_assets (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bucket_name          VARCHAR(150) NOT NULL,
    object_key           TEXT NOT NULL,
    mime_type            VARCHAR(150) NOT NULL,
    file_size_bytes      BIGINT,
    sha256               CHAR(64),
    visibility           VARCHAR(20) NOT NULL DEFAULT 'private',
    uploaded_by          UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_media_location UNIQUE(bucket_name, object_key),
    CONSTRAINT chk_media_file_size CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
    CONSTRAINT chk_media_visibility CHECK (visibility IN ('private', 'public')),
    CONSTRAINT chk_media_sha256 CHECK (sha256 IS NULL OR sha256 ~ '^[0-9a-fA-F]{64}$')
);
CREATE INDEX IF NOT EXISTS idx_media_uploaded_by ON media_assets(uploaded_by);

CREATE TABLE IF NOT EXISTS questions (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                 VARCHAR(100) NOT NULL UNIQUE,
    subject_id           UUID NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    topic_id             UUID REFERENCES topics(id) ON DELETE SET NULL,
    grade                SMALLINT NOT NULL,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_by           UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_questions_grade CHECK (grade BETWEEN 1 AND 5)
);
CREATE INDEX IF NOT EXISTS idx_questions_subject_grade ON questions(subject_id, grade);
CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic_id);

CREATE TABLE IF NOT EXISTS question_versions (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id          UUID NOT NULL REFERENCES questions(id) ON DELETE RESTRICT,
    version              INTEGER NOT NULL,
    question_type        VARCHAR(30) NOT NULL,
    difficulty           SMALLINT NOT NULL DEFAULT 3,
    content              JSONB NOT NULL,
    grading              JSONB NOT NULL DEFAULT '{}'::jsonb,
    explanation          JSONB NOT NULL DEFAULT '{}'::jsonb,
    max_score            NUMERIC(10,2) NOT NULL DEFAULT 1,
    status               VARCHAR(20) NOT NULL DEFAULT 'draft',
    reviewed_by          UUID REFERENCES users(id) ON DELETE SET NULL,
    published_at         TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_question_versions_number UNIQUE (question_id, version),
    CONSTRAINT chk_question_version_positive CHECK (version >= 1),
    CONSTRAINT chk_question_version_difficulty CHECK (difficulty BETWEEN 1 AND 5),
    CONSTRAINT chk_question_version_type CHECK (question_type IN (
        'single_choice', 'multiple_choice', 'fill_blank', 'ordering',
        'matching', 'drag_drop', 'image_choice', 'audio_choice',
        'free_text', 'interactive'
    )),
    CONSTRAINT chk_question_version_json CHECK (
        jsonb_typeof(content) = 'object'
        AND jsonb_typeof(grading) = 'object'
        AND jsonb_typeof(explanation) = 'object'
    ),
    CONSTRAINT chk_question_version_max_score CHECK (max_score > 0),
    CONSTRAINT chk_question_version_status CHECK (status IN ('draft', 'published', 'archived'))
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_one_published_version_per_question
    ON question_versions(question_id) WHERE status = 'published';
CREATE INDEX IF NOT EXISTS idx_question_versions_status_difficulty
    ON question_versions(status, difficulty);

CREATE TABLE IF NOT EXISTS question_skills (
    question_version_id  UUID NOT NULL REFERENCES question_versions(id) ON DELETE CASCADE,
    skill_id             UUID NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
    is_primary           BOOLEAN NOT NULL DEFAULT FALSE,
    weight               NUMERIC(5,4) NOT NULL DEFAULT 1,
    PRIMARY KEY (question_version_id, skill_id),
    CONSTRAINT chk_question_skill_weight CHECK (weight > 0 AND weight <= 1)
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_primary_skill_per_question_version
    ON question_skills(question_version_id) WHERE is_primary;
CREATE INDEX IF NOT EXISTS idx_question_skills_skill ON question_skills(skill_id);

CREATE TABLE IF NOT EXISTS lesson_questions (
    lesson_id            UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    question_version_id  UUID NOT NULL REFERENCES question_versions(id) ON DELETE RESTRICT,
    sort_order           INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (lesson_id, question_version_id)
);
CREATE INDEX IF NOT EXISTS idx_lesson_questions_question
    ON lesson_questions(question_version_id);

-- ======================== C. TESTS AND SUBMISSIONS =============================

CREATE TABLE IF NOT EXISTS assessments (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                 VARCHAR(100) NOT NULL UNIQUE,
    subject_id           UUID NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    topic_id             UUID REFERENCES topics(id) ON DELETE SET NULL,
    lesson_id            UUID REFERENCES lessons(id) ON DELETE SET NULL,
    grade                SMALLINT NOT NULL,
    title                VARCHAR(255) NOT NULL,
    description          TEXT,
    assessment_type      VARCHAR(30) NOT NULL DEFAULT 'practice',
    status               VARCHAR(20) NOT NULL DEFAULT 'draft',
    time_limit_seconds   INTEGER,
    max_attempts         INTEGER NOT NULL DEFAULT 1,
    settings             JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by           UUID REFERENCES users(id) ON DELETE SET NULL,
    published_at         TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_assessment_grade CHECK (grade BETWEEN 1 AND 5),
    CONSTRAINT chk_assessment_type CHECK (assessment_type IN (
        'practice', 'homework', 'quiz', 'test', 'placement', 'adaptive'
    )),
    CONSTRAINT chk_assessment_status CHECK (status IN ('draft', 'published', 'archived')),
    CONSTRAINT chk_assessment_limit CHECK (time_limit_seconds IS NULL OR time_limit_seconds > 0),
    CONSTRAINT chk_assessment_max_attempts CHECK (max_attempts >= 1),
    CONSTRAINT chk_assessment_settings CHECK (jsonb_typeof(settings) = 'object')
);
CREATE INDEX IF NOT EXISTS idx_assessments_subject_grade
    ON assessments(subject_id, grade, status);

CREATE TABLE IF NOT EXISTS assessment_items (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id        UUID NOT NULL REFERENCES assessments(id) ON DELETE RESTRICT,
    question_version_id  UUID NOT NULL REFERENCES question_versions(id) ON DELETE RESTRICT,
    position             INTEGER NOT NULL,
    points               NUMERIC(10,2) NOT NULL DEFAULT 1,
    is_required          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_assessment_item_position UNIQUE(assessment_id, position),
    CONSTRAINT uq_assessment_item_version UNIQUE(id, assessment_id, question_version_id),
    CONSTRAINT chk_assessment_item_position CHECK (position >= 1),
    CONSTRAINT chk_assessment_item_points CHECK (points > 0)
);
CREATE INDEX IF NOT EXISTS idx_assessment_items_question
    ON assessment_items(question_version_id);

CREATE TABLE IF NOT EXISTS student_assignments (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    assessment_id        UUID NOT NULL REFERENCES assessments(id) ON DELETE RESTRICT,
    assigned_by          UUID REFERENCES users(id) ON DELETE SET NULL,
    assignment_source    VARCHAR(20) NOT NULL DEFAULT 'teacher',
    status               VARCHAR(20) NOT NULL DEFAULT 'assigned',
    available_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    due_at               TIMESTAMPTZ,
    completed_at         TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_assignment_student_assessment UNIQUE (id, student_id, assessment_id),
    CONSTRAINT chk_assignment_source CHECK (assignment_source IN (
        'teacher', 'system', 'guardian', 'self'
    )),
    CONSTRAINT chk_assignment_status CHECK (status IN (
        'assigned', 'in_progress', 'completed', 'cancelled', 'expired'
    )),
    CONSTRAINT chk_assignment_dates CHECK (due_at IS NULL OR due_at >= available_at)
);
CREATE INDEX IF NOT EXISTS idx_assignments_student_status
    ON student_assignments(student_id, status, available_at DESC);
CREATE INDEX IF NOT EXISTS idx_assignments_assessment
    ON student_assignments(assessment_id);

CREATE TABLE IF NOT EXISTS attempts (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id        UUID NOT NULL,
    student_id           UUID NOT NULL,
    assessment_id        UUID NOT NULL,
    attempt_no           INTEGER NOT NULL DEFAULT 1,
    status               VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    started_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    submitted_at         TIMESTAMPTZ,
    graded_at            TIMESTAMPTZ,
    total_score          NUMERIC(10,2) NOT NULL DEFAULT 0,
    max_score            NUMERIC(10,2) NOT NULL DEFAULT 0,
    correct_count        INTEGER NOT NULL DEFAULT 0,
    answered_count       INTEGER NOT NULL DEFAULT 0,
    grading_details      JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_attempt_assignment_no UNIQUE (assignment_id, attempt_no),
    CONSTRAINT uq_attempt_assessment UNIQUE (id, assessment_id),
    CONSTRAINT fk_attempt_assignment_identity
        FOREIGN KEY (assignment_id, student_id, assessment_id)
        REFERENCES student_assignments(id, student_id, assessment_id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_attempt_no CHECK (attempt_no >= 1),
    CONSTRAINT chk_attempt_status CHECK (status IN (
        'in_progress', 'submitted', 'graded', 'abandoned'
    )),
    CONSTRAINT chk_attempt_times CHECK (submitted_at IS NULL OR submitted_at >= started_at),
    CONSTRAINT chk_attempt_grades CHECK (
        total_score >= 0 AND max_score >= 0
        AND total_score <= max_score
        AND correct_count >= 0 AND answered_count >= 0
        AND correct_count <= answered_count
    ),
    CONSTRAINT chk_attempt_details CHECK (jsonb_typeof(grading_details) = 'object')
);
CREATE INDEX IF NOT EXISTS idx_attempts_student_time
    ON attempts(student_id, submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_attempts_assessment
    ON attempts(assessment_id, submitted_at DESC);

-- Composite FKs below guarantee an answer belongs to the same assessment as
-- the parent attempt AND points to the exact version configured in its item.
CREATE TABLE IF NOT EXISTS attempt_answers (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id           UUID NOT NULL,
    assessment_id        UUID NOT NULL,
    assessment_item_id   UUID NOT NULL,
    question_version_id  UUID NOT NULL,
    answer_no            INTEGER NOT NULL DEFAULT 1,
    student_answer       JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_correct           BOOLEAN,
    score                NUMERIC(10,2),
    grading_status       VARCHAR(20) NOT NULL DEFAULT 'pending',
    feedback             JSONB NOT NULL DEFAULT '{}'::jsonb,
    response_time_ms     INTEGER,
    hint_count           INTEGER NOT NULL DEFAULT 0,
    answered_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_answer_attempt_assessment
        FOREIGN KEY (attempt_id, assessment_id)
        REFERENCES attempts(id, assessment_id) ON DELETE CASCADE,
    CONSTRAINT fk_answer_item_version
        FOREIGN KEY (assessment_item_id, assessment_id, question_version_id)
        REFERENCES assessment_items(id, assessment_id, question_version_id)
        ON DELETE RESTRICT,
    CONSTRAINT uq_answer_iteration UNIQUE (attempt_id, assessment_item_id, answer_no),
    CONSTRAINT chk_answer_no CHECK (answer_no >= 1),
    CONSTRAINT chk_answer_json CHECK (
        jsonb_typeof(student_answer) = 'object' AND jsonb_typeof(feedback) = 'object'
    ),
    CONSTRAINT chk_answer_score CHECK (score IS NULL OR score >= 0),
    CONSTRAINT chk_answer_grading CHECK (grading_status IN (
        'pending', 'graded', 'needs_review'
    )),
    CONSTRAINT chk_answer_time CHECK (response_time_ms IS NULL OR response_time_ms >= 0),
    CONSTRAINT chk_answer_hints CHECK (hint_count >= 0)
);
CREATE INDEX IF NOT EXISTS idx_answers_attempt ON attempt_answers(attempt_id);
CREATE INDEX IF NOT EXISTS idx_answers_question_time
    ON attempt_answers(question_version_id, answered_at DESC);

-- ======================== D. PERSONALIZED LEARNING ===========================

CREATE TABLE IF NOT EXISTS student_skill_mastery (
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    skill_id             UUID NOT NULL REFERENCES skills(id) ON DELETE RESTRICT,
    mastery_score        NUMERIC(5,4) NOT NULL DEFAULT 0,
    confidence           NUMERIC(5,4) NOT NULL DEFAULT 0,
    questions_attempted  INTEGER NOT NULL DEFAULT 0,
    correct_count        INTEGER NOT NULL DEFAULT 0,
    recent_accuracy      NUMERIC(5,4),
    hint_usage_rate      NUMERIC(5,4),
    last_practiced_at    TIMESTAMPTZ,
    next_review_at       TIMESTAMPTZ,
    model_version        VARCHAR(50) NOT NULL DEFAULT 'rule_v1',
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (student_id, skill_id),
    CONSTRAINT chk_mastery_range CHECK (
        mastery_score BETWEEN 0 AND 1 AND confidence BETWEEN 0 AND 1
        AND (recent_accuracy IS NULL OR recent_accuracy BETWEEN 0 AND 1)
        AND (hint_usage_rate IS NULL OR hint_usage_rate BETWEEN 0 AND 1)
    ),
    CONSTRAINT chk_mastery_counts CHECK (
        questions_attempted >= 0 AND correct_count >= 0
        AND correct_count <= questions_attempted
    )
);
CREATE INDEX IF NOT EXISTS idx_mastery_student_score
    ON student_skill_mastery(student_id, mastery_score);
CREATE INDEX IF NOT EXISTS idx_mastery_next_review
    ON student_skill_mastery(next_review_at) WHERE next_review_at IS NOT NULL;

CREATE TABLE IF NOT EXISTS student_lesson_progress (
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    lesson_id            UUID NOT NULL REFERENCES lessons(id) ON DELETE RESTRICT,
    status               VARCHAR(20) NOT NULL DEFAULT 'not_started',
    completion_ratio     NUMERIC(5,4) NOT NULL DEFAULT 0,
    first_started_at     TIMESTAMPTZ,
    last_accessed_at     TIMESTAMPTZ,
    completed_at         TIMESTAMPTZ,
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (student_id, lesson_id),
    CONSTRAINT chk_lesson_progress_status CHECK (
        status IN ('not_started', 'in_progress', 'completed')
    ),
    CONSTRAINT chk_lesson_completion CHECK (completion_ratio BETWEEN 0 AND 1)
);
CREATE INDEX IF NOT EXISTS idx_lesson_progress_student_status
    ON student_lesson_progress(student_id, status);

CREATE TABLE IF NOT EXISTS student_learning_plans (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    subject_id           UUID NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    title                VARCHAR(255) NOT NULL,
    status               VARCHAR(20) NOT NULL DEFAULT 'draft',
    start_date           DATE,
    end_date             DATE,
    generated_by         VARCHAR(30) NOT NULL DEFAULT 'rules',
    model_version        VARCHAR(50),
    plan_metadata        JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_plan_status CHECK (status IN (
        'draft', 'active', 'paused', 'completed', 'archived'
    )),
    CONSTRAINT chk_plan_generator CHECK (generated_by IN (
        'rules', 'teacher', 'ai', 'guardian'
    )),
    CONSTRAINT chk_plan_dates CHECK (
        start_date IS NULL OR end_date IS NULL OR end_date >= start_date
    ),
    CONSTRAINT chk_plan_metadata CHECK (jsonb_typeof(plan_metadata) = 'object')
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_active_plan_per_student_subject
    ON student_learning_plans(student_id, subject_id) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_learning_plans_student_status
    ON student_learning_plans(student_id, status);

CREATE TABLE IF NOT EXISTS learning_plan_items (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learning_plan_id     UUID NOT NULL REFERENCES student_learning_plans(id) ON DELETE CASCADE,
    position             INTEGER NOT NULL,
    skill_id             UUID REFERENCES skills(id) ON DELETE RESTRICT,
    lesson_id            UUID REFERENCES lessons(id) ON DELETE RESTRICT,
    assessment_id        UUID REFERENCES assessments(id) ON DELETE RESTRICT,
    target_mastery       NUMERIC(5,4),
    status               VARCHAR(20) NOT NULL DEFAULT 'pending',
    due_at               TIMESTAMPTZ,
    completed_at         TIMESTAMPTZ,
    notes                TEXT,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_plan_item_order UNIQUE (learning_plan_id, position),
    CONSTRAINT chk_plan_item_position CHECK (position >= 1),
    CONSTRAINT chk_plan_item_target CHECK (
        target_mastery IS NULL OR target_mastery BETWEEN 0 AND 1
    ),
    CONSTRAINT chk_plan_item_content CHECK (
        skill_id IS NOT NULL OR lesson_id IS NOT NULL OR assessment_id IS NOT NULL
    ),
    CONSTRAINT chk_plan_item_status CHECK (status IN (
        'pending', 'in_progress', 'completed', 'skipped'
    ))
);
CREATE INDEX IF NOT EXISTS idx_plan_items_skill ON learning_plan_items(skill_id);

CREATE TABLE IF NOT EXISTS learning_plan_history (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learning_plan_id     UUID NOT NULL REFERENCES student_learning_plans(id) ON DELETE RESTRICT,
    change_type          VARCHAR(40) NOT NULL,
    snapshot             JSONB NOT NULL DEFAULT '{}'::jsonb,
    changed_by           UUID REFERENCES users(id) ON DELETE SET NULL,
    changed_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_plan_history_snapshot CHECK (jsonb_typeof(snapshot) = 'object')
);
CREATE INDEX IF NOT EXISTS idx_plan_history_plan_time
    ON learning_plan_history(learning_plan_id, changed_at DESC);

CREATE TABLE IF NOT EXISTS student_recommendations (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    skill_id             UUID REFERENCES skills(id) ON DELETE RESTRICT,
    question_version_id  UUID REFERENCES question_versions(id) ON DELETE RESTRICT,
    assessment_id        UUID REFERENCES assessments(id) ON DELETE RESTRICT,
    reason_code          VARCHAR(60) NOT NULL,
    explanation          TEXT,
    priority             SMALLINT NOT NULL DEFAULT 50,
    status               VARCHAR(20) NOT NULL DEFAULT 'pending',
    model_version        VARCHAR(50) NOT NULL DEFAULT 'rule_v1',
    expires_at           TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_recommendation_target CHECK (
        NUM_NONNULLS(question_version_id, assessment_id) = 1
    ),
    CONSTRAINT chk_recommendation_priority CHECK (priority BETWEEN 0 AND 100),
    CONSTRAINT chk_recommendation_status CHECK (status IN (
        'pending', 'shown', 'accepted', 'completed', 'dismissed', 'expired'
    ))
);
CREATE INDEX IF NOT EXISTS idx_recommendations_student_status_priority
    ON student_recommendations(student_id, status, priority DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_recommendations_skill
    ON student_recommendations(skill_id);

-- The event stream is append-only in normal application logic.
CREATE TABLE IF NOT EXISTS learning_events (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    event_type           VARCHAR(80) NOT NULL,
    attempt_id           UUID REFERENCES attempts(id) ON DELETE SET NULL,
    question_version_id  UUID REFERENCES question_versions(id) ON DELETE SET NULL,
    skill_id             UUID REFERENCES skills(id) ON DELETE SET NULL,
    properties           JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    received_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_learning_event_properties CHECK (jsonb_typeof(properties) = 'object')
);
CREATE INDEX IF NOT EXISTS idx_learning_events_student_time
    ON learning_events(student_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_learning_events_type_time
    ON learning_events(event_type, occurred_at DESC);

-- ======================== E. ANALYTICS / PRIVACY ==============================

CREATE TABLE IF NOT EXISTS question_statistics (
    question_version_id  UUID PRIMARY KEY REFERENCES question_versions(id) ON DELETE RESTRICT,
    attempts_count       BIGINT NOT NULL DEFAULT 0,
    correct_count        BIGINT NOT NULL DEFAULT 0,
    incorrect_count      BIGINT NOT NULL DEFAULT 0,
    avg_response_time_ms NUMERIC(12,2),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_question_stats_counts CHECK (
        attempts_count >= 0 AND correct_count >= 0 AND incorrect_count >= 0
        AND correct_count + incorrect_count <= attempts_count
    ),
    CONSTRAINT chk_question_stats_response CHECK (
        avg_response_time_ms IS NULL OR avg_response_time_ms >= 0
    )
);

CREATE TABLE IF NOT EXISTS student_daily_statistics (
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    stat_date            DATE NOT NULL,
    subject_id           UUID NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    active_seconds       INTEGER NOT NULL DEFAULT 0,
    questions_answered   INTEGER NOT NULL DEFAULT 0,
    correct_answers      INTEGER NOT NULL DEFAULT 0,
    assessments_completed INTEGER NOT NULL DEFAULT 0,
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (student_id, stat_date, subject_id),
    CONSTRAINT chk_daily_stats_counts CHECK (
        active_seconds >= 0
        AND questions_answered >= 0
        AND correct_answers >= 0
        AND assessments_completed >= 0
        AND correct_answers <= questions_answered
    )
);
CREATE INDEX IF NOT EXISTS idx_daily_stats_date_subject
    ON student_daily_statistics(stat_date, subject_id);

CREATE TABLE IF NOT EXISTS audit_logs (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_user_id        UUID REFERENCES users(id) ON DELETE SET NULL,
    action               VARCHAR(100) NOT NULL,
    entity_type          VARCHAR(100) NOT NULL,
    entity_id            UUID,
    old_values           JSONB,
    new_values           JSONB,
    ip_address           INET,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_audit_old_json CHECK (
        old_values IS NULL OR jsonb_typeof(old_values) = 'object'
    ),
    CONSTRAINT chk_audit_new_json CHECK (
        new_values IS NULL OR jsonb_typeof(new_values) = 'object'
    )
);
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_time
    ON audit_logs(actor_user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity_time
    ON audit_logs(entity_type, entity_id, created_at DESC);

-- Record grant/withdrawal history rather than overwriting old consent records.
CREATE TABLE IF NOT EXISTS privacy_consents (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id           UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
    guardian_user_id     UUID REFERENCES users(id) ON DELETE SET NULL,
    purpose_code         VARCHAR(80) NOT NULL,
    policy_version       VARCHAR(50) NOT NULL,
    consent_given        BOOLEAN NOT NULL,
    recorded_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at           TIMESTAMPTZ,
    notes                TEXT,
    CONSTRAINT chk_consent_dates CHECK (
        expires_at IS NULL OR expires_at >= recorded_at
    )
);
CREATE INDEX IF NOT EXISTS idx_privacy_consents_student_purpose
    ON privacy_consents(student_id, purpose_code, recorded_at DESC);

-- ======================== F. COMMON UPDATE TRIGGER ============================

CREATE OR REPLACE FUNCTION education_set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$;

DO $$
DECLARE
    table_name TEXT;
    trigger_name TEXT;
BEGIN
    FOREACH table_name IN ARRAY ARRAY[
        'users', 'schools', 'student_profiles', 'classes',
        'subjects', 'topics', 'lessons', 'skills', 'media_assets',
        'questions', 'question_versions', 'assessments',
        'student_assignments', 'attempts', 'attempt_answers',
        'student_skill_mastery', 'student_lesson_progress',
        'student_learning_plans', 'learning_plan_items',
        'student_recommendations', 'question_statistics',
        'student_daily_statistics'
    ] LOOP
        trigger_name := 'trg_' || table_name || '_updated_at';
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger
            WHERE tgname = trigger_name
              AND tgrelid = FORMAT('public.%I', table_name)::regclass
        ) THEN
            EXECUTE FORMAT(
                'CREATE TRIGGER %I BEFORE UPDATE ON public.%I '
                || 'FOR EACH ROW EXECUTE FUNCTION public.education_set_updated_at()',
                trigger_name, table_name
            );
        END IF;
    END LOOP;
END;
$$;

-- ======================== G. SAFE STUDENT CONTENT VIEW ========================
-- Only published question content; NEVER includes grading, solutions or answer keys.
-- Still apply authentication and authorization in the backend.
CREATE OR REPLACE VIEW v_published_question_content AS
SELECT
    q.id AS question_id,
    q.code AS question_code,
    q.subject_id,
    q.topic_id,
    q.grade,
    qv.id AS question_version_id,
    qv.version,
    qv.question_type,
    qv.difficulty,
    qv.content,
    qv.max_score
FROM questions AS q
JOIN question_versions AS qv ON qv.question_id = q.id
WHERE q.is_active = TRUE
  AND qv.status = 'published';

-- ======================== H. INITIAL MASTER DATA ==============================
-- Only subjects are seeded. Real lessons, skills and questions come from CMS/API.
INSERT INTO subjects (code, name_vi, sort_order) VALUES
    ('MATH', 'Toán', 1),
    ('VIETNAMESE', 'Tiếng Việt', 2),
    ('ENGLISH', 'Tiếng Anh', 3),
    ('SCIENCE', 'Khoa học', 4),
    ('HISTORY_GEOGRAPHY', 'Lịch sử và Địa lý', 5),
    ('INFORMATICS', 'Tin học', 6),
    ('ETHICS', 'Đạo đức', 7)
ON CONFLICT (code) DO NOTHING;

COMMIT;

-- ============================================================================
-- Example verification (run after import):
--   SELECT COUNT(*) AS table_count
--   FROM information_schema.tables
--   WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
--   SELECT code, name_vi FROM subjects ORDER BY sort_order;
--
-- Application notes:
--   * Reuse question_versions.id in assessment_items; never silently edit
--     already-published question content or assessments with assignments.
--   * The backend validates JSON shape per question_type, prevents raw answer
--     keys from leaving server, and checks teacher/parent/student permissions.
--   * The backend enforces max_attempts, assessment publication, allowed times,
--     score <= assessment_item.points, and consistent curriculum taxonomy.
--   * Use a DB transaction to submit an attempt and its answer records.
--   * Recompute student_skill_mastery and analytics from answer/event history;
--     they are derived materialized summaries, not the source of truth.
--   * For minors: minimize PII, audit consent, enforce data retention and
--     deletion policies, and restrict access to private student storage.
-- ============================================================================
