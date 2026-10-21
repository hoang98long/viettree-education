from fastapi import APIRouter, Depends

from app.core.dependencies import database
from app.core.security import admin_user
from app.operations import system_report

router = APIRouter(prefix="/api/v1/admin", tags=["operations"])


@router.get("/system-status", response_model=dict)
def system_status(user=Depends(admin_user), conn=database):
    return system_report(conn)


@router.get("/release-status", response_model=dict)
def release_status(user=Depends(admin_user), conn=database):
    from app.services.release_readiness import release_report

    return release_report(conn)
