"""A tiny DB pool must not block the threads that release its connections."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from time import sleep

import pytest
from anyio import to_thread
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.db import connection, db


@pytest.mark.integration
def test_connection_waiters_do_not_starve_endpoint_or_commit_threads(test_engine, monkeypatch):
    with test_engine.connect() as conn:
        db.load(conn)
    limited = create_engine(
        test_engine.url, pool_size=1, max_overflow=0, pool_timeout=2, hide_parameters=True
    )
    monkeypatch.setattr("app.db.engine", lambda: limited)

    @asynccontextmanager
    async def lifespan(_app):
        limiter = to_thread.current_default_thread_limiter()
        previous = limiter.total_tokens
        limiter.total_tokens = 1
        try:
            yield
        finally:
            limiter.total_tokens = previous

    application = FastAPI(lifespan=lifespan)

    @application.get("/query")
    def query(conn=Depends(connection, scope="function")):
        sleep(0.02)
        return {"value": conn.execute(text("SELECT 1")).scalar_one()}

    try:
        with TestClient(application) as client, ThreadPoolExecutor(max_workers=6) as pool:
            responses = list(pool.map(lambda _: client.get("/query"), range(6)))
            assert all(r.status_code == 200 and r.json() == {"value": 1} for r in responses)
        assert limited.pool.checkedout() == 0
    finally:
        limited.dispose()
