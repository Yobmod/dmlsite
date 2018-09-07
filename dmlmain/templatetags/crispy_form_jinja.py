from crispy_forms.utils import render_crispy_form
from django_jinja import library
from jinja2 import contextfunction, exceptions, runtime  # , contextfilter
from django.forms import Form
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django.conf import settings


@contextfunction
@library.global_function
def crispify(context: runtime.Context, form: Form) -> str:
    # print(context)
    if not form:  # if context not passing a form
        raise exceptions.TemplateSyntaxError(lineno=0, 
                                             name='crispify template function Error', 
                                             filename='meeehhh', 
                                             message=f"""No form found in context for crispy tag""")
    crispied = render_crispy_form(form, helper=None, context=context)
    return crispied


@library.filter
def crispy(form: Form, label_class: str = "", field_class: str = "", template_pack: str = "") -> str:
    template_pack = template_pack or settings.CRISPY_TEMPLATE_PACK or 'bootstrap3'

    if not isinstance(template_pack, str) or not isinstance(label_class, str) or not isinstance(field_class, str): 
        raise TypeError('Crispy template filter requires string arguments')
    if not form:  # if context not passing a form
        raise exceptions.TemplateSyntaxError(lineno=0, 
                                             name='crispy template filter Error', 
                                             filename='meeehhh', 
                                             message=f"""No form found in context for crispy filter""")
    crispied = as_crispy_form(form, 
                              template_pack=template_pack, 
                              label_class=label_class,  # adds class to labels eg. col-lg-2
                              field_class=field_class)  # adds class to fields
    return crispied
