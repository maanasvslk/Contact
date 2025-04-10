from django.contrib import admin
from django.contrib.auth import get_user_model
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
        # Simplified to show users for both databases
        users = User.objects.values_list('username', 'email')
        user_list = ", ".join([f"{user[0]} ({user[1]})" for user in users])
        html = "<h1>Database Users</h1><table border='1'><tr><th>Database</th><th>Users</th></tr>"
        html += f"<tr><td>default</td><td>{user_list}</td></tr>"
        html += "</table>"
        return HttpResponse(html)

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(User)

@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at', 'version')  # No phone and address in default
    list_filter = ('submitted_at', 'version')
    search_fields = ('name', 'email', 'message', 'phone_number', 'address')

    def get_queryset(self, request):
        # Fetch messages from both databases
        default_messages = ContactMessage.objects.using('default').all()
        v2_messages = ContactMessage.objects.using('v2').all()

        all_messages = {
            'default': default_messages,
            'v2': v2_messages
        }

        return all_messages

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        all_messages = self.get_queryset(request)

        # Pass the grouped messages (by db_name) to the template
        extra_context['all_messages'] = all_messages

        return super().changelist_view(request, extra_context=extra_context)
