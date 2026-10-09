"""Explicit access for each question version, including standalone bank questions."""

from alembic import op

revision = "0004_question_authoring"
down_revision = "0003_memberships"


def upgrade():
    op.execute("""
        CREATE TABLE question_version_access_policies (
            question_version_id UUID PRIMARY KEY REFERENCES question_versions(id) ON DELETE RESTRICT,
            minimum_plan_code VARCHAR(20) NOT NULL REFERENCES membership_plans(code),
            updated_by UUID REFERENCES users(id),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        INSERT INTO question_version_access_policies(question_version_id, minimum_plan_code)
        SELECT v.id, CASE WHEN EXISTS (
            SELECT 1 FROM assessment_items i
            JOIN assessments a ON a.id = i.assessment_id
            LEFT JOIN content_access_policies p ON p.assessment_id = a.id
            LEFT JOIN content_access_policies l ON l.lesson_id = a.lesson_id
            WHERE i.question_version_id = v.id
              AND (p.minimum_plan_code = 'vip' OR l.minimum_plan_code = 'vip')
        ) OR EXISTS (
            SELECT 1 FROM lesson_questions q
            JOIN content_access_policies p ON p.lesson_id = q.lesson_id
            WHERE q.question_version_id = v.id AND p.minimum_plan_code = 'vip'
        ) THEN 'vip' ELSE 'free' END
        FROM question_versions v;
    """)


def downgrade():
    op.drop_table("question_version_access_policies")
