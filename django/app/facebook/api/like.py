# coding: utf-8
from django.conf.urls import url
from common.api import BaseResource

from tastypie.utils import trailing_slash


class LikeResource(BaseResource):

    class Meta(BaseResource.Meta):
        resource_name = 'like'

        with_friend_allowed_methods = ['get']

    def base_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/with/(?P<friend_facebook_id>\d{1,32})%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_with_friend'),
                name="api_dispatch_like_with_friend",
            ),
        ]

    def dispatch_with_friend(self, request, **kwargs):
        return self.dispatch('with_friend', request, **kwargs)

    def get_with_friend(self, request, **kwargs):
        friend_facebook_id = kwargs.get('friend_facebook_id')
        user = request.user

        response = user.fql(
            """
                SELECT page_id, name, page_url, pic_square FROM page WHERE page_id IN (
                    SELECT page_id FROM page_fan WHERE uid = '{friend_facebook_id}' AND page_id IN (
                        SELECT page_id FROM page_fan WHERE uid = me()
                    )
                )
            """.format(friend_facebook_id=friend_facebook_id)
        )

        return self.create_response(request, response.get('data'))
