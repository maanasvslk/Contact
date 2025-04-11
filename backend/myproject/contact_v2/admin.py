from django.contrib import admin
from contact.admin import admin_site  # Import the existing admin_site
from .models import ContactMessageV2

@admin.register(ContactMessageV2, site=admin_site)
class ContactMessageV2Admin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address', 'message', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')
    # No custom get_queryset; rely on database router