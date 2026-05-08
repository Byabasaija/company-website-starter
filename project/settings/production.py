import environ
import dj_database_url
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS').replace(' ', '').split(',')
_cors_raw = env('ALLOWED_CORS', default='').replace(' ', '')
CORS_ALLOWED_ORIGINS = [o for o in _cors_raw.split(',') if o]
CSRF_TRUSTED_ORIGINS = [o for o in _cors_raw.split(',') if o]

DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL'))}

GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS', default='')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=465)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Storage
STORAGE_BACKEND = env('STORAGE_BACKEND', default='local')

if STORAGE_BACKEND == 's3':
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
    AWS_STORAGE_BUCKET_NAME = env('AWS_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_REGION', default='us-east-1')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
elif STORAGE_BACKEND == 'gcs':
    from google.oauth2 import service_account
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
    GS_BUCKET_NAME = env('GCS_BUCKET_NAME')
    GS_PROJECT_ID = env('GCS_PROJECT_ID')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        BASE_DIR / env('GCS_CRED_PATH')
    )
# else: Django default FileSystemStorage — works on cPanel
