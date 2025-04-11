class ContactRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'contact':
            return 'contact_1'
        if model._meta.app_label == 'contact_v2':
            return 'contact_v2'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'contact':
            return 'contact_1'
        if model._meta.app_label == 'contact_v2':
            return 'contact_v2'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'contact':
            return db == 'contact_1'
        if app_label == 'contact_v2':
            return db == 'contact_v2'
        return None