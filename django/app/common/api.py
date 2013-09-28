# coding: utf-8
from tastypie.resources import Resource
from tastypie.authentication import SessionAuthentication


class BaseResource(Resource):
    class Meta:
        authentication = SessionAuthentication()