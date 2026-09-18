#!/bin/bash
set -e

mkdir -p "${DJANGO_DB_DIR:-.}"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Ensuring instructor account exists..."
python manage.py create_instructor

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn on 0.0.0.0:8000..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 1
