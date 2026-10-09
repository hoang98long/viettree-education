"""Monotonic revisions for concurrent draft editing and review."""

from alembic import op

revision = "0005_authoring_revisions"
down_revision = "0004_question_authoring"


def upgrade():
    for table in ("question_versions", "assessments"):
        op.execute(
            f"ALTER TABLE {table} ADD COLUMN edit_revision INTEGER NOT NULL DEFAULT 1 CHECK (edit_revision >= 1)"
        )


def downgrade():
    for table in ("assessments", "question_versions"):
        op.drop_column(table, "edit_revision")
