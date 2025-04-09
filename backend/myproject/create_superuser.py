from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import IntegrityError

def create_superuser():
    try:
        # Check if the superuser already exists
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="vslk.maanas@example.com",
                password="maanas6114"
            )
            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")
    except IntegrityError:
        print("Superuser creation failed due to integrity error.")

if __name__ == "__main__":
    create_superuser()
