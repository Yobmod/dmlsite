from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def homepage(request):
	return render(request, 'dmlmain/homepage.html')	

def contact_admins(request):
	return render(request, 'dmlmain/contact_admins.html')

@login_required
def django_admin_page(request):
	return render(request, 'dmlmain/admin')
	

