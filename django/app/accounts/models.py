# coding: utf-8
import json
import requests
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'facebook_id'

    facebook_id = models.CharField(_('facebook id'), max_length=20, unique=True)
    facebook_access_token = models.CharField(_('facebook access token'), max_length=255, unique=True)

    def __unicode__(self):
        return self.email

    def fql(self, query):
        if isinstance(query, dict):
            query = json.dumps(query)

        response = requests.get(
            'https://graph.facebook.com/fql',
            params={
                'q': query,
                'access_token': self.facebook_access_token,
            },
        )

        return response.json()

    def graph_delete(self, url, params={}):

        url = 'https://graph.facebook.com' + url

        params.update({
            'access_token': self.facebook_access_token,
        })

        response = requests.delete(
            url,
            params=params,
        )

        return response.json()
