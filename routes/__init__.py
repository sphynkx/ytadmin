from fastapi import FastAPI
from . import auth_rt, health_rt, ui_rt, users_rt

def register_routes(app: FastAPI):
    app.include_router(auth_rt.router)
    app.include_router(health_rt.router)
    app.include_router(ui_rt.router)
    app.include_router(users_rt.router)