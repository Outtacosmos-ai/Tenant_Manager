from rest_framework.response import Response
from rest_framework import status

class CustomResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        response_data = {
            'status': 'success',
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message=None, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {
            'status': 'error',
            'message': message,
            'errors': errors
        }
        return Response(response_data, status=status_code)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
