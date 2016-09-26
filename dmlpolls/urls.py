from django.conf.urls import url
from . import views

#app_name = 'dmlpolls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='poll_index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='poll_detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='poll_results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='poll_vote'),
]