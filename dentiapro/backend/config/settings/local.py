from .base import *

# Enable debug mode for development
DEBUG = True

# Allowed hosts for local development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Local secret key for development only
SECRET_KEY = 'django-insecure-local-key-for-development'

# Local database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'dentiapro_local',
        'USER': 'dentiapro_user',
        'PASSWORD': 'dentiapro_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# CORS settings to allow all origins in development
CORS_ORIGIN_ALLOW_ALL = True

# Debug toolbar settings
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# IPs allowed for debug toolbar
INTERNAL_IPS = ['127.0.0.1']

# Swagger settings for development environment
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    },
    'DOC_EXPANSION': 'none',
}
