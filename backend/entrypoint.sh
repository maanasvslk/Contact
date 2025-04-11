#!/bin/sh
set -e

cd /app/myproject

# Wait for PostgreSQL to be ready using psql
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Reset migrations if needed
if ! python manage.py migrate --check; then
  echo "Resetting migrations and creating tables..."

  # Clear existing migrations
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find . -path "*/migrations/*.pyc" -delete

  # Create fresh migrations
  python manage.py makemigrations

  # Force table creation
  python manage.py migrate --run-syncdb

  # Apply migrations properly
  python manage.py migrate
  python manage.py migrate contact --database=contact_1
  python manage.py migrate contact_v2 --database=contact_v2
fi

# Normal startup
python manage.py migrate
python manage.py migrate contact --database=contact_1
python manage.py migrate contact_v2 --database=contact_v2
DJANGO_SETTINGS_MODULE=myproject.settings python /app/create_superuser.py
exec python manage.py runserver 0.0.0.0:8000