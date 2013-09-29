# coding: utf-8
from django.conf.urls import patterns, url, include
from facebook.api import (PhotoResource, FriendResource, LikeResource, PostResource,
                          CommentResource)
from .views import FacebookLoginView


photo_resource = PhotoResource()
friend_resource = FriendResource()
like_resource = LikeResource()
post_resource = PostResource()
comment_resource = CommentResource()


urlpatterns = patterns(
    '',
    url(r'^login/$', FacebookLoginView.as_view(), name='facebook_login'),
    url(r'^api/', include(photo_resource.urls)),
    url(r'^api/', include(friend_resource.urls)),
    url(r'^api/', include(like_resource.urls)),
    url(r'^api/', include(post_resource.urls)),
    url(r'^api/', include(comment_resource.urls)),
)
