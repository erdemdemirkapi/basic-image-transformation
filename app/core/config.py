import logging
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Image Transformation"
    API_V1: str = "/api/v1"

    LOGGING_LEVEL: str = "INFO"
    LOG_FILE: str = os.getenv("LOG_FILE", default="app.log")
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", default=True)
    LOG_TO_CONSOLE: bool = os.getenv("LOG_TO_CONSOLE", default=True)

    class Config:
        env_file = ".env"


settings = Settings()

log_handlers = []
if settings.LOG_TO_CONSOLE:
    log_handlers.append(logging.StreamHandler())

if settings.LOG_TO_FILE:
    log_handlers.append(logging.FileHandler(settings.LOG_FILE))

logging.basicConfig(
    level=settings.LOGGING_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=log_handlers
)
