# coding: utf-8
from django.conf.urls import url
from tastypie.utils import trailing_slash
from common.api import BaseResource


class CommentResource(BaseResource):

    class Meta(BaseResource):
        related_name = 'comment'
        mutual_allowed_methods = ['get']

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        return [
            url(r"^(?P<resource_name>%s)/mutual/(?P<friend_facebook_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_mutual'), name="api_dispatch_mutual"),
        ]

    def dispatch_mutual(self, request, **kwargs):
        return self.dispatch('mutual', request, **kwargs)

    def get_mutual(self, request, **kwargs):
        user = request.user
        friend_facebook_id = kwargs.get('friend_facebook_id')

        query1 = 'SELECT post_id, text FROM comment WHERE post_id IN (SELECT post_id FROM stream WHERE source_id = me() LIMIT 100000000) AND fromid = \'{friend_facebook_id}\' LIMIT 100000'.format(friend_facebook_id=friend_facebook_id)
        query2 = 'SELECT post_id, text FROM comment WHERE post_id IN (SELECT post_id FROM stream WHERE source_id = \'{friend_facebook_id}\' LIMIT 100000000) AND fromid = me() LIMIT 100000'.format(friend_facebook_id=friend_facebook_id)

        response = user.fql({
            'query_source1': query1,
            'query_source2': query2,
        })

        comments = {}
        facebook_post = 'https://www.facebook.com/{0}/posts/{1}'

        for result in response.get('data'):
            for post in result.get('fql_result_set'):
                if post.get('post_id') not in comments:
                    comments[post.get('post_id')] = {}
                user_id, post_id = post.get('post_id').split('_')
                post['permalink'] = facebook_post.format(user_id, post_id)
                comments[post.get('post_id')].update(post)

        return self.create_response(request, comments.values())
