# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'facebook_access_token'

    facebook_id = models.CharField(_('facebook id'), max_length=20, unique=True, null=True)
    facebook_access_token = models.CharField(_('facebook access token'), max_length=255, unique=True)

    def __unicode__(self):
        return self.email
