#!/bin/bash
set -e

cd /app/myproject

# Wait for PostgreSQL with timeout
timeout 60 bash -c "until PGPASSWORD=$DB_PASSWORD psql -h '$DB_HOST' -U '$DB_USER' -d '$DB_NAME' -c '\q'; do
  echo 'Waiting for PostgreSQL...'
  sleep 2
done" || {
  echo "PostgreSQL not available after 60 seconds"
  exit 1
}

# Set Python path explicitly
export PYTHONPATH=/app:/app/myproject

# Reset migrations if needed
if ! python manage.py migrate --check; then
  echo "Resetting migrations..."
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find . -path "*/migrations/*.pyc" -delete
fi

# Generate and run migrations for all databases
echo "Creating migrations..."
python manage.py makemigrations
python manage.py makemigrations contact
python manage.py makemigrations contact_v2

echo "Applying migrations..."
python manage.py migrate
python manage.py migrate contact --database=contact_1
python manage.py migrate contact_v2 --database=contact_v2

# Create superuser
DJANGO_SETTINGS_MODULE=myproject.settings python /app/create_superuser.py

# Start server
exec python manage.py runserver 0.0.0.0:8000