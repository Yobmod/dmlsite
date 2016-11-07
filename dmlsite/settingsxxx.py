
import os
import dj_database_url

DEBUG = False

from .general_settings import *

try:
	from .production_settings import *
except ImportError:
	pass

try:
	from .local_settings import *
except ImportError:
	pass
