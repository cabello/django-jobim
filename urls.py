from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^leilao/', include('leilao.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', 'lojinha.views.index', name='leilao_index'),

    url(
        r'^eletrodomesticos$',
        'lojinha.views.products_by_category',
        name='leilao_eletrodomesticos',
        kwargs={'category_slug': 'eletrodomesticos'}
    ),

    url(
        r'^eletronicos$',
        'lojinha.views.products_by_category',
        name='leilao_eletronicos',
        kwargs={'category_slug': 'eletronicos'}
    ),

    url(
        r'^escritorio$',
        'lojinha.views.products_by_category',
        name='leilao_escritorio',
        kwargs={'category_slug': 'escritorio'}
    ),

    url(
        r'^livros$',
        'lojinha.views.products_by_category',
        name='leilao_livros',
        kwargs={'category_slug': 'livros'}
    ),

    url(
        r'^moveis$',
        'lojinha.views.products_by_category',
        name='leilao_moveis',
        kwargs={'category_slug': 'moveis'}
    ),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        'lojinha.views.product_view',
        name='leilao_product_view'
    ),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/lance$',
        'lojinha.views.bid',
        name='leilao_product_bid'
    ),

    url(r'^sobre$', 'lojinha.views.about', name='leilao_sobre'),
    url(r'^contato$', 'lojinha.views.contact', name='leilao_contato'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
