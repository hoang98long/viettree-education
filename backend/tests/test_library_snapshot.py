import pytest
from sqlalchemy import event, select

from app.db import db
from app.fixtures.development import seed
from app.services.lesson_library import lesson_library
from tests.test_concurrency import create_student


@pytest.mark.integration
def test_library_count_and_page_remain_consistent_when_progress_changes_between_reads(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        user = create_student(conn)
        lessons = db.table("lessons")
        topics, subjects = db.table("topics"), db.table("subjects")
        lesson_id = conn.execute(
            select(lessons.c.id)
            .select_from(
                lessons.join(topics, lessons.c.topic_id == topics.c.id).join(
                    subjects, subjects.c.id == topics.c.subject_id
                )
            )
            .where(topics.c.grade == 4, subjects.c.code == "MATH", lessons.c.status == "published")
            .limit(1)
        ).scalar_one()
        progress = db.table("student_lesson_progress")
        conn.execute(
            progress.insert().values(
                student_id=user["id"], lesson_id=lesson_id, status="in_progress"
            )
        )
    changed = False
    with test_engine.begin() as reader:

        def concurrent_completion(conn, cursor, statement, parameters, context, executemany):
            nonlocal changed
            if not changed and "student_lesson_progress" in statement and "lessons" in statement:
                changed = True
                with test_engine.begin() as writer:
                    writer.execute(
                        progress.update()
                        .where(
                            progress.c.student_id == user["id"], progress.c.lesson_id == lesson_id
                        )
                        .values(status="completed", completion_ratio=1)
                    )

        event.listen(reader, "after_cursor_execute", concurrent_completion)
        first = lesson_library(reader, user, progress="completed")
        assert changed
        assert first["summary"]["total"] == 0
        assert first["items"] == []
        second = lesson_library(reader, user, progress="completed")
        assert second["summary"]["total"] == len(second["items"]) == 1
