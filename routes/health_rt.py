from fastapi import APIRouter, Depends, HTTPException
from db.targets_db import get_all_targets, add_target, delete_target
from services.health_poll_srv import MEMORY_STATUS
from routes.auth_rt import get_current_user

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/targets", dependencies=[Depends(get_current_user)])
async def list_targets():
    return await get_all_targets()

@router.post("/targets", dependencies=[Depends(get_current_user)])
async def create_target(host: str, port: int, key: str | None = None):
    if not host or not port:
        raise HTTPException(status_code=400, detail="host and port required")
    await add_target(host, port, key)
    return {"ok": True}

@router.delete("/targets/{target_id}", dependencies=[Depends(get_current_user)])
async def remove_target(target_id: int):
    await delete_target(target_id)
    return {"ok": True}

@router.get("/targets/status", dependencies=[Depends(get_current_user)])
async def targets_status():
    return list(MEMORY_STATUS.get("targets", {}).values())