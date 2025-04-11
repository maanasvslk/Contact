#!/bin/sh
set -e

cd /app/myproject

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Reset migrations if tables don't exist
if ! python manage.py migrate --check; then
  echo "Resetting migrations..."
  python manage.py migrate --fake contact zero
  python manage.py migrate --fake contact_v2 zero
  python manage.py migrate --fake zero

  # Clear migration records
  echo "DELETE FROM django_migrations WHERE app IN ('contact', 'contact_v2');" | python manage.py dbshell

  # Create fresh migrations
  rm -f contact/migrations/0*.py
  rm -f contact_v2/migrations/0*.py
  python manage.py makemigrations contact
  python manage.py makemigrations contact_v2

  # Force table creation
  python manage.py migrate --run-syncdb
  python manage.py migrate contact --database=contact_1 --fake
  python manage.py migrate contact_v2 --database=contact_v2 --fake
fi

# Normal startup
python manage.py migrate
python manage.py migrate contact --database=contact_1
python manage.py migrate contact_v2 --database=contact_v2
DJANGO_SETTINGS_MODULE=myproject.settings python /app/create_superuser.py
exec python manage.py runserver 0.0.0.0:8000