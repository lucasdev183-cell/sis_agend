"""
Development settings for jt_sistemas project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database - Can use SQLite for development if needed
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Development-specific middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Session settings for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email backend for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache configuration for development (use dummy cache)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Static files configuration for development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Logging configuration for development
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['root']['level'] = 'DEBUG'

# Django Debug Toolbar (optional - uncomment if you want to use it)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1', 'localhost']

print(f"🚀 JT Sistemas running in DEVELOPMENT mode")
print(f"📊 Database: PostgreSQL at {DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"🔧 Debug mode: {DEBUG}")