from django.shortcuts import render
from django.conf import settings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow superusers/staff to still access the backend to test fixes
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)
        
        # Allow requests to /admin/
        if request.path.startswith('/admin'):
            return self.get_response(request)

        # Check if maintenance mode is on
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return render(request, 'maintenance.html', status=503)

        return self.get_response(request)