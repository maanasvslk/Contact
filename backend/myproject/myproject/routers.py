import os

class DynamicVersionDatabaseRouter:
    def db_for_read(self, model, **hints):
        # Use the current version's database for ContactMessage
        if model._meta.app_label == 'contact':
            version = os.getenv('VERSION', 'v1')
            return f'mydb_{version}'
        return 'default'

    def db_for_write(self, model, **hints):
        # Use the current version's database for ContactMessage
        if model._meta.app_label == 'contact':
            version = os.getenv('VERSION', 'v1')
            return f'mydb_{version}'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migrations only on the current version's database
        version = os.getenv('VERSION', 'v1')
        current_db = f'mydb_{version}'
        if db == current_db:
            return True
        return False