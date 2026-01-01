import asyncpg
import logging
from typing import List, Dict, Any, Optional
from config.main_conf import settings

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.pool.Pool] = None

async def init_app_db_pool():
    global _pool
    if _pool is not None:
        return
    try:
        _pool = await asyncpg.create_pool(
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            min_size=1,
            max_size=5,
            command_timeout=5
        )
        logger.info("App DB pool initialized")
    except Exception as e:
        logger.error(f"Failed to init app DB pool: {e}")
        _pool = None

async def close_app_db_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("App DB pool closed")

async def fetch_all_users() -> List[Dict[str, Any]]:
    """
    SELECT * FROM users in the application database.
    Returns list of dicts with all columns.
    """
    global _pool
    if _pool is None:
        raise RuntimeError("App DB pool is not initialized")
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
        result: List[Dict[str, Any]] = []
        for r in rows:
            result.append(dict(r))
        return result