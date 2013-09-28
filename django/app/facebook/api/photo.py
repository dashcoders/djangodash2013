# coding: utf-8
from common.api import BaseResource


class PhotoResource(BaseResource):
    class Meta:
        resource_name = 'photo'

    def obj_get_list(self, bundle, **kwargs):
        return []