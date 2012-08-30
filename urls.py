# -*- coding: utf-8 -*-

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
    (r'^$', 'ihuilife.views.index'),
    
    #淘宝客商品入库
    (r'^catfeeds/admin/search/$', 'ihuilife.apps.catfeeds.views.search_index'),
    (r'^catfeeds/admin/taobaokeshopping/$', 'ihuilife.apps.catfeeds.views.taobaoke_shopping'),
    
    #普通商品入库
    (r'^catfeeds/admin/numiid/$', 'ihuilife.apps.catfeeds.views.num_iid_index'),
    (r'^catfeeds/admin/taobaoshopping/$', 'ihuilife.apps.catfeeds.views.taobao_shopping'),    
    
    #获取商品类目
    (r'^catfeeds/admin/getcatitems/$', 'ihuilife.apps.catfeeds.utils.get_itemcats'),
    
    #为商品打分
    (r'^catfeeds/admin/recommendcat/$', 'ihuilife.apps.catfeeds.views.recommendcat'),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_PATH}),
)
