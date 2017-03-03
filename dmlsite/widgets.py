from django import forms

class AMarkField(forms.Field):
	default_error_messages = {
		'not_an_a': (u'you can only input A here! damn!'),
		}

	def to_python(self, value):
		if value in validators.EMPTY_VALUES:
			return None
		if value != 'A':
			raise ValidationError(self.error_messages['not_an_a'])
		return value

from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


class MyWidget(Widget):
	template_name = 'dmlmain/my_widget.html' #must be in namesapced templates folder

	def get_context(self, name, value, attrs=None):
		return {'widget': {
			'name': name,
			'value': value,
		}}

	def render(self, name, value, attrs=None):
		context = self.get_context(name, value, attrs)
		template = loader.get_template(self.template_name).render(context)
		return mark_safe(template)
