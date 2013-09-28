# coding: utf-8
from tastypie.authentication import Authentication
from django.conf.urls import url
from django.core.cache import cache
from common.api import BaseResource

from tastypie.utils import trailing_slash


class PhotoResource(BaseResource):

    class Meta(BaseResource.Meta):
        resource_name = 'photo'
        authentication = Authentication()

        with_friend_allowed_methods = ['get']
        detail_allowed_methos = ['get', 'delete']

    def delete_detail(self, request, **kwargs):
        user = request.user
        response = user.graph_delete(url='/{0}/likes'.format(kwargs['pk']))
        # response = user.graph_delete(url='/{0}/tags/{1}'.format(kwargs['pk'], user.facebook_id))
        # not working, see issue: https://developers.facebook.com/bugs/122135101317762

        return self.create_response(request, response)

    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
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
        cache_id = 'photo_list_user_mutual_%s_%s' % (user.facebook_id, friend_facebook_id)

        cached_photos = cache.get(cache_id)

        if cached_photos:
            return self.create_response(request, cached_photos)

        response = user.fql({
            'query1_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo WHERE owner = \'{friend_facebook_id}\') AND subject = me()'.format(friend_facebook_id=friend_facebook_id),
            'query2_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo WHERE owner = me()) AND subject = \'{friend_facebook_id}\''.format(friend_facebook_id=friend_facebook_id),
            'query3_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo_tag WHERE subject = me()) AND subject = \'100000754284842\' AND pid IN (SELECT pid, src_big FROM photo WHERE owner = me() AND owner != \'{friend_facebook_id}\')'.format(friend_facebook_id=friend_facebook_id),
            'query1_photos': 'SELECT pid, src_big, can_delete, caption, link, object_id FROM photo WHERE pid IN (SELECT pid FROM #query1_tags)',
            'query2_photos': 'SELECT pid, src_big, can_delete, caption, link, object_id FROM photo WHERE pid IN (SELECT pid FROM #query2_tags)',
            'query3_photos': 'SELECT pid, src_big, can_delete, caption, link, object_id FROM photo WHERE pid IN (SELECT pid FROM #query3_tags)',
        })

        photos = {}
        for results in response.get('data'):
            for result in results.get('fql_result_set'):
                if result.get('pid') not in photos:
                    photos[result.get('pid')] = {}
                photos[result.get('pid')].update(result)

        cache.set(cache_id, photos.values(), 24 * 60 * 60)

        return self.create_response(request, photos.values())
