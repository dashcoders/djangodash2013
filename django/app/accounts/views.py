# coding: utf-8
import requests
from urlparse import parse_qs
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from util.cbv import LoginRequiredMixin
# from .forms import LoginForm


class HomeTemplateView(TemplateView):
    template_name = 'accounts/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(*args, **kwargs)

        context['facebook_id'] = settings.FACEBOOK_APP_ID
        context['facebook_redirect_uri'] = settings.FACEBOOK_REDIRECT_URI + reverse('accounts_login')

        return context


class FacebookLogin(View):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts_home'))

        error = None

        if 'code' in self.request.GET.keys():
            params = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI + reverse('accounts_login'),
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

        if error:
            messages.error(self.request, error)
        else:
            messages.success(self.request, 'Congrats!!')

        return HttpResponseRedirect(reverse('accounts_home'))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('accounts_login'))
