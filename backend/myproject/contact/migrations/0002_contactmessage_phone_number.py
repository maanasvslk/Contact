# backend/myproject/contact/migrations/0002_contactmessage_phone_number.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ContactMessage',
            name='phone_number',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
    ]