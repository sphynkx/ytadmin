import asyncio
import logging
from config.main_conf import settings
from services.grpcurl_exec_srv import exec_grpcurl
from db.targets_db import get_all_targets

logger = logging.getLogger(__name__)

# In-memory storage for UI
MEMORY_STATUS = {
    "healthy": False,
    "last_check": "Never",
    "details": {},
    # statuses per all monitored targets
    "targets": {}  # key -> {"host","port","healthy","status_code","details"}
}

async def poll_one_target(host: str, port: int):
    target = f"{host}:{port}"

    info = await exec_grpcurl(
        host, port,
        method=settings.INFO_METHOD,
        timeout_sec=settings.INFO_TIMEOUT_SEC
    )
    healthy_info = isinstance(info, dict) and not info.get("error")

    healthy_check = False
    status_code = "UNKNOWN"
    check = None
    if settings.ADMIN_PULL_ENABLED:
        check = await exec_grpcurl(
            host, port,
            method="grpc.health.v1.Health/Check",
            data={"service": ""}
        )
        healthy_check = (isinstance(check, dict) and check.get("status") == "SERVING")
        status_code = check.get("status") if isinstance(check, dict) else "ERROR"

    healthy = healthy_info or healthy_check

    details = {"source": "grpcurl", "target": target}
    if healthy_info:
        details["info"] = info
        if "app_name" in info:
            details["app_name"] = info["app_name"]
        if "uptime" in info:
            details["uptime"] = info["uptime"]
    else:
        if isinstance(info, dict) and info.get("error"):
            details["info_error"] = info["error"]

    if settings.ADMIN_PULL_ENABLED and isinstance(check, dict):
        details["raw_status"] = check.get("status")

    return {
        "host": host,
        "port": port,
        "healthy": healthy,
        "status_code": status_code if settings.ADMIN_PULL_ENABLED else ("INFO_OK" if healthy_info else "ERROR"),
        "details": details
    }

async def health_poll_worker():
    logger.info(f"--- Poll Worker Started (targets from DB) ---")
    
    try:
        while True:
            try:
                targets = await get_all_targets()
                statuses = {}
                for t in targets:
                    host = t["host"]
                    port = int(t["port"])
                    res = await poll_one_target(host, port)
                    statuses[f"{host}:{port}"] = res

                MEMORY_STATUS["targets"] = statuses

                MEMORY_STATUS["healthy"] = all(s["healthy"] for s in statuses.values()) if statuses else False
                MEMORY_STATUS["details"] = {"targets_count": len(statuses)}
            except Exception as e:
                logger.error(f"Poll worker iteration error: {e}")
            
            await asyncio.sleep(settings.ADMIN_POLL_INTERVAL_SEC)

    except asyncio.CancelledError:
        logger.info("Health poll worker stopped by cancel signal")
        raise