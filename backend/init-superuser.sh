#!/bin/bash
set -e

# No need to wait for PostgreSQL anymore
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

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