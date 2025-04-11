from django.urls import path, include
from contact.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('contact.urls')),
    path('v2/', include('contact_v2.urls')),
    path('api/', include('contact.urls')),
    path('api/v2/', include('contact_v2.urls')),  # Corrected to match template
]