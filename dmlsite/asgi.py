import os
import django
from channels.routing import get_default_application
from channels.asgi import get_channel_layer

os.environ.setdefault(“DJANGO_SETTINGS_MODULE”, “dmlsite.settings”)


application = get_default_application()
channel_layer = get_channel_layer()