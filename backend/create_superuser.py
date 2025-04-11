import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="vslk.maanas@example.com",
            password="maanas6114"
        )
        print("Superuser created successfully.")

if __name__ == "__main__":
    create_superuser()