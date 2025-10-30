from fastapi import APIRouter, UploadFile

from src.services.images_service import ImagesService

router = r = APIRouter(prefix="/images", tags=["Изображения"])


@r.post("", summary="Загрузить изображение")
def upload_image(image: UploadFile):
    ImagesService().upload_image(image)
