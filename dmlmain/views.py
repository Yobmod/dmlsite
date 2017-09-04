from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ContactForm
from .models import SignUp
from django.http import HttpResponse
from django.views.generic import View
from dmlmain.utils import render_to_pdf
import datetime

from django_user_agents.utils import get_user_agent


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
	user_agent = get_user_agent(request)
	if user_agent.is_mobile == False:
			return render(request, 'dmlmain/homepage.html', context)
	else:
		#return render(request, 'dmlmain/homepage_mob.html', context)
		return HttpResponse("you are on a mobile")

from django_q.tasks import async, result
import . import tasks

def contact_admins(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_name = form.cleaned_data.get('name')
		form_email = form.cleaned_data.get('email')
		form_message = form.cleaned_data.get('message')

		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, form_email] #send copy to myself
		contact_message = "%s: %s via %s"%(form_name, form_message, from_email)
		send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

		async('tasks.create_html_report', hook='tasks.email_report')

	context = {'form':form,}
	return render(request, 'dmlmain/contact_admins.html', context)


@login_required
def django_admin_page(request):
	return render(request, 'dmlmain/admin')


def register(request):
	return render(request, 'registration/registration_form.html')

from django.template.loader import get_template

class GenerateInvoice(View):
	def get(self, request, *args, **kwargs):
		amount = 13490
		invoice_id = 12345
		customer_name = "John Cooper"
		context = {
			'today': datetime.date.today(),
			'amount': 39.99,
			'customer_name': 'Cooper Mann',
			'invoice_id': 1233434,
			}
		pdf = render_to_pdf('pdf/test.html', context)
		return HttpResponse(pdf, content_type='application/pdf')

class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		template = get_template('pdf/test.html')
		amount = 13490 # = Invoice.amount etc from a model. Then can be added by form
		invoice_id = 12345
		customer_name = "John Cooper"
		context = {
			"invoice_id": invoice_id,
			"customer_name": customer_name,
			"amount": amount,
			"today": datetime.date.today(),
			}
		html = template.render(context)
		pdf = render_to_pdf('pdf/test.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" %("company_name " + str(invoice_id))
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")

		# response = HttpResponseRedirect("URL u want to redirect to"
		# response['Content-Disposition'] = "attachment; filename='%s'" % ("attachment; filename='yourpdffilename')
		# return response﻿
