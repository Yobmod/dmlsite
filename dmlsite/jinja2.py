from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment
from compressor.offline.jinja2 import url_for, SpacelessExtension
from compressor.contrib.jinja2ext import CompressorExtension
import jinja2.ext

def environment(**options):

    extensions = [
        CompressorExtension,
        SpacelessExtension,
     ]
    # env = Environment(extensions=extensions)
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env