from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer


def contact_page(request):
    return render(request, 'index.html', {'is_contact_v2': False})  # Explicitly set to False

class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form submitted successfully"})
        return Response(serializer.errors, status=400)

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer