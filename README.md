Install requirements
```bash
pip install -r requirements.txt
```
Apply migrations
```bash
alembic upgrade head
```
Run with pure python
```bash
python -m src.main
```
Run Fastapi Dev (running with uvicorn from main with pycharm RUN is kinda lagging on reloads)
```bash
fastapi dev src/main.py
```
Celery start worker (on windows with pool=solo)
```bash
celery --app=src.tasks.celery_base:celery_app worker -l info --pool=solo
```
Celery beat start (on windows)
```bash
celery --app=src.tasks.celery_base:celery_app beat -l info
```
Create src/static/images folder