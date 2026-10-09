"""Baseline 34 bảng đã import; tuyệt đối không tạo/xóa schema gốc."""
from alembic import op

from app.db import Database

revision = "0001_baseline"
down_revision = None


def upgrade():
    Database().validate(op.get_bind(), include_auth=False)


def downgrade():
    pass
