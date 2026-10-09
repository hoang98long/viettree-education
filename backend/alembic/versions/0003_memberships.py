"""Add time-limited memberships and explicit content policies; preserve original learning tables."""

from alembic import op

revision = "0003_memberships"
down_revision = "0002_auth_sessions"


def upgrade():
    op.execute("""
        CREATE TABLE membership_plans (
            code VARCHAR(20) PRIMARY KEY CHECK (code IN ('free', 'vip')),
            name VARCHAR(100) NOT NULL, is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        CREATE TABLE membership_plan_features (
            plan_code VARCHAR(20) NOT NULL REFERENCES membership_plans(code),
            feature_code VARCHAR(100) NOT NULL,
            PRIMARY KEY (plan_code, feature_code)
        );
        CREATE TABLE student_memberships (
            student_id UUID PRIMARY KEY REFERENCES student_profiles(student_id) ON DELETE RESTRICT,
            plan_code VARCHAR(20) NOT NULL REFERENCES membership_plans(code) CHECK (plan_code = 'vip'),
            starts_at TIMESTAMPTZ NOT NULL, ends_at TIMESTAMPTZ NOT NULL,
            status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'revoked')),
            source VARCHAR(20) NOT NULL DEFAULT 'admin' CHECK (source IN ('admin', 'payment')),
            granted_by UUID REFERENCES users(id), revoked_by UUID REFERENCES users(id),
            revoked_at TIMESTAMPTZ, revoke_reason VARCHAR(500),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CHECK (ends_at > starts_at),
            CHECK ((status = 'revoked') = (revoked_at IS NOT NULL))
        );
        CREATE INDEX idx_memberships_expiry ON student_memberships(ends_at) WHERE status = 'active';
        CREATE TABLE membership_operations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            student_id UUID NOT NULL REFERENCES student_profiles(student_id),
            actor_user_id UUID NOT NULL REFERENCES users(id),
            idempotency_key UUID NOT NULL, operation VARCHAR(20) NOT NULL
                CHECK (operation IN ('grant', 'extend', 'revoke')),
            request_fingerprint VARCHAR(64) NOT NULL,
            response_snapshot JSONB NOT NULL CHECK (jsonb_typeof(response_snapshot) = 'object'),
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            UNIQUE (actor_user_id, idempotency_key)
        );
        CREATE INDEX idx_membership_operations_student ON membership_operations(student_id, created_at DESC);
        CREATE TABLE content_access_policies (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            lesson_id UUID UNIQUE REFERENCES lessons(id) ON DELETE RESTRICT,
            assessment_id UUID UNIQUE REFERENCES assessments(id) ON DELETE RESTRICT,
            minimum_plan_code VARCHAR(20) NOT NULL REFERENCES membership_plans(code),
            learning_level VARCHAR(20) NOT NULL DEFAULT 'basic'
                CHECK (learning_level IN ('basic', 'reinforcement', 'advanced')),
            preview JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(preview) = 'object'),
            updated_by UUID REFERENCES users(id), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CHECK (num_nonnulls(lesson_id, assessment_id) = 1)
        );
        CREATE TABLE attempt_access_grants (
            attempt_id UUID PRIMARY KEY REFERENCES attempts(id) ON DELETE RESTRICT,
            membership_student_id UUID NOT NULL REFERENCES student_memberships(student_id),
            allowed_until TIMESTAMPTZ NOT NULL, granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            revoked_at TIMESTAMPTZ, CHECK (allowed_until > granted_at)
        );
        CREATE INDEX idx_attempt_grants_student ON attempt_access_grants(membership_student_id);
        INSERT INTO membership_plans(code, name) VALUES ('free', 'Miễn phí'), ('vip', 'VIP');
        INSERT INTO membership_plan_features(plan_code, feature_code)
        SELECT p.code, f.code FROM membership_plans p CROSS JOIN (VALUES
            ('learning.basic'), ('practice.basic'), ('results.own'), ('skills.own'),
            ('learning_plan.basic'), ('accessibility.text_size')
        ) AS f(code);
        INSERT INTO membership_plan_features(plan_code, feature_code) VALUES
            ('vip', 'learning.advanced'), ('vip', 'practice.advanced'),
            ('vip', 'practice.challenge'), ('vip', 'learning_plan.adaptive');
        INSERT INTO content_access_policies(lesson_id, minimum_plan_code)
            SELECT id, 'free' FROM lessons;
        INSERT INTO content_access_policies(assessment_id, minimum_plan_code)
            SELECT id, 'free' FROM assessments;
    """)


def downgrade():
    for name in (
        "attempt_access_grants",
        "content_access_policies",
        "membership_operations",
        "student_memberships",
        "membership_plan_features",
        "membership_plans",
    ):
        op.drop_table(name)
