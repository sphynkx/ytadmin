import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_TITLE: str = "Admin Control Plane"
    
    ADMIN_HOST: str = "0.0.0.0" 
    ADMIN_PORT: int = 9090
    
    ADMIN_ENABLED: bool = True
    ADMIN_POLL_INTERVAL_SEC: int = 10

    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "SECRET"

    TARGET_APP_HOST: str = "localhost"
    TARGET_APP_PORT: int = 50051
    
    ADMIN_INGEST_HOST: str = "0.0.0.0"
    ADMIN_INGEST_PORT: int = 50052
    
    DB_PATH: str = "admin.db"

    class Config:
        env_file = ".env"

settings = Settings()