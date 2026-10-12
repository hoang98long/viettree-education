"""Account edit revisions and temporary password lifecycle; preserve existing accounts."""

from alembic import op

revision = "0008_account_management"
down_revision = "0007_lesson_studio"


def upgrade():
    op.execute("""
        ALTER TABLE users
          ADD COLUMN account_revision INTEGER NOT NULL DEFAULT 1 CHECK (account_revision >= 1),
          ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT FALSE,
          ADD COLUMN password_changed_at TIMESTAMPTZ;
    """)


def downgrade():
    op.execute("""
        ALTER TABLE users DROP COLUMN password_changed_at,
          DROP COLUMN must_change_password, DROP COLUMN account_revision;
    """)
