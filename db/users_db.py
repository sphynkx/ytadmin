from db.sqlite_db import get_db_connection
from utils.security_ut import get_password_hash
from config.main_conf import settings
import logging

logger = logging.getLogger(__name__)

async def get_user_by_username(username: str):
    async with get_db_connection() as db:
        async with db.execute("SELECT * FROM users WHERE username = ?", (username,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def create_user(username: str, password_str: str):
    hashed = get_password_hash(password_str)
    async with get_db_connection() as db:
        await db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed)
        )
        await db.commit()

async def ensure_admin_exists():
    target_user = settings.ADMIN_USERNAME
    user = await get_user_by_username(target_user)
    
    if not user:
        logger.info(f"--- [DB] Creating initial admin user: {target_user} ---")
        await create_user(target_user, settings.ADMIN_PASSWORD)
    else:
        logger.info(f"--- [DB] Admin user '{target_user}' already exists ---")