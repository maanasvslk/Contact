from django.db import models

class ContactMessageV2(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'v2_schema"."contactmessagev2'  # Schema-qualified table name
        verbose_name = 'Contact Message V2'
        verbose_name_plural = 'Contact Messages V2'

    def __str__(self):
        return f"{self.name} - {self.email}"