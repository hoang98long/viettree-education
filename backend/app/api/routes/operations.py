from fastapi import APIRouter, Depends

from app.core.dependencies import database
from app.core.security import admin_user
from app.operations import system_report

router = APIRouter(prefix="/api/v1/admin", tags=["operations"])


@router.get("/system-status", response_model=dict)
def system_status(user=Depends(admin_user), conn=database):
    return system_report(conn)
