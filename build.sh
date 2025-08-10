#!/bin/bash
set -e

echo "Building Nexus application..."

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
