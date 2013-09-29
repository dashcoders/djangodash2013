# coding: utf-8
from django.conf.urls import url
from django.core.cache import cache
from tastypie.utils import trailing_slash
from common.api import BaseResource


class PostResource(BaseResource):

    class Meta(BaseResource.Meta):
        related_name = 'post'

        mutual_allowed_methods = ['get']
        list_allowed_methos = ['get']

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        return [
            # url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/mutual/(?P<friend_facebook_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_mutual'), name="api_dispatch_mutual"),
        ]

    def dispatch_mutual(self, request, **kwargs):
        return self.dispatch('mutual', request, **kwargs)

    def get_mutual(self, request, **kwargs):
        user = request.user
        friend_facebook_id = kwargs.get('friend_facebook_id')
        cache_id = 'post_list_user_mutual_%s_%s' % (user.facebook_id, friend_facebook_id)

        cached_posts = cache.get(cache_id)

        if cached_posts:
            return self.create_response(request, cached_posts)

        response = user.fql({
            'query_my_posts': 'SELECT post_id, message, permalink, actor_id, created_time, attachment FROM stream WHERE source_id=\'{friend_facebook_id}\' AND actor_id = me() LIMIT 1000000'.format(friend_facebook_id=friend_facebook_id),
            'query_my_posts_tag': 'SELECT post_id, message, permalink, actor_id, created_time, attachment FROM stream WHERE source_id=me() AND target_id=\'{friend_facebook_id}\' AND actor_id = me() LIMIT 1000000'.format(friend_facebook_id=friend_facebook_id),
            'query_friend_posts': 'SELECT post_id, message, permalink, actor_id, created_time, attachment FROM stream WHERE source_id=me() AND target_id=me() AND actor_id=\'{friend_facebook_id}\' LIMIT 1000000'.format(friend_facebook_id=friend_facebook_id),
        })

        posts = {}
        for results in response.get('data'):
            for result in results.get('fql_result_set'):
                posts[result.get('post_id')] = result

        cache.set(cache_id, posts.values(), 24 * 60 * 60)

        return self.create_response(request, posts.values())
