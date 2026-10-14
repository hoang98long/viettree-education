import json
import logging
import time
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.router import router
from app.core.config import settings
from app.db import SchemaNotReady, db, engine
from app.operations import readiness

logger = logging.getLogger("viettree")
logging.basicConfig(level=logging.INFO, format="%(message)s")
production = settings().app_env == "production"
app = FastAPI(
    title="VietTree Education API",
    version="0.1.0",
    docs_url=None if production else "/docs",
    redoc_url=None if production else "/redoc",
    openapi_url=None if production else "/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["Content-Type", "X-CSRF-Token", "Idempotency-Key"],
)


app.include_router(router)


@app.exception_handler(RequestValidationError)
async def invalid_request(request, error):
    # Không phản chiếu input: có thể chứa password hoặc câu trả lời của học sinh.
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Dữ liệu gửi lên chưa đúng định dạng. Hãy kiểm tra các trường và thử lại"
        },
    )


@app.middleware("http")
async def request_logging(request: Request, call_next):
    started = time.monotonic()
    request.state.received_at = datetime.now(UTC)
    request.state.request_id = uuid4().hex
    try:
        response = await call_next(request)
    except Exception as error:
        # Không log exception text/traceback: có thể chứa SQL, bí mật hoặc input.
        logger.error(
            json.dumps(
                {
                    "error": "unexpected_error",
                    "type": type(error).__name__,
                    "request_id": request.state.request_id,
                }
            )
        )
        response = JSONResponse(
            status_code=500,
            content={
                "detail": "Hệ thống tạm gặp lỗi. Hãy thử lại hoặc gửi mã hỗ trợ "
                + request.state.request_id[:12]
                + " cho quản trị viên"
            },
        )
    if not getattr(request.state, "academy_asset_cache", False):
        response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["X-Frame-Options"] = "DENY"
    logger.info(
        json.dumps(
            {
                "method": request.method,
                "status": response.status_code,
                "duration_ms": round((time.monotonic() - started) * 1000),
                "request_id": request.state.request_id,
            }
        )
    )
    return response


@app.exception_handler(SQLAlchemyError)
async def database_error(request, error):
    original = getattr(error, "orig", None)
    logger.error(
        json.dumps(
            {
                "error": "database_operation_failed",
                "type": type(error).__name__,
                "sqlstate": getattr(original, "sqlstate", None),
                "constraint": getattr(getattr(original, "diag", None), "constraint_name", None),
                "request_id": request.state.request_id,
            }
        )
    )
    return JSONResponse(
        status_code=503, content={"detail": "Dữ liệu tạm chưa truy cập được. Hãy thử lại nhé"}
    )


@app.exception_handler(SchemaNotReady)
async def schema_error(request, error):
    logger.error(json.dumps({"error": "schema_not_ready", "request_id": request.state.request_id}))
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Schema chưa sẵn sàng. Quản trị viên hãy chạy check-schema và migration"
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        with engine().connect() as conn:
            readiness.check(conn)
            # Compose waits for /ready before exposing the site. Reflect the
            # API metadata here, so a login burst does not initialize it while
            # holding every connection in the small VPS pool.
            db.load(conn)
        return {"status": "ready"}
    except (SQLAlchemyError, SchemaNotReady):
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "detail": "Kiểm tra DB / schema / alembic"},
        )
