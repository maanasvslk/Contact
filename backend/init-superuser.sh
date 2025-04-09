#!/bin/bash

# Run migrations
python manage.py migrate

# Create a superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'vslk.maanas@gmail.com', 'maanas6114')" | python manage.py shell

# Exit successfully
exit 0