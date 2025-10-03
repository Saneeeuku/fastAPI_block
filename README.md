Install requirements
```bash
pip install -r requirements.txt
```

Apply migrations if needed
```bash
alembic upgrade head
```
Run Dev
```bash
fastapi dev src/main.py
```

Celery start worker (on windows with pool=solo)
```bash
celery --app=src.tasks.celery_base:celery_app worker -l info --pool=solo
```
