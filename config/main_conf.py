import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_TITLE: str = "Admin Control Plane"
    
    ADMIN_HOST: str = "0.0.0.0" 
    ADMIN_PORT: int = 9090
    
    ADMIN_ENABLED: bool = True
    ADMIN_POLL_INTERVAL_SEC: int = 10

    # Enables/disables pull polling of grpc.health.v1 Health/Check
    ADMIN_PULL_ENABLED: bool = True
    # Push data staleness threshold (in seconds) if pull is disabled
    PUSH_STALE_THRESHOLD_SEC: int = 60

    # Universal method for obtaining complete info from an app/services (via `grpcurl` + reflection)
    INFO_METHOD: str = "grpc.health.v1.Info/All"
    INFO_TIMEOUT_SEC: int = 3

    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "SECRET"

    TARGET_APP_HOST: str = "localhost"
    TARGET_APP_PORT: int = 50051
    
    DB_PATH: str = "admin.db"

    class Config:
        env_file = ".env"

settings = Settings()