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


class About(TemplateView):
    template_name = 'jobim/about.html'

    def get_context_data(self, **kwargs):
        about_content = get_template('jobim/about.txt').render(Context())
        return {'about_content': about_content}


class ContactView(FormView):
    form_class = ContactForm
    store = None
    template_name = 'jobim/contact.html'

    def get_context_data(self, **kwargs):
        contact_email = settings.CONTACT_EMAIL
        return {
            'contact_form': kwargs['form'],
            'contact_email': contact_email,
            'store_url': self.kwargs.get('store_url')}

    def get_form_kwargs(self):
        store = self.get_store()
        contact = Contact(store=store)
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs.update({'instance': contact})
        return kwargs

    def get_store(self):
        if self.store is None:
            store_url = self.kwargs.get('store_url')
            self.store = get_object_or_404(Store, url=store_url)

        return self.store

    def get_success_url(self):
        store = self.get_store()
        self.success_url = reverse(
            'jobim:contact_success',
            kwargs={'store_url': store.url})
        return super(ContactView, self).get_success_url()

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)


class ContactSuccess(TemplateView):
    template_name = 'jobim/contact_success.html'

    def get_context_data(self, **kwargs):
        return {'store_url': self.kwargs.get('store_url')}


class Index(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        self.url = reverse('jobim:about')
        return super(Index, self).get_redirect_url(**kwargs)


class ProductDetail(DetailView):
    model = Product
    queryset = Product.available.all()

    def get_context_data(self, **kwargs):
        product = kwargs.get('object')
        kwargs['photos'] = product.photo_set.all()
        kwargs['bid_form'] = BidForm()
        return super(ProductDetail, self).get_context_data(**kwargs)

    def get_object(self, queryset=None):
        self.kwargs['slug'] = self.kwargs.get('product_slug')
        return super(ProductDetail, self).get_object(queryset)


class ProductListByCategory(ListView):
    category = None
    context_object_name = 'products'
    template_name_suffix = '_list_by_category'

    def get_context_data(self, **kwargs):
        return super(ProductListByCategory, self).get_context_data(
            category=self.category, **kwargs)

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(Category, slug=category_slug)
        self.queryset = Product.available.filter(category=self.category)
        return super(ProductListByCategory, self).get_queryset()


class ToBid(FormView):
    form_class = BidForm
    product = None
    template_name = 'jobim/product_detail.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        product = self.get_product()
        photos = product.photo_set.all()
        kwargs['product'] = product
        kwargs['photos'] = photos
        kwargs['bid_form'] = kwargs.get('form')
        return super(ToBid, self).get_context_data(**kwargs)

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
        self.success_url = reverse(
            'jobim:product_detail',
            args=[category_slug, product_slug])
        return super(ToBid, self).get_success_url()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, BID_SUCCESS)
        return super(ToBid, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, BID_ERROR)
        return super(ToBid, self).form_invalid(form)
