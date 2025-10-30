import shutil

from fastapi import UploadFile

from src.services.base_service import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    def upload_image(self, image: UploadFile):
        image_path = f"src/static/images/{image.filename}"
        with open(image_path, mode="wb+") as f:
            shutil.copyfileobj(image.file, f)
        resize_image.delay(image_path)
