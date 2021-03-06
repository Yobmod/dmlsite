from django.conf.urls import url
from . import views


app_name = "blog"
urlpatterns = [
    url(r"^$", views.post_list, name="post_list"),
    url(r"^drafts/$", views.post_draft_list, name="post_draft_list"),
    url(r"^post/(?P<pk>\d+)/$", views.post_detail, name="post_detail"),
    url(r"^post/new/$", views.post_new, name="post_new"),
    url(r"^post/(?P<pk>\d+)/edit/$", views.post_edit, name="post_edit"),
    url(r"^post/(?P<pk>\d+)/publish/$", views.post_publish, name="post_publish"),
    url(r"^post/(?P<pk>\d+)/unpublish/$", views.post_unpublish, name="post_unpublish"),
    url(r"^post/(?P<pk>\d+)/dremove/$", views.draft_remove, name="draft_remove"),
    url(r"^post/(?P<pk>\d+)/tag/$", views.tag_post, name="tag_post"),
    url(
        r"^post/(?P<pk>\d+)/comment/$",
        views.add_comment_to_post,
        name="add_comment_to_post",
    ),
    url(
        r"^comment/(?P<pk>\d+)/approve/$", views.comment_approve, name="comment_approve"
    ),
    url(r"^comment/(?P<pk>\d+)/remove/$", views.comment_remove, name="comment_remove"),
    url(r"^test/$", views.post_test, name="post_test"),
]
