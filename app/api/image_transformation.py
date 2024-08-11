import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageOps
from io import BytesIO
import base64

router = APIRouter()
logger = logging.getLogger(__name__)


class ImageTransformationRequest(BaseModel):
    image: str
    transformation_type: str
    angle: int = None
    width: int = None
    height: int = None


@router.post("/transform-image/")
async def transform_image(request: ImageTransformationRequest):
    try:
        image_data = base64.b64decode(request.image)
        image = Image.open(BytesIO(image_data))
        logger.info(f"Image decoded successfully for transformation type: {request.transformation_type}")
    except Exception as e:
        logger.error(f"Failed to decode image: {str(e)}")
        raise HTTPException(status_code=422, detail="Invalid image")

    if request.transformation_type == "grayscale":
        image = ImageOps.grayscale(image)
        logger.info("Transformation: grayscale applied.")
    elif request.transformation_type == "rotate":
        angle = request.angle
        if not angle:
            raise HTTPException(status_code=422, detail="Missing parameter: angle")
        image = image.rotate(angle)
        logger.info("Transformation: rotate applied.")
    elif request.transformation_type == "resize":
        width = request.width
        height = request.height
        if not (width or height):
            raise HTTPException(status_code=422, detail="Missing parameter: width or height")
        image = image.resize((width, height))
        logger.info("Transformation: resize applied.")
    else:
        logger.warning(f"Invalid transformation type: {request.transformation_type}")
        raise HTTPException(status_code=422, detail="Invalid transformation type")

    try:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logger.info("Image transformation successful")
        return {"transformed_image": img_str}
    except Exception as e:
        logger.error(f"Failed to encode transformed image: {str(e)}")
        raise HTTPException(status_code=422, detail="Failed to encode transformed image")
