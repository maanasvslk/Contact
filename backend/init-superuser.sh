#!/bin/bash

# Skip migrations since they were run during the build
echo "Skipping migrations (already run during build)..."

# Create superuser using a more reliable method
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print("Superuser 'admin' created successfully.")
else:
    print("Superuser 'admin' already exists.")
EOF

# Check if the superuser creation was successful
if [ $? -eq 0 ]; then
    echo "Superuser creation completed."
else
    echo "Failed to create superuser."
    exit 1
fi

exit 0