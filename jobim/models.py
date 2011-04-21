# -*- coding: utf-8 -*-

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'categoria'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim_category_view', [self.slug])


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='nome')
    slug = models.CharField(max_length=250)
    description = models.TextField(verbose_name=u'descrição')
    category = models.ForeignKey(Category, verbose_name='categoria')
    cover = models.ImageField(
        upload_to='thumbnails',
        max_length=250,
        verbose_name='capa')
    sold = models.BooleanField(verbose_name='vendido')

    class Meta:
        verbose_name = 'produto'
        ordering = ('-id',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jobim_product_view', [self.category.slug, self.slug])

    def status(self):
        if self.sold:
            return 'Vendido'
        else:
            bidset = self.bid_set.filter(accepted=True).order_by('-value')
            if bidset.count():
                return 'Maior oferta: R$ %s' % bidset[0].value
            else:
                return 'Esperando oferta'


class Photo(models.Model):
    product = models.ForeignKey(Product, verbose_name='produto')
    file = models.ImageField(
        upload_to='photos',
        max_length=250,
        verbose_name='imagem')

    class Meta:
        verbose_name = 'foto'

    def __unicode__(self):
        return u'%s #%s' % (self.product.name, self.pk)


class Bid(models.Model):
    product = models.ForeignKey(Product, verbose_name='produto')
    value = models.IntegerField(verbose_name='valor')
    mail = models.CharField(max_length=128, verbose_name='e-mail')
    accepted = models.BooleanField(verbose_name='aceita')

    class Meta:
        verbose_name = 'lance'

    def __unicode__(self):
        return u'%s R$%s %s' % (self.product.name, str(self.value), self.mail)

    @models.permalink
    def get_absolute_url(self):
        product = self.product
        return ('jobim_product_view', [product.category.slug, product.slug])


class Contact(models.Model):
    name = models.CharField(max_length=64, verbose_name='nome', blank=True)
    email = models.CharField(max_length=128, verbose_name='e-mail')
    phone = models.CharField(
        max_length=32,
        verbose_name='telefone',
        blank=True)
    subject = models.CharField(
        max_length=128,
        verbose_name='assunto',
        blank=True)
    message = models.TextField(verbose_name='mensagem', blank=True)
    read = models.BooleanField(verbose_name='lido')

    class Meta:
        verbose_name = 'contato'

    def __unicode__(self):
        return u'%s <%s> - %s' % (self.name, self.email, self.subject)
