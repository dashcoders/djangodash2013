import os
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'development.db'),
    }
}

FACEBOOK_REDIRECT_URI = 'http://127.0.0.1:8000/facebook/login/'
FACEBOOK_APP_ID = '369338983199733'
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
