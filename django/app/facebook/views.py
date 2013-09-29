# coding: utf-8
import requests
from urllib import urlencode
from urlparse import parse_qs
from django.conf import settings
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


class FacebookLoginView(View):

    def get(self, *args, **kwargs):
        error = None

        if 'error' in self.request.GET:
            return redirect('home')

        elif 'code' in self.request.GET:
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
            return HttpResponseRedirect(
                'https://graph.facebook.com/oauth/authorize?%s' % urlencode({
                    'client_id': settings.FACEBOOK_APP_ID,
                    'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                    'scope': ','.join(settings.FACEBOOK_SCOPES),
                })
            )

        return redirect('app')
