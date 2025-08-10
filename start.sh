#!/bin/bash

# Start script for Railway deployment
set -e

echo "Starting Nexus application with Celery..."

# Prepare static files and run migrations
mkdir -p staticfiles
python manage.py collectstatic --noinput
python manage.py migrate

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A nexus worker --loglevel=info --detach --pidfile=/tmp/celery_worker.pid

# Start Celery beat in background (optional, for scheduled tasks)
echo "Starting Celery beat..."
celery -A nexus beat --loglevel=info --detach --pidfile=/tmp/celery_beat.pid

# Start the web server
echo "Starting web server..."
exec gunicorn nexus.wsgi:application --bind 0.0.0.0:$PORT
