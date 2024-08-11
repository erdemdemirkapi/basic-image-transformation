from fastapi import FastAPI
from app.api.image_transformation import router as image_transformation_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(image_transformation_router, prefix=settings.API_V1_STR)
