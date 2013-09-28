# coding: utf-8
from django.conf.urls import patterns, url
from .views import LogoutView


urlpatterns = patterns(
    '',
    url(r'^logout/$', LogoutView.as_view(), name='accounts_logout'),
)
