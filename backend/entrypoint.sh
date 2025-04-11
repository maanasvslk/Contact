#!/bin/bash
set -e

cd /app/myproject

# Wait for PostgreSQL with password
timeout 60 bash -c "until PGPASSWORD=$DB_PASSWORD psql -h '$DB_HOST' -U '$DB_USER' -d '$DB_NAME' -c '\q'; do
  echo 'Waiting for PostgreSQL...'
  sleep 2
done" || {
  echo "PostgreSQL not available after 60 seconds"
  exit 1
}

# Create schemas with password
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "CREATE SCHEMA IF NOT EXISTS contact_schema; CREATE SCHEMA IF NOT EXISTS v2_schema;"

# Normal migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
DJANGO_SETTINGS_MODULE=myproject.settings python /app/create_superuser.py

# Start server
exec python manage.py runserver 0.0.0.0:8000