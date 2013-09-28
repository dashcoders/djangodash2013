# coding: utf-8
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from util.cbv import LoginRequiredMixin
# from .forms import LoginForm


class HomeTemplateView(TemplateView):
    template_name = 'accounts/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(*args, **kwargs)

        context['facebook_id'] = settings.FACEBOOK_APP_ID
        context['facebook_redirect_uri'] = settings.FACEBOOK_REDIRECT_URI

        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))
