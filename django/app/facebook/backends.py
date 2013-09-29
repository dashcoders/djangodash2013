# coding: utf-8
import requests
# from django.utils.translation import ugettext as _
from accounts.models import User
from django.conf import settings


class FacebookBackend(object):

    def authenticate(self, token):
        response_profile = requests.get(
            'https://graph.facebook.com/me/',
            params={
                'access_token': token,
            }
        )

        facebook_profile = response_profile.json()

        if 'error' in facebook_profile:
            return None

        try:
            user = User.objects.get(facebook_id=facebook_profile.get('id'))
        except User.DoesNotExist:
            user = User(facebook_id=facebook_profile.get('id'))

        if facebook_profile.get('id') in settings.FACEBOOK_ADMINS:
            user.is_staff = True
            user.is_superuser = True

        user.username = facebook_profile.get('id')
        user.set_unusable_password()
        user.facebook_access_token = token
        user.email = facebook_profile.get('email', '')
        user.first_name = facebook_profile.get('first_name')
        user.last_name = facebook_profile.get('last_name')
        user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
