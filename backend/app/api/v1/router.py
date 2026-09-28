from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.catalog.router import router as catalog_router
from app.modules.exercises.router import router as exercises_router
from app.modules.students.router import router as students_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(catalog_router)
api_router.include_router(exercises_router)
api_router.include_router(students_router)
