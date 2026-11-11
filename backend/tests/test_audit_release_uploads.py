import base64
from io import BytesIO
from uuid import uuid4

import pytest
from fastapi import HTTPException
from PIL import Image
from sqlalchemy import event, select

from app.academy import uploads
from app.db import db
from app.services.content_review import review_learning_content
from app.services.release_readiness import release_report


def test_disallowed_image_decoder_is_never_invoked(monkeypatch):
    buffer = BytesIO()
    Image.new("RGB", (2, 2), "white").save(buffer, format="GIF")
    Image.init()
    original, accept = Image.OPEN["GIF"]
    calls = []

    def factory(*args, **kwargs):
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setitem(Image.OPEN, "GIF", (factory, accept))
    with pytest.raises(HTTPException) as error:
        uploads.upload(
            None, {"id": uuid4()}, {"data": base64.b64encode(buffer.getvalue()).decode()}
        )
    assert error.value.status_code == 422
    assert not calls, "Unsupported formats must be rejected before their plugin parses input"


@pytest.mark.integration
def test_release_diagnostics_identifies_pending_editorial_update_without_writes(conn):
    lessons = db.table("lessons")
    before = list(conn.execute(select(lessons.c.id, lessons.c.content)).all())
    report = release_report(conn)
    pending = next(row for row in report["checks"] if row["code"] == "editorial_content")
    assert not pending["ok"] and pending["count"] > 0
    assert list(conn.execute(select(lessons.c.id, lessons.c.content)).all()) == before
    assert any(row["code"] == "editorial_content" for row in report["next_steps"])
    review_learning_content(conn, apply=True)
    assert next(
        row for row in release_report(conn)["checks"] if row["code"] == "editorial_content"
    )["ok"]


@pytest.mark.integration
def test_editorial_preview_reads_lessons_and_drafts_in_two_queries(conn):
    queries = []

    def record(_conn, _cursor, statement, _parameters, _context, _many):
        queries.append(statement)

    event.listen(conn, "before_cursor_execute", record)
    try:
        report = review_learning_content(conn)
    finally:
        event.remove(conn, "before_cursor_execute", record)
    assert len(report["items"]) == 232 and report["counts"]["eligible"] > 0
    assert len(queries) == 2, (
        "Diagnostics must batch the whole inventory instead of querying per lesson"
    )
