from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', 'jobim.views.index', name='leilao_index'),

    url(
        r'^eletrodomesticos$',
        'jobim.views.products_by_category',
        name='leilao_eletrodomesticos',
        kwargs={'category_slug': 'eletrodomesticos'}),

    url(
        r'^eletronicos$',
        'jobim.views.products_by_category',
        name='leilao_eletronicos',
        kwargs={'category_slug': 'eletronicos'}),

    url(
        r'^escritorio$',
        'jobim.views.products_by_category',
        name='leilao_escritorio',
        kwargs={'category_slug': 'escritorio'}),

    url(
        r'^livros$',
        'jobim.views.products_by_category',
        name='leilao_livros',
        kwargs={'category_slug': 'livros'}),

    url(
        r'^moveis$',
        'jobim.views.products_by_category',
        name='leilao_moveis',
        kwargs={'category_slug': 'moveis'}),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$',
        'jobim.views.product_view',
        name='leilao_product_view'),

    url(
        r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/lance$',
        'jobim.views.bid',
        name='leilao_product_bid'),

    url(r'^sobre$', 'jobim.views.about', name='leilao_sobre'),

    url(r'^contato$', 'jobim.views.contact', name='leilao_contato'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
