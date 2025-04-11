from django.shortcuts import redirect
import os


class VersionRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        app_version = os.environ.get('APP_VERSION', '1')
        path = request.path

        if app_version == '2' and path == '/':
            return redirect('/v2/')
        elif app_version == '1' and path.startswith('/v2/'):
            return redirect('/')

        return self.get_response(request)
