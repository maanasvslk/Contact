from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import ContactMessageV2  # Corrected from ContactMessage
from .serializers import ContactMessageV2Serializer  # Correct

def contact_v2_page(request):
    return render(request, 'index.html', {'is_contact_v2': True})

class ContactFormV2View(APIView):
    def post(self, request):
        serializer = ContactMessageV2Serializer(data=request.data)  # Correct
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form submitted successfully"})
        return Response(serializer.errors, status=400)

class ContactMessageV2CreateView(generics.CreateAPIView):
    queryset = ContactMessageV2.objects.all()  # Corrected from ContactMessage
    serializer_class = ContactMessageV2Serializer  # Correct