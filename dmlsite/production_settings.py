
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['*']
DEBUG = False
SECRET_KEY = 'u8&hn$a@%16^xvg+t5#abg(p6+&+y&qms6!@$cf*$-q3!^lge+'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yobmod@gmail.com'
EMAIL_HOST_PASSWORD = '3Monsters'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


ROOT_URLCONF = 'dmlsite.urls'
WSGI_APPLICATION = 'dmlsite.wsgi.application'

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
		'CONN_MAX_AGE': 600,
	}
}

DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

 AWS_STORAGE_BUCKET_NAME = 'dmlsite'
 AWS_ACCESS_KEY_ID = 'AKIAIC3XZR7SNQEGZONQ'
 AWS_SECRET_ACCESS_KEY = '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'
 AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
 STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
 STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
 DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
 AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

 AWS_S3_OBJECT_PARAMETERS = {
 	 'CacheControl': 'max-age=864000',    #86400 = 1 day
 	 }
