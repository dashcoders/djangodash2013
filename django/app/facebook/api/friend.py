# coding: utf-8
from django.conf.urls import url
from django.core.cache import cache
from tastypie.utils import trailing_slash
from common.api import BaseResource


class FriendResource(BaseResource):

    class Meta(BaseResource.Meta):
        related_name = 'friend'

        mutual_allowed_methods = ['get']
        list_allowed_methos = ['get']

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/mutual/(?P<friend_facebook_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_mutual'), name="api_dispatch_mutual"),
        ]

    def dispatch_mutual(self, request, **kwargs):
        return self.dispatch('mutual', request, **kwargs)

    def get_mutual(self, request, **kwargs):
        user = request.user
        friend_facebook_id = kwargs.get('friend_facebook_id')
        cache_id = 'friend_list_user_mutual_%s_%s' % (user.facebook_id, friend_facebook_id)

        cached_friends = cache.get(cache_id)

        if cached_friends:
            return self.create_response(request, cached_friends)

        query = user.fql({
            'query_friends': 'SELECT name, pic, pic_big, pic_small, profile_url, uid FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = \'{friend_facebook_id}\' AND uid2 IN (SELECT uid2 FROM friend WHERE uid1=me()))'.format(friend_facebook_id=friend_facebook_id),
        })

        response = []

        if query.get('data'):
            response = query.get('data')[0].get('fql_result_set' or [])

        cache.set(cache_id, response, 24 * 60 * 60)

        return self.create_response(request, response)

    def get_list(self, request, **kwargs):
        user = request.user
        cache_id = 'friend_list_user_%s' % user.facebook_id

        cached_friends = cache.get(cache_id)

        if cached_friends:
            return self.create_response(request, cached_friends)

        query = user.fql({
            'query_friends': 'SELECT name, pic_big, pic_small, profile_url, uid FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1=me())',
        })

        response = []

        if query.get('data'):
            response = query.get('data')[0].get('fql_result_set' or [])

        cache.set(cache_id, response, 24 * 60 * 60)

        return self.create_response(request, response)
