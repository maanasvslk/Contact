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
    list_display = ('name', 'email', 'message', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')

    def get_queryset(self, request):
        # Fetch messages from all databases
        all_messages = []
        databases = [db for db in connections.databases.keys()]
        for db in databases:
            with connections[db].cursor() as cursor:
                try:
                    cursor.execute("SELECT id, name, email, message, submitted_at FROM contact_contactmessage")
                    messages = cursor.fetchall()
                    for msg in messages:
                        all_messages.append((db, ContactMessage(id=msg[0], name=msg[1], email=msg[2], message=msg[3], submitted_at=msg[4])))
                except Exception as e:
                    print(f"Error fetching messages from {db}: {str(e)}")
        return ContactMessage.objects.all()

    def changelist_view(self, request, extra_context=None):
        # Provide all_messages for the template
        all_messages = []
        databases = [db for db in connections.databases.keys()]
        for db in databases:
            with connections[db].cursor() as cursor:
                try:
                    cursor.execute("SELECT id, name, email, message, submitted_at FROM contact_contactmessage")
                    messages = cursor.fetchall()
                    for msg in messages:
                        all_messages.append((db, ContactMessage(id=msg[0], name=msg[1], email=msg[2], message=msg[3], submitted_at=msg[4])))
                except Exception as e:
                    print(f"Error fetching messages from {db}: {str(e)}")
        extra_context = extra_context or {}
        extra_context['all_messages'] = all_messages
        return super().changelist_view(request, extra_context=extra_context)