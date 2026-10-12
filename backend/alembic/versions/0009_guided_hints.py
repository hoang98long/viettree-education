"""Enable guided hints for VIP; retain all existing plan features and memberships."""

from alembic import op

revision = "0009_guided_hints"
down_revision = "0008_account_management"


def upgrade():
    op.execute("""
        INSERT INTO membership_plan_features(plan_code, feature_code)
        VALUES ('vip', 'learning.guided_hints') ON CONFLICT DO NOTHING
    """)


def downgrade():
    op.execute("""
        DELETE FROM membership_plan_features
        WHERE plan_code = 'vip' AND feature_code = 'learning.guided_hints'
    """)
