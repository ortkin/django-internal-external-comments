from django.conf.urls import url, include
from internal_external_comments import views

urlpatterns = [
    url(r'^', include('django_comments.urls')),
    url(r'^create/$', views.CommentCreateView.as_view(), name='comments-create'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.CommentDetailView.as_view(), name='comments-detail'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.CommentUpdateView.as_view(), name='comments-update'),
    url(r'^delete/(?P<pk>[[0-9]+)/$', views.CommentDeleteView.as_view(), name='comments-delete'),
    url(r'^list/$', views.CommentListView.as_view(), name='comments-list'),
    url(r'^listmodel/(?P<app_label>[\w-]+)/(?P<model>[\w-]+)/(?P<object_pk>[0-9]+)/$',
        views.CommentObjectListView.as_view(), name='comments-object-list'),
]
