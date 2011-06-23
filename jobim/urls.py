from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^about$', views.About.as_view(), name='about'),

    url(r'^(?P<store_url>[-\w]+)/contact$',
        views.ContactView.as_view(),
        name='contact'),

    url(
        r'^(?P<store_url>[-\w]+)/contact/success$',
        views.ContactSuccess.as_view(),
        name='contact_success'),

    url(
        r'^(?P<category_slug>[-\w]+)$',
        views.ProductListByCategory.as_view(),
        name='category_view',),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        views.ProductDetail.as_view(),
        name='product_detail'),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/bid$',
        views.ToBid.as_view(),
        name='product_bid'), )
