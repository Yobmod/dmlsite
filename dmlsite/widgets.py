from django import forms
from django.template import loader
from django.utils.safestring import mark_safe


class MyWidget(forms.Widget):
	template_name = 'dmlmain/my_widget.html'  # must be in namesapced templates folder

	def get_context(self, name, value, attrs=None):
		return {'widget': {
			'name': name,
			'value': value,
		}}

	def render(self, name, value, attrs=None):
		context = self.get_context(name, value, attrs)
		template = loader.get_template(self.template_name).render(context)
		return mark_safe(template)
