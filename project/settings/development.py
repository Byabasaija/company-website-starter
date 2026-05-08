import environ
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env.local')

DEBUG = True
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-only-key')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS += ['django_browser_reload']
MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS', default='')

INTERNAL_IPS = ['127.0.0.1']
