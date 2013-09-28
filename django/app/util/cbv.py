# coding: utf-8
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @login_required
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
