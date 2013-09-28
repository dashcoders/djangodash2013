# coding: utf-8
from django.conf.urls import url
from common.api import BaseResource

from tastypie.utils import trailing_slash


class PhotoResource(BaseResource):

    class Meta(BaseResource.Meta):
        resource_name = 'photo'

        with_friend_allowed_methods = ['get']

    def base_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/with/(?P<friend_facebook_id>\d{1,32})%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_with_friend'),
                name="api_dispatch_with_friend",
            ),
        ]

    def dispatch_with_friend(self, request, **kwargs):
        return self.dispatch('with_friend', request, **kwargs)

    def get_with_friend(self, request, **kwargs):
        friend_facebook_id = kwargs.get('friend_facebook_id')

        user = request.user

        response = user.fql({
            'query1_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo WHERE owner = \'{friend_facebook_id}\') AND subject = me()'.format(friend_facebook_id=friend_facebook_id),
            'query2_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo WHERE owner = me()) AND subject = \'{friend_facebook_id}\''.format(friend_facebook_id=friend_facebook_id),
            'query3_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo_tag WHERE subject = me()) AND subject = \'100000754284842\' AND pid IN (SELECT pid, src_big FROM photo WHERE owner = me() AND owner != \'{friend_facebook_id}\')'.format(friend_facebook_id=friend_facebook_id),
            'query1_photos': 'SELECT pid, src_big, src_small FROM photo WHERE pid IN (SELECT pid FROM #query1_tags)',
            'query2_photos': 'SELECT pid, src_big, src_small FROM photo WHERE pid IN (SELECT pid FROM #query2_tags)',
            'query3_photos': 'SELECT pid, src_big, src_small, src, link FROM photo WHERE pid IN (SELECT pid FROM #query3_tags)',
        })

        photos = {}
        for results in response.get('data'):
            for result in results.get('fql_result_set'):
                if result.get('pid') not in photos:
                    photos[result.get('pid')] = {}
                photos[result.get('pid')].update(result)

                print photos[result.get('pid')]

        return self.create_response(request, photos.values())
