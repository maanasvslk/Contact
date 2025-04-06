from django.contrib import admin
from .models import ContactMessage
from django.db import connections


class MultiDBAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Default queryset from the current versioned database
        return super().get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        # Fetch data from all databases
        all_messages = []
        for db_name in connections.databases.keys():
            if db_name != 'default':  # Skip the default database if not versioned
                with connections[db_name].cursor():
                    qs = ContactMessage.objects.using(db_name).all()
                    all_messages.extend([(db_name, msg) for msg in qs])

        extra_context = extra_context or {}
        extra_context['all_messages'] = all_messages
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(ContactMessage, MultiDBAdmin)