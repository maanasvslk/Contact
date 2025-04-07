from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import connections
from django.http import HttpResponse
from django.urls import path

User = get_user_model()

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('databases/', self.admin_view(self.databases_view), name='databases'),
        ]
        return urls + custom_urls

    def databases_view(self, request):
        # Get all databases from settings
        databases = [db for db in connections.databases.keys() if db != 'default']

        # Collect user data from each database
        db_users = {}
        for db in databases:
            with connections[db].cursor() as cursor:
                try:
                    cursor.execute("SELECT username, email FROM auth_user")
                    users = cursor.fetchall()
                    db_users[db] = users
                except Exception as e:
                    db_users[db] = f"Error: {str(e)}"

        # Render the data in a simple HTML table
        html = "<h1>Versioned Databases</h1><table border='1'><tr><th>Database</th><th>Users</th></tr>"
        for db, users in db_users.items():
            if isinstance(users, list):
                user_list = ", ".join([f"{user[0]} ({user[1]})" for user in users])
            else:
                user_list = users
            html += f"<tr><td>{db}</td><td>{user_list}</td></tr>"
        html += "</table>"
        return HttpResponse(html)

# Replace the default admin site with the custom one
admin.site = CustomAdminSite(name='custom_admin')

# Register your models as usual
admin.site.register(User)