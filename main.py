import asyncio
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from config.main_conf import settings
from db.database_db import init_db
from db.users_db import ensure_admin_exists
from services.health_poll_srv import health_poll_worker
from routes import auth_rt, health_rt, ui_rt
from routes import register_routes


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("--- STARTUP: Initializing DB ---")
    await init_db()
    await ensure_admin_exists()
    
    logger.info("--- STARTUP: Launching Background Tasks ---")
    poll_task = asyncio.create_task(health_poll_worker())
    
    yield
    
    logger.info("--- SHUTDOWN: Stopping Background Tasks ---")
    settings.ADMIN_ENABLED = False
    await poll_task

app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan, docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.ADMIN_HOST, port=settings.ADMIN_PORT, reload=True)