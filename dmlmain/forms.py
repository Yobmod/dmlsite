from django import forms
from .models import SignUp


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ["name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # domain, extension = provider.split('.')
        # if domain == "dmlsite":
        # 	raise forms.ValidationError("Already have email")
        # if extension != "ac.uk":
        #	...
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name


class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=200)
