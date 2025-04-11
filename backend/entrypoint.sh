#!/bin/sh
set -e

# Wait for Django to initialize
echo "Waiting for Django to initialize..."
sleep 5

# Set Python path
export PYTHONPATH=/app/myproject

# Run migrations
echo "Running migrations for default database..."
python /app/myproject/manage.py migrate --noinput

echo "Running migrations for contact..."
python /app/myproject/manage.py migrate contact --database=contact_1 --noinput

echo "Running migrations for contact_v2..."
python /app/myproject/manage.py migrate contact_v2 --database=contact_v2 --noinput

# Create superuser
echo "Creating superuser..."
python /app/create_superuser.py

# Start server
echo "Starting Django server..."
exec python /app/myproject/manage.py runserver 0.0.0.0:8000