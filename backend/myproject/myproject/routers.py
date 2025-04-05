# myproject/routers.py
import os

class DynamicVersionDatabaseRouter:
    def db_for_read(self, model, **hints):
        # Get the version from environment variable (Git commit hash or Jenkins build number)
        version = os.getenv('VERSION', 'v1')  # Default to 'v1' if VERSION isn't set
        db_name = f"mydb_{version}"  # Database name dynamically based on version
        return db_name

    def db_for_write(self, model, **hints):
        # Get the version from environment variable (Git commit hash or Jenkins build number)
        version = os.getenv('VERSION', 'v1')  # Default to 'v1' if VERSION isn't set
        db_name = f"mydb_{version}"  # Database name dynamically based on version
        return db_name

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Ensure migrations are applied to the correct versioned database
        version = os.getenv('VERSION', 'v1')  # Default to 'v1' if VERSION isn't set
        db_name = f"mydb_{version}"  # Database name dynamically based on version
        if db == db_name and app_label == 'contact':  # Ensure app label matches
            return True
        return False
