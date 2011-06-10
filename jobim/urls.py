from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='jobim_index'),

    url(r'^about$', views.About.as_view(), name='jobim_about'),

    url(r'^contact$', 'jobim.views.contact', name='jobim_contact'),

    url(
        r'^(?P<category_slug>[-\w]+)$',
        views.ProductListByCategory.as_view(),
        name='jobim_category_view',),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        'jobim.views.product_view',
        name='jobim_product_view'),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/bid$',
        'jobim.views.bid',
        name='jobim_product_bid'), )
