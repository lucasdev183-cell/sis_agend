"""
Production settings for jt_sistemas project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')], default=['*'])

# Security settings for production
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files configuration for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Logging configuration for production
LOGGING['handlers']['file']['level'] = 'WARNING'
LOGGING['root']['level'] = 'WARNING'

# Additional security headers
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# CORS settings for production (restrict to your domains)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS', 
    cast=lambda v: [s.strip() for s in v.split(',')],
    default=[]
)

print(f"🚀 JT Sistemas running in PRODUCTION mode")
print(f"📊 Database: PostgreSQL at {DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"🔒 Security: SSL Redirect enabled, HSTS configured")