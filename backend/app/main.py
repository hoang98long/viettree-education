import json
import logging
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api import router
from app.authoring_api import router as authoring_router
from app.core.config import settings
from app.db import db, engine
from app.lesson_api import router as lesson_router
from app.membership_api import router as membership_router
from app.vip_api import router as vip_router

logger = logging.getLogger("viettree")
logging.basicConfig(level=logging.INFO, format="%(message)s")
app = FastAPI(title="VietTree Education API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["Content-Type", "X-CSRF-Token", "Idempotency-Key"],
)
app.include_router(router)
app.include_router(membership_router)
app.include_router(authoring_router)
app.include_router(vip_router)
app.include_router(lesson_router)


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
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    logger.info(
        json.dumps(
            {
                "method": request.method,
                "status": response.status_code,
                "duration_ms": round((time.monotonic() - started) * 1000),
            }
        )
    )
    return response


@app.exception_handler(SQLAlchemyError)
async def database_error(request, error):
    logger.error(json.dumps({"error": "database_operation_failed", "type": type(error).__name__}))
    return JSONResponse(
        status_code=503, content={"detail": "Dữ liệu tạm chưa truy cập được. Hãy thử lại nhé"}
    )


@app.exception_handler(RuntimeError)
async def schema_error(request, error):
    logger.error(json.dumps({"error": "schema_not_ready"}))
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
            conn.execute(text("SELECT 1"))
            db.validate(conn)
        return {"status": "ready"}
    except (SQLAlchemyError, RuntimeError):
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "detail": "Kiểm tra DB / schema / alembic"},
        )
