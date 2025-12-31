from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from routes.auth_rt import SESSIONS

router = APIRouter(tags=["UI"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index(request: Request):
    session_id = request.cookies.get("session_id")
    user = SESSIONS.get(session_id)
    
    if not user:
        return templates.TemplateResponse("login.html", {"request": request})
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": user})

@router.get("/targets")
async def targets_page(request: Request):
    session_id = request.cookies.get("session_id")
    user = SESSIONS.get(session_id)
    
    if not user:
        return templates.TemplateResponse("login.html", {"request": request})
    
    return templates.TemplateResponse("targets.html", {"request": request, "username": user})