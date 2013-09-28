# coding: utf-8
from django.conf.urls import url
from tastypie.utils import trailing_slash
from common.api import BaseResource


class FriendResource(BaseResource):

    class Meta(BaseResource.Meta):
        related_name = 'friends'
        list_allowed_methods = ['get']

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        return [
            url(r"^(?P<resource_name>%s)/with/(?P<friend_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
        ]

    def dispatch_list(self, request, **kwargs):
        return self.dispatch('list', request, **kwargs)

    def get_list(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        user = request.user

        query = user.fql({
            'query_friends': 'SELECT name, pic_big, profile_url, uid, username FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = \'%s\' AND uid2 IN (SELECT uid2 FROM friend WHERE uid1=me()))' % kwargs.get('friend_id'),
        })

        response = []

        if query.get('data'):
            response = query.get('data')[0].get('fql_result_set' or [])

        return self.create_response(request, response)
