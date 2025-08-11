#!/bin/bash

# Start script for Railway deployment
set -e

echo "Starting Nexus application..."

# Prepare static files and run migrations
mkdir -p staticfiles
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()

# Check if superuser exists
if not User.objects.filter(is_superuser=True).exists():
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'hello@kingsleyusa.dev')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    try:
        User.objects.create_superuser(username, email, password)
        print(f'✅ Superuser \"{username}\" created successfully!')
    except Exception as e:
        print(f'❌ Failed to create superuser: {e}')
else:
    print('✅ Superuser already exists')
"

# Populate database with TMDb movies (fetch if database has fewer than 500 movies)
echo "Checking if database needs movie data..."
python manage.py shell -c "
from movies.models import Movie

movie_count = Movie.objects.count()
if movie_count < 500:
    print(f'Database has {movie_count} movies (less than 500), fetching more from TMDb...')
    print(f'Current Movie count: {movie_count}')
    # This will be handled by the management command
    exit(0)
else:
    print(f'Database already has {movie_count} movies (500+), skipping fetch')
    exit(1)
" && {
    echo "Fetching movies from TMDb (popular, top-rated, upcoming, now-playing, trending)..."
    python manage.py fetch_tmdb_movies --pages=20 || echo "Failed to fetch movies, continuing anyway..."
    echo "Database population completed!"
} || echo "Skipping movie fetch - database has sufficient movies"

# Start single Celery worker with limited resources (Railway free tier)
echo "Starting Celery worker with limited resources..."
celery -A nexus worker --loglevel=info --concurrency=1 --max-memory-per-child=100000 --detach --pidfile=/tmp/celery_worker.pid

# Start the web server with fewer workers for memory efficiency
echo "Starting web server..."
exec gunicorn nexus.wsgi:application --bind 0.0.0.0:$PORT --workers=1 --max-requests=1000 --timeout=30
