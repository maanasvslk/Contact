#!/bin/bash
set -e

# Wait for the database to be ready
until python -c "import psycopg2; psycopg2.connect(dbname='mydb_${VERSION}', user='postgres', password='maanas6114', host='db', port='5432')" 2>/dev/null; do
  echo "Waiting for PostgreSQL to be ready for migrations..."
  sleep 2
done

# Apply migrations
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Create the superuser non-interactively
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'vslk.maanas@example.com', 'maanas6114')
    print("Superuser created successfully!")
else:
    print("Superuser already exists, skipping creation.")
EOF