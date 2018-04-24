# import os
# import dj_database_url
from .general_settings import *
DEBUG = False

try:
    from .production_settings import *
except ImportError:
    pass

try:
    from .local_settings import *
except ImportError:
    pass
