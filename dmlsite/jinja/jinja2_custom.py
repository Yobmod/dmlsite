from jinja2 import Environment, ext  # , FileSystemLoader

from django_jinja.builtins import extensions as djjn_extensions
from django_jinja.loaders import FileSystemLoader as djjn_FileStstemLoader

from compressor.contrib.jinja2ext import CompressorExtension
# from pipeline.jinja2 import PipelineExtension
# from compressor.offline.jinja2 import url_for, SpacelessExtension
# from typing import Any


loaders = [
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',
    'jina2.FileSystemLoader'
]

extensions = [
    CompressorExtension, 
    ext.do, 
    ext.loopcontrols, 
    ext.with_, 
    ext.i18n, 
    ext.autoescape,
    djjn_extensions.CsrfExtensionCacheExtension, 
    djjn_extensions.TimezoneExtension, 
    djjn_extensions.UrlsExtension, 
    djjn_extensions.StaticFilesExtension, 
    djjn_extensions.DjangoFiltersExtension,
    # PipelineExtension,
]


def dmlsite_jinja_env(**options: dict) -> Environment:
    env = Environment(loader=djjn_FileStstemLoader('templates/'), extensions=extensions)
    return env


"""from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment
from compressor.offline.jinja2 import url_for, SpacelessExtension
from compressor.contrib.jinja2ext import CompressorExtension
import jinja2.ext
from typing import Any

def environment(**options: Any) -> Environment:

    extensions = [
        CompressorExtension,
        SpacelessExtension,
     ]

    # env = Environment(extensions=extensions)
    env = Environment(extensions=extensions)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env"""
