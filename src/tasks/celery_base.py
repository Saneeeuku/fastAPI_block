from celery import Celery

from src.config import settings


celery_app = Celery(
    main="tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks"
    ]
)

celery_app.conf.beat_schedule = {
    "beats": {
        "task": "today_checkins_bookings",
        "schedule": 5,
    }
}
