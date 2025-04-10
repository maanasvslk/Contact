from django.db import models
from utils.versioning import get_current_version
# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # New in v2
    address = models.TextField(blank=True, null=True)  # New in v2
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add= True)
    version = models.CharField(max_length=10, default=get_current_version)

    def __str__(self):
        return f"{self.name} - {self.email}"
