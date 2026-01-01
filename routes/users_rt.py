from fastapi import APIRouter, Depends
from routes.auth_rt import get_current_user
from db.app_db_pg_srv import fetch_all_users

router = APIRouter(prefix="/api", tags=["Users"])

@router.get("/app/users", dependencies=[Depends(get_current_user)])
async def list_app_users():
    return await fetch_all_users()