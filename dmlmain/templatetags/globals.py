import json
import logging
from datetime import datetime
from typing import Dict

from django.conf import settings
from django.contrib.sites.models import Site
from django.forms.widgets import Widget, CheckboxInput
from django.forms import Field
from django.http import HttpRequest
from django.template import defaultfilters
# from django.template.loader import datetime
from django.utils.timezone import get_current_timezone

from allauth.socialaccount import providers
from django_jinja import library
from webpack_loader.templatetags import webpack_loader as wl


logger = logging.getLogger(__name__)


@library.global_function
def build_absolute_uri(relative_url: str) -> str:
    domain = Site.objects.get_current().domain
    protocol = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
    absolute_url = '{}://{}{}'.format(protocol, domain, relative_url)
    return absolute_url


@library.global_function
def render_bundle(bundle_name: str, extension: None=None, config: str='DEFAULT', attrs: str='') -> str:
    return wl.render_bundle(bundle_name, extension, config, attrs)


@library.global_function
def cookielaw(request: HttpRequest) -> str:
    if request.COOKIES.get('cookielaw_accepted', False):
        return ''
    return datetime('cookielaw/cookielaw.jinja', request=request)
    # shuld be jango datetime filter function

@library.global_function
def now(format_string: str) -> str:
    """
    Simulates the Django https://docs.djangoproject.com/en/dev/ref/templates/builtins/#now default templatetag
    Usage: {{ now('Y') }}
    """
    tzinfo = get_current_timezone() if settings.USE_TZ else None
    return defaultfilters.date(datetime.now(tz=tzinfo), format_string)


@library.global_function
def should_enable_discourse(is_public: bool) -> bool:
    """
    Returns True if we are not in DEBUG mode and the detail object (the wagtail Page or django Model, e.g.,
    Codebase/CodebaseRelease/Event/Job) is public. If there is no 'live' attribute, default to True as it is public by
    default.
    """
    return is_public and not settings.DEPLOY_ENVIRONMENT.is_development()


@library.global_function
def is_debug() -> bool:
    return settings.DEBUG


@library.global_function
def release_version() -> str:
    return settings.RELEASE_VERSION


@library.global_function
def is_production() -> bool:
    return settings.DEPLOY_ENVIRONMENT.is_production() and not settings.DEBUG


@library.global_function
def deploy_environment() -> str:
    return settings.DEPLOY_ENVIRONMENT


@library.global_function
def sentry_public_dsn() -> str:
    return settings.RAVEN_CONFIG.get('public_dsn')


@library.global_function
def provider_login_url(request: HttpRequest, provider_id: str, **kwargs: Dict[str, object]) -> str:
    provider = providers.registry.by_id(provider_id, request)
    next_url = request.GET.get('next', None)
    if next_url:
        kwargs['next'] = next_url
    return provider.get_login_url(request, **kwargs)


"""
@library.global_function
def get_choices_display(selected_choice, choices):
    "
    Takes a model_utils.Choices key entry alongside its parent set of Choices and returns the display value for that
    particular selected_choice. Tries a pair tuple first ("foo", "Display value for foo") and then the triple
    (<numeric_id>, "foo", "Display value for foo")
    "
    try:
        return choices[selected_choice]
    except:
        return choices[getattr(choices, selected_choice)]
"""


@library.filter
def is_checkbox(bound_field: Widget) -> bool:
    return isinstance(bound_field.field.widget, CheckboxInput)


"""
from jinja2 import Markup
from core.fields import render_sanitized_markdown
@library.filter
def markdown(text: str):
    "
    Returns a sanitized HTML string representing the rendered version of the incoming Markdown text.
    :param text: string markdown source text to be converted
    :return: sanitized html string, explicitly marked as safe via jinja2.Markup
    "
    return Markup(render_sanitized_markdown(text))
"""


@library.filter
def add_field_css(field: Field, css_classes: str) -> Widget:
    if field.errors:
        css_classes += ' is-invalid'
    css_classes = field.css_classes(css_classes)
    deduped_css_classes = ' '.join(set(css_classes.split(' ')))
    return field.as_widget(attrs={'class': deduped_css_classes})


"""
from django.utils.dateparse import parse_datetime
from core.serializers import FULL_DATE_FORMAT
from typing import Optional as Opt
@library.filter
def format_datetime_str(text: Opt[str], format_string=FULL_DATE_FORMAT):
    if text is None:
        return None
    d = parse_datetime(text)
    return format_datetime(d, format_string)
"""

"""
from core.serializers import FULL_DATE_FORMAT
@library.filter
def format_datetime(date_obj, format_string=FULL_DATE_FORMAT):
    if date_obj is None:
        return None
    return date_obj.strftime(format_string)
"""


@library.filter
def to_json(value: object) -> str:
    return json.dumps(value)


# # http://stackoverflow.com/questions/6453652/how-to-add-the-current-query-string-to-an-url-in-a-django-template
# @register.simple_tag
# def query_transform(request, **kwargs):
#     updated = request.GET.copy()
#     for k, v in kwargs.iteritems():
#         updated[k] = v
#
#     return updated.urlencode()
