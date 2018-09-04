jinja import Environment, FileSystemLoader
from jinja2.ext import do, loopcontrols, with_, i18n, autoescape

from compressor.contrib.jinja2ext import CompressorExtension
# from pipeline.jinja2 import PipelineExtension
# from compressor.offline.jinja2 import url_for, SpacelessExtension


loaders = ['django_jinja.loaders.FileSystemLoader',
           'django_jinja.loaders.AppLoader',
]

def dmlsite_jinja_env(**options):
    env = jinja2.Environment(loaders=FileSystemLoader('templates/'), extensions=[CompressorExtension])
    return env

"""
            "extensions": [
                'pipeline.jinja2.PipelineExtension',
                'compressor.contrib.jinja2ext.CompressorExtension',
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ]
"""