from django.conf.urls import url
# from django.urls import re_path  # , path, include

from . import views

app_name = 'dmlchat'

urlpatterns = [
	url(r'^$', views.chat_main, name='chat_main'),

	url(r'^(?P<room_name>[^/]+)/$', views.chat_room, name='chat_room'),


	# url(r'^test/$', views.chat_test, name='test'),

	]
