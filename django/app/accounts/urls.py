# coding: utf-8
from django.conf.urls import patterns, url
from .views import FacebookLogin, LogoutView


urlpatterns = patterns(
    '',
    url(r'^login/$', FacebookLogin.as_view(), name='accounts_login'),
    url(r'^logout/$', LogoutView.as_view(), name='accounts_logout'),
)
