from django.urls import path
from .views import ContactFormView, ContactMessageCreateView, contact_page

urlpatterns = [
    path('', contact_page, name='home'),  # <- this will show the HTML page
    path('api/contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    path('contact/', ContactFormView.as_view(), name='contact_form'),
]
