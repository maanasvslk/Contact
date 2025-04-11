import os
import django
import sys

# Add /app to Python path (just in case)
sys.path.append('/app')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model

try:
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'vslk.maanas@example.com', 'maanas6114')
        print("Superuser created successfully")
    else:
        print("Superuser already exists")
except Exception as e:
    print(f"Error creating superuser: {e}")
    sys.exit(1)