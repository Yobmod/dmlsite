# from django.template.loader import get_template
# import os
# from twilio.rest import Client

# from .tasks import create_html_report, email_report
# from django_q.tasks import async_task, result
from django.contrib.auth.decorators import login_required
from django.shortcuts import render  # , redirect, get_object_or_404

# from datetime import timezone
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ContactForm
from .models import SignUp
from django.http import HttpResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import View
from dmlmain.utils import render_to_pdf
import datetime
from django_user_agents.utils import get_user_agent

from typing import Any


def homepage(request: WSGIRequest) -> HttpResponse:
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # if not instance.name:
        # instance.name = "Visitor"
        # name = form.cleaned_data.get("name")
        instance.save()
        # 'text' is name of template tag, text is what is shown

    if request.user.is_authenticated and request.user.is_staff:
        text = f"Hello {request.user}, valued employee, printing signups "
        i = 1
        for instance in SignUp.objects.all():
            print(i)
            print(instance)
            i += 1
    elif request.user.is_authenticated:
        text = f"Hello {request.user}"
    else:
        text = "Welcome visitor"
    context = {"text": text, "form": form}
    user_agent = get_user_agent(request)
    if user_agent.is_mobile is False:
        return render(request, "dmlmain/homepage.html", context)
    else:
        # return render(request, 'dmlmain/homepage_mob.html', context)
        return HttpResponse("you are on a mobile")


def contact_admins(request: WSGIRequest) -> HttpResponse:
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_name = form.cleaned_data.get("name")
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        subject = "dmlsite contact"
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, form_email]  # send copy to myself
        contact_message = "%s: %s via %s" % (form_name, form_message, from_email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)
        # async_task('dmlmain.tasks.create_html_report', , hook='dmlmain.tasks.test_hook')
    context = {"form": form}
    return render(request, "dmlmain/contact_admins.html", context)


def contact_jinja(request: HttpRequest) -> HttpResponse:
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_name = form.cleaned_data.get("name")
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        subject = "dmlsite contact"
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, form_email]  # send copy to myself
        contact_message = "%s: %s via %s" % (form_name, form_message, from_email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)
        # async_task('dmlmain.tasks.create_html_report', , hook='dmlmain.tasks.test_hook')
    context = {"form": form}
    return render(request, "dmlmain/contact_jinja.jinja", context)


"""
def contact_SMS(request: HttpRequest) -> HttpResponse:
    form = SMSForm(request.POST or None)
    if form.is_valid():
        form_name = form.cleaned_data.get("name")
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        PHONE_NUMBER = os.environ["PHONE_NUMBER"]
        TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
        TWILIO_ACC_SID = os.environ["TWILIO_ACC_SID"]
        TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=PHONE_NUMBER,
            from_=TWILIO_NUMBER,
            body="%s: %s via %s" % (form_name, form_message, form_email),
        )
    context = {"form": form}
    return render(request, "dmlmain/contact_SMS.html", context)
"""


@login_required
def django_admin_page(request: HttpRequest) -> HttpResponse:
    return render(request, "dmlmain/admin")


def register(request: HttpRequest) -> HttpResponse:
    return render(request, "registration/registration_form.html")


class GenerateInvoice(View):
    def get(
        self, request: HttpRequest, name: str = "Default", *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if "amount" in kwargs:
            amount = kwargs["amount"]
        else:
            amount = None
        invoice_id = 12345

        context = {
            "today": datetime.date.today(),
            "amount": amount,
            "customer_name": name,
            "invoice_id": invoice_id,
        }
        pdf = render_to_pdf("pdf/test.html", context)
        return HttpResponse(pdf, content_type="application/pdf")


class GeneratePdf(View):
    def get(
        self, request: HttpRequest, name: str = "Default", *args: Any, **kwargs: Any
    ) -> HttpResponse:
        # template = get_template("pdf/test.html")
        # = Invoice.amount etc from a model. Then can be added by form
        if "amount" in kwargs:
            amount = kwargs["amount"]
        else:
            amount = None
        invoice_id = 12345
        customer_name = name
        context = {
            "invoice_id": invoice_id,
            "customer_name": customer_name,
            "amount": amount,
            "today": datetime.date.today(),
        }
        # html = template.render(context)
        pdf = render_to_pdf("pdf/test.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Invoice_%s.pdf" % ("company_name " + str(invoice_id))
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Not found")

        # response = HttpResponseRedirect("URL u want to redirect to"
        # response['Content-Disposition'] = "attachment; filename='%s'" % ("attachment; filename='yourpdffilename')
        # return response﻿


def handler404(request):
    return render(request, '404.html', status=404)
    

def handler500(request):
    return render(request, '500.html', status=500)
