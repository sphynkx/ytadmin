from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from db.users_db import get_user_by_username
from utils.security_ut import verify_password
import uuid

router = APIRouter(tags=["Auth"])

# In-memory session storage {session_id: username}
SESSIONS = {} 

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(form_data.username)
    
    if not user or not verify_password(user['password_hash'], form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user['username']
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="strict",
        max_age=3600 * 12
    )
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    response.delete_cookie("session_id")
    return {"message": "Logged out"}

async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return SESSIONS[session_id]