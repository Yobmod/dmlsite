from jinja2 import Environment, FileSystemLoader
from jinja2.ext import do, loopcontrols, with_, i18n, autoescape

from compressor.contrib.jinja2ext import CompressorExtension
# from pipeline.jinja2 import PipelineExtension
# from compressor.offline.jinja2 import url_for, SpacelessExtension
from typing import Any


loaders = [
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',
    'jina2.FileSystemLoader'
]

extensions = [CompressorExtension, do, loopcontrols, with_, i18n, autoescape]


def dmlsite_jinja_env(**options: Any):
    env = Environment(loaders=FileSystemLoader('templates/'), extensions=extensions)
    return env


"""
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ]
"""

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
