import aiosqlite
from contextlib import asynccontextmanager
from config.main_conf import settings

@asynccontextmanager
async def get_db_connection():
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db