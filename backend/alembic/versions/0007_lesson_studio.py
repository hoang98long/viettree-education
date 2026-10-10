"""Separate editable lesson drafts from the lesson visible to students."""

from alembic import op

revision = "0007_lesson_studio"
down_revision = "0006_vip_learning_tools"


def upgrade():
    op.execute("""
        CREATE TABLE lesson_drafts (
            lesson_id UUID PRIMARY KEY REFERENCES lessons(id) ON DELETE RESTRICT,
            payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
            source_fingerprint CHAR(64) NOT NULL,
            edit_revision INTEGER NOT NULL DEFAULT 1 CHECK (edit_revision >= 1),
            status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'published')),
            updated_by UUID REFERENCES users(id) ON DELETE SET NULL,
            reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
            reviewed_at TIMESTAMPTZ,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)


def downgrade():
    # Only working copies are removed. Published lessons, policies and history remain.
    op.drop_table("lesson_drafts")
