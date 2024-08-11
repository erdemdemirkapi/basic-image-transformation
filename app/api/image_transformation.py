from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageOps
from io import BytesIO
import base64

router = APIRouter()


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
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid image")

    if request.transformation_type == "grayscale":
        image = ImageOps.grayscale(image)
    elif request.transformation_type == "rotate":
        angle = request.angle
        if not angle:
            raise HTTPException(status_code=422, detail="Missing parameter: angle")
        image = image.rotate(angle)
    elif request.transformation_type == "resize":
        width = request.width
        height = request.height
        if not (width or height):
            raise HTTPException(status_code=422, detail="Missing parameter: width or height")
        image = image.resize((width, height))
    else:
        raise HTTPException(status_code=422, detail="Invalid transformation type")

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"transformed_image": img_str}
