import os

class DynamicVersionDatabaseRouter:
    def db_for_read(self, model, **hints):
        version = os.getenv('VERSION', 'v1')
        return f'mydb_{version}'

    def db_for_write(self, model, **hints):
        version = os.getenv('VERSION', 'v1')
        return f'mydb_{version}'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        version = os.getenv('VERSION', 'v1')
        return db == f'mydb_{version}'