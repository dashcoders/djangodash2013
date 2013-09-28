# coding: utf-8
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    error_messages = {
        'bad_credentials': _('User or password incorrect')
    }

    username = forms.CharField(label=_('username'), max_length=20)
    # password = forms.CharField(label=_('password'), max_length=20, widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        cleaned_data = super(LoginForm, self).clean(*args, **kwargs)
        username = cleaned_data.get('username')
        # password = cleaned_data.get('password')
        user = authenticate(username=username)
        if not user:
            raise forms.ValidationError(self.error_messages['bad_credentials'])
        self.user_cache = user
        return cleaned_data
