CREATE TABLE ai_programs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), code VARCHAR(80) UNIQUE NOT NULL,
 title VARCHAR(160) NOT NULL, description TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_grades (
 grade SMALLINT PRIMARY KEY CHECK (grade BETWEEN 1 AND 5), program_id UUID NOT NULL REFERENCES ai_programs(id),
 curriculum JSONB NOT NULL CHECK (jsonb_typeof(curriculum) = 'object')
);
CREATE TABLE ai_units (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), grade SMALLINT NOT NULL REFERENCES ai_grades(grade),
 code VARCHAR(80) UNIQUE NOT NULL, title VARCHAR(180) NOT NULL, position SMALLINT NOT NULL CHECK(position > 0),
 description TEXT NOT NULL, UNIQUE(grade, position)
);
CREATE TABLE ai_lessons (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), unit_id UUID NOT NULL REFERENCES ai_units(id),
 code VARCHAR(80) UNIQUE NOT NULL, title VARCHAR(180) NOT NULL, position SMALLINT NOT NULL CHECK(position > 0),
 revision INTEGER NOT NULL DEFAULT 1 CHECK(revision > 0), created_by UUID REFERENCES users(id),
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 UNIQUE(unit_id, position)
);
CREATE TABLE ai_lesson_versions (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), lesson_id UUID NOT NULL REFERENCES ai_lessons(id),
 version INTEGER NOT NULL CHECK(version > 0), status VARCHAR(20) NOT NULL DEFAULT 'draft'
 CHECK(status IN ('draft','review','published','archived')),
 payload JSONB NOT NULL CHECK(jsonb_typeof(payload) = 'object'), created_by UUID REFERENCES users(id),
 reviewed_by UUID REFERENCES users(id), published_at TIMESTAMPTZ,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), UNIQUE(lesson_id, version)
);
CREATE UNIQUE INDEX ai_one_published_version ON ai_lesson_versions(lesson_id) WHERE status = 'published';
CREATE INDEX ai_versions_catalog ON ai_lesson_versions(status, lesson_id);
CREATE TABLE ai_staff_roles (
 user_id UUID NOT NULL REFERENCES users(id), role VARCHAR(20) NOT NULL CHECK(role IN ('editor','reviewer')),
 assigned_by UUID NOT NULL REFERENCES users(id), PRIMARY KEY(user_id, role)
);
CREATE TABLE ai_media_assets (
 id UUID PRIMARY KEY REFERENCES media_assets(id), code VARCHAR(120) UNIQUE NOT NULL,
 category VARCHAR(30) NOT NULL, alt TEXT NOT NULL CHECK(length(btrim(alt)) > 0),
 license TEXT NOT NULL, source TEXT NOT NULL, status VARCHAR(20) NOT NULL
 CHECK(status IN ('draft','review','approved','archived')), width INTEGER NOT NULL CHECK(width > 0),
 height INTEGER NOT NULL CHECK(height > 0), bundled BOOLEAN NOT NULL DEFAULT FALSE,
 reviewed_by UUID REFERENCES users(id), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_media_variants (
 asset_id UUID NOT NULL REFERENCES ai_media_assets(id), kind VARCHAR(20) NOT NULL,
 object_key TEXT NOT NULL, mime_type VARCHAR(100) NOT NULL, sha256 CHAR(64) NOT NULL,
 width INTEGER NOT NULL, height INTEGER NOT NULL, file_size_bytes BIGINT NOT NULL,
 PRIMARY KEY(asset_id, kind)
);
CREATE TABLE ai_media_usages (
 lesson_version_id UUID NOT NULL REFERENCES ai_lesson_versions(id), asset_id UUID NOT NULL REFERENCES ai_media_assets(id),
 purpose VARCHAR(30) NOT NULL, PRIMARY KEY(lesson_version_id, asset_id, purpose)
);
CREATE TABLE ai_assignments (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), lesson_id UUID NOT NULL REFERENCES ai_lessons(id),
 class_id UUID NOT NULL REFERENCES classes(id), assigned_by UUID NOT NULL REFERENCES users(id),
 due_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), UNIQUE(lesson_id, class_id),
 CHECK(due_at IS NULL OR due_at > created_at)
);
CREATE TABLE ai_assignment_targets (
 assignment_id UUID NOT NULL REFERENCES ai_assignments(id), student_id UUID NOT NULL REFERENCES student_profiles(student_id),
 PRIMARY KEY(assignment_id, student_id)
);
CREATE TABLE ai_attempts (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), student_id UUID NOT NULL REFERENCES student_profiles(student_id),
 version_id UUID NOT NULL REFERENCES ai_lesson_versions(id), step_id VARCHAR(60) NOT NULL,
 idempotency_key UUID NOT NULL, level SMALLINT NOT NULL CHECK(level BETWEEN 1 AND 3),
 answers JSONB NOT NULL CHECK(jsonb_typeof(answers) = 'object'), score NUMERIC(5,4) NOT NULL CHECK(score BETWEEN 0 AND 1),
 feedback JSONB NOT NULL CHECK(jsonb_typeof(feedback) = 'object'), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 UNIQUE(student_id, idempotency_key)
);
CREATE INDEX ai_attempts_student_version ON ai_attempts(student_id, version_id, created_at DESC);
CREATE TABLE ai_progress (
 student_id UUID NOT NULL REFERENCES student_profiles(student_id), lesson_id UUID NOT NULL REFERENCES ai_lessons(id),
 version_id UUID NOT NULL REFERENCES ai_lesson_versions(id), next_step INTEGER NOT NULL DEFAULT 0 CHECK(next_step >= 0),
 completed_at TIMESTAMPTZ, updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), PRIMARY KEY(student_id, lesson_id)
);
CREATE TABLE ai_competency_progress (
 student_id UUID NOT NULL REFERENCES student_profiles(student_id), competency VARCHAR(50) NOT NULL,
 evidence_count INTEGER NOT NULL DEFAULT 0 CHECK(evidence_count >= 0),
 successful_count INTEGER NOT NULL DEFAULT 0 CHECK(successful_count BETWEEN 0 AND evidence_count),
 PRIMARY KEY(student_id, competency)
);
CREATE TABLE ai_projects (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), grade SMALLINT NOT NULL REFERENCES ai_grades(grade),
 code VARCHAR(80) UNIQUE NOT NULL, title VARCHAR(160) NOT NULL, brief TEXT NOT NULL,
 rubric JSONB NOT NULL CHECK(jsonb_typeof(rubric) = 'object')
);
CREATE TABLE ai_project_submissions (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), project_id UUID NOT NULL REFERENCES ai_projects(id),
 student_id UUID NOT NULL REFERENCES student_profiles(student_id), class_id UUID REFERENCES classes(id),
 artifact JSONB NOT NULL CHECK(jsonb_typeof(artifact) = 'object'), revision INTEGER NOT NULL DEFAULT 1,
 status VARCHAR(20) NOT NULL CHECK(status IN ('draft','submitted','reviewed')), feedback TEXT,
 reviewed_by UUID REFERENCES users(id), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 UNIQUE(project_id, student_id)
);
CREATE TABLE ai_rubric_scores (
 submission_id UUID PRIMARY KEY REFERENCES ai_project_submissions(id), scores JSONB NOT NULL,
 total NUMERIC(5,2) NOT NULL CHECK(total BETWEEN 0 AND 100), reviewer_id UUID NOT NULL REFERENCES users(id),
 updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_badges (
 code VARCHAR(80) PRIMARY KEY, title VARCHAR(160) NOT NULL, description TEXT NOT NULL,
 threshold SMALLINT NOT NULL CHECK(threshold > 0), asset_id UUID NOT NULL REFERENCES ai_media_assets(id)
);
CREATE TABLE ai_student_badges (
 student_id UUID NOT NULL REFERENCES student_profiles(student_id), badge_code VARCHAR(80) NOT NULL REFERENCES ai_badges(code),
 earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), PRIMARY KEY(student_id, badge_code)
);
CREATE TABLE ai_rewards_ledger (
 student_id UUID NOT NULL REFERENCES student_profiles(student_id), lesson_id UUID NOT NULL REFERENCES ai_lessons(id),
 points INTEGER NOT NULL CHECK(points BETWEEN 0 AND 100), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 PRIMARY KEY(student_id, lesson_id)
);
CREATE TABLE ai_prompt_templates (
 mode VARCHAR(40) NOT NULL, version INTEGER NOT NULL, template TEXT NOT NULL,
 status VARCHAR(20) NOT NULL CHECK(status IN ('draft','approved','archived')), PRIMARY KEY(mode, version)
);
CREATE TABLE ai_provider_configs (
 code VARCHAR(30) PRIMARY KEY CHECK(code IN ('simulation','ollama')), enabled BOOLEAN NOT NULL DEFAULT FALSE,
 policy_approved BOOLEAN NOT NULL DEFAULT FALSE, updated_by UUID REFERENCES users(id), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_feature_flags (
 code VARCHAR(50) PRIMARY KEY, enabled BOOLEAN NOT NULL DEFAULT FALSE, updated_by UUID REFERENCES users(id)
);
CREATE TABLE ai_generation_jobs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), requested_by UUID NOT NULL REFERENCES users(id),
 template VARCHAR(60) NOT NULL, parameters JSONB NOT NULL, status VARCHAR(20) NOT NULL
 CHECK(status IN ('queued','running','review','approved','failed')), asset_id UUID REFERENCES ai_media_assets(id),
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_moderation_reviews (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), student_id UUID REFERENCES student_profiles(student_id),
 reason_code VARCHAR(40) NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','reviewed')),
 reviewed_by UUID REFERENCES users(id), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_content_approvals (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), version_id UUID NOT NULL REFERENCES ai_lesson_versions(id),
 actor_id UUID NOT NULL REFERENCES users(id), action VARCHAR(30) NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_audit_logs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), actor_id UUID REFERENCES users(id), action VARCHAR(80) NOT NULL,
 entity_id UUID, metadata JSONB NOT NULL DEFAULT '{}', created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE ai_events (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), student_id UUID NOT NULL REFERENCES student_profiles(student_id),
 lesson_id UUID REFERENCES ai_lessons(id), event_type VARCHAR(40) NOT NULL, properties JSONB NOT NULL DEFAULT '{}',
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ai_events_student_time ON ai_events(student_id, created_at DESC);
CREATE TABLE ai_usage_windows (
 scope_hash CHAR(64) NOT NULL, day DATE NOT NULL, requests INTEGER NOT NULL DEFAULT 0 CHECK(requests >= 0),
 PRIMARY KEY(scope_hash, day)
);
