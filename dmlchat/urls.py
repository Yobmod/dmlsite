from django.conf.urls import url

from . import views

app_name = 'dmlchat'

urlpatterns = [
	url(r'^$', views.chat_main, name='chat'),

	url(r'^test/$', views.chat_test, name='test'),

	]
