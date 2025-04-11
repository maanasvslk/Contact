#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput
python manage.py migrate contact --database=contact_1 --noinput
python manage.py migrate contact_v2 --database=contact_v2 --noinput

echo "Creating superuser..."
python /app/create_superuser.py

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000