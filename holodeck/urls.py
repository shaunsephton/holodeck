from django.conf.urls import patterns, include, url
from django.contrib import admin

from holodeck import api

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bitpile.views.home', name='home'),
    # url(r'^bitpile/', include('bitpile.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/store/$', api.store, name='holodeck-api-store'),
)
