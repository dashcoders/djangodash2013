# coding: utf-8
from django.conf.urls import url
from tastypie.utils import trailing_slash
from common.api import BaseResource


class CommentResource(BaseResource):

    class Meta(BaseResource):
        related_name = 'comment'
        in_posts_by_friend_allowed_methods = ['get']

    def base_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/from/(?P<from_facebook_id>(\d+|me))/in_posts_by/(?P<to_facebook_id>(\d+|me))%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_in_posts_by_friend'),
                name="api_dispatch_in_posts_by_friend"
            ),
        ]

    def dispatch_in_posts_by_friend(self, request, **kwargs):
        return self.dispatch('in_posts_by_friend', request, **kwargs)

    def get_in_posts_by_friend(self, request, **kwargs):
        user = request.user
        from_facebook_id = kwargs.get('from_facebook_id')
        to_facebook_id = kwargs.get('to_facebook_id')

        query_comments = user.fql(
            """
                SELECT post_id, text
                FROM comment
                WHERE
                    post_id IN (SELECT post_id FROM stream WHERE source_id = {to_facebook_id} LIMIT 1000000)
                    AND fromid = {from_facebook_id}
                LIMIT 10000
            """.format(from_facebook_id='me()' if from_facebook_id == 'me' else from_facebook_id,
                       to_facebook_id='me()' if to_facebook_id == 'me' else to_facebook_id)
        )

        comments = []
        facebook_post = 'https://www.facebook.com/{}/posts/{}'

        for comment in query_comments.get('data'):
            user_id, post_id = comment.get('post_id').split('_')
            comment['permalink'] = facebook_post.format(user_id, post_id)
            comments.append(comment)

        return self.create_response(request, comments)
