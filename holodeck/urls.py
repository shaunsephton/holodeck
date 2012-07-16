from django.conf.urls import patterns, include, url
from django.contrib import admin
from holodeck import api, views

admin.autodiscover()

urlpatterns = patterns('',


    # Account
    url(r'^login/$', views.login, name='holodeck-login'),
    url(r'^logout/$', views.logout, name='holodeck-logout'),

    # Dashboards
    url(r'^dashboards/new/$', views.new_dashboard, name='holodeck-new-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)$', views.view_dashboard, name='holodeck-view-dashboard'),
    
    # Metrics
    url(r'^metrics/(?P<dashboard_id>\d+)/new/$', views.new_metric, name='holodeck-new-metric'),
    url(r'^metrics/(?P<metric_id>\d+)/edit/$', views.manage_metric, name='holodeck-manage-metric'),
    url(r'^metrics/(?P<metric_id>\d+)/remove/$', views.remove_metric, name='holodeck-remove-metric'),
    
    url(r'^$', views.holodeck, name='holodeck'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/store/$', api.store, name='holodeck-api-store'),
)
