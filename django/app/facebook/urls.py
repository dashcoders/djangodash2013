# coding: utf-8
from django.conf.urls import patterns, url, include
from facebook.api import PhotoResource, FriendResource
from .views import FacebookLoginView


photo_resource = PhotoResource()
friend_resource = FriendResource()


urlpatterns = patterns(
    '',
    url(r'^login/$', FacebookLoginView.as_view(), name='facebook_login'),
    url(r'^api/', include(photo_resource.urls)),
    url(r'^api/', include(friend_resource.urls)),
)
