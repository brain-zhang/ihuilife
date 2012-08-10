from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ihuilife.views.home', name='home'),
    # url(r'^ihuilife/', include('ihuilife.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    (r'^catfeeds/admin/$', 'ihuilife.apps.catfeeds.views.index'),
    (r'^catfeeds/admin/shopping$', 'ihuilife.apps.catfeeds.views.shopping'),
    (r'^catfeeds/admin/getcatitems$', 'ihuilife.apps.catfeeds.utils.get_itemcats'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_PATH}),
)
