import os
import django
from channels.routing import get_default_application
from channels.asgi import get_channel_layer
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault(“DJANGO_SETTINGS_MODULE”, “dmlsite.settings”)
django.setup()


channel_layer = get_channel_layer()

application = get_default_application()
application = DjangoWhiteNoise(application)