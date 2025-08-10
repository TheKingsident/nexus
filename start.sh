#!/bin/bash

# Start script for Railway deployment
set -e

echo "Starting Nexus application..."

# Prepare static files and run migrations
mkdir -p staticfiles
python manage.py collectstatic --noinput
python manage.py migrate

# Start single Celery worker with limited resources (Railway free tier)
echo "Starting Celery worker with limited resources..."
celery -A nexus worker --loglevel=info --concurrency=1 --max-memory-per-child=100000 --detach --pidfile=/tmp/celery_worker.pid

# Start the web server with fewer workers for memory efficiency
echo "Starting web server..."
exec gunicorn nexus.wsgi:application --bind 0.0.0.0:$PORT --workers=1 --max-requests=1000 --timeout=30
