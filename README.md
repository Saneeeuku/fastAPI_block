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
```bash
mkdir src/static/images
```
Docker commands
```bash
docker run --name booking_db -p 6432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=booking \
  --network=my_network \
  --volume pg_booking_data:/var/lib/postgresql \
  -d postgres:18.0
```
```bash
docker run --name booking_nginx --network=my_network --volume ./nginx.conf:/etc/nginx/nginx.conf --rm -p 80:80 nginx
```
# --volume //c/Users/shark/PycharmProjects/FastAPI_booking_gitlab/nginx.conf:/etc/nginx/nginx.conf - for windows need to conf full path