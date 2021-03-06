import os
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DJANGO_DATABASE_NAME'),
        'USER': os.getenv('DJANGO_DATABASE_USER'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST'),
        'PORT': '',
    }
}

FACEBOOK_REDIRECT_URI = 'http://forgetmyex.net/facebook/login/'
FACEBOOK_APP_ID = '551248321618177'
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
