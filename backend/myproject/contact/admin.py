from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import connections
from django.http import HttpResponse
from django.urls import path
from .models import ContactMessage

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
        if not databases:  # If no additional databases, use 'default'
            databases = ['default']

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

# Create an instance of CustomAdminSite
admin_site = CustomAdminSite(name='custom_admin')

# Register the User model
admin_site.register(User)

# Register the ContactMessage model
@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'submitted_at', 'database')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message', 'phone')

    def get_queryset(self, request):
        # Get all messages from all databases
        messages = []
        for db_name in ['v1', 'v2']:
            try:
                with connections[db_name].cursor() as cursor:
                    cursor.execute("""
                        SELECT id, name, email, phone, message, submitted_at 
                        FROM contact_contactmessage
                    """)
                    for row in cursor.fetchall():
                        msg = ContactMessage(
                            id=row[0],
                            name=row[1],
                            email=row[2],
                            phone=row[3],
                            message=row[4],
                            submitted_at=row[5]
                        )
                        msg.database = db_name
                        messages.append(msg)
            except Exception as e:
                print(f"Error querying {db_name}: {str(e)}")
        return messages

    def database(self, obj):
        return obj.database
    database.short_description = 'Database'