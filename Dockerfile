FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONPATH="/app:${PYTHONPATH}"

RUN sed -i 's/\r$//' docker_start_celery__non_root.sh
RUN sed -i 's/\r$//' docker_start_with_migrations.sh

RUN adduser --disabled-password --gecos '' --uid 1000 celeryuser
RUN chown -R celeryuser:celeryuser /app
USER celeryuser

