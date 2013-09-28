# coding: utf-8
from django.conf.urls import url
from common.api import BaseResource

from tastypie.utils import trailing_slash


class PhotoResource(BaseResource):

    class Meta(BaseResource.Meta):
        resource_name = 'photo'

    def obj_get_list(self, bundle, **kwargs):
        user = bundle.request.user

        response = user.fql({
            'query1_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo WHERE owner = \'100000754284842\') AND subject = me()',
            'query2_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo WHERE owner = me()) AND subject = \'100000754284842\'',
            'query3_tags': 'SELECT pid, xcoord, ycoord FROM photo_tag WHERE pid IN (SELECT pid FROM photo_tag WHERE subject = me()) AND subject = \'100000754284842\' AND pid IN (SELECT pid, src_big FROM photo WHERE owner = me() AND owner != \'100000754284842\')',
            'query1_photos': 'SELECT pid, src_big, src_small FROM photo WHERE pid IN (SELECT pid FROM #query1_tags)',
            'query2_photos': 'SELECT pid, src_big, src_small FROM photo WHERE pid IN (SELECT pid FROM #query2_tags)',
            'query3_photos': 'SELECT pid, src_big, src_small, src, link FROM photo WHERE pid IN (SELECT pid FROM #query3_tags)',
        })

        print response

        return []
