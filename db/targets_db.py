from typing import List, Optional
from db.sqlite_db import get_db_connection

async def _next_sort_index(db) -> int:
    async with db.execute("SELECT COALESCE(MAX(sort_index), -1) AS max_idx FROM targets") as cursor:
        row = await cursor.fetchone()
        max_idx = row["max_idx"] if row else -1
        return int(max_idx) + 1

async def add_target(host: str, port: int, key: Optional[str] = None, app_name: Optional[str] = None):
    async with get_db_connection() as db:
        next_idx = await _next_sort_index(db)
        await db.execute(
            "INSERT INTO targets (host, port, key, app_name, sort_index) VALUES (?, ?, ?, ?, ?)",
            (host, port, key, app_name, next_idx)
        )
        await db.commit()

async def get_all_targets():
    async with get_db_connection() as db:
        async with db.execute("SELECT * FROM targets ORDER BY sort_index ASC, created_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def delete_target(target_id: int):
    async with get_db_connection() as db:
        await db.execute("DELETE FROM targets WHERE id = ?", (target_id,))
        await db.commit()

async def update_target(target_id: int, host: Optional[str] = None, port: Optional[int] = None, key: Optional[str] = None, app_name: Optional[str] = None):
    fields = []
    params = []
    if host is not None:
        fields.append("host = ?")
        params.append(host)
    if port is not None:
        fields.append("port = ?")
        params.append(port)
    if key is not None:
        fields.append("key = ?")
        params.append(key)
    if app_name is not None:
        fields.append("app_name = ?")
        params.append(app_name)
    if not fields:
        return
    params.append(target_id)
    async with get_db_connection() as db:
        await db.execute(f"UPDATE targets SET {', '.join(fields)} WHERE id = ?", params)
        await db.commit()

async def reorder_targets(order: List[int]):
    # order = list of target IDs in desired order, assign incremental sort_index
    async with get_db_connection() as db:
        for idx, tid in enumerate(order):
            await db.execute("UPDATE targets SET sort_index = ? WHERE id = ?", (idx, tid))
        await db.commit()