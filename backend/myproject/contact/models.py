# models.py

from django.db import models

# Base class for common fields
class BaseContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10)

    class Meta:
        abstract = True

# Model for the 'default' database (without phone_number and address)
class ContactMessageDefault(BaseContactMessage):
    class Meta:
        db_table = 'contact_message'
        app_label = 'your_app'
        verbose_name = 'Contact Message (default)'
        verbose_name_plural = 'Contact Messages (default)'

# Model for the 'v2' database (with phone_number and address)
class ContactMessageV2(BaseContactMessage):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'contact_message'
        app_label = 'your_app'
        verbose_name = 'Contact Message (v2)'
        verbose_name_plural = 'Contact Messages (v2)'
        using = 'v2'  # Specify the v2 database
