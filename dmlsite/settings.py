# import os
# import dj_database_url
import dotenv

try:
    dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from .general_settings import *
DEBUG = False

try:
    ##from .production_settings import *
except ImportError:
   # pass


try:
    from .local_settings import *
except ImportError:
    pass
