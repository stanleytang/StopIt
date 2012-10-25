from django.conf.urls import patterns, include, url
from transit.views import index, stop

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stopit.views.home', name='home'),
    # url(r'^stopit/', include('stopit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'transit.views.index'),
    url(r'^stop/', 'transit.views.stop'),
    url(r'^route/', 'transit.views.route'),
    url(r'^route_map/', 'transit.views.route_map'),
)
