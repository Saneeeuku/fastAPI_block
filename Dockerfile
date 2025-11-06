FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONPATH="/app:${PYTHONPATH}"

RUN mkdir -p src/static/images

RUN adduser --disabled-password --gecos '' --uid 1000 baseuser
RUN chown -R baseuser:baseuser /app
USER baseuser