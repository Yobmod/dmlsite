from django import template
from django_jinja import library as djjn_library
from jinja2.exceptions import TemplateSyntaxError
from urllib.parse import quote_plus

register = template.Library()


class bcolors():
    HEADER = b'\033[95m'
    OKBLUE = b'\033[94m'
    OKGREEN = b'\033[92m'
    WARNING = b'\033[93m'
    FAIL = b'\033[91m'
    ENDC = b'\033[0m'
    BOLD = b'\033[1m'
    UNDERLINE = b'\033[4m'


@register.filter
def urlify(value: str) -> str:
    return quote_plus(value)


@djjn_library.filter
def urlify_jn(value: str) -> str:
    try:
        urlified = quote_plus(value)
    except TemplateSyntaxError as te:
        message = f'{te}. From {{"string" | urilify_jn()}} tag?'
        print(message)
    except Exception as e:
        print(e)
    print(bytes.decode(bcolors.WARNING) + "Warning: No active frommets remain. Continue?")
    return urlified


@djjn_library.global_function
def urlify_tag(value: str) -> str:
    return quote_plus(value)
