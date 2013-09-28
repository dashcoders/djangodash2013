# coding: utf-8
from django.conf import settings
from django.views.generic import View
from django.shortcuts import redirect

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
