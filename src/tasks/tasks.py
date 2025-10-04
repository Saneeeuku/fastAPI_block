import asyncio
import os

from PIL import Image

from src.database import async_new_session_null_pool
from src.tasks.celery_base import celery_app
from src.utils.db_manager import DBManager


@celery_app.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    img = Image.open(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)
        new_file_name = f"{name}_{size}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    print(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


async def get_today_checkins_bookings():
    print("Start async today checkins")
    async with DBManager(session_factory=async_new_session_null_pool) as db:
        today_bookings = await db.bookings.get_today_checkins()
    print(f"{today_bookings=}")


@celery_app.task(name="today_checkins_bookings")
def send_emails_to_users_with_today_checkins():
    asyncio.run(get_today_checkins_bookings())
