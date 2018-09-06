from classytags.core import Tag
# from classytags.utils import flatten_context
# from classytags.helpers import InclusionTag
from django import template, VERSION
from django.template import Context, RequestContext, Template
from django.template.context import BaseContext
from django.template.loader import render_to_string

import warnings
from typing import Optional as Opt, Dict

from jinja2.runtime import Context


register = template.Library()

"""
change library to django_jinja
Set template to .jinja (?)
Get template_filename for context
Get request from the context
Get context
Render template

"""


def flatten_context(context: Context) -> Context:
    """ """
    def do_flatten(context: Context) -> dict:
        flat: dict = {}
        for d in context.dicts:
            if isinstance(d, (Context, RequestContext)):
                flat.update(do_flatten(d))
            else:
                flat.update(d)
        return flat

    if callable(getattr(context, 'flatten', None)) and VERSION[:2] <= (1, 9):
        return context.flatten()
    elif isinstance(context, BaseContext):
        return do_flatten(context)
    return context


class InclusionTag(Tag):
    """
    A helper Tag class which allows easy inclusion tags.
    The template attribute must be set.
    Instead of render_tag, override get_context in your subclasses.
    Optionally override get_template in your subclasses.
    """
    template: Opt[str] = None
    push_context = False

    def render_tag(self, context: Context, **kwargs: dict) -> str:
        """INTERNAL!Gets the context and data to render."""

        template = self.get_template(context, **kwargs)
        if self.push_context:
            safe_context = flatten_context(context)
            data = self.get_context(safe_context, **kwargs)
            safe_context.update(**data)
            output = render_to_string(template, safe_context)
        else:
            new_context = context.new(
                flatten_context(self.get_context(context, **kwargs))
            )
            data = flatten_context(new_context)
            output = render_to_string(template, data)
        return output

    def get_template(self, context: Context, **kwargs: Dict[str, object]) -> Template:
        """Returns the template to be used for the current context and arguments."""
        return self.template

    def get_context(self, context: Context, **kwargs: dict) -> Context:
        """Returns the context to render the template with."""
        return {}


class CookielawBanner(InclusionTag):
    """ Displays cookie law banner only if user has not dismissed it yet."""
    
    template = 'cookielaw/banner.html'

    def render_tag(self, context: Context, **kwargs: dict) -> str:
        template_filename = self.get_template(context, **kwargs)
        if 'request' not in context:
            warnings.warn('No request object in context. '
                          'Are you sure you have django.core.context_processors.request enabled?')
        if context['request'].COOKIES.get('cookielaw_accepted', False):
            return ''
        data = self.get_context(context, **kwargs)

        if VERSION[:2] < (1, 10):
            return render_to_string(template_filename, data, context_instance=context)
        else:
            return render_to_string(template_filename, data, context.request)


register.tag(CookielawBanner)
