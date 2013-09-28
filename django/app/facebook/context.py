# coding: utf-8
from django.conf import settings


def global_context(request):
    return {
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
        'FACEBOOK_REDIRECT_URI': settings.FACEBOOK_REDIRECT_URI,
    }
