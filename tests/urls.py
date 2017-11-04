# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from internal_external_comments.urls import urlpatterns as comments_urls

urlpatterns = [
    url(r'^', include(comments_urls, namespace='comments_urls')),
]
