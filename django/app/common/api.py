# coding: utf-8
from tastypie.resources import Resource


class BaseResource(Resource):
    class Meta:
    	authentication = SessionAuthentication()