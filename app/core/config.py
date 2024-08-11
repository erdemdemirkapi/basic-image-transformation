import logging
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Image Transformation"
    API_V1_STR: str = "/api/v1"

    LOGGING_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()

logging.basicConfig(
    level=settings.LOGGING_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
