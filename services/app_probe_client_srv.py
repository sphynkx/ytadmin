import grpc
import logging
from config.main_conf import settings

from services.ytadmin_proto import yurtube_pb2, yurtube_pb2_grpc

logger = logging.getLogger(__name__)

async def get_app_identity():
    """Requests ServiceIdentity from the application (pull)."""
    target = f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}"
    try:
        async with grpc.aio.insecure_channel(target) as channel:
            stub = yurtube_pb2_grpc.AppProbeStub(channel)
            resp = await stub.GetIdentity(yurtube_pb2.IdentityRequest(), timeout=2.0)
            return {
                "name": resp.name,
                "instance_id": resp.instance_id,
                "host": resp.host,
                "version": resp.version,
            }
    except Exception as e:
        logger.warning(f"GetIdentity failed: {e}")
        return None