# backend/myproject/contact/admin.py
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
        databases = [db for db in connections.databases.keys() if db != 'default']
        if not databases:
            databases = ['default']

        db_users = {}
        for db in databases:
            try:
                with connections[db].cursor() as cursor:
                    cursor.execute("SELECT username, email FROM auth_user")
                    users = cursor.fetchall()
                    db_users[db] = users
            except Exception as e:
                db_users[db] = f"Error: {str(e)}"

        html = "<h1>Versioned Databases</h1><table border='1'><tr><th>Database</th><th>Users</th></tr>"
        for db, users in db_users.items():
            if isinstance(users, list):
                user_list = ", ".join([f"{user[0]} ({user[1]})" for user in users])
            else:
                user_list = users
            html += f"<tr><td>{db}</td><td>{user_list}</td></tr>"
        html += "</table>"
        return HttpResponse(html)

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(User)

@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'get_phone_number', 'message', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')

    def get_phone_number(self, obj):
        return getattr(obj, 'phone_number', 'N/A')
    get_phone_number.short_description = 'Phone Number'

    def get_queryset(self, request):
        return super().get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        all_messages = []
        databases = [db for db in connections.databases.keys() if db != 'default']
        for db in databases:
            try:
                messages = ContactMessage.objects.using(db).all()
                for msg in messages:
                    all_messages.append((db, msg))
            except Exception as e:
                print(f"Error fetching messages from {db}: {str(e)}")

        extra_context = extra_context or {}
        extra_context['all_messages'] = all_messages
        return super().changelist_view(request, extra_context=extra_context)

