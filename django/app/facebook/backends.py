# coding: utf-8
import requests
# from django.utils.translation import ugettext as _
from accounts.models import User


class FacebookBackend(object):
    def authenticate(self, token):
        facebook_profile = self.get_facebook_profile(token)

        if 'error' in facebook_profile.keys():
            return None

        try:
            user = User.objects.get(facebook_id=facebook_profile['id'])
        except User.DoesNotExist:
            user = User(facebook_id=facebook_profile['id'])

        user.set_unusable_password()
        user.facebook_access_token = token
        user.email = facebook_profile.get('email')
        user.first_name = facebook_profile.get('first_name')
        user.last_name = facebook_profile.get('last_name')
        user.save()

        return user

    def get_facebook_profile(self, token):
        url = 'https://graph.facebook.com/me/'

        params = {
            'access_token': token,
        }

        response = requests.get(
            url,
            params=params,
            headers={
                'Content-type': 'application/json',
                'Accept': 'application/json',
            },
        )

        print response.json
        print response.json()

        return response.json()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
