# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from stdimage import StdImageField


class Category(models.Model):
    name = models.CharField(_('name'), max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim:category_view', [self.slug])


class ProductsAvailableManager(models.Manager):
    def get_query_set(self):
        queryset = super(ProductsAvailableManager, self).get_query_set()
        return queryset.filter(sold=False)


class Product(models.Model):
    name = models.CharField(_('name'), max_length=250)
    slug = models.CharField(max_length=250)
    description = models.TextField(_('description'))
    category = models.ForeignKey(Category, verbose_name=_('category'))
    cover = StdImageField(
        _('cover'),
        upload_to='thumbnails',
        max_length=250,
        blank=True,
        size=(200, 150))
    sold = models.BooleanField(_('sold'))

    objects = models.Manager()
    available = ProductsAvailableManager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('-id',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim:product_detail', [self.category.slug, self.slug])

    def status(self):
        if self.sold:
            return _('Sold')
        else:
            bidset = self.bid_set.filter(accepted=True).order_by('-amount')
            if bidset.count():
                return _('Current bid: U$ %s') % bidset[0].amount
            else:
                return _('Waiting bid')


class Photo(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'))
    image_file = StdImageField(
        _('image file'),
        upload_to='photos',
        max_length=250,
        size=(700, 525))

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    def __unicode__(self):
        return u'%s #%s' % (self.product.name, self.pk)


class Bid(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'))
    amount = models.IntegerField(_('amount'))
    email = models.CharField(_('email'), max_length=128)
    accepted = models.BooleanField(_('accepted'))

    class Meta:
        verbose_name = _('bid')
        verbose_name_plural = _('bids')

    def __unicode__(self):
        amount = str(self.amount)
        return _('%(product)s U$%(amount)s %(email)s') % {
            'product': self.product.name,
            'amount': amount,
            'email': self.email, }

    @models.permalink
    def get_absolute_url(self):
        product = self.product
        return ('jobim:product_detail', [product.category.slug, product.slug])


class Contact(models.Model):
    name = models.CharField(_('name'), max_length=64, blank=True)
    email = models.CharField(_('email'), max_length=128)
    phone_number = models.CharField(
        _('phone number'), max_length=32, blank=True)
    subject = models.CharField(_('subject'), max_length=128, blank=True)
    message = models.TextField(_('message'), blank=True)
    read = models.BooleanField(_('read'),)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __unicode__(self):
        return u'%s <%s> - %s' % (self.name, self.email, self.subject)


class Store(models.Model):
    name = models.CharField(_('name'), max_length=32)
    slogan = models.CharField(_('slogan'), max_length=128)
    url = models.SlugField(max_length=16)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def __unicode__(self):
        return u'%s - %s' % (self.url, self.name)
