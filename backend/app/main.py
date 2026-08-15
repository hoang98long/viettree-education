from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import Base, engine
from app import models  # noqa: F401 - imports all SQLAlchemy mappings

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)  # development bootstrap; replace with Alembic migration in production
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["Hệ thống"])
def health():
    return {"status": "ok", "service": "viettree-api"}
