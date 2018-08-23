"""dmlsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import re_path, path
#import django.contrib.auth.views                #The login views redirect to admin here, or to previous page in dmlmain
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from controlcenter.views import controlcenter
from django.conf.urls.static import static
from django.conf import settings

# admin.autodiscover()

urlpatterns = [
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', admin.site.urls),
	path('admin/dashboard/', controlcenter.urls),
	#url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
	#url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^', include('dmlmain.urls')),
	url(r'^blog/', include('dmlblog.urls', namespace='blog')),
	re_path(r'^polls/', include('dmlpolls.urls', namespace='polls')),
	url(r'^comments/', include('dmlcomments.urls', namespace='comments')),
	url(r'^research/', include('dmlresearch.urls', namespace='research')),
	url(r'^chat/', include('dmlchat.urls', namespace='chat')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
