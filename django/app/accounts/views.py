# coding: utf-8
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
# from .forms import LoginForm


class HomeTemplateView(TemplateView):
    template_name = 'accounts/home.html'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
