web: python manage.py migrate && gunicorn nexus.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A nexus worker --loglevel=info
beat: celery -A nexus beat --loglevel=info
