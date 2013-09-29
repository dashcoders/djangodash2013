from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^app/$', TemplateView.as_view(template_name='app.html'), name='app'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^facebook/', include('facebook.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
