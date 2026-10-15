"""Account-owned lesson bookmarks; no changes to existing learning records."""

from alembic import op

revision = "0012_lesson_bookmarks"
down_revision = "0011_classes_vip_training"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE student_lesson_bookmarks (
            student_id UUID NOT NULL REFERENCES student_profiles(student_id) ON DELETE CASCADE,
            lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            PRIMARY KEY (student_id, lesson_id)
        )
    """)
    op.execute("CREATE INDEX idx_lesson_bookmarks_lesson ON student_lesson_bookmarks(lesson_id)")


def downgrade():
    raise RuntimeError("Giữ dữ liệu bài đã lưu; rollback ứng dụng tương thích thay vì xóa bảng.")
