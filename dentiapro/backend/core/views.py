from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to ensure the application is running.
    Useful for monitoring tools like Prometheus or AWS Health Checks.
    """
    return JsonResponse({'status': 'ok', 'environment': settings.ENVIRONMENT}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def version_info(request):
    """
    Returns version information about the application.
    This helps clients understand which version of the backend they are interacting with.
    """
    version_data = {
        'app_name': 'Dentiapro',
        'version': '1.0.0',  # Update as per your release
        'description': 'Multi-tenant Dental Management Application'
    }
    return JsonResponse(version_data, status=200)
