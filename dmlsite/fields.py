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
