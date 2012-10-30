from django.conf.urls import patterns, include, url
from transit.views import index, stop
from django.conf import settings

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
    url(r'^stop_map_search/', 'transit.views.stop_map_search'),
    url(r'^stop/', 'transit.views.stop'),
    url(r'^route/', 'transit.views.route'),
    url(r'^route_map/', 'transit.views.route_map'),
)

# Development AND Production are using media files
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns