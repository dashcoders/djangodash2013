# coding: utf-8
import requests
from urlparse import parse_qs
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login


class FacebookLoginView(View):

    def get(self, *args, **kwargs):
        error = None

        if 'error' in self.request.GET.keys():
            return redirect('home')

        if 'code' in self.request.GET.keys():
            params = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'code': self.request.GET.get('code'),
            }

            url = 'https://graph.facebook.com/oauth/access_token'

            response = requests.get(
                url,
                params=params,
            )

            data = parse_qs(response.content)
            access_token = data['access_token'][0]

            user = authenticate(token=access_token)
            if user:
                if user.is_active:
                    login(self.request, user)
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        else:
            error = 'AUTH_DENIED'

        return redirect('home')
