from db.sqlite_db import get_db_connection

# DB scheme
INIT_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host TEXT NOT NULL,
    port INTEGER NOT NULL,
    key TEXT,
    app_name TEXT,            -- user-provided display name for dashboard
    sort_index INTEGER DEFAULT 0, -- ordering index for dashboard/targets list
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_targets_host_port ON targets(host, port);
"""

async def init_db():
    async with get_db_connection() as db:
        await db.executescript(INIT_SQL)
        await db.commit()