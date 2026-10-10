"""Enable VIP library, personal reports and review of already graded own answers."""

from alembic import op

revision = "0006_vip_learning_tools"
down_revision = "0005_authoring_revisions"


def upgrade():
    op.execute("""
        INSERT INTO membership_plan_features(plan_code, feature_code)
        VALUES ('vip', 'vip.library'), ('vip', 'review.mistakes'), ('vip', 'reports.personal')
        ON CONFLICT DO NOTHING
    """)


def downgrade():
    # Chỉ thu hồi ba quyền mới, giữ nguyên nội dung, bài làm và gói đã cấp.
    op.execute("""
        DELETE FROM membership_plan_features WHERE plan_code = 'vip'
        AND feature_code IN ('vip.library', 'review.mistakes', 'reports.personal')
    """)
