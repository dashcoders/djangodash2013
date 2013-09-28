# coding: utf-8
import json
import requests
# from django.utils.translation import ugettext as _
from accounts.models import User


class FacebookBackend(object):
    def authenticate(self, token):
        facebook_profile = self.get_facebook_profile(token)

        try:
            user = User.object.get(facebook_id=facebook_profile['id'])
        except User.DoesNotExist:
            user = User.get(facebook_id=facebook_profile['id'])

        user.set_unusable_password()
        user.facebook_access_token = token
        user.email = facebook_profile.get('email')
        user.first_name = facebook_profile.get('first_name')
        user.last_name = facebook_profile.get('last_name')
        user.save()

        print user

    def get_facebook_profile(self, token):
        url = 'https://graph.facebook.com/me/'

        params = {
            'access_token': token,
            'metadata': 1,
        }

        response = requests.get(
            url,
            params=params,
            headers={
                'Content-type': 'application/json',
                'Accept': 'application/json',
            },
        )

        return self._parse_json(response.content)

    def _parse_json(self, content):
        try:
            data = json.loads(content)
        except Exception:
            print 'Error parsing JSON response', content
            raise Exception(error_message=content)
        return data
