import grpc
import logging
from config.main_conf import settings

try:
    from services.ytadmin_proto import ytadmin_pb2, ytadmin_pb2_grpc
except ImportError:
    ytadmin_pb2 = None
    ytadmin_pb2_grpc = None

logger = logging.getLogger(__name__)

async def check_app_health_grpc():
    """
    Makes a gRPC request to the target application.
    Target App (Server) <- Admin Service (Client)
    """
    if ytadmin_pb2 is None:
        return {"healthy": False, "error": "Proto stubs not found"}

    target = f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}"
    
    try:
        # Use insecure channel for test!! TODO: add TLS
        async with grpc.aio.insecure_channel(target) as channel:
            stub = ytadmin_pb2_grpc.HealthServiceStub(channel)
            
            response = await stub.Check(ytadmin_pb2.HealthRequest(), timeout=2.0)
            
            return {
                "healthy": response.healthy,
                "status_code": "OK" if response.healthy else "UNHEALTHY",
                "details": {"version": response.version, "msg": response.status_message},
                "error": None
            }

    except grpc.RpcError as e:
        code = e.code() if hasattr(e, 'code') else "UNKNOWN"
        return {
            "healthy": False, 
            "status_code": str(code), 
            "error": e.details() if hasattr(e, 'details') else str(e)
        }
    except Exception as e:
        return {
            "healthy": False, 
            "status_code": "INTERNAL", 
            "error": str(e)
        }