from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import path
from .models import ContactMessageDefault, ContactMessageV2

User = get_user_model()

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('databases/', self.admin_view(self.databases_view), name='databases'),
        ]
        return urls + custom_urls

    def databases_view(self, request):
        # Simplified to show users for both databases
        users = User.objects.values_list('username', 'email')
        user_list = ", ".join([f"{user[0]} ({user[1]})" for user in users])
        html = "<h1>Database Users</h1><table border='1'><tr><th>Database</th><th>Users</th></tr>"
        html += f"<tr><td>default</td><td>{user_list}</td></tr>"
        html += "</table>"
        return HttpResponse(html)

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(User)

@admin.register(ContactMessageDefault)
class ContactMessageDefaultAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at', 'version')
    list_filter = ('submitted_at', 'version')
    search_fields = ('name', 'email', 'message')

@admin.register(ContactMessageV2)
class ContactMessageV2Admin(admin.ModelAdmin):
    list_display = ('name', 'email','phone_number', 'address', 'message', 'submitted_at', 'version')
    list_filter = ('submitted_at', 'version')
    search_fields = ('name', 'email', 'message', 'phone_number', 'address')