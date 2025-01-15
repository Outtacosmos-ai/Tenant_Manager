from .base import *

# Disable debug mode for production
DEBUG = False

# Allowed hosts for production
ALLOWED_HOSTS = ['dentiapro.com', 'www.dentiapro.com']

# HTTPS settings to enforce secure connections
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS) settings
SECURE_HSTS_SECONDS = 31536000  # Enforce HTTPS for 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Additional security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Logging settings for error tracking
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/errors.log',  # Use a directory accessible to the server
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# CORS settings for production (restrict to trusted origins)
CORS_ALLOWED_ORIGINS = [
    'https://dentiapro.com',
    'https://www.dentiapro.com',
]

# Default database settings (example for PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('DB_NAME', 'dentiapro_prod'),
        'USER': os.getenv('DB_USER', 'dentiapro_prod_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secure_password'),
        'HOST': os.getenv('DB_HOST', 'db_host'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Static and media files
STATIC_ROOT = '/path/to/staticfiles/'  # Update to the correct static root directory
MEDIA_ROOT = '/path/to/media/'  # Update to the correct media root directory

# Email settings for error notifications (example using SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mailtrap.io')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your_email_user')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your_email_password')
DEFAULT_FROM_EMAIL = 'noreply@dentiapro.com'
SERVER_EMAIL = 'errors@dentiapro.com'

# Swagger and API security settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}
