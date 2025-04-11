from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer

import os
from django.shortcuts import redirect, render

def version_redirect_view(request):
    app_version = os.environ.get('APP_VERSION', '1')  # Default to 1
    if app_version == '2':
        return redirect('/v2/')
    return render(request, 'index.html', {'is_contact_v2': False})  # directly serve V1



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