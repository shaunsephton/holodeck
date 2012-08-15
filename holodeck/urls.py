from django.conf.urls import patterns, include, url
from django.contrib import admin
from holodeck import api, views

admin.autodiscover()

urlpatterns = patterns('',
    # Accounts.
    url(r'^login/$', views.login, name='holodeck-login'),
    url(r'^logout/$', views.logout, name='holodeck-logout'),

    # Dashboards.
    url(r'^dashboards/new/$', views.new_dashboard, name='holodeck-new-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)$', views.view_dashboard, name='holodeck-view-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)/manage/$', views.manage_dashboard, name='holodeck-manage-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)/export/$', views.export_dashboard, name='holodeck-export-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)/export/(?P<share_key>[\w-]+)/$', views.export_shared_dashboard, name='holodeck-export-shared-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)/remove/$', views.remove_dashboard, name='holodeck-remove-dashboard'),
    url(r'^dashboards/(?P<dashboard_id>\d+)/(?P<share_key>[\w-]+)/$', views.share_dashboard, name='holodeck-share-dashboard'),
    
    # Metrics.
    url(r'^metrics/(?P<dashboard_id>\d+)/new/$', views.new_metric, name='holodeck-new-metric'),
    url(r'^metrics/(?P<metric_id>\d+)/edit/$', views.manage_metric, name='holodeck-manage-metric'),
    url(r'^metrics/(?P<metric_id>\d+)/remove/$', views.remove_metric, name='holodeck-remove-metric'),
    url(r'^metrics/(?P<metric_id>\d+)/purge-samples/$', views.purge_metric_samples, name='holodeck-purge-metric-samples'),
    
    # API.
    url(r'^api/store/$', api.store, name='holodeck-api-store'),

    # Misc.
    url(r'^$', views.holodeck, name='holodeck'),
    url(r'^admin/', include(admin.site.urls)),
)
