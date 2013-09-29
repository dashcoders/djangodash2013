# coding: utf-8
from django.conf.urls import url
from django.core.cache import cache
from tastypie.utils import trailing_slash
from common.api import BaseResource


class PostResource(BaseResource):

    class Meta(BaseResource.Meta):
        related_name = 'post'

        tagged_allowed_methods = ['get']
        in_timeline_allowed_methods = ['get']

    def base_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/from/(?P<from_facebook_id>(\d+|me))/tagged/(?P<to_facebook_id>(\d+|me))%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_tagged'),
                name="api_dispatch_tagged"
            ),
            url(
                r"^(?P<resource_name>%s)/from/(?P<from_facebook_id>(\d+|me))/in_timeline/(?P<to_facebook_id>(\d+|me))%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_in_timeline'),
                name="api_dispatch_in_timeline"
            ),
        ]

    def dispatch_tagged(self, request, **kwargs):
        return self.dispatch('tagged', request, **kwargs)

    def dispatch_in_timeline(self, request, **kwargs):
        return self.dispatch('in_timeline', request, **kwargs)

    def get_tagged(self, request, **kwargs):
        user = request.user
        from_facebook_id = kwargs.get('from_facebook_id')
        to_facebook_id = kwargs.get('to_facebook_id')

        query_tags = user.fql(
            """
                SELECT post_id, actor_id
                FROM stream_tag
                WHERE
                    target_id = {to_facebook_id}
                    AND actor_id = {from_facebook_id}
                LIMIT 10000
            """.format(from_facebook_id='me()' if from_facebook_id == 'me' else from_facebook_id,
                       to_facebook_id='me()' if to_facebook_id == 'me' else to_facebook_id)
        )

        posts = []
        tagged_posts = query_tags.get('data')

        if tagged_posts:
            posts_ids = []
            for tagged_post in tagged_posts:
                posts_ids.append("'{}_{}'".format(tagged_post.get('actor_id'), tagged_post.get('post_id')))

            query_posts = user.fql(
                """
                    SELECT post_id, message, permalink, actor_id, created_time, attachment
                    FROM stream
                    WHERE
                        post_id IN ({post_ids})
                    LIMIT 10000
                """.format(
                    post_ids=','.join(posts_ids),
                )
            )

            posts = query_posts.get('data')

        return self.create_response(request, posts)

    def get_in_timeline(self, request, **kwargs):
        user = request.user
        from_facebook_id = kwargs.get('from_facebook_id')
        to_facebook_id = kwargs.get('to_facebook_id')

        query_posts = user.fql(
            """
                SELECT post_id, message, permalink, actor_id, created_time, attachment
                FROM stream
                WHERE
                    source_id = {from_facebook_id}
                    AND actor_id = {to_facebook_id}
                LIMIT 10000
            """.format(from_facebook_id='me()' if from_facebook_id == 'me' else from_facebook_id,
                       to_facebook_id='me()' if to_facebook_id == 'me' else to_facebook_id)
        )

        posts = query_posts.get('data')

        return self.create_response(request, posts)
