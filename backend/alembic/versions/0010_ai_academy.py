"""Isolated Academy tables; preserve all existing LMS data and roles."""

from pathlib import Path

from sqlalchemy import text

from alembic import op
from app.academy.tables import TABLES

revision = "0010_ai_academy"
down_revision = "0009_guided_hints"


def upgrade():
    source = Path(__file__).resolve().parents[2] / "app/academy/schema.sql"
    op.execute(source.read_text(encoding="utf-8"))


def downgrade():
    connection = op.get_bind()
    if any(
        connection.execute(text(f"SELECT EXISTS(SELECT 1 FROM {name})")).scalar_one()
        for name in TABLES
    ):
        raise RuntimeError(
            "Academy có dữ liệu: giữ nguyên, dùng backup/restore riêng; không downgrade phá dữ liệu"
        )
    for name in reversed(TABLES):
        op.drop_table(name)
