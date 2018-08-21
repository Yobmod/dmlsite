# import os
# import dj_database_url
import dotenv
from .general_settings import *
DEBUG = True

try:
    dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
except:
    pass


try:
    from .production_settings import *
except ImportError:
   pass


try:
    from .local_settings import *
except ImportError:
    pass
