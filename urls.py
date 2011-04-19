from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', 'lojinha.views.index', name='leilao_index'),

    url(
        r'^eletrodomesticos$',
        'lojinha.views.products_by_category',
        name='leilao_eletrodomesticos',
        kwargs={'category_slug': 'eletrodomesticos'}),

    url(
        r'^eletronicos$',
        'lojinha.views.products_by_category',
        name='leilao_eletronicos',
        kwargs={'category_slug': 'eletronicos'}),

    url(
        r'^escritorio$',
        'lojinha.views.products_by_category',
        name='leilao_escritorio',
        kwargs={'category_slug': 'escritorio'}),

    url(
        r'^livros$',
        'lojinha.views.products_by_category',
        name='leilao_livros',
        kwargs={'category_slug': 'livros'}),

    url(
        r'^moveis$',
        'lojinha.views.products_by_category',
        name='leilao_moveis',
        kwargs={'category_slug': 'moveis'}),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        'lojinha.views.product_view',
        name='leilao_product_view'),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/lance$',
        'lojinha.views.bid',
        name='leilao_product_bid'),

    url(r'^sobre$', 'lojinha.views.about', name='leilao_sobre'),

    url(r'^contato$', 'lojinha.views.contact', name='leilao_contato'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
