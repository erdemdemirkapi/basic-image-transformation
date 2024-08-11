from fastapi import FastAPI, Request
import logging
import time

from app.api.image_transformation import router as image_transformation_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(image_transformation_router, prefix=settings.API_V1_STR)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_time = time.time()

    logger.info(f"Received request: {request.method} {request.url}")
    logger.info(f"Request Headers: {request.headers}")

    response = await call_next(request)

    response_time = time.time() - request_time
    logger.info(f"Response Status: {response.status_code} in {response_time:.4f}s")

    return response
