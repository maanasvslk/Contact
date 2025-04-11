from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer

from django.shortcuts import redirect
import os


def version_redirect_view(request):
    app_version = os.environ.get('APP_VERSION', '1')
    path = request.path

    # Redirect / to /v2/ only if not already at /v2/
    if app_version == '2' and path == '/':
        return redirect('/v2/')

    # Redirect /v2/ to / only if that's not the current version
    if app_version == '1' and path == '/v2/':
        return redirect('/')

    # Otherwise, no redirect (avoids loop)
    return None


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