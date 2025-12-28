import grpc
import logging
from typing import Dict, Any

from config.main_conf import settings
from db.history_db import save_snapshot

from services.ytadmin_proto import yurtube_pb2, yurtube_pb2_grpc

logger = logging.getLogger(__name__)

class AdminIngestServicer(yurtube_pb2_grpc.AdminIngestServicer):
    async def PushHealth(self, request: yurtube_pb2.PushHealthRequest, context: grpc.aio.ServicerContext) -> yurtube_pb2.PushAck:
        try:
            identity = request.identity
            identity_dict: Dict[str, Any] = {
                "name": identity.name,
                "instance_id": identity.instance_id,
                "host": identity.host,
                "version": identity.version,
            }
            checks = dict(request.checks) if request.checks else {}
            metrics = dict(request.metrics) if request.metrics else {}

            details = {
                "identity": identity_dict,
                "checks": checks,
                "metrics": metrics,
                "ts_iso": request.ts_iso,
                "source": "push"
            }

            host_for_db = identity.host or "unknown"

            await save_snapshot(
                host=host_for_db,
                healthy=bool(request.healthy),
                status_code="PUSH",
                details=details,
                error=None
            )

            return ytadmin_pb2.PushAck(ok=True, message="Health snapshot ingested")
        except Exception as e:
            logger.exception("PushHealth processing failed")
            return ytadmin_pb2.PushAck(ok=False, message=str(e))

    async def PushEffConf(self, request: yurtube_pb2.PushEffConfRequest, context: grpc.aio.ServicerContext) -> yurtube_pb2.PushAck:
        try:
            identity = request.identity
            logger.info(f"EffConf push from {identity.name} ({identity.host}) redacted_keys={list(request.redacted_keys)}")
            return yurtube_pb2.PushAck(ok=True, message="EffConf accepted")
        except Exception as e:
            logger.exception("PushEffConf processing failed")
            return ytadmin_pb2.PushAck(ok=False, message=str(e))

async def start_ingest_server():
    """
    Starts the admin panel's gRPC server to receive Push* RPCs.
    Returns a server object (must be stopped during shutdown).
    """
    server = grpc.aio.server()
    yurtube_pb2_grpc.add_AdminIngestServicer_to_server(AdminIngestServicer(), server)
    bind_addr = f"{settings.ADMIN_INGEST_HOST}:{settings.ADMIN_INGEST_PORT}"
    server.add_insecure_port(bind_addr)
    await server.start()
    logger.info(f"AdminIngest gRPC server started on {bind_addr}")
    return server