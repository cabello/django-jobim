# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from stdimage import StdImageField


class ProductsAvailableManager(models.Manager):
    def get_query_set(self):
        queryset = super(ProductsAvailableManager, self).get_query_set()
        return queryset.filter(status='AVLB')


class ProductsSoldManager(models.Manager):
    def get_query_set(self):
        queryset = super(ProductsSoldManager, self).get_query_set()
        return queryset.filter(status='SOLD')


class Product(models.Model):
    STATUS_CHOICES = (
        ('AVLB', _('Available')),
        ('SOLD', _('Sold')),
        ('RSRV', _('Reserved')),
        ('DRFT', _('Draft')))

    store = models.ForeignKey('Store', verbose_name=_('store'))
    name = models.CharField(_('name'), max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField(_('description'))
    cover = StdImageField(
        _('cover'),
        upload_to='thumbnails',
        max_length=250,
        blank=True,
        size=(200, 150))
    status = models.CharField(
        _('status'), max_length=4, choices=STATUS_CHOICES, default='AVLB')

    objects = models.Manager()
    available = ProductsAvailableManager()
    sold = ProductsSoldManager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('-id',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim:product_detail', (self.store.url, self.slug,))

    def bid_status(self):
        if self.status == 'SOLD':
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
    datetime = models.DateTimeField(_('datetime'), auto_now_add=True)

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
        return product.get_absolute_url()


class Contact(models.Model):
    store = models.ForeignKey('Store', verbose_name=_('store'))
    name = models.CharField(_('name'), max_length=64, blank=True)
    email = models.CharField(_('email'), max_length=128)
    phone_number = models.CharField(
        _('phone number'), max_length=32, blank=True)
    subject = models.CharField(_('subject'), max_length=128, blank=True)
    message = models.TextField(_('message'), blank=True)
    read = models.BooleanField(_('read'),)
    datetime = models.DateTimeField(_('datetime'), auto_now_add=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __unicode__(self):
        return u'%s <%s> - %s' % (self.name, self.email, self.subject)


class StoreOnlineManager(models.Manager):
    def get_query_set(self):
        queryset = super(StoreOnlineManager, self).get_query_set()
        return queryset.filter(status='ON')


class Store(models.Model):
    STATUS_CHOICES = (('ON', _('Online')), ('OFF', _('Offline')))

    name = models.CharField(_('name'), max_length=32)
    slogan = models.CharField(_('slogan'), max_length=128)
    url = models.SlugField(max_length=16)
    email = models.CharField(_('email'), max_length=128)
    status = models.CharField(
        _('status'), max_length=3, choices=STATUS_CHOICES, default='ON')
    about_content = models.TextField(_('about content'))

    objects = models.Manager()
    online = StoreOnlineManager()

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def __unicode__(self):
        return u'%s' % self.url


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'))
    store = models.ForeignKey(Store, verbose_name=_('store'))

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __unicode__(self):
        return u'%s (%s)' % (self.user.username, self.store.url)
