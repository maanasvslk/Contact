#!/bin/sh
set -e  # Exit on any error
echo "Waiting for Django to initialize..."
sleep 5  # Give time for initialization
echo "Running migrations for contact..."
python /app/myproject/manage.py migrate contact --database=contact_1
echo "Running migrations for contact_v2..."
python /app/myproject/manage.py migrate contact_v2 --database=contact_v2
echo "Starting Django server..."
exec python /app/myproject/manage.py runserver 0.0.0.0:8000