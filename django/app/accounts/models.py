# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'email'

    facebook_id = models.CharField(_('facebook id'), max_length=20)
    facebook_access_token = models.CharField(_('facebook access token'), max_length=320)

    def __unicode__(self):
        return self.email
