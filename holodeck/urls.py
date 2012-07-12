from django.conf.urls import patterns, include, url
from django.contrib import admin
from holodeck import api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/store/$', api.store, name='holodeck-api-store'),
)
