# coding: utf-8
from django.conf.urls.defaults import patterns, url, include
from facebook.api import PhotoResource

photo_resource = PhotoResource()


urlpatterns = patterns('',
    url(r'^api/', include(photo_resource.urls)),
)