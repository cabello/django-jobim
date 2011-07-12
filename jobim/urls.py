from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^(?P<store_url>[-\w]+)/about/$',
        views.About.as_view(),
        name='about'),

    url(r'^(?P<store_url>[-\w]+)/contact/$',
        views.ContactView.as_view(),
        name='contact'),

    url(
        r'^(?P<store_url>[-\w]+)/contact/success/$',
        views.ContactSuccess.as_view(),
        name='contact_success'),

    url(
        r'^(?P<store_url>[-\w]+)/$',
        views.ProductList.as_view(),
        name='product_list',),

    url(
        r'^(?P<store_url>[-\w]+)/(?P<product_slug>[-\w]+)/$',
        views.ProductDetail.as_view(),
        name='product_detail'),

    url(
        r'^(?P<store_url>[-\w]+)/(?P<product_slug>[-\w]+)/bid/$',
        views.ToBid.as_view(),
        name='product_bid'), )
