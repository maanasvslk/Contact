from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f"{self.name} - {self.email}"
