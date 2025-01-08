from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-local-key-for-development'

# Database
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

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True

# Debug toolbar settings
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']