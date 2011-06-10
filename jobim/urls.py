from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^about$', views.About.as_view(), name='about'),

    url(r'^contact$', views.Contact.as_view(), name='contact'),

    url(
        r'^contact/success$',
        views.ContactSuccess.as_view(),
        name='contact_success'),

    url(
        r'^(?P<category_slug>[-\w]+)$',
        views.ProductListByCategory.as_view(),
        name='category_view',),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        'jobim.views.product_view',
        name='product_view'),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/bid$',
        'jobim.views.bid',
        name='product_bid'), )
