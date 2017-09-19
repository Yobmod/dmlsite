from django.conf.urls import url, include
from . import views

#app_name = 'dmlpolls'
urlpatterns = [

	url(r'^$', views.index, name='poll_index'),
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='poll_detail'),
	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='poll_results'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='poll_vote'),
	url(r'^polls/', include('dmlpolls.urls')),
#    url(r'^admin/', admin.site.urls),
]
