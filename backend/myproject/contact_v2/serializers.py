from rest_framework import serializers
from .models import ContactMessageV2  # Correct

class ContactMessageV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessageV2  # Correct
        fields = '__all__'