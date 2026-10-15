"""Phiên có thể thu hồi và giới hạn đăng nhập dùng chung giữa các worker."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

revision = "0002_auth_sessions"
down_revision = "0001_baseline"


def upgrade():
    op.create_table(
        "auth_sessions",
        sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("csrf_hash", sa.String(64), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
    )
    op.create_index("idx_auth_sessions_user", "auth_sessions", ["user_id"])
    op.create_table(
        "auth_login_limits",
        sa.Column("key_hash", sa.String(64), primary_key=True),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("failures", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade():
    # Rollback explicite chỉ xóa hai bảng bổ sung; không đụng dữ liệu học tập.
    op.drop_table("auth_login_limits")
    op.drop_index("idx_auth_sessions_user", table_name="auth_sessions")
    op.drop_table("auth_sessions")
