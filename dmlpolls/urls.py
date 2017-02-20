from django.conf.urls import url
from . import views

#app_name = 'dmlpolls'
urlpatterns = [
    #url(r'^index$', views.IndexView.as_view(), name='poll_index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='poll_detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='poll_results'),


	url(r'^$', views.poll_list, name='poll_list'),
	url(r'^(?P<pk>[0-9]+)/$', views.poll_detail, name='poll_detail'),
	url(r'^question/add/$', views.addpoll, name='add_poll'),
	url(r'^(?P<question_id>[0-9]+)/add_choice/$', views.add_choice, name = 'add_choice'),
	url(r'^(?P<pk>[0-9]+)/vote/$', views.vote, name='poll_vote'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.results, name='poll_results'),


]
