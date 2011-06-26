from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.generic import (
    DetailView, FormView, ListView, RedirectView, TemplateView)

from jobim.forms import BidForm, ContactForm
from jobim.models import Bid, Category, Contact, Product, Store


BID_SUCCESS = _(
    'We received your bid, if it is interesting we will get into contact.')
BID_ERROR = _(
    'There were problems with the bid, please correct the errors below.')


class StoreMixin(object):
    store = None

    def get_context_data(self, **kwargs):
        context = super(StoreMixin, self).get_context_data(**kwargs)
        context.update({'store_url': self.kwargs.get('store_url')})
        return context

    def get_store(self):
        if self.store is None:
            store_url = self.kwargs.get('store_url')
            self.store = get_object_or_404(Store.online, url=store_url)

        return self.store


class About(StoreMixin, TemplateView):
    template_name = 'jobim/about.html'

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        store = self.get_store()
        context.update({'about_content': store.about_content})
        return context


class ContactView(StoreMixin, FormView):
    form_class = ContactForm
    template_name = 'jobim/contact.html'

    def get_context_data(self, **kwargs):
        contact_email = self.get_store().email

        context = super(ContactView, self).get_context_data(**kwargs)
        context.update({
            'contact_form': kwargs['form'],
            'contact_email': contact_email})
        return context

    def get_form_kwargs(self):
        store = self.get_store()
        contact = Contact(store=store)
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs.update({'instance': contact})
        return kwargs

    def get_success_url(self):
        store = self.get_store()
        self.success_url = reverse(
            'jobim:contact_success',
            kwargs={'store_url': store.url})
        return super(ContactView, self).get_success_url()

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)


class ContactSuccess(StoreMixin, TemplateView):
    template_name = 'jobim/contact_success.html'


class Index(StoreMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        store = self.get_store()
        self.url = reverse('jobim:about', kwargs={'store_url': store.url})
        return super(Index, self).get_redirect_url(**kwargs)


class ProductDetail(StoreMixin, DetailView):
    model = Product
    queryset = Product.available.all()

    def get_context_data(self, **kwargs):
        product = kwargs.get('object')
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context.update({
            'photos': product.photo_set.all(),
            'bid_form': BidForm()})
        return context

    def get_object(self, queryset=None):
        self.kwargs['slug'] = self.kwargs.get('product_slug')
        return super(ProductDetail, self).get_object(queryset)


class ProductListByCategory(StoreMixin, ListView):
    category = None
    context_object_name = 'products'
    template_name_suffix = '_list_by_category'

    def get_context_data(self, **kwargs):
        return super(ProductListByCategory, self).get_context_data(
            category=self.category,
            **kwargs)

    def get_queryset(self):
        store = self.get_store()

        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(Category, slug=category_slug)

        qs = Product.available.filter(store=store)
        qs = qs.filter(category=self.category)
        self.queryset = qs
        return super(ProductListByCategory, self).get_queryset()


class ToBid(StoreMixin, FormView):
    form_class = BidForm
    product = None
    template_name = 'jobim/product_detail.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        product = self.get_product()
        photos = product.photo_set.all()
        context = super(ToBid, self).get_context_data(**kwargs)
        context.update({
            'product': product,
            'photos': photos,
            'bid_form': kwargs.get('form')})
        return context

    def get_form_kwargs(self):
        product = self.get_product()
        bid = Bid(product=product)
        kwargs = super(ToBid, self).get_form_kwargs()
        kwargs.update({'instance': bid})
        return kwargs

    def get_product(self):
        if self.product is None:
            product_slug = self.kwargs.get('product_slug')
            self.product = get_object_or_404(
                Product.available, slug=product_slug)

        return self.product

    def get_success_url(self):
        category_slug = self.kwargs.get('category_slug')
        product_slug = self.kwargs.get('product_slug')
        store_url = self.get_store().url

        self.success_url = reverse(
            'jobim:product_detail',
            args=[store_url, category_slug, product_slug])
        return super(ToBid, self).get_success_url()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, BID_SUCCESS)
        return super(ToBid, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, BID_ERROR)
        return super(ToBid, self).form_invalid(form)
