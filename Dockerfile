FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' docker_start_with_migrations.sh

CMD ["/app/docker_start_with_migrations.sh"]