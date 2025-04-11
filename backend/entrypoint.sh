# entrypoint.sh

#!/bin/sh
set -e

# Set Python path to include /app
export PYTHONPATH=/app/myproject

# Change to Django project directory
cd /app/myproject

echo "Running migrations..."
python manage.py migrate --noinput
python manage.py migrate contact --database=contact_1 --noinput
python manage.py migrate contact_v2 --database=contact_v2 --noinput

echo "Creating superuser..."
# Run from project directory with proper environment
DJANGO_SETTINGS_MODULE=myproject.settings python /app/create_superuser.py

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
