"""
WSGI config for dmlsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


try:
	dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
except KeyError:
	pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmlsite.settings")

application = get_wsgi_application()


application = DjangoWhiteNoise(application)
