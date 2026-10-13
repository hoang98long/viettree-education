"""Register all public API modules in one place."""

from fastapi import APIRouter

from app.academy.api import router as academy_router
from app.academy.management_api import router as academy_management_router
from app.api.routes.accounts import router as accounts_router
from app.api.routes.administration import router as administration_router
from app.api.routes.assessments import router as assessments_router
from app.api.routes.attempts import router as attempts_router
from app.api.routes.auth import router as auth_router
from app.api.routes.authoring import router as authoring_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.curriculum import router as curriculum_router
from app.api.routes.learning import router as learning_router
from app.api.routes.lesson_library import router as lesson_library_router
from app.api.routes.lesson_studio import router as lesson_studio_router
from app.api.routes.memberships import router as memberships_router
from app.api.routes.operations import router as operations_router
from app.api.routes.vip import router as vip_router
from app.classroom.api import router as classroom_router

router = APIRouter()
router.include_router(lesson_library_router)
router.include_router(auth_router)
router.include_router(catalog_router)
router.include_router(learning_router)
router.include_router(assessments_router)
router.include_router(attempts_router)
router.include_router(administration_router)
router.include_router(memberships_router)
router.include_router(authoring_router)
router.include_router(vip_router)
router.include_router(lesson_studio_router)
router.include_router(curriculum_router)
router.include_router(accounts_router)
router.include_router(operations_router)
router.include_router(academy_management_router)
router.include_router(academy_router)
router.include_router(classroom_router)
