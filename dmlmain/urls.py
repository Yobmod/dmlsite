from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
	url(r'^contact/$', views.contact_admins, name='contact_admins'),
	url(r'^admin/$', views.django_admin_page, name='django_admin_page'), #link to admin

	url(r'^accounts/', include('registration.backends.default.urls'), name='accounts'),
		#names = 'auth_login' /login 'auth_logout' 'registration_register' 'auth_password_reset' 'registration_activate'

	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
	url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),

	url(r'^test/$', views.GeneratePdf.as_view(), name='test'),
	url(r'^invoice/$', views.GenerateInvoice.as_view(), name='invoice'),
	]
