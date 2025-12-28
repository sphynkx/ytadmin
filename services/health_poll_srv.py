import asyncio
import logging
import time
from config.main_conf import settings
from services.grpc_client_srv import check_app_health_grpc
from db.history_db import save_snapshot
from services.app_probe_client_srv import get_app_identity

logger = logging.getLogger(__name__)

# In-memory storage for UI
MEMORY_STATUS = {
    "healthy": False,
    "last_check": "Never",
    "details": {}
}

async def health_poll_worker():
    logger.info(f"--- Poll Worker Started (Target: {settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}) ---")
    
    try:
        while True:
            try:
                if settings.ADMIN_PULL_ENABLED:
                    result = await check_app_health_grpc()
                    
                    # Refresh memory
                    MEMORY_STATUS["healthy"] = result.get("healthy", False)

                    enriched_details = result.get("details") or {}
                    cached_identity = MEMORY_STATUS.get("details", {}).get("identity")
                    if not cached_identity:
                        ident = await get_app_identity()
                        if ident:
                            cached_identity = ident
                    if cached_identity:
                        enriched_details["identity"] = cached_identity

                    enriched_details.setdefault("target", f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}")

                    MEMORY_STATUS["details"] = enriched_details

                    # Write history to DB
                    await save_snapshot(
                        host=f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}",
                        healthy=result.get("healthy", False),
                        status_code=str(result.get("status_code")),
                        details=enriched_details,
                        error=result.get("error")
                    )
                else:
                    # Push-only
                    last_push = MEMORY_STATUS.get("last_push_ts")
                    now = time.time()
                    if last_push and (now - last_push) < settings.PUSH_STALE_THRESHOLD_SEC:
                        MEMORY_STATUS["healthy"] = True
                        status_code = "PUSH_OK"
                    else:
                        MEMORY_STATUS["healthy"] = False
                        status_code = "PUSH_STALE"

                    await save_snapshot(
                        host=f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}",
                        healthy=MEMORY_STATUS["healthy"],
                        status_code=status_code,
                        details=MEMORY_STATUS.get("details"),
                        error=None
                    )
            except Exception as e:
                logger.error(f"Poll worker iteration error: {e}")
            
            await asyncio.sleep(settings.ADMIN_POLL_INTERVAL_SEC)

    except asyncio.CancelledError:
        logger.info("Health poll worker stopped by cancel signal")
        raise