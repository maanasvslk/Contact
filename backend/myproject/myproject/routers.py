class contact_1:
    route_app_labels = {'contact'}  # Match your app name

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'contact_1'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'contact_1'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'contact_1'
        return None



class contact_v2:  # New router
    route_app_labels = {'contact_v2'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'contact_v2'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'contact_v2'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'contact_v2'
        return None