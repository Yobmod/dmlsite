from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ContactForm
from .models import SignUp

def homepage(request):
	form = SignUpForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		#if not instance.name:
		#	instance.name = "Visitor"
		name = form.cleaned_data.get('name')
		instance.save()
		  #'text' is name of template tag, text is what is shown

	if request.user.is_authenticated() and request.user.is_staff:
		text = "Hello %s, valued employee, printing signups" %(request.user)
		i = 1
		for instance in SignUp.objects.all():
			print(i)
			print(instance)
			i += 1
	elif request.user.is_authenticated():
			text = "Hello %s" %(request.user)
	else:
			text = "Welcome visitor"
	context = {'text': text, 'form':form,}
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


def register(request):
	return render(request, 'registration/registration_form.html')

def test(request):
	return render(request, 'test/test.html')
