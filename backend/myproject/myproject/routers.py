# backend/myproject/myproject/routers.py
import os

class DynamicVersionDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'contact':
            version = os.getenv('VERSION', 'v1').lower()
            return f'mydb_{version}'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'contact':
            version = os.getenv('VERSION', 'v1').lower()
            return f'mydb_{version}'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        version = os.getenv('VERSION', 'v1').lower()
        current_db = f'mydb_{version}'  # Fixed typo
        if app_label == 'contact':
            return db == current_db
        return db == 'default'