
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['*']
DEBUG = False

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





