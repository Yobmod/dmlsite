
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['dmlsite.herokuapp.com', "127.0.0.1"]
SITE_ID = 3
ROOT_URLCONF = 'dmlsite.urls'
WSGI_APPLICATION = 'dmlsite.wsgi.application'
DEBUG = False

if not DEBUG:   # redirects to https on heroku
    SECURE_SSL_REDIRECT = True  # [1]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CHANNEL_LAYERS = {
     'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get("REDIS_URL")],
        },
    },
}

try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    pass

# GEOIP_PATH=os.environ['GEOIP_GEOLITE2_PATH']

try:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = ""  # use in view if different from host
except KeyError:
    pass

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dmlsite',
        'USER': 'dmlsite',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        # 'CONN_MAX_AGE': 600,
    }
}

DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

Q_CLUSTER = {
    'name': 'dmlsite',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

try:
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_ACCESS_KEY_ID = os.environ['AWSAccessKeyId']
    AWS_SECRET_ACCESS_KEY = os.environ['AWSSecretKey']
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=864000',    # 86400 = 1 day
    }
except KeyError:
    pass

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'dmlsite.storages_custom.MediaStorage'


STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'dmlsite.storages_custom.CachedS3BotoStorage'

COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE
