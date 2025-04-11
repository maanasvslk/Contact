from django.urls import path
from .views import ContactFormV2View, ContactMessageV2CreateView, contact_v2_page

urlpatterns = [
    path('', contact_v2_page, name='contact_v2_home'),
    path('contact_v2/', ContactMessageV2CreateView.as_view(), name='contact_v2_create'),  # Changed from api/contact_v2/
    path('form/', ContactFormV2View.as_view(), name='contact_v2_form'),  # Changed from contact_v2/
]