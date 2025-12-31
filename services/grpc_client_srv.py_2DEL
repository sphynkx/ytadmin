import grpc
import logging
from config.main_conf import settings
from grpc_health.v1 import health_pb2, health_pb2_grpc

logger = logging.getLogger(__name__)

async def check_app_health_grpc():
    """
    Makes a gRPC request to the standard grpc.health.v1.Health service on the target application.
    """
    target = f"{settings.TARGET_APP_HOST}:{settings.TARGET_APP_PORT}"
    
    try:
        async with grpc.aio.insecure_channel(target) as channel:
            stub = health_pb2_grpc.HealthStub(channel)
            
            request = health_pb2.HealthCheckRequest(service="")
            
            response = await stub.Check(request, timeout=2.0)
            
            is_serving = (response.status == health_pb2.HealthCheckResponse.SERVING)
            status_name = health_pb2.HealthCheckResponse.ServingStatus.Name(response.status)
            
            return {
                "healthy": is_serving,
                "status_code": status_name,
                "details": {"msg": "Standard Health Check OK"},
                "error": None
            }

    except grpc.RpcError as e:
        code = e.code() if hasattr(e, 'code') else "UNKNOWN"
        details = e.details() if hasattr(e, 'details') else str(e)
        return {
            "healthy": False, 
            "status_code": str(code),
            "details": {},
            "error": details
        }
    except Exception as e:
        return {
            "healthy": False, 
            "status_code": "INTERNAL", 
            "details": {},
            "error": str(e)
        }