from unittest.mock import Mock

import pytest
from sqlalchemy import Column, Integer, Table
from sqlalchemy.exc import OperationalError

from app.db import Database


def test_failed_reflection_does_not_publish_partial_tables_and_can_retry(monkeypatch):
    database = Database()
    monkeypatch.setattr(database, "validate", Mock())
    calls = 0

    def reflect(metadata, connection, only):
        nonlocal calls
        calls += 1
        Table("users", metadata, Column("id", Integer, primary_key=True))
        if calls == 1:
            raise OperationalError("reflection interrupted", {}, Exception("offline"))
        Table("auth_sessions", metadata, Column("id", Integer, primary_key=True))

    monkeypatch.setattr("app.db.MetaData.reflect", reflect)
    with pytest.raises(OperationalError):
        database.load(Mock())
    assert not database.metadata.tables
    database.load(Mock())
    assert set(database.metadata.tables) == {"users", "auth_sessions"}
    database.load(Mock())
    assert calls == 2
