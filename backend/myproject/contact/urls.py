from django.urls import path
from .views import ContactFormView, ContactMessageCreateView

urlpatterns = [
    path('api/contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    path('contact/', ContactFormView.as_view(), name='contact_form'),
]