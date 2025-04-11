from django.urls import path, include
from contact.admin import admin_site
from contact.views import contact_page


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', contact_page, name='home'),

    # Only this view handles redirects based on APP_VERSION

    # These are actual views/logic
    path('api/', include('contact.urls')),
    path('api/v2/', include('contact_v2.urls')),
    path('v2/', include('contact_v2.urls')),  # v2 content
]
