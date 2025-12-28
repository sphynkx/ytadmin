import json
from db.sqlite_db import get_db_connection

async def save_snapshot(host: str, healthy: bool, status_code: str = None, details: dict = None, error: str = None):
    details_json = json.dumps(details) if details else None
    
    async with get_db_connection() as db:
        await db.execute(
            """
            INSERT INTO health_snapshots 
            (service_host, healthy, status_code, details_json, error_message) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (host, healthy, status_code, details_json, error)
        )
        await db.commit()

async def get_recent_snapshots(limit: int = 10):
    async with get_db_connection() as db:
        async with db.execute(
            "SELECT * FROM health_snapshots ORDER BY created_at DESC LIMIT ?", 
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]