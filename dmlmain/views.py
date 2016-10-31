from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ContactForm

def homepage(request):
	if request.user.is_authenticated():
		text = "Hello %s" %(request.user)
	else:
		text = "Welcome visitor"
	form = SignUpForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		#if not instance.name:
		#	instance.name = "Visitor"
		name = form.cleaned_data.get('name')
		instance.save
	context = {'text': text, 'form':form,}  #'text' is name of template tag, text is what is shown
	return render(request, 'dmlmain/homepage.html', context)


def contact_admins(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_name = form.cleaned_data.get('name')
		form_email = form.cleaned_data.get('email')
		form_message = form.cleaned_data.get('message')

		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'other@email.com']
		contact_message = "%s: %s via %s"%(form_name, form_message, form_email)
		send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

	context = {'form':form,}
	return render(request, 'dmlmain/contact_admins.html', context)


@login_required
def django_admin_page(request):
	return render(request, 'dmlmain/admin')
