"""Classes, scoped recognition, reference prices and VIP training policies."""

from pathlib import Path

from alembic import op

revision = "0011_classes_vip_training"
down_revision = "0010_ai_academy"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        (Path(__file__).resolve().parents[2] / "app/classroom/schema.sql").read_text(
            encoding="utf-8"
        )
    )


def downgrade():
    # Policy changes affect paid access and enrolled children; never silently reverse them.
    raise RuntimeError(
        "Giữ migration có dữ liệu/chính sách; rollback ứng dụng tương thích hoặc restore vào database mới"
    )
