from utils.versioning import get_current_version

class VersionDatabaseRouter:
    def db_for_read(self, model, **hints):
        return get_current_version()

    def db_for_write(self, model, **hints):
        return get_current_version()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == get_current_version()
