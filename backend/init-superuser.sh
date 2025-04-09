#!/bin/bash
set -e

# Start server in background
python myproject/manage.py runserver 0.0.0.0:8000 &

# Wait for server to be ready
sleep 5

# Create superuser
python myproject/manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
EOF

# Keep container running
wait