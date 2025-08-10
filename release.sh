#!/usr/bin/env bash
# release.sh

set -e

echo "=== Railway Release Script ==="
echo "Environment: ${RAILWAY_ENVIRONMENT:-development}"

# Check environment variables
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "WARNING: DATABASE_URL not set"
    echo "Available environment variables:"
    env | grep -E "(DB_|DATABASE_|POSTGRES_)" || echo "No database-related env vars found"
else
    echo "DATABASE_URL is set (${DATABASE_URL:0:50}...)"
fi

echo "Starting release process..."

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if environment variables are set..."
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser with provided credentials..."
    python manage.py create_admin || echo "Failed to create superuser, continuing..."
else
    echo "Superuser environment variables not set, skipping..."
    echo "To create a superuser, set these environment variables:"
    echo "  - DJANGO_SUPERUSER_USERNAME"
    echo "  - DJANGO_SUPERUSER_EMAIL" 
    echo "  - DJANGO_SUPERUSER_PASSWORD"
fi

echo "Release process completed successfully!"
