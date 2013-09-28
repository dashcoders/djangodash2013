from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('accounts.urls')),
    url(r'^facebook/', include('facebook.urls')),
)
