"""Production entry point with bounded workers, connections and graceful stop."""

import uvicorn

from app.core.config import settings


def server_options():
    config = settings()
    return dict(
        host="0.0.0.0",
        port=8000,
        workers=config.server_workers,
        limit_concurrency=config.server_limit_concurrency,
        timeout_graceful_shutdown=config.server_graceful_timeout,
        proxy_headers=True,
        forwarded_allow_ips="172.30.40.2",
        access_log=False,
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", **server_options())
