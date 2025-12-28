import asyncio
import logging
from config.main_conf import settings
from services.grpc_client_srv import check_app_health_grpc
from db.history_db import save_snapshot

logger = logging.getLogger(__name__)

# In-memory storage for UI
MEMORY_STATUS = {
    "healthy": False,
    "last_check": "Never",
    "details": {}
}

async def health_poll_worker():
    logger.info(f"--- Poll Worker Started (Target: {settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}) ---")
    
    while settings.ADMIN_ENABLED:
        try:
            result = await check_app_health_grpc()
            
            # Refresh memory
            MEMORY_STATUS["healthy"] = result.get("healthy", False)
            MEMORY_STATUS["details"] = result
            
            # Write history to DB
            await save_snapshot(
                host=f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}",
                healthy=result.get("healthy", False),
                status_code=str(result.get("status_code")),
                details=result.get("details"),
                error=result.get("error")
            )
            
        except Exception as e:
            logger.error(f"Poll worker error: {e}")
            
        await asyncio.sleep(settings.ADMIN_POLL_INTERVAL_SEC)