from django.conf.urls import url
from internal_external_comments import views

urlpatterns = [

    url(r'^post/$', views.CommentCreate.as_view(), name='comments-post-comment'),
    url(r'^posted/$', views.CommentDetail.as_view(), name='comments-comment-done'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view(), name='comments-detail'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.CommentUpdate.as_view(), name='comments-update'),
    url(r'^delete/(?P<pk>[[0-9]+)/$', views.CommentDelete.as_view(), name='comments-delete'),
    url(r'^list/$', views.CommentList.as_view(), name='comments-list'),
    url(r'^list/(?P<app_label>)/(?P<model>)/(?P<object_pk>[0-9]+)/$',
        views.CommentObjectListView.as_view(), name='comments-object-list'),
]
