from django.urls import path, include
from contact.admin import admin_site  # Import the custom admin site

urlpatterns = [
    path('admin/', admin_site.urls),  # Use the custom admin site
    path('', include('contact.urls')),
    path('api/', include('contact.urls'))
]