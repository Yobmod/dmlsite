from django.conf.urls import url
from . import views



app_name = 'dmlcomments'
urlpatterns = [

	url(r'^(?P<pk>\d+)/thread/$', views.comment_thread, name='comment_thread'), #detail view of single comment thread
	url(r'^(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),

	#url(r'^$', views.comment_list, name='comment_list'), #list all comments, filter by approved / question / author /date? Searchable?
	#url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
	#url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

]
