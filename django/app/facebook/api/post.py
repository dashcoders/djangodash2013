# coding: utf-8
from django.conf.urls import url
from django.core.cache import cache
from tastypie.utils import trailing_slash
from common.api import BaseResource


class PostResource(BaseResource):

    class Meta(BaseResource.Meta):
        related_name = 'post'

        in_friend_allowed_methods = ['get']
        tagged_friend_allowed_methods = ['get']

    def base_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/in/(?P<friend_facebook_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_in_friend'),
                name="api_dispatch_in_friend"
            ),
            url(
                r"^(?P<resource_name>%s)/tagged/(?P<friend_facebook_id>\d+)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_tagged_friend'),
                name="api_dispatch_tagged_friend"
            ),
        ]

    def dispatch_in_friend(self, request, **kwargs):
        return self.dispatch('in_friend', request, **kwargs)

    def dispatch_tagged_friend(self, request, **kwargs):
        return self.dispatch('tagged_friend', request, **kwargs)

    def get_in_friend(self, request, **kwargs):
        user = request.user
        friend_facebook_id = kwargs.get('friend_facebook_id')

        query_tags = user.fql(
            """
                SELECT post_id, actor_id
                FROM stream_tag
                WHERE
                    target_id = me()
                    AND actor_id = '{friend_facebook_id}'
                LIMIT 10000
            """.format(
                friend_facebook_id=friend_facebook_id,
            )
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
                    friend_facebook_id=friend_facebook_id,
                    post_ids=','.join(posts_ids),
                )
            )

            posts = query_posts.get('data')

        return self.create_response(request, posts)

    def get_tagged_friend(self, request, **kwargs):
        user = request.user
        friend_facebook_id = kwargs.get('friend_facebook_id')

        query_tags = user.fql(
            """
                SELECT post_id, actor_id
                FROM stream_tag
                WHERE
                    target_id = '{friend_facebook_id}'
                    AND actor_id = me()
                LIMIT 10000
            """.format(
                friend_facebook_id=friend_facebook_id,
            )
        )

        print """
                SELECT post_id, actor_id
                FROM stream_tag
                WHERE
                    target_id = '{friend_facebook_id}'
                    AND actor_id = me()
                LIMIT 10000
            """.format(
                friend_facebook_id=friend_facebook_id,
            )

        posts = []
        tagged_posts = query_tags.get('data')

        print tagged_posts

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
                    friend_facebook_id=friend_facebook_id,
                    post_ids=','.join(posts_ids),
                )
            )

            posts = query_posts.get('data')

        return self.create_response(request, posts)
