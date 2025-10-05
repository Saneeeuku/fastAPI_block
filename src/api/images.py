import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image


router = r = APIRouter(prefix="/images", tags=["Изображения"])


@r.post("", summary="Загрузить изображение")
def upload_image(image: UploadFile):
    image_path = f"src/static/images/{image.filename}"
    with open(image_path, mode="wb+") as f:
        shutil.copyfileobj(image.file, f)
    resize_image.delay(image_path)
