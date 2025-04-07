#!/bin/bash
set -e
echo "Checking for psycopg2..."
python -c "import psycopg2" || { echo "psycopg2 not installed!"; exit 1; }
echo "psycopg2 is installed."

until python -c "import psycopg2; psycopg2.connect(dbname='mydb_v1', user='postgres', password='maanas6114', host='db', port='5432')" 2>/dev/null; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done
echo "PostgreSQL is ready!"

python /app/myproject/manage.py runserver 0.0.0.0:8000 || { echo "Django server failed to start!"; sleep infinity; }