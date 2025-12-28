from fastapi import APIRouter, Depends
from db.history_db import get_recent_snapshots
from services.health_poll_srv import MEMORY_STATUS
from routes.auth_rt import get_current_user

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("/current", dependencies=[Depends(get_current_user)])
async def get_current_status():
    return MEMORY_STATUS

@router.get("/history", dependencies=[Depends(get_current_user)])
async def get_history(limit: int = 20):
    return await get_recent_snapshots(limit)