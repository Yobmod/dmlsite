import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    # django essentials
    'channels',
    'rest_framework',
    'storages',
    'compressor',
    'django_user_agents',



    # my apps
    'dmlblog',
    'dmlpolls',
    'dmlmain',
    'dmlcomments',
    'dmlresearch',
    'dmlchat',
    'dmlgeo',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.facebook',
    # 'django_otp',
    # 'django_otp.plugins.otp_static',
    # 'django_otp.plugins.otp_totp',
    # 'two_factor',
    # 'user_sessions',

    # dev tools
    'django_extensions',  # werkzeug, pytest-django
    'sslserver',
    'controlcenter',


    # other tools
    'markdown_deux',
    'pagedown',
    'cookielaw',
    'taggit',
    'sorl.thumbnail',
    'embed_video',
    'registration',
    'chartjs',
    'sitetree',
    'crispy_forms',
    # 'hitcount',
    # 'jchart',
    # 'emoji',

    'django_q',
    # 'django_whoshere', #django-ipware

]

ACCOUNT_ACTIVATION_DAYS = 28  # activation window if using verifcation etc;
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in after registration.
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # "mandatory", "optional"
LOGIN_REDIRECT_URL = '/'
# SOCIALACCOUNT_QUERY_EMAIL=True   email from me or twitter?

SOCIALACCOUNT_PROVIDERS = {
    #'facebook': {}, 
    #'google':{}, 
    'github':{},
    'twitter':{},
}

CONTROLCENTER_DASHBOARDS = (
    'dmlsite.dashboard.MyDashboard',
)

TAGGIT_CASE_INSENSITIVE = True
CRISPY_TEMPLATE_PACK = 'bootstrap3'  # or bootstap, bootstrap4, uni-forms

MIDDLEWARE = [

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django_whoshere.middleware.TrackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',

]

ROOT_URLCONF = 'dmlsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, 'templates'),
                    os.path.join(BASE_DIR, 'templates', 'allauth', 'accounts'),
                    os.path.join(PROJECT_ROOT, 'dmlmain', 'templates', 'allauth', 'accounts')
                ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",

            ],
        },
    },
]

WSGI_APPLICATION = 'dmlsite.wsgi.application'

TEST_RUNNER = 'dmlsite.testrunners.PytestTestRunner'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dmlsite',
        'USER': 'dmlsite',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 600,
    }
}

Q_CLUSTER = {
    'name': 'dmlsite',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

ASGI_APPLICATION = 'dmlsite.routing.application'

DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = True

CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'django.core.cache.backends.memcached.MemcachedCache',
        # 'django.core.cache.backends.memcached.PyLibMCCache',
        # 'LOCATION': '/var/tmp/django_cache',
        'LOCATION': 'djangoq-localmem',
    }
}
# USER_AGENTS_CACHE = 'default' # or none to use djangocache

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'GB'
USE_I18N = True
USE_L10N = True
USE_TZ = True

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
LIBSASS_OUTPUT_STYLE = 'nested'  # 'compressed'
LIBSASS_PRECISION = 8

# GEOIP_PATH=os.environ['GEOIP_GEOLITE2_PATH'] #overwritten in prod
# GEOIP_CITY=os.environ['GEOIP_GEOLITE2_CITY_FILENAME']
# GEOIP_COUNTRY=os.environ['GEOIP_GEOLITE2_COUNTRY_FILENAME']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
COMPRESS_ROOT = STATIC_ROOT

# WHITENOISE_AUTOREFRESH # =DEBUG
WHITENOISE_ROOT = STATIC_ROOT


STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'), )

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter'  # default
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_OUTPUT_DIR = 'compressed'
COMPRESS_CSS_BACKEND = 'django_compressor.css.CssCompressor'
COMPRESS_JS_BACKEND = 'django_compressor.js.JsCompressor'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
