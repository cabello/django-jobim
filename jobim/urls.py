from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'jobim.views.index', name='jobim_index'),

    url(r'^about$', 'jobim.views.about', name='jobim_about'),

    url(r'^contact$', 'jobim.views.contact', name='jobim_contact'),

    url(
        r'^(?P<category_slug>[-\w]+)$',
        'jobim.views.products_by_category',
        name='jobim_category_view',),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        'jobim.views.product_view',
        name='jobim_product_view'),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/bid$',
        'jobim.views.bid',
        name='jobim_product_bid'), )
