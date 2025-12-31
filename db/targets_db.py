from db.sqlite_db import get_db_connection

async def add_target(host: str, port: int, key: str | None = None):
    async with get_db_connection() as db:
        await db.execute(
            "INSERT INTO targets (host, port, key) VALUES (?, ?, ?)",
            (host, port, key)
        )
        await db.commit()

async def get_all_targets():
    async with get_db_connection() as db:
        async with db.execute("SELECT * FROM targets ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def delete_target(target_id: int):
    async with get_db_connection() as db:
        await db.execute("DELETE FROM targets WHERE id = ?", (target_id,))
        await db.commit()