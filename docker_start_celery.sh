#!/bin/bash
echo "Running as user: $(whoami)"
echo "Python path: $(which python)"
echo "Celery path: $(which celery)"

celery --app=src.tasks.celery_base:celery_app worker --loglevel=INFO