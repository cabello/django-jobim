# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim_category_view', [self.slug])


class ProductsAvailableManager(models.Manager):
    def get_query_set(self):
        queryset = super(ProductsAvailableManager, self).get_query_set()
        return queryset.filter(sold=False)


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey(Category)
    cover = models.ImageField(
        upload_to='thumbnails',
        max_length=250,
        blank=True)
    sold = models.BooleanField()

    objects = models.Manager()
    available = ProductsAvailableManager()

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim_product_view', [self.category.slug, self.slug])

    def status(self):
        if self.sold:
            return 'Sold'
        else:
            bidset = self.bid_set.filter(accepted=True).order_by('-amount')
            if bidset.count():
                return 'Current bid: U$ %s' % bidset[0].amount
            else:
                return 'Waiting bid'


class Photo(models.Model):
    product = models.ForeignKey(Product)
    image_file = models.ImageField(upload_to='photos', max_length=250)

    def __unicode__(self):
        return u'%s #%s' % (self.product.name, self.pk)


class Bid(models.Model):
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    email = models.CharField(max_length=128)
    accepted = models.BooleanField()

    def __unicode__(self):
        amount = str(self.amount)
        return u'%s R$%s %s' % (self.product.name, amount, self.email)

    @models.permalink
    def get_absolute_url(self):
        product = self.product
        return ('jobim_product_view', [product.category.slug, product.slug])


class Contact(models.Model):
    name = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32, blank=True)
    subject = models.CharField(max_length=128, blank=True)
    message = models.TextField(blank=True)
    read = models.BooleanField()

    def __unicode__(self):
        return u'%s <%s> - %s' % (self.name, self.email, self.subject)
