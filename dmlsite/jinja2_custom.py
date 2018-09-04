import jinja2
from compressor.contrib.jinja2ext import CompressorExtension

def dmlsite_jinja_env(**options):
    env = jinja2.Environment(extensions=[CompressorExtension])
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