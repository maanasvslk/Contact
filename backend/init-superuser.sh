#!/bin/bash

echo "Creating superuser..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" 2>/dev/null; then
    echo "Superuser 'admin' created successfully."
else
    echo "Superuser 'admin' already exists."
fi
echo "Superuser creation completed."