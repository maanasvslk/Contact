from django.urls import path, include, re_path
from contact.admin import admin_site
from contact.views import version_redirect_view

urlpatterns = [
    path('admin/', admin_site.urls),

    # Redirects only at these entry points
    path('', version_redirect_view),
    path('v2/', version_redirect_view),

    path('api/', include('contact.urls')),
    path('api/v2/', include('contact_v2.urls')),
    path('v2/', include('contact_v2.urls')),  # actual content routes
]
